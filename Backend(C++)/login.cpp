#include <iostream>
#include <string>
#include <cstdlib>
#include <cstring>
#include <mysql.h>
using namespace std;
int main() {
    string username, password;
    if (!getline(cin, username) || !getline(cin, password)) {
        cout << "LOGIN_FAILED";
        return 0;
    }
    if (username.empty() || password.empty()) {
        cout << "LOGIN_FAILED";
        return 0;
    }
    const char* db_password = getenv("DB_PASSWORD");
    if (db_password == nullptr) {
        cerr << "DATABASE_CONFIG_ERROR";
        return 2;
    }
    MYSQL* conn = mysql_init(nullptr);
    if (conn == nullptr) {
        cerr << "MYSQL_INIT_FAILED";
        return 2;
    }
    if (!mysql_real_connect(
            conn,
            "localhost",
            "root",
            db_password,
            "codepulse",
            3306,
            nullptr,
            0)) {
        cerr << "DATABASE_ERROR: " << mysql_error(conn);
        mysql_close(conn);
        return 2;
    }
    const char* query =
        "SELECT password_hash FROM users "
        "WHERE username = ? LIMIT 1";
    MYSQL_STMT* stmt = mysql_stmt_init(conn);
    if (stmt == nullptr) {
        cerr << "QUERY_INIT_ERROR";
        mysql_close(conn);
        return 2;
    }
    if (mysql_stmt_prepare(
            stmt, query,
            static_cast<unsigned long>(strlen(query))) != 0) {
        cerr << "QUERY_ERROR: " << mysql_stmt_error(stmt);
        mysql_stmt_close(stmt);
        mysql_close(conn);
        return 2;
    }
    MYSQL_BIND param[1]{};
    unsigned long username_length =
        static_cast<unsigned long>(username.size());
    param[0].buffer_type = MYSQL_TYPE_STRING;
    param[0].buffer = username.data();
    param[0].buffer_length = username_length;
    param[0].length = &username_length;
    if (mysql_stmt_bind_param(stmt, param) != 0 ||
        mysql_stmt_execute(stmt) != 0) {
        cerr << "QUERY_ERROR: " << mysql_stmt_error(stmt);
        mysql_stmt_close(stmt);
        mysql_close(conn);
        return 2;
    }
    char hash_buffer[256]{};
    unsigned long hash_length = 0;
bool is_null = false;
bool error = false;
    MYSQL_BIND result[1]{};
    result[0].buffer_type = MYSQL_TYPE_STRING;
    result[0].buffer = hash_buffer;
    result[0].buffer_length = sizeof(hash_buffer) - 1;
    result[0].length = &hash_length;
    result[0].is_null = &is_null;
    result[0].error = &error;
    if (mysql_stmt_bind_result(stmt, result) != 0) {
        cerr << "RESULT_BIND_ERROR: " << mysql_stmt_error(stmt);
        mysql_stmt_close(stmt);
        mysql_close(conn);
        return 2;
    }
    int fetch_status = mysql_stmt_fetch(stmt);
    if (fetch_status == MYSQL_NO_DATA) {
        cout << "LOGIN_FAILED";
    } else if (fetch_status != 0 || is_null || error ||
               hash_length >= sizeof(hash_buffer)) {
        cerr << "RESULT_FETCH_ERROR: " << mysql_stmt_error(stmt);
        mysql_stmt_close(stmt);
        mysql_close(conn);
        return 2;
    } else {
        hash_buffer[hash_length] = '\0';
        cout << "HASH:" << hash_buffer;
    }
    mysql_stmt_free_result(stmt);
    mysql_stmt_close(stmt);
    mysql_close(conn);
    return 0;
}
