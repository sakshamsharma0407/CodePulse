
#include <iostream>
#include <string>
#include <cstdlib>
#include <mysql.h>

using namespace std;

// Linked list node
struct SubmissionNode {
    int submission_id;
    int question_id;
    string submitted_code;
    string status;
    string submitted_at;

    SubmissionNode* next;
    
    SubmissionNode(int sid, int qid, string code,
                   string stat, string date) {
        submission_id = sid;
        question_id = qid;
        submitted_code = code;
        status = stat;
        submitted_at = date;
        next = nullptr;
    }
};

// Linked list class
class SubmissionHistory {
private:
    SubmissionNode* head;
    SubmissionNode* tail;

public:
    SubmissionHistory() {
        head = nullptr;
        tail = nullptr;
    }

    // Insert a submission at the end
    void insertSubmission(int sid, int qid, string code,
                          string status, string date) {
        SubmissionNode* newNode =
            new SubmissionNode(sid, qid, code, status, date);

        if (head == nullptr) {
            head = tail = newNode;
        } else {
            tail->next = newNode;
            tail = newNode;
        }
    }

    // Display linked list as JSON
    static string escapeJSON(const string& s) {
        string result;

        for (char c : s) {
            switch (c) {
                case '"': result += "\\\""; break;
                case '\\': result += "\\\\"; break;
                case '\n': result += "\\n"; break;
                case '\r': result += "\\r"; break;
                case '\t': result += "\\t"; break;
                default:
                    if (static_cast<unsigned char>(c) < 32) {
                        result += ' ';
                    } else {
                        result += c;
                    }
            }
        }

        return result;
    }

    void displayHistory() {
        cout << "{\"history\":[";

        SubmissionNode* temp = head;
        bool first = true;

        while (temp != nullptr) {
            if (!first) cout << ",";

            cout << "{";
            cout << "\"submission_id\":" << temp->submission_id << ",";
            cout << "\"question_id\":" << temp->question_id << ",";
            cout << "\"submitted_code\":\""
                 << escapeJSON(temp->submitted_code) << "\",";
            cout << "\"status\":\""
                 << escapeJSON(temp->status) << "\",";
            cout << "\"submitted_at\":\""
                 << escapeJSON(temp->submitted_at) << "\"";
            cout << "}";

            first = false;
            temp = temp->next;
        }

        cout << "]}" << endl;
    }

    // Free linked list memory
    void deleteHistory() {
        SubmissionNode* temp = head;

        while (temp != nullptr) {
            SubmissionNode* nextNode = temp->next;
            delete temp;
            temp = nextNode;
        }

        head = nullptr;
        tail = nullptr;
    }

    ~SubmissionHistory() {
        deleteHistory();
    }
};

int main(int argc, char* argv[]) {

    if (argc < 2) {
        cerr << "Username missing";
        return 1;
    }

    string username = argv[1];

    const char* host = getenv("DB_HOST");
    const char* user = getenv("DB_USER");
    const char* password = getenv("DB_PASSWORD");
    const char* database = getenv("DB_NAME");

    if (!host || !user || !password || !database) {
        cerr << "Database configuration missing";
        return 1;
    }

    MYSQL* conn = mysql_init(nullptr);

    if (!conn) {
        cerr << "MySQL initialization failed";
        return 1;
    }

    if (!mysql_real_connect(conn, host, user, password,
                            database, 0, nullptr, 0)) {
        cerr << mysql_error(conn);
        mysql_close(conn);
        return 1;
    }

    // Escape username before using it in the query
    string escapedUsername;
    escapedUsername.resize(username.length() * 2 + 1);

    unsigned long escapedLength = mysql_real_escape_string(
        conn,
        &escapedUsername[0],
        username.c_str(),
        static_cast<unsigned long>(username.length())
    );

    escapedUsername.resize(escapedLength);

    string query =
        "SELECT s.submission_id, s.question_id, "
        "s.submitted_code, s.status, s.submitted_at "
        "FROM submissions s "
        "INNER JOIN users u ON s.user_id = u.id "
        "WHERE u.username = '" + escapedUsername + "' "
        "ORDER BY s.submission_id DESC";

    if (mysql_query(conn, query.c_str())) {
        cerr << mysql_error(conn);
        mysql_close(conn);
        return 1;
    }

    MYSQL_RES* result = mysql_store_result(conn);

    if (!result) {
        cerr << mysql_error(conn);
        mysql_close(conn);
        return 1;
    }

    SubmissionHistory history;

    MYSQL_ROW row;
    unsigned long* lengths;

    // Fetch database records and insert into linked list
    while ((row = mysql_fetch_row(result))) {

        lengths = mysql_fetch_lengths(result);

        int submission_id = atoi(row[0]);
        int question_id = atoi(row[1]);

        string code = row[2] ? string(row[2], lengths[2]) : "";
        string status = row[3] ? row[3] : "";
        string submitted_at = row[4] ? row[4] : "";

        history.insertSubmission(
            submission_id,
            question_id,
            code,
            status,
            submitted_at
        );
    }

    // Traverse linked list and display history
    history.displayHistory();

    mysql_free_result(result);
    mysql_close(conn);

    return 0;
}
