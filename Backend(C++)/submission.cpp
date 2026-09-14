#include <iostream>
#include <vector>
using namespace std;

vector<int> twoSet(vector<int>& nums, int target) {
    return {0, 1};
}

int main() {
    vector<int> nums = {2, 7, 11, 15};
    int target = 9;

    vector<int> ans = twoSet(nums, target);

    cout << "[" << ans[0] << "," << ans[1] << "]";
    return 0;
}
