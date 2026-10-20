#include <iostream>
#include <string>
#include <cstring>
#include <cstdlib>
#include <regex>
#include <cctype>
#include <mysql.h>

using namespace std;

class User {
private:
    string email;
    string username;
    string passwordHash;

public:
    User(const string& e, const string& u, const string& hash)
        : email(e), username(u), passwordHash(hash) {}

    static string validateSignup(
        const string& email,
        const string& username,
        const string& password,
        const string& confirmPassword
    ) {
        if (email.empty() || username.empty() ||
            password.empty() || confirmPassword.empty()) {
            return "Please enter all details.";
        }

        const regex emailPattern(
            R"([A-Za-z0-9._%+-]+@gmail\.com)"
        );

        const regex usernamePattern(
            R"([A-Za-z0-9_]{3,30})"
        );

        if (!regex_match(email, emailPattern)) {
            return "Please enter a valid Gmail address.";
        }

        if (!regex_match(username, usernamePattern)) {
            return "Username must be 3-30 characters and contain only letters, numbers, and underscores.";
        }

        if (password != confirmPassword) {
            return "Passwords do not match.";
        }

        if (password.length() < 8) {
            return "Password must be at least 8 characters long.";
        }

        bool uppercase = false;
        bool special = false;

        for (unsigned char ch : password) {
            if (isupper(ch)) {
                uppercase = true;
            }

            if (!isalnum(ch) && !isspace(ch)) {
                special = true;
            }
        }

        if (!uppercase) {
            return "Password must contain an uppercase letter.";
        }

        if (!special) {
            return "Password must contain a special character.";
        }

        return "VALID";
    }

    bool signup() {
        const char* dbPassword = getenv("DB_PASSWORD");

        if (dbPassword == nullptr || strlen(dbPassword) == 0) {
            cerr << "ERROR: DB_PASSWORD is not set.\n";
            return false;
        }

        MYSQL* conn = mysql_init(nullptr);

        if (conn == nullptr) {
            cerr << "ERROR: MySQL initialization failed.\n";
            return false;
        }

        unsigned int timeout = 5;
        mysql_options(conn, MYSQL_OPT_CONNECT_TIMEOUT, &timeout);
        mysql_options(conn, MYSQL_OPT_READ_TIMEOUT, &timeout);
        mysql_options(conn, MYSQL_OPT_WRITE_TIMEOUT, &timeout);

        if (mysql_real_connect(
                conn,
                "127.0.0.1",
                "root",
                dbPassword,
                "codepulse",
                3306,
                nullptr,
                0
            ) == nullptr) {
            cerr << "ERROR: " << mysql_error(conn) << '\n';
            mysql_close(conn);
            return false;
        }

        // Check whether email or username already exists.
        const char* checkQuery =
            "SELECT id FROM users "
            "WHERE email = ? OR username = ? LIMIT 1";

        MYSQL_STMT* checkStmt = mysql_stmt_init(conn);

        if (checkStmt == nullptr) {
            cerr << "ERROR: " << mysql_error(conn) << '\n';
            mysql_close(conn);
            return false;
        }

        if (mysql_stmt_prepare(
                checkStmt,
                checkQuery,
                static_cast<unsigned long>(strlen(checkQuery))
            ) != 0) {
            cerr << "ERROR: "
                 << mysql_stmt_error(checkStmt) << '\n';
            mysql_stmt_close(checkStmt);
            mysql_close(conn);
            return false;
        }

        MYSQL_BIND params[2]{};

        params[0].buffer_type = MYSQL_TYPE_STRING;
        params[0].buffer = const_cast<char*>(email.c_str());
        params[0].buffer_length =
            static_cast<unsigned long>(email.size());

        params[1].buffer_type = MYSQL_TYPE_STRING;
        params[1].buffer = const_cast<char*>(username.c_str());
        params[1].buffer_length =
            static_cast<unsigned long>(username.size());

        bool queryOK =
            mysql_stmt_bind_param(checkStmt, params) == 0 &&
            mysql_stmt_execute(checkStmt) == 0 &&
            mysql_stmt_store_result(checkStmt) == 0;

        if (!queryOK) {
            cerr << "ERROR: "
                 << mysql_stmt_error(checkStmt) << '\n';
            mysql_stmt_close(checkStmt);
            mysql_close(conn);
            return false;
        }

        if (mysql_stmt_num_rows(checkStmt) > 0) {
            cout << "USER_EXISTS\n";

            mysql_stmt_free_result(checkStmt);
            mysql_stmt_close(checkStmt);
            mysql_close(conn);
            return false;
        }

        mysql_stmt_free_result(checkStmt);
        mysql_stmt_close(checkStmt);

        // Insert the new user.
        const char* insertQuery =
            "INSERT INTO users (email, username, password_hash) "
            "VALUES (?, ?, ?)";

        MYSQL_STMT* insertStmt = mysql_stmt_init(conn);

        if (insertStmt == nullptr) {
            cerr << "ERROR: " << mysql_error(conn) << '\n';
            mysql_close(conn);
            return false;
        }

        if (mysql_stmt_prepare(
                insertStmt,
                insertQuery,
                static_cast<unsigned long>(strlen(insertQuery))
            ) != 0) {
            cerr << "ERROR: "
                 << mysql_stmt_error(insertStmt) << '\n';
            mysql_stmt_close(insertStmt);
            mysql_close(conn);
            return false;
        }

        MYSQL_BIND insertParams[3]{};

        insertParams[0].buffer_type = MYSQL_TYPE_STRING;
        insertParams[0].buffer =
            const_cast<char*>(email.c_str());
        insertParams[0].buffer_length =
            static_cast<unsigned long>(email.size());

        insertParams[1].buffer_type = MYSQL_TYPE_STRING;
        insertParams[1].buffer =
            const_cast<char*>(username.c_str());
        insertParams[1].buffer_length =
            static_cast<unsigned long>(username.size());

        insertParams[2].buffer_type = MYSQL_TYPE_STRING;
        insertParams[2].buffer =
            const_cast<char*>(passwordHash.c_str());
        insertParams[2].buffer_length =
            static_cast<unsigned long>(passwordHash.size());

        bool success =
            mysql_stmt_bind_param(insertStmt, insertParams) == 0 &&
            mysql_stmt_execute(insertStmt) == 0;

        if (success) {
            cout << "SIGNUP_SUCCESS\n";
        } else {
            cerr << "ERROR: "
                 << mysql_stmt_error(insertStmt) << '\n';
            cout << "SIGNUP_FAILED\n";
        }

        mysql_stmt_close(insertStmt);
        mysql_close(conn);

        return success;
    }
};


int main(int argc, char* argv[]) {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // Mode 1: Validate form before OTP.
    if (argc > 1 && string(argv[1]) == "--validate") {
        string email, username, password, confirmPassword;

        if (!getline(cin, email) ||
            !getline(cin, username) ||
            !getline(cin, password) ||
            !getline(cin, confirmPassword)) {
            cout << "Please enter all details.\n";
            return 1;
        }

        cout << User::validateSignup(
            email, username, password, confirmPassword
        ) << '\n';

        return 0;
    }

    // Mode 2: Check whether email or username already exists.
    if (argc > 1 && string(argv[1]) == "--check") {
        string email, username;

        if (!getline(cin, email) || !getline(cin, username) ||
            email.empty() || username.empty()) {
            cout << "CHECK_FAILED\n";
            return 1;
        }

        const char* dbPassword = getenv("DB_PASSWORD");
        if (dbPassword == nullptr) {
            cerr << "DB_PASSWORD is not set.\n";
            return 2;
        }

        MYSQL* conn = mysql_init(nullptr);
        if (conn == nullptr) {
            cerr << "MYSQL_INIT_FAILED\n";
            return 2;
        }

        if (!mysql_real_connect(
                conn, "127.0.0.1", "root", dbPassword,
                "codepulse", 3306, nullptr, 0)) {
            cerr << mysql_error(conn) << '\n';
            mysql_close(conn);
            return 2;
        }

        const char* query =
            "SELECT id FROM users "
            "WHERE email = ? OR username = ? LIMIT 1";

        MYSQL_STMT* stmt = mysql_stmt_init(conn);

        if (stmt == nullptr ||
            mysql_stmt_prepare(
                stmt, query,
                static_cast<unsigned long>(strlen(query))
            ) != 0) {
            cerr << "QUERY_ERROR\n";
            if (stmt != nullptr) mysql_stmt_close(stmt);
            mysql_close(conn);
            return 2;
        }

        MYSQL_BIND params[2]{};
        unsigned long emailLen = email.size();
        unsigned long usernameLen = username.size();

        params[0].buffer_type = MYSQL_TYPE_STRING;
        params[0].buffer = email.data();
        params[0].buffer_length = emailLen;
        params[0].length = &emailLen;

        params[1].buffer_type = MYSQL_TYPE_STRING;
        params[1].buffer = username.data();
        params[1].buffer_length = usernameLen;
        params[1].length = &usernameLen;

        if (mysql_stmt_bind_param(stmt, params) != 0 ||
            mysql_stmt_execute(stmt) != 0 ||
            mysql_stmt_store_result(stmt) != 0) {
            cerr << mysql_stmt_error(stmt) << '\n';
            mysql_stmt_close(stmt);
            mysql_close(conn);
            return 2;
        }

        bool exists = mysql_stmt_num_rows(stmt) > 0;
        cout << (exists ? "USER_EXISTS\n" : "AVAILABLE\n");

        mysql_stmt_free_result(stmt);
        mysql_stmt_close(stmt);
        mysql_close(conn);
        return 0;
    }

    // Mode 3: Create account after OTP verification.
    string email, username, passwordHash;

    if (!getline(cin, email) ||
        !getline(cin, username) ||
        !getline(cin, passwordHash) ||
        email.empty() || username.empty() || passwordHash.empty()) {
        cout << "SIGNUP_FAILED\n";
        return 1;
    }

    User user(email, username, passwordHash);
    return user.signup() ? 0 : 1;
}