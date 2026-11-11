#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <sstream>
#include <vector>
#include <windows.h>
#include <mysql.h>
#include "Submit.h"
using namespace std;

string normalize(const string& text) {
    stringstream ss(text);
    string word, result;

    while (ss >> word) {
        if (!result.empty())
            result += " ";
        result += word;
    }

    return result;
}

MYSQL* connectDatabase() {
    const char* host = getenv("DB_HOST");
    const char* user = getenv("DB_USER");
    const char* password = getenv("DB_PASSWORD");
    const char* database = getenv("DB_NAME");

    if (!host || !user || !password || !database) {
        cout << "DATABASE_CONFIGURATION_MISSING\n";
        return NULL;
    }

    MYSQL* conn = mysql_init(NULL);
    if (!conn) return NULL;

    if (!mysql_real_connect(conn, host, user, password, database, 0, NULL, 0)) {
        cout << "DATABASE_CONNECTION_FAILED: " << mysql_error(conn) << "\n";
        mysql_close(conn);
        return NULL;
    }
    return conn;
}
int getUserId(MYSQL* conn, const string& username) {
    if (conn == NULL || username.empty())
        return 0;

    string query =
        "SELECT id FROM users WHERE username = ? LIMIT 1";

    MYSQL_STMT* stmt = mysql_stmt_init(conn);

    if (stmt == NULL)
        return 0;

    if (mysql_stmt_prepare(stmt, query.c_str(), query.length()) != 0) {
        cout << "USER_LOOKUP_ERROR: "
             << mysql_stmt_error(stmt) << "\n";
        mysql_stmt_close(stmt);
        return 0;
    }

    MYSQL_BIND params[1] = {};
    unsigned long usernameLength = username.length();

    params[0].buffer_type = MYSQL_TYPE_STRING;
    params[0].buffer = const_cast<char*>(username.c_str());
    params[0].buffer_length = usernameLength;
    params[0].length = &usernameLength;

    if (mysql_stmt_bind_param(stmt, params) != 0) {
        cout << "USER_BIND_ERROR: "
             << mysql_stmt_error(stmt) << "\n";
        mysql_stmt_close(stmt);
        return 0;
    }

    if (mysql_stmt_execute(stmt) != 0) {
        cout << "USER_QUERY_ERROR: "
             << mysql_stmt_error(stmt) << "\n";
        mysql_stmt_close(stmt);
        return 0;
    }

    int user_id = 0;

    MYSQL_BIND result[1] = {};

    result[0].buffer_type = MYSQL_TYPE_LONG;
    result[0].buffer = &user_id;

    if (mysql_stmt_bind_result(stmt, result) != 0) {
        cout << "USER_RESULT_ERROR: "
             << mysql_stmt_error(stmt) << "\n";
        mysql_stmt_close(stmt);
        return 0;
    }

    int fetchResult = mysql_stmt_fetch(stmt);

    mysql_stmt_close(stmt);

    if (fetchResult != 0 || user_id <= 0)
        return 0;

    return user_id;
}
bool runWithTimeout(DWORD timeoutMs) {
    STARTUPINFOA si = {};
    PROCESS_INFORMATION pi = {};
    si.cb = sizeof(si);

    string command =
        "cmd.exe /C \"submission.exe < test_input.txt > test_output.txt\"";

    if (!CreateProcessA(
        NULL, &command[0], NULL, NULL, FALSE,
        CREATE_NO_WINDOW, NULL, NULL, &si, &pi
    )) {
        return false;
    }

    DWORD status = WaitForSingleObject(pi.hProcess, timeoutMs);
    bool success = false;

    if (status == WAIT_OBJECT_0) {
        DWORD exitCode = 1;
        if (GetExitCodeProcess(pi.hProcess, &exitCode))
            success = (exitCode == 0);
    } else {
        TerminateProcess(pi.hProcess, 1);
        WaitForSingleObject(pi.hProcess, 1000);
    }

    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);

    return success;
}
int main(int argc, char* argv[]) {

    if (argc < 3) {
        cout << "Usage: evaluator.exe <question_id> <username>\n";
        return 1;
    }

    string question = argv[1];
    string username = argv[2];

    int question_id = atoi(argv[1]);

    if (question_id <= 0) {
        cout << "Invalid question ID\n";
        return 1;
    }

    if (username.empty()) {
        cout << "Username missing\n";
        return 1;
    }

    MYSQL* conn = connectDatabase();

    if (conn == NULL) {
        cout << "Cannot connect to database. Submission not evaluated.\n";
        return 1;
    }

    int user_id = getUserId(conn, username);

    if (user_id <= 0) {
        cout << "USER_NOT_FOUND: " << username << "\n";
        mysql_close(conn);
        return 1;
    }

    cout << "USER_VERIFIED\n";

    string code, line;
    while (getline(cin, line))
        code += line + "\n";

    if (code.empty()) {
        cout << "No code submitted\n";
        mysql_close(conn);
        return 1;
    }

    ofstream source("submission.cpp");
    source << code;
    source.close();
    int compileResult = system("g++ submission.cpp -o submission.exe 2> compile_error.txt");
    if (compileResult != 0) {
        ifstream compileFile("compile_error.txt");
        string compileError((istreambuf_iterator<char>(compileFile)),
                            istreambuf_iterator<char>());
        cout << "COMPILATION ERROR\n" << compileError << "\n";

        if (conn) {
            if (user_id > 0) {
                Submission attempt(user_id, question_id, code, "COMPILATION ERROR");
                if (!attempt.saveSubmission(conn))
                    cout << "Could not save submission to database\n";
            }
            mysql_close(conn);
        }
        return 0;
    }

    vector<pair<string, string>> tests;

if (question == "1") {
    tests = {
        {"4 9\n2 7 11 15\n", "0 1"},
        {"3 6\n3 2 4\n", "1 2"},
        {"2 6\n3 3\n", "0 1"},
        {"3 -1\n-3 2 5\n", "0 1"},
        {"5 13\n1 2 4 6 7\n", "3 4"},
        {"3 100\n1 2 3\n", "-1"}
    };
}
else if (question == "2") {
    tests = {
        {"5 2\n1 2 3 4 5\n", "2 1 4 3 5"},
        {"6 3\n1 2 3 4 5 6\n", "3 2 1 6 5 4"},
        {"4 1\n1 2 3 4\n", "1 2 3 4"},
        {"3 3\n1 2 3\n", "3 2 1"},
        {"2 3\n1 2\n", "1 2"},
        {"1 1\n9\n", "9"}
    };
}
else if (question == "3") {
    tests = {
        {"()[]{}\n", "true"},
        {"([)]\n", "false"},
        {"{[]}\n", "true"},
        {"((\n", "false"},
        {"(]\n", "false"},
        {"([]{})\n", "true"}
    };
}
else if (question == "4") {
    tests = {
        {"5\n1 2 3 4 5\n3\n", "2"},
        {"5\n1 2 3 4 5\n8\n", "-1"},
        {"5\n1 2 3 4 5\n1\n", "0"},
        {"5\n1 2 3 4 5\n5\n", "4"},
        {"1\n7\n7\n", "0"},
        {"4\n-5 -2 0 9\n-2\n", "1"}
    };
}
else if (question == "5") {
    tests = {
        {"9\n-2 1 -3 4 -1 2 1 -5 4\n", "6"},
        {"4\n1 2 3 4\n", "10"},
        {"3\n-5 -2 -8\n", "-2"},
        {"1\n7\n", "7"},
        {"5\n-2 -3 4 -1 2\n", "5"},
        {"4\n-1 -2 -3 -4\n", "-1"}
    };
}
else if (question == "6") {
    tests = {
        {"3\n1 2 4\n3\n1 3 4\n", "1 1 2 3 4 4"},
        {"2\n1 5\n2\n2 6\n", "1 2 5 6"},
        {"0\n3\n1 2 3\n", "1 2 3"},
        {"0\n0\n", ""},
        {"1\n5\n1\n2\n", "2 5"},
        {"3\n-3 0 8\n2\n-2 9\n", "-3 -2 0 8 9"}
    };
}
else if (question == "7") {
    tests = {
        {"4 5\n11110\n11010\n11000\n00000\n", "1"},
        {"4 5\n11000\n11000\n00100\n00011\n", "3"},
        {"2 2\n00\n00\n", "0"},
        {"2 2\n11\n11\n", "1"},
        {"1 1\n1\n", "1"},
        {"3 3\n101\n010\n101\n", "5"}
    };
}
else if (question == "8") {
    tests = {
        {"abcabcbb\n", "3"},
        {"bbbbb\n", "1"},
        {"abcdef\n", "6"},
        {"pwwkew\n", "3"},
        {"a\n", "1"},
        {"dvdf\n", "3"}
    };
}
else if (question == "9") {
    tests = {
        {"4\n4 5 2 25\n", "5 25 25 -1"},
        {"4\n4 3 2 1\n", "-1 -1 -1 -1"},
        {"1\n5\n", "-1"},
        {"3\n1 2 3\n", "2 3 -1"},
        {"5\n2 2 3 1 4\n", "3 3 4 4 -1"},
        {"4\n-2 -1 -3 0\n", "-1 0 0 -1"}
    };
}
else if (question == "10") {
    tests = {
        {"7\n3 9 20 -1 -1 15 7\n", "3 9 20 15 7"},
        {"3\n1 2 3\n", "1 2 3"},
        {"1\n5\n", "5"},
        {"0\n", ""},
        {"3\n1 -1 2\n", "1 2"},
        {"5\n1 2 3 4 5\n", "1 2 3 4 5"}
    };
}
else if (question == "11") {
    tests = {
        {"6 2\n3 2 1 5 6 4\n", "5"},
        {"4 1\n1 2 3 4\n", "4"},
        {"5 5\n1 2 3 4 5\n", "1"},
        {"5 3\n5 5 4 3 2\n", "4"},
        {"1 1\n-7\n", "-7"},
        {"6 3\n-1 -2 -3 -4 -5 -6\n", "-3"}
    };
}
else if (question == "12") {
    tests = {
        {"6 15\n10 5 2 7 1 9\n", "4"},
        {"5 3\n1 2 1 1 1\n", "3"},
        {"4 0\n1 -1 2 -2\n", "4"},
        {"3 10\n1 2 3\n", "0"},
        {"5 5\n-1 2 3 -2 2\n", "3"},
        {"1 7\n7\n", "1"}
    };
}
else if (question == "13") {
    tests = {
        {"4\n3 2 0 -4\n1\n", "true"},
        {"1\n1\n-1\n", "false"},
        {"3\n1 2 3\n-1\n", "false"},
        {"2\n1 2\n0\n", "true"},
        {"0\n-1\n", "false"},
        {"3\n1 2 3\n2\n", "true"}
    };
}
else if (question == "14") {
    tests = {
        {"2 1\n1 0\n", "true"},
        {"2 2\n1 0\n0 1\n", "false"},
        {"1 0\n", "true"},
        {"3 3\n1 0\n2 1\n0 2\n", "false"},
        {"4 3\n1 0\n2 1\n3 2\n", "true"},
        {"3 3\n1 0\n2 0\n2 1\n", "true"}
    };
}
else if (question == "15") {
    tests = {
        {"12\n0 1 0 2 1 0 1 3 2 1 2 1\n", "6"},
        {"6\n4 2 0 3 2 5\n", "9"},
        {"3\n2 0 2\n", "2"},
        {"4\n1 2 3 4\n", "0"},
        {"5\n3 0 0 2 0\n", "4"},
        {"1\n5\n", "0"}
    };
}
else if (question == "16") {
    tests = {
        {"0\n", "0"},
        {"1\n", "1"},
        {"2\n", "1"},
        {"6\n", "8"},
        {"7\n", "13"},
        {"10\n", "55"}
    };
}
else if (question == "17") {
    tests = {
        {"5\n1 2 3 4 5\n", "15"},
        {"4\n1 2 3 4\n", "10"},
        {"1\n9\n", "9"},
        {"3\n-1 -2 -3\n", "-6"},
        {"0\n", "0"},
        {"5\n0 0 0 0 0\n", "0"}
    };
}
else if (question == "18") {
    tests = {
        {"hello\n", "olleh"},
        {"abcd\n", "dcba"},
        {"a\n", "a"},
        {"racecar\n", "racecar"},
        {"ab\n", "ba"},
        {"12345\n", "54321"}
    };
}
else if (question == "19") {
    tests = {
        {"madam\n", "true"},
        {"hello\n", "false"},
        {"level\n", "true"},
        {"world\n", "false"},
        {"a\n", "true"},
        {"abba\n", "true"}
    };
}
else if (question == "20") {
    tests = {
        {"2 3\n", "8"},
        {"3 4\n", "81"},
        {"2 0\n", "1"},
        {"5 1\n", "5"},
        {"0 5\n", "0"},
        {"-2 3\n", "-8"}
    };
}
else if (question == "21") {
    tests = {
        {"0\n", "1"},
        {"1\n", "1"},
        {"5\n", "120"},
        {"7\n", "5040"},
        {"3\n", "6"},
        {"10\n", "3628800"}
    };
}
else if (question == "22") {
    tests = {
        {"5\n5 1 4 2 8\n", "1 2 4 5 8"},
        {"4\n4 3 2 1\n", "1 2 3 4"},
        {"1\n5\n", "5"},
        {"3\n-1 0 -5\n", "-5 -1 0"},
        {"5\n2 2 1 1 3\n", "1 1 2 2 3"},
        {"0\n", ""}
    };
}
else if (question == "23") {
    tests = {
        {"5\n64 25 12 22 11\n", "11 12 22 25 64"},
        {"4\n4 3 2 1\n", "1 2 3 4"},
        {"1\n8\n", "8"},
        {"3\n-1 0 -5\n", "-5 -1 0"},
        {"5\n3 3 2 2 1\n", "1 2 2 3 3"},
        {"0\n", ""}
    };
}
else if (question == "24") {
    tests = {
        {"6\n5 2 4 6 1 3\n", "1 2 3 4 5 6"},
        {"4\n4 3 2 1\n", "1 2 3 4"},
        {"1\n9\n", "9"},
        {"3\n-1 0 -5\n", "-5 -1 0"},
        {"5\n2 2 1 1 3\n", "1 1 2 2 3"},
        {"0\n", ""}
    };
}
else if (question == "25") {
    tests = {
        {"4\n5 2 3 1\n", "1 2 3 5"},
        {"4\n4 3 2 1\n", "1 2 3 4"},
        {"1\n7\n", "7"},
        {"3\n-1 0 -5\n", "-5 -1 0"},
        {"5\n3 3 2 2 1\n", "1 2 2 3 3"},
        {"0\n", ""}
    };
}
else if (question == "26") {
    tests = {
        {"6\n10 7 8 9 1 5\n", "1 5 7 8 9 10"},
        {"4\n4 3 2 1\n", "1 2 3 4"},
        {"1\n7\n", "7"},
        {"3\n-1 0 -5\n", "-5 -1 0"},
        {"5\n2 2 2 1 1\n", "1 1 2 2 2"},
        {"0\n", ""}
    };
}
else if (question == "27") {
    tests = {
        {"hello\n", "olleh"},
        {"abcd\n", "dcba"},
        {"a\n", "a"},
        {"level\n", "level"},
        {"12345\n", "54321"},
        {"ab\n", "ba"}
    };
}
else if (question == "28") {
    tests = {
        {"anagram nagaram\n", "true"},
        {"rat car\n", "false"},
        {"a a\n", "true"},
        {"abc ab\n", "false"},
        {"listen silent\n", "true"},
        {"aabb bbaa\n", "true"}
    };
}
else if (question == "29") {
    tests = {
        {"3\nflower flow flight\n", "fl"},
        {"3\ndog racecar car\n", ""},
        {"1\nhello\n", "hello"},
        {"2\nabc xyz\n", ""},
        {"3\ninterspecies interstellar interstate\n", "inters"},
        {"2\nsame same\n", "same"}
    };
}
else if (question == "30") {
    tests = {
        {"leetcode\n", "0"},
        {"loveleetcode\n", "2"},
        {"aabbc\n", "4"},
        {"aabb\n", "-1"},
        {"z\n", "0"},
        {"aabbcdde\n", "4"}
    };
}
else if (question == "31") {
    tests = {
        {"5\npush 3\npush 5\ngetMin\npop\ntop\n", "3\n3\n"},
        {"4\npush 7\ntop\ngetMin\npop\n", "7\n7\n"},
        {"2\npush 4\ngetMin\n", "4\n"},
        {"3\npush 2\npush 1\ngetMin\n", "1\n"},
        {"5\npush 5\npush 2\npush 2\npop\ngetMin\n", "2\n"},
        {"4\npush -3\npush -1\ntop\ngetMin\n", "-1\n-3\n"}
    };
}
else if (question == "32") {
    tests = {
        {"5\n2 1 + 3 *\n", "9"},
        {"5\n4 13 5 / +\n", "6"},
        {"1\n5\n", "5"},
        {"3\n2 3 +\n", "5"},
        {"3\n7 2 /\n", "3"},
        {"5\n5 1 2 + 4 * +\n", "17"}
    };
}
else if (question == "33") {
    tests = {
        {"6\n2 1 5 6 2 3\n", "10"},
        {"2\n2 4\n", "4"},
        {"1\n5\n", "5"},
        {"3\n0 0 0\n", "0"},
        {"4\n2 2 2 2\n", "8"},
        {"5\n1 2 3 4 5\n", "9"}
    };
}
else if (question == "34") {
    tests = {
        {"7\n3 9 20 -1 -1 15 7\n", "3"},
        {"1\n5\n", "1"},
        {"1\n9\n", "1"},
        {"3\n1 2 3\n", "2"},
        {"0\n", "0"},
        {"5\n1 2 -1 3 4\n", "3"}
    };
}
else if (question == "35") {
    tests = {
        {"4 5\n11110\n11010\n11000\n00000\n", "1"},
        {"4 5\n11000\n11000\n00100\n00011\n", "3"},
        {"1 1\n0\n", "0"},
        {"1 1\n1\n", "1"},
        {"3 3\n101\n010\n101\n", "5"},
        {"2 3\n111\n101\n", "1"}
    };
}
else if (question == "36") {
    tests = {
        {"7\n3 9 20 -1 -1 15 7\n", "3 9 20 15 7"},
        {"3\n1 2 3\n", "1 2 3"},
        {"1\n9\n", "9"},
        {"0\n", ""},
        {"3\n1 -1 2\n", "1 2"},
        {"5\n1 2 3 4 5\n", "1 2 3 4 5"}
    };
}
else if (question == "37") {
    tests = {
        {"7\n3 5 1 6 2 0 8\n5 1\n", "3"},
        {"7\n3 5 1 6 2 0 8\n6 2\n", "5"},
        {"3\n2 1 3\n1 3\n", "2"},
        {"3\n2 1 3\n1 1\n", "1"},
        {"1\n5\n5 5\n", "5"},
        {"7\n3 5 1 6 2 0 8\n6 8\n", "3"}
    };
}
else if (question == "38") {
    tests = {
        {"2 1\n1 0\n", "true"},
        {"2 2\n1 0\n0 1\n", "false"},
        {"1 0\n", "true"},
        {"3 3\n1 0\n2 1\n0 2\n", "false"},
        {"4 3\n1 0\n2 1\n3 2\n", "true"},
        {"3 3\n1 0\n2 0\n2 1\n", "true"}
    };
}
else if (question == "39") {
    tests = {
        {"7\n1 2 3 4 5 6 7\n4 7\n", "4"},
        {"7\n1 2 3 4 5 6 7\n4 5\n", "2"},
        {"3\n2 1 3\n1 3\n", "2"},
        {"3\n2 1 3\n1 1\n", "0"},
        {"7\n1 2 3 4 5 6 7\n4 6\n", "4"},
        {"7\n1 2 3 4 5 6 7\n8 4\n", "-1"}
    };
}
else {
    cout << "Unknown question";
    mysql_close(conn);
    return 1;
}


int passed = 0;
bool failed = false;

for (int i = 0; i < (int)tests.size(); i++) {
    ofstream input("test_input.txt");
    input << tests[i].first;
    input.close();

bool success = runWithTimeout(5000);

    string actual;
    ifstream output("test_output.txt");

    if (output) {
        actual.assign(
            (istreambuf_iterator<char>(output)),
            istreambuf_iterator<char>()
        );
        output.close();
    }

    string expected = tests[i].second;

    if (success &&
    normalize(actual) == normalize(expected)) {
        passed++;
    } else {
        failed = true;

        cout << "\nTest " << i + 1 << ": FAIL\n";
        cout << "Input:\n" << tests[i].first << "\n";
        cout << "-------------------------\n";
        cout << "Expected Output:\n";
        cout << (expected.empty() ? "(empty)" : expected) << "\n";
        cout << "-------------------------\n";
        cout << "Your Output:\n";
        cout << (actual.empty() ? "(empty)" : actual) << "\n";
        cout << "-------------------------\n";

        break;
    }
}

string finalStatus;
if (failed) {
    finalStatus = "NOT ACCEPTED";
    cout << "NOT ACCEPTED\n";
} else {
    finalStatus = "ACCEPTED";
    cout << "\nPassed: " << passed
         << "/" << tests.size() << "\n";
    cout << "ACCEPTED\n";
}

// Save every evaluated attempt, whether accepted or rejected.
if (conn) {
    Submission attempt(user_id, question_id, code, finalStatus);
    if (attempt.saveSubmission(conn))
        cout << "SUBMISSION_SAVED\n";
    else
        cout << "SUBMISSION_SAVE_FAILED\n";
    mysql_close(conn);
} else {
    cout << "SUBMISSION_NOT_SAVED_DATABASE_UNAVAILABLE\n";
}

return 0;
}