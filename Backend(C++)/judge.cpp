#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>

using namespace std;

int main()
{
    string code;
    string line;

    // Read submitted code
    while (getline(cin, line))
    {
        code += line + "\n";
    }

    if (code.empty())
    {
        cout << "No code submitted.";
        return 1;
    }

    // Save submission
    ofstream source("submission.cpp");

    if (!source)
    {
        cout << "Judge Error: Cannot create submission.cpp";
        return 1;
    }

    source << code;
    source.close();

    // Compile
    int compileResult = system(
    "g++ submission.cpp -o submission.exe 2> compile_error.txt"
);

if (compileResult != 0)
{
    cout << "Compilation Error:\n";

    ifstream errorFile("compile_error.txt");

    while (getline(errorFile, line))
        cout << line << '\n';

    errorFile.close();

    return 1;
}

// Run submission
int runResult = system(
    ".\\submission.exe > output.txt 2> runtime_error.txt"
);

if (runResult != 0)
{
    cout << "Runtime Error:\n";

    ifstream errorFile("runtime_error.txt");

    bool hasError = false;

    while (getline(errorFile, line))
    {
        cout << line << '\n';
        hasError = true;
    }

    errorFile.close();

    if (!hasError)
    {
        cout << "Program exited with code: "
             << runResult << '\n';
    }

    return 1;
}

// Read program output
ifstream outputFile("output.txt");

if (!outputFile)
{
    cout << "Judge Error: output.txt not found";
    return 1;
}

while (getline(outputFile, line))
    cout << line << '\n';

outputFile.close();

return 0;
}