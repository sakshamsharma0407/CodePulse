#include <iostream>
#include <vector>
using namespace std;

vector<int> twoSet(vector<int>& nums, int target) {
    for (int i = 0; i < nums.size(); i++) {
        for (int j = i + 1; j < nums.size(); j++) {
            if (nums[i] + nums[j] == target) {
                return {i, j};
            }
        }
    }
    return {};
}

int main() {
    int n, target;
    cin >> n >> target;

    vector<int> nums(n);
    for (int i = 0; i < n; i++)
        cin >> nums[i];

    vector<int> ans = twoSet(nums, target);

    if (ans.size() == 2)
        cout << ans[0] << " " << ans[1];
    else
        cout << "-1";

    return 0;
}
