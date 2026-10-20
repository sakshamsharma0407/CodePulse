
#include <iostream>
#include <string>
#include <cstdlib>
#include <cstring>
#include <mysql.h>

using namespace std;

int main() {
    string email;
    getline(cin, email);

    const char* dbPassword = getenv("DB_PASSWORD");

    if (email.empty() || dbPassword == nullptr) {
        cout << "EMAIL_CHECK_FAILED";
        return 1;
    }

    MYSQL* conn = mysql_init(nullptr);
    if (!conn) {
        cout << "EMAIL_CHECK_FAILED";
        return 1;
    }

    if (!mysql_real_connect(conn, "localhost", "root",
            dbPassword, "codepulse", 3306, nullptr, 0)) {
        cout << "EMAIL_CHECK_FAILED";
        mysql_close(conn);
        return 1;
    }

    const char* query = "SELECT 1 FROM users WHERE email = ? LIMIT 1";
    MYSQL_STMT* stmt = mysql_stmt_init(conn);

    if (!stmt || mysql_stmt_prepare(stmt, query, strlen(query)) != 0) {
        cout << "EMAIL_CHECK_FAILED";
        if (stmt) mysql_stmt_close(stmt);
        mysql_close(conn);
        return 1;
    }

    unsigned long length = static_cast<unsigned long>(email.size());
    MYSQL_BIND param{};
    param.buffer_type = MYSQL_TYPE_STRING;
    param.buffer = email.data();
    param.buffer_length = length;
    param.length = &length;

    int found = 0;
    MYSQL_BIND result{};
    result.buffer_type = MYSQL_TYPE_LONG;
    result.buffer = &found;

    if (mysql_stmt_bind_param(stmt, &param) != 0 ||
        mysql_stmt_execute(stmt) != 0 ||
        mysql_stmt_bind_result(stmt, &result) != 0) {
        cout << "EMAIL_CHECK_FAILED";
    } else if (mysql_stmt_fetch(stmt) == 0) {
        cout << "EMAIL_FOUND";
    } else {
        cout << "EMAIL_NOT_FOUND";
    }

    mysql_stmt_close(stmt);
    mysql_close(conn);
    return 0;
}

