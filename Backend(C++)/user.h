#ifndef USER_H
#define USER_H

#include <string>

class User
{
private:
    int id;
    std::string username;
    std::string email;
    std::string password;

public:
    User();
    User(std::string username, std::string email, std::string password);

    void setUsername(std::string username);
    void setEmail(std::string email);
    void setPassword(std::string password);

    std::string getUsername();
    std::string getEmail();
    std::string getPassword();

    bool login();
};

#endif