
#ifndef SUBMISSION_H
#define SUBMISSION_H

#include <iostream>
#include <string>
#include <mysql.h>

using namespace std;

class Submission {
private:
    int user_id;
    int question_id;
    string submitted_code;
    string status;

public:
    Submission(int uid, int qid, string code, string result) {
        user_id = uid;
        question_id = qid;
        submitted_code = code;
        status = result;
    }

    bool saveSubmission(MYSQL* conn) {
        if (conn == NULL) {
            cout << "Database connection failed";
            return false;
        }

        string query =
            "INSERT INTO submissions "
            "(user_id, question_id, submitted_code, status) "
            "VALUES (?, ?, ?, ?)";

        MYSQL_STMT* stmt = mysql_stmt_init(conn);

        if (stmt == NULL)
            return false;

        if (mysql_stmt_prepare(
                stmt, query.c_str(), query.length()) != 0) {
            cout << mysql_stmt_error(stmt);
            mysql_stmt_close(stmt);
            return false;
        }

        MYSQL_BIND params[4] = {};

        unsigned long codeLength = submitted_code.length();
        unsigned long statusLength = status.length();

        params[0].buffer_type = MYSQL_TYPE_LONG;
        params[0].buffer = &user_id;

        params[1].buffer_type = MYSQL_TYPE_LONG;
        params[1].buffer = &question_id;

        params[2].buffer_type = MYSQL_TYPE_STRING;
        params[2].buffer = const_cast<char*>(
            submitted_code.c_str());
        params[2].buffer_length = codeLength;
        params[2].length = &codeLength;

        params[3].buffer_type = MYSQL_TYPE_STRING;
        params[3].buffer = const_cast<char*>(
            status.c_str());
        params[3].buffer_length = statusLength;
        params[3].length = &statusLength;

        if (mysql_stmt_bind_param(stmt, params) != 0) {
            cout << mysql_stmt_error(stmt);
            mysql_stmt_close(stmt);
            return false;
        }

        if (mysql_stmt_execute(stmt) != 0) {
            cout << mysql_stmt_error(stmt);
            mysql_stmt_close(stmt);
            return false;
        }

        mysql_stmt_close(stmt);
        return true;
    }
};

#endif
