
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

    if (!mysql_real_connect(
            conn, "localhost", "root",
            dbPassword, "codepulse", 3306, nullptr, 0)) {
        cout << "EMAIL_CHECK_FAILED";
        mysql_close(conn);
        return 1;
    }

    const char* query =
        "SELECT username FROM users WHERE email = ? LIMIT 1";

    MYSQL_STMT* stmt = mysql_stmt_init(conn);

    if (!stmt ||
        mysql_stmt_prepare(stmt, query, strlen(query)) != 0) {
        cout << "EMAIL_CHECK_FAILED";
        if (stmt) mysql_stmt_close(stmt);
        mysql_close(conn);
        return 1;
    }

    unsigned long emailLength =
        static_cast<unsigned long>(email.size());

    MYSQL_BIND param{};
    param.buffer_type = MYSQL_TYPE_STRING;
    param.buffer = email.data();
    param.buffer_length = emailLength;
    param.length = &emailLength;

    if (mysql_stmt_bind_param(stmt, &param) != 0 ||
        mysql_stmt_execute(stmt) != 0) {
        cout << "EMAIL_CHECK_FAILED";
        mysql_stmt_close(stmt);
        mysql_close(conn);
        return 1;
    }

    char username[256]{};
    unsigned long usernameLength = 0;
    my_bool usernameIsNull = 0;

    MYSQL_BIND result{};
    result.buffer_type = MYSQL_TYPE_STRING;
    result.buffer = username;
    result.buffer_length = sizeof(username) - 1;
    result.length = &usernameLength;
    result.is_null = &usernameIsNull;

    if (mysql_stmt_bind_result(stmt, &result) != 0) {
        cout << "EMAIL_CHECK_FAILED";
    } else {
        int fetchStatus = mysql_stmt_fetch(stmt);

        if (fetchStatus == 0 && !usernameIsNull &&
            usernameLength < sizeof(username)) {

            username[usernameLength] = '\0';

            cout << "EMAIL_FOUND\n";
            cout << "USERNAME:" << username;
        } else if (fetchStatus == MYSQL_NO_DATA) {
            cout << "EMAIL_NOT_FOUND";
        } else {
            cout << "EMAIL_CHECK_FAILED";
        }
    }

    mysql_stmt_close(stmt);
    mysql_close(conn);

    return 0;
}
