#include "User.h"
#include <iostream>

using namespace std;

User::User()
{
    id = 0;
}

User::User(string username, string email, string password)
{
    this->username = username;
    this->email = email;
    this->password = password;
}

void User::setUsername(string username)
{
    this->username = username;
}

void User::setEmail(string email)
{
    this->email = email;
}

void User::setPassword(string password)
{
    this->password = password;
}

string User::getUsername()
{
    return username;
}

string User::getEmail()
{
    return email;
}

string User::getPassword()
{
    return password;
}

bool User::login()
{
    // MySQL login logic will go here
    return false;
}