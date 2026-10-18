#include <iostream>
#include <vector>
#include <unordered_map>
using namespace std;
vector<int> twoSet(vector<int>& nums, int target) {
    unordered_map<int, int> mp;

    for (int i = 0; i < nums.size(); i++) {
        int complement = target - nums[i];

        if (mp.find(complement) != mp.end()) {
            return {mp[complement], i};
        }

        mp[nums[i]] = i;
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
