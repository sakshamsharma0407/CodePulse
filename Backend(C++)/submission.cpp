
#include <iostream>
using namespace std;

long long power(int x, int n) {
    if (n == 0)
        return 1;

    if (n == 1)
        return x;

    long long half = power(x, n / 2);

    if (n % 2 == 0)
        return half * half;
    else
        return x * half * half;
}

int main() {
    int x, n;
    cin >> x >> n;

    cout << power(x, n);
    return 0;
}
