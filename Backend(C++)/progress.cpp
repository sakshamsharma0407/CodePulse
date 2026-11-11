
#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <queue>
#include <cstdlib>
#include <iomanip>
#include <limits>
#include <mysql.h>

using namespace std;

struct Question {
    int id;
    string title;
    vector<string> topics;
    string difficulty;
    bool solved = false;
};

struct Topic {
    string name;
    int solved;
    int total;
    double percentage;
};

// Escape special characters for JSON
string jsonEscape(const string& value) {
    string result;

    for (char c : value) {
        switch (c) {
            case '"': result += "\\\""; break;
            case '\\': result += "\\\\"; break;
            case '\n': result += "\\n"; break;
            case '\r': result += "\\r"; break;
            case '\t': result += "\\t"; break;

            default:
                if (static_cast<unsigned char>(c) >= 32)
                    result += c;
        }
    }

    return result;
}

// Compare topics by percentage, weakest first
bool comesBefore(const Topic& a, const Topic& b) {
    if (a.percentage != b.percentage)
        return a.percentage < b.percentage;

    return a.name < b.name;
}

// Merge Sort
void merge(vector<Topic>& topics, int left, int mid, int right) {
    vector<Topic> temp;

    int i = left;
    int j = mid + 1;

    while (i <= mid && j <= right) {

        if (comesBefore(topics[i], topics[j]))
            temp.push_back(topics[i++]);
        else
            temp.push_back(topics[j++]);
    }

    while (i <= mid)
        temp.push_back(topics[i++]);

    while (j <= right)
        temp.push_back(topics[j++]);

    for (int k = 0; k < static_cast<int>(temp.size()); k++)
        topics[left + k] = temp[k];
}

void mergeSort(vector<Topic>& topics, int left, int right) {
    if (left >= right)
        return;

    int mid = left + (right - left) / 2;

    mergeSort(topics, left, mid);
    mergeSort(topics, mid + 1, right);

    merge(topics, left, mid, right);
}

// Execute MySQL query
MYSQL_RES* runQuery(MYSQL* conn, const string& query) {

    if (mysql_query(conn, query.c_str()) != 0) {
        cerr << "MYSQL_ERROR: " << mysql_error(conn) << endl;
        return nullptr;
    }

    return mysql_store_result(conn);
}

int main(int argc, char* argv[]) {

    // Check username
    if (argc < 2) {
        cerr << "ERROR: Username not provided." << endl;
        return 1;
    }

    string username = argv[1];

    // Database configuration
    const char* host = getenv("DB_HOST");
    const char* dbUser = getenv("DB_USER");
    const char* dbPassword = getenv("DB_PASSWORD");
    const char* dbName = getenv("DB_NAME");

    if (!host || !dbUser || !dbPassword || !dbName) {
        cerr << "ERROR: Database configuration missing." << endl;
        return 1;
    }

    // Initialize MySQL
    MYSQL* conn = mysql_init(nullptr);

    if (!conn) {
        cerr << "ERROR: MySQL initialization failed." << endl;
        return 1;
    }

    // Connect to database
    if (!mysql_real_connect(
            conn,
            host,
            dbUser,
            dbPassword,
            dbName,
            3306,
            nullptr,
            0)) {

        cerr << "MYSQL_CONNECTION_ERROR: "
             << mysql_error(conn) << endl;

        mysql_close(conn);
        return 1;
    }

    // Escape username
    char* escapedUsername = new char[username.length() * 2 + 1];

    unsigned long escapedLength = mysql_real_escape_string(
        conn,
        escapedUsername,
        username.c_str(),
        static_cast<unsigned long>(username.length())
    );

    string safeUsername(escapedUsername, escapedLength);

    delete[] escapedUsername;

    // Find user ID
    string userQuery =
        "SELECT id FROM users WHERE username = '" +
        safeUsername + "' LIMIT 1";

    MYSQL_RES* userResult = runQuery(conn, userQuery);

    if (!userResult) {
        mysql_close(conn);
        return 1;
    }

    MYSQL_ROW userRow = mysql_fetch_row(userResult);

    if (!userRow) {
        cerr << "ERROR: User not found." << endl;

        mysql_free_result(userResult);
        mysql_close(conn);

        return 1;
    }

    string userId = userRow[0];

    mysql_free_result(userResult);

    // Get total and accepted submissions
    string statsQuery =
        "SELECT COUNT(*), "
        "COALESCE(SUM(status = 'ACCEPTED'), 0) "
        "FROM submissions WHERE user_id = " + userId;

    MYSQL_RES* statsResult = runQuery(conn, statsQuery);

    if (!statsResult) {
        mysql_close(conn);
        return 1;
    }

    MYSQL_ROW statsRow = mysql_fetch_row(statsResult);

    int totalSubmissions = statsRow ? atoi(statsRow[0]) : 0;
    int acceptedSubmissions = statsRow ? atoi(statsRow[1]) : 0;

    mysql_free_result(statsResult);

    // Get distinct solved question IDs
    string solvedQuery =
        "SELECT DISTINCT question_id FROM submissions "
        "WHERE user_id = " + userId +
        " AND status = 'ACCEPTED'";

    MYSQL_RES* solvedResult = runQuery(conn, solvedQuery);

    if (!solvedResult) {
        mysql_close(conn);
        return 1;
    }

    unordered_map<int, bool> solvedMap;

    MYSQL_ROW solvedRow;

    while ((solvedRow = mysql_fetch_row(solvedResult))) {
        solvedMap[atoi(solvedRow[0])] = true;
    }

    mysql_free_result(solvedResult);

    mysql_close(conn);

    // Read question count from Python
    int n;

    if (!(cin >> n) || n < 0) {
        cerr << "ERROR: Invalid question data." << endl;
        return 1;
    }

    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    vector<Question> questions(n);

    // Hash map: topic -> {solved count, total count}
    unordered_map<string, pair<int, int>> topicStats;

    int totalSolved = 0;

    int easyTotal = 0;
    int mediumTotal = 0;
    int hardTotal = 0;

    int easySolved = 0;
    int mediumSolved = 0;
    int hardSolved = 0;

    // Process questions
    for (int i = 0; i < n; i++) {

        // Question ID
        if (!(cin >> questions[i].id)) {
            cerr << "ERROR: Invalid question ID." << endl;
            return 1;
        }

        cin.ignore(numeric_limits<streamsize>::max(), '\n');

        // Question title
        if (!getline(cin, questions[i].title)) {
            cerr << "ERROR: Invalid question title." << endl;
            return 1;
        }

        // Number of topics for this question
        int topicCount;

        if (!(cin >> topicCount) || topicCount < 0) {
            cerr << "ERROR: Invalid topic count." << endl;
            return 1;
        }

        cin.ignore(numeric_limits<streamsize>::max(), '\n');

        // Read every topic separately
        for (int j = 0; j < topicCount; j++) {

            string topicName;

            if (!getline(cin, topicName)) {
                cerr << "ERROR: Invalid topic name." << endl;
                return 1;
            }

            if (!topicName.empty()) {
                questions[i].topics.push_back(topicName);
            }
        }

        // Difficulty
        if (!getline(cin, questions[i].difficulty)) {
            cerr << "ERROR: Invalid difficulty." << endl;
            return 1;
        }

        // Check if question is solved
        questions[i].solved =
            solvedMap.find(questions[i].id) != solvedMap.end();

        if (questions[i].solved)
            totalSolved++;

        // Count each topic independently
        for (const string& topicName : questions[i].topics) {

            topicStats[topicName].second++;

            if (questions[i].solved)
                topicStats[topicName].first++;
        }

        // Difficulty-wise statistics
        if (questions[i].difficulty == "Easy") {

            easyTotal++;

            if (questions[i].solved)
                easySolved++;
        }
        else if (questions[i].difficulty == "Medium") {

            mediumTotal++;

            if (questions[i].solved)
                mediumSolved++;
        }
        else if (questions[i].difficulty == "Hard") {

            hardTotal++;

            if (questions[i].solved)
                hardSolved++;
        }
    }

    // Convert hash map into topic vector
    vector<Topic> topics;

    for (const auto& entry : topicStats) {

        Topic t;

        t.name = entry.first;
        t.solved = entry.second.first;
        t.total = entry.second.second;

        t.percentage =
            t.total > 0
            ? (double)t.solved / t.total * 100
            : 0;

        topics.push_back(t);
    }

    // Sort topics from weakest to strongest
    if (!topics.empty()) {
        mergeSort(topics, 0, static_cast<int>(topics.size()) - 1);
    }

    // Queue for recommendations
    queue<int> recommendationQueue;

    // Avoid duplicate question recommendations
    unordered_set<int> recommended;

    for (const Topic& topic : topics) {

        for (const Question& question : questions) {

            if (question.solved)
                continue;

            bool belongsToTopic = false;

            for (const string& questionTopic : question.topics) {

                if (questionTopic == topic.name) {
                    belongsToTopic = true;
                    break;
                }
            }

            if (belongsToTopic &&
                recommended.find(question.id) == recommended.end()) {

                recommendationQueue.push(question.id);
                recommended.insert(question.id);
            }
        }
    }

    // Calculate overall completion
    double completion =
        n > 0
        ? (double)totalSolved / n * 100
        : 0;

    // Calculate submission accuracy
    double accuracy =
        totalSubmissions > 0
        ? (double)acceptedSubmissions / totalSubmissions * 100
        : 0;

    // JSON output
    cout << fixed << setprecision(1);

    cout << "{";

    cout << "\"total_questions\":" << n << ",";
    cout << "\"solved_questions\":" << totalSolved << ",";
    cout << "\"overall_percentage\":" << completion << ",";
    cout << "\"total_submissions\":" << totalSubmissions << ",";
    cout << "\"accepted_submissions\":" << acceptedSubmissions << ",";
    cout << "\"accuracy\":" << accuracy << ",";

    // Difficulty-wise progress
    cout << "\"difficulty\":{";

    cout << "\"Easy\":[" << easySolved << "," << easyTotal << "],";
    cout << "\"Medium\":[" << mediumSolved << "," << mediumTotal << "],";
    cout << "\"Hard\":[" << hardSolved << "," << hardTotal << "]";

    cout << "},";

    // Topic-wise progress
    cout << "\"topics\":[";

    for (int i = 0; i < static_cast<int>(topics.size()); i++) {

        if (i > 0)
            cout << ",";

        cout << "{";

        cout << "\"name\":\""
             << jsonEscape(topics[i].name) << "\",";

        cout << "\"solved\":" << topics[i].solved << ",";
        cout << "\"total\":" << topics[i].total << ",";
        cout << "\"percentage\":" << topics[i].percentage;

        cout << "}";
    }

    cout << "],";

    // Weakest topic
    cout << "\"weakest_topic\":";

    if (!topics.empty() && topics[0].solved < topics[0].total) {
        cout << "\"" << jsonEscape(topics[0].name) << "\"";
    }
    else {
        cout << "null";
    }

    cout << ",";

    // Recommended questions
    cout << "\"recommendations\":[";

    int count = 0;

    while (!recommendationQueue.empty() && count < 5) {

        if (count > 0)
            cout << ",";

        cout << recommendationQueue.front();

        recommendationQueue.pop();

        count++;
    }

    cout << "]";

    cout << "}";

    return 0;
}
