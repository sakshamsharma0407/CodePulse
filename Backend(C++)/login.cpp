#include <iostream>
#include <string>

using namespace std;

int main(int argc, char* argv[])
{
    if (argc < 3)
    {
        cout << "Missing username or password" << endl;
        return 1;
    }

    string username = argv[1];
    string password = argv[2];

    cout << "Username: " << username << endl;
    cout << "Password received" << endl;

    return 0;
}