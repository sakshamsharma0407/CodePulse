import streamlit as st
import bcrypt
import random
import smtplib
from email.message import EmailMessage
import subprocess
import os
import subprocess
from streamlit_ace import st_ace
from openai import OpenAI
import smtplib
import ssl
from pathlib import Path
import mysql.connector
import json
BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_PATH = BASE_DIR / "Backend(C++)"
LOGIN_PATH = BACKEND_PATH / "login.exe"
SIGNUP_PATH = BACKEND_PATH / "signup.exe"
RECOVERY_PATH = BACKEND_PATH / "recovery.exe"
PROGRESS_PATH = BACKEND_PATH / "progress.exe"
CHECK_EMAIL_PATH = os.path.join(BACKEND_PATH, "recovery.exe")
EVALUATOR_PATH = BACKEND_PATH / "evaluator.exe"
history_path = os.path.join(BACKEND_PATH, "history.exe")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
def codepulse_chatbot(problem):
    st.subheader("🤖 CodePulse AI")
    chat_key = f"chat_messages_{problem['title']}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = []
    for message in st.session_state[chat_key]:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    prompt = st.chat_input(
        f"Ask about {problem['title']}..."
    )
    if prompt:
        st.session_state[chat_key].append({
            "role": "user",
            "content": prompt
        })
        try:
            with st.spinner("🤖 CodePulse AI is thinking..."):
                response = client.responses.create(
                model="gpt-5.6-luna",
                instructions="""
You are CodePulse AI, a coding tutor.

Rules:
1. Give hints which doesnt contain any code.
2. Keep responses under 100 words.
3. Use simple, beginner-friendly language.
4. Answer only about the current coding problem.
5. For debugging, briefly explain the likely issue.
6. Give short time and space complexity explanations.
7. Do not give the any solution and tell sorry they can,t.
8. Do not invent hidden test cases.
9. Encourage the student to think and try the problem.
""",
                    input=(
                f"Problem: {problem['title']}\n\n"
                f"Description: {problem['description']}\n\n"
                f"Student question: {prompt}"
            )
        )
                answer = response.output_text

        except Exception as e:
            answer = f"AI Error: {e}"
        st.session_state[chat_key].append({
            "role": "assistant",
            "content": answer
        })

        st.rerun()
st.markdown("""
<style>

/* OUTER COMBINED BOX */
.st-key-problem1_box {
    background-color: #222222 !important;
    border: 1px solid #454d52 !important;
    border-radius: 10px !important;
    padding: 0 !important;
    overflow: hidden !important;
}

/* TITLE BACKGROUND */
.st-key-problem1_title {
    background-color: #222222 !important;
    padding: 15px 20px !important;
    border-bottom: 1px solid #454d52 !important;
}

/* QUESTION BACKGROUND */
.st-key-problem1_question {
    background-color: #1a1a1a !important;
    padding: 15px 20px !important;
}

/* SOLVE BUTTON */
.st-key-problem1_question button {
    background-color: #1976D2 !important;
    color: white !important;
    border: 1px solid #1976D2 !important;
}

.st-key-problem1_question button:hover {
    background-color: #1565C0 !important;
    border-color: #1565C0 !important;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
.st-key-login_box {
    background-color: #1a1a1a !important;
    border: 1px solid #444444 !important;
    border-radius: 10px !important;
    padding: 30px !important;
    box-sizing: border-box !important;
    min-height: 450px !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
.st-key-otp_box {
    background-color: #1a1a1a !important;
    border: 1px solid #444444 !important;
    border-radius: 10px !important;
    padding: 30px !important;
    box-sizing: border-box !important;
    min-height: 100px !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
.block-container {
    padding-top: 0rem;
    padding-left: 3rem;
    padding-right: 3rem;
    max-width: 100%;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
    .stApp {
        background-color: #151515;
    }

    .block-container {
        background-color: #151515;
    }
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* OTHER BUTTONS */
div.stButton > button {
    background-color: #151515 !important;
    color: white !important;
    border: 2px solid #151515 !important;
    border-radius: 8px !important;
}
/* =========================
   NAVIGATION BAR
   ========================= */

.st-key-navbar {
    background-color: #1a1a1a !important;

    width: 100vw !important;
    max-width: 100vw !important;
    border: 1px solid #555555 !important;
    margin-left: calc(50% - 50vw) !important;
    margin-right: calc(50% - 50vw) !important;

    margin-top: -5rem  !important;
    padding: 10px 15px !important;

    box-sizing: border-box !important;
}
/* OTHER BUTTONS HOVER */
div.stButton > button:hover {
    background-color: #151515!important;
    color: white !important;
    border: 2px solid #151515 !important;
}

/* NAVBAR — keep unchanged */
.st-key-navbar div.stButton > button {
    background-color: #1a1a1a !important;
    color: white !important;
    border: 1px solid #1a1a1a !important;
}

.st-key-nav div.stButton > button {
    background-color: #222222 !important;
    color: white !important;
    border: 1px solid #444444 !important;
}

.st-key-nav div.stButton > button:hover {
    background-color: #333333 !important;
    border: 1px solid #555555 !important;
}: 1px solid #1a1a1a !important;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

.st-key-submit_problem1 button {
    background-color: #00c853 !important;
    color: white !important;
    border: 1px solid #00c853 !important;
    border-radius: 8px !important;
}

.st-key-submit_problem1 button:hover {
    background-color: #00a844 !important;
    border-color: #00a844 !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

.st-key-description_box {
    background-color: #1a1a1a !important;
    border: 1px solid #454d52 !important;
    border-radius: 10px !important;
    padding: 20px !important;
    margin-top: 15px !important;
}

</style>
""", unsafe_allow_html=True)
question_topics = {
    1: ["Arrays"],
    2: ["Linked List"],
    3: ["Stack"],
    4: ["Binary Search"],
    5: ["Arrays"],
    6: ["Linked List"],
    7: ["Graphs"],
    8: ["Strings"],
    9: ["Arrays"],
    10: ["Trees"],
    11: ["Arrays"],
    12: ["Arrays"],
    13: ["Linked List"],
    14: ["Graphs"],
    15: ["Stack"],
    16: ["Recursion"],
    17: ["Arrays", "Recursion"],
    18: ["Strings", "Recursion"],
    19: ["Strings", "Recursion"],
    20: ["Recursion"],
    21: ["Recursion"],
    22: ["Arrays", "Sorting"],
    23: ["Arrays", "Sorting"],
    24: ["Arrays", "Sorting"],
    25: ["Arrays", "Sorting"],
    26: ["Arrays", "Sorting"],
    27: ["Strings"],
    28: ["Strings"],
    29: ["Arrays", "Strings"],
    30: ["Strings"],
    31: ["Stack"],
    32: ["Stack"],
    33: ["Arrays"],
    34: ["Trees"],
    35: ["Trees"],
    36: ["Trees"],
    37: ["Trees"],
    38: ["Graphs"],
    39: ["Graphs", "Trees"]
}
questions = {
    1: {
        "title": "Two Sum Array",
"difficulty": "Easy",
"description": (
    "You are given a list of integers and a target value. "
    "Your task is to find two different elements in the list "
    "whose sum is equal to the given target."
),
"example": """Input: nums = [2,7,11,15], target = 9
Output: [0,1]""",
"starter_code": """#include <iostream>
#include <vector>
using namespace std;

vector<int> twoSum(vector<int>& nums, int target) {
    // Student writes solution here
}

int main() {
    int n, target;
    cin >> n >> target;

    vector<int> nums(n);
    for (int i = 0; i < n; i++)
        cin >> nums[i];

    vector<int> ans = twoSum(nums, target);

    if (ans.size() == 2)
        cout << ans[0] << " " << ans[1];
    else
        cout << "-1";

    return 0;
}"""
    },

    2: {
        "title": "Reverse a linked list in groups of K",
        "difficulty": "Hard",
        "description": "Reverse the given linked list in groups of K nodes.",
        "example": """Input: 1 -> 2 -> 3 -> 4 -> 5, k = 2
Output: 2 -> 1 -> 4 -> 3 -> 5""",
        "starter_code": """#include <iostream>
using namespace std;

struct Node {
    int data;
    Node* next;
    Node(int val) : data(val), next(nullptr) {}
};

Node* reverseKGroup(Node* head, int k) {
    // Student writes their solution here
}
int main() {
    int n, k;
    cin >> n >> k;

    Node* head = nullptr;
    Node* tail = nullptr;

    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        Node* node = new Node(x);

        if (!head)
            head = tail = node;
        else {
            tail->next = node;
            tail = node;
        }
    }

    head = reverseKGroup(head, k);

    while (head) {
        cout << head->data;
        if (head->next) cout << " ";
        head = head->next;
    }

    return 0;
}"""
    },
    3: {
        "title": "Valid Parentheses",
        "difficulty": "Easy",
        "description": (
            "Given a string containing '(', ')', '{', '}', '[' and ']'. "
            "Determine whether the brackets are valid, correctly matched "
            "and properly nested."
        ),
        "example": """Input: s = "()[]{}"
Output: true""",
        "starter_code": """#include <iostream>
#include <string>
#include <stack>
using namespace std;

bool isValid(string s) {
    // Write your code here
}

int main() {
    string s;
    cin >> s;

    cout << (isValid(s) ? "true" : "false");
    return 0;
}"""
    },

    4: {
        "title": "Binary Search",
        "difficulty": "Easy",
        "description": (
            "Given a sorted array of integers and a target value, find the "
            "index of the target using binary search. Return -1 if the target "
            "does not exist."
        ),
        "example": """Input: nums = [1,3,5,7,9], target = 5
Output: 2""",
        "starter_code": """#include <iostream>
#include <vector>
using namespace std;

int binarySearch(vector<int>& nums, int target) {
    // Write your code here
}

int main() {
    int n, target;
    cin >> n;

    vector<int> nums(n);
    for (int i = 0; i < n; i++)
        cin >> nums[i];

    cin >> target;
    cout << binarySearch(nums, target);

    return 0;
}"""
    },

    5: {
        "title": "Maximum Subarray",
        "difficulty": "Easy",
        "description": (
            "Given an integer array, find the contiguous subarray with the "
            "largest sum and return the maximum sum."
        ),
        "example": """Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6""",
        "starter_code": """#include <iostream>
#include <vector>
using namespace std;

int maxSubArray(vector<int>& nums) {
    // Write your code here
}
int main() {
    int n;
    cin >> n;

    vector<int> nums(n);
    for (int i = 0; i < n; i++) {
        cin >> nums[i];
    }

    cout << maxSubArray(nums);

    return 0;
}"""
    },

    6: {
        "title": "Merge Two Sorted Lists",
        "difficulty": "Easy",
        "description": (
            "Given the heads of two sorted linked lists, merge them into "
            "one sorted linked list and return its head."
        ),
        "example": """Input:
List 1: 1 -> 2 -> 4
List 2: 1 -> 3 -> 4

Output:
1 -> 1 -> 2 -> 3 -> 4 -> 4""",
        "starter_code": """#include <iostream>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;

    ListNode(int x) {
        val = x;
        next = NULL;
    }
};

ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
    // Write your code here
}

int main() {
    int n, m;
    cin >> n;

    ListNode* list1 = nullptr;
    ListNode* tail1 = nullptr;

    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        ListNode* node = new ListNode(x);

        if (!list1) list1 = tail1 = node;
        else {
            tail1->next = node;
            tail1 = node;
        }
    }

    cin >> m;

    ListNode* list2 = nullptr;
    ListNode* tail2 = nullptr;

    for (int i = 0; i < m; i++) {
        int x;
        cin >> x;
        ListNode* node = new ListNode(x);

        if (!list2) list2 = tail2 = node;
        else {
            tail2->next = node;
            tail2 = node;
        }
    }

    ListNode* ans = mergeTwoLists(list1, list2);

    while (ans) {
        cout << ans->val;
        if (ans->next) cout << " ";
        ans = ans->next;
    }

    return 0;
}"""
    },

    7: {
        "title": "Number of Islands",
        "difficulty": "Medium",
        "description": (
            "Given a 2D grid containing '1' representing land and '0' "
            "representing water, count the number of islands."
        ),
        "example": """Input:
[
  ["1","1","0","0"],
  ["1","0","0","1"],
  ["0","0","1","1"],
  ["0","0","0","0"]
]

Output: 2""",
        "starter_code": """#include <iostream>
#include <vector>
using namespace std;

void dfs(vector<vector<char>>& grid, int r, int c) {
    // Write your code here
}

int numIslands(vector<vector<char>>& grid) {
    // Write your code here
}

int main() {
    int rows, cols;
    cin >> rows >> cols;

    vector<vector<char>> grid(rows, vector<char>(cols));

    for (int i = 0; i < rows; i++)
        for (int j = 0; j < cols; j++)
            cin >> grid[i][j];

    cout << numIslands(grid);
    return 0;
}"""
    },

    8: {
        "title": "Longest Substring Without Repeating Characters",
        "difficulty": "Medium",
        "description": (
            "Given a string, find the length of the longest substring "
            "that contains no repeated characters."
        ),
        "example": """Input: s = "abcabcbb"
Output: 3

Explanation: The answer is "abc".""",
        "starter_code": """#include <iostream>
#include <string>
#include <unordered_set>
using namespace std;

int lengthOfLongestSubstring(string s) {
    // Write your code here
}

int main() {
    string s;
    cin >> s;

    cout << lengthOfLongestSubstring(s);
    return 0;
}"""
    },

    9: {
        "title": "Next Greater Element",
        "difficulty": "Medium",
        "description": (
            "For every element in the array, find the first greater element "
            "to its right. If no greater element exists, return -1."
        ),
        "example": """Input: nums = [4,5,2,10,8]
Output: [5,10,10,-1,-1]""",
        "starter_code": """#include <iostream>
#include <vector>
#include <stack>
using namespace std;

vector<int> nextGreaterElement(vector<int>& nums) {
    // Write your code here
}

int main() {
    int n;
    cin >> n;

    vector<int> nums(n);
    for (int i = 0; i < n; i++)
        cin >> nums[i];

    vector<int> ans = nextGreaterElement(nums);

    for (int i = 0; i < (int)ans.size(); i++) {
        if (i) cout << " ";
        cout << ans[i];
    }

    return 0;
}"""
    },

    10: {
        "title": "Binary Tree Level Order Traversal",
        "difficulty": "Medium",
        "description": (
            "Given the root of a binary tree, return the values of its "
            "nodes level by level from left to right."
        ),
        "example": """Input:
        3
       / \\
      9  20
         / \\
        15  7

Output: [[3],[9,20],[15,7]]""",
        "starter_code": """#include <iostream>
#include <vector>
#include <queue>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;

    TreeNode(int x) {
        val = x;
        left = NULL;
        right = NULL;
    }
};

vector<vector<int>> levelOrder(TreeNode* root) {
    // Write your code here
}

int main() {
    int n;
    cin >> n;

    if (n == 0) {
        cout << "";
        return 0;
    }

    vector<int> values(n);
    for (int i = 0; i < n; i++)
        cin >> values[i];

    if (values[0] == -1) {
        cout << "";
        return 0;
    }

    vector<TreeNode*> nodes(n, nullptr);

    for (int i = 0; i < n; i++)
        if (values[i] != -1)
            nodes[i] = new TreeNode(values[i]);

    for (int i = 0; i < n; i++) {
        if (!nodes[i]) continue;

        int left = 2 * i + 1;
        int right = 2 * i + 2;

        if (left < n) nodes[i]->left = nodes[left];
        if (right < n) nodes[i]->right = nodes[right];
    }

    vector<vector<int>> ans = levelOrder(nodes[0]);

    for (const auto& level : ans)
        for (int x : level)
            cout << x << " ";

    return 0;
}"""
    },

    11: {
        "title": "Kth Largest Element",
        "difficulty": "Medium",
        "description": (
            "Given an integer array and an integer k, return the kth "
            "largest element in the array."
        ),
        "example": """Input: nums = [3,2,1,5,6,4], k = 2
Output: 5""",
        "starter_code": """#include <iostream>
#include <vector>
#include <queue>
using namespace std;

int findKthLargest(vector<int>& nums, int k) {
    // Write your code here
}

int main() {
    int n, k;
    cin >> n >> k;

    vector<int> nums(n);
    for (int i = 0; i < n; i++)
        cin >> nums[i];

    cout << findKthLargest(nums, k);
    return 0;
}"""
    },

    12: {
        "title": "Longest Subarray With Sum K",
        "difficulty": "Medium",
        "description": (
            "Given an array of integers and an integer K, find the length "
            "of the longest subarray whose sum is equal to K."
        ),
        "example": """Input: nums = [10,5,2,7,1,9], k = 15
Output: 4""",
        "starter_code": """#include <iostream>
#include <vector>
#include <unordered_map>
using namespace std;

int longestSubarray(vector<int>& nums, int k) {
    // Write your code here
}

int main() {
    int n, k;
    cin >> n >> k;

    vector<int> nums(n);
    for (int i = 0; i < n; i++)
        cin >> nums[i];

    cout << longestSubarray(nums, k);
    return 0;
}"""
    },

    13: {
        "title": "Detect Cycle in Linked List",
        "difficulty": "Medium",
        "description": (
            "Given the head of a linked list, determine whether the linked "
            "list contains a cycle."
        ),
        "example": """Input: 3 -> 2 -> 0 -> -4
                 ^         |
                 |___|

Output: true""",
        "starter_code": """#include <iostream>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;

    ListNode(int x) {
        val = x;
        next = NULL;
    }
};

bool hasCycle(ListNode* head) {
    // Write your code here
}

int main() {
    int n;
    cin >> n;

    vector<ListNode*> nodes;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        nodes.push_back(new ListNode(x));
        if (i > 0)
            nodes[i - 1]->next = nodes[i];
    }

    int pos;
    cin >> pos;

    if (n > 0 && pos >= 0 && pos < n)
        nodes[n - 1]->next = nodes[pos];

    cout << (hasCycle(n ? nodes[0] : nullptr) ? "true" : "false");
    return 0;
}"""
    },

    14: {
        "title": "Course Schedule",
        "difficulty": "Medium",
        "description": (
            "There are a number of courses you need to take. Some courses "
            "have prerequisites. Determine whether it is possible to finish "
            "all courses."
        ),
        "example": """Input: numCourses = 2
prerequisites = [[1,0]]

Output: true""",
        "starter_code": """#include <iostream>
#include <vector>
using namespace std;

bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
    // Write your code here
}

int main() {
    int n, m;
    cin >> n >> m;

    vector<vector<int>> prerequisites(m, vector<int>(2));

    for (int i = 0; i < m; i++)
        cin >> prerequisites[i][0] >> prerequisites[i][1];

    cout << (canFinish(n, prerequisites) ? "true" : "false");
    return 0;
}"""
    },

    15: {
        "title": "Trapping Rain Water",
        "difficulty": "Hard",
        "description": (
            "Given an array representing the height of bars, calculate "
            "how much rainwater can be trapped between the bars."
        ),
        "example": """Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6""",
        "starter_code": """#include <iostream>
#include <vector>
using namespace std;

int trap(vector<int>& height) {
    // Write your code here
}

int main() {
    int n;
    cin >> n;

    vector<int> height(n);
    for (int i = 0; i < n; i++)
        cin >> height[i];

    cout << trap(height);
    return 0;
}
"""
    },
    16: {
    "title": "Fibonacci Number",
    "difficulty": "Easy",
    "description": (
        "Given an integer n, return the nth Fibonacci number using recursion."
    ),
    "example": """Input: n = 6
Output: 8""",
    "starter_code": """#include <iostream>
using namespace std;

int fibonacci(int n) {
    // Write your code here
}

int main() {
    int n;
    cin >> n;

    cout << fibonacci(n);
    return 0;
}"""
},

17: {
    "title": "Sum of Array Using Recursion",
    "difficulty": "Easy",
    "description": (
        "Given an integer array, calculate the sum of all its elements "
        "using recursion."
    ),
    "example": """Input: nums = [1,2,3,4,5]
Output: 15""",
    "starter_code": """#include <iostream>
#include <vector>
using namespace std;

int arraySum(vector<int>& nums, int index) {
    // Write your code here
}

int main() {
    int n;
    cin >> n;

    vector<int> nums(n);
    for (int i = 0; i < n; i++)
        cin >> nums[i];

    cout << arraySum(nums, 0);
    return 0;
}"""
},

18: {
    "title": "Reverse a String Using Recursion",
    "difficulty": "Easy",
    "description": (
        "Given a string, reverse it using recursion."
    ),
    "example": """Input: s = "hello"
Output: "olleh" """,
    "starter_code": """#include <iostream>
#include <string>
using namespace std;

void reverseString(string& s, int left, int right) {
    // Write your code here
}

int main() {
    string s;
    cin >> s;

    if (!s.empty())
        reverseString(s, 0, (int)s.size() - 1);

    cout << s;
    return 0;
}"""
},

19: {
    "title": "Check Palindrome Using Recursion",
    "difficulty": "Easy",
    "description": (
        "Given a string, determine whether it is a palindrome using recursion."
    ),
    "example": """Input: s = "madam"
Output: true""",
    "starter_code": """#include <iostream>
#include <string>
using namespace std;

bool isPalindrome(string& s, int left, int right) {
    // Write your code here
}

int main() {
    string s;
    cin >> s;

    cout << (isPalindrome(s, 0, (int)s.size() - 1)
             ? "true" : "false");

    return 0;
}"""
},

20: {
    "title": "Power of a Number",
    "difficulty": "Medium",
    "description": (
        "Given two integers x and n, calculate x raised to the power n "
        "using recursion."
    ),
    "example": """Input: x = 2, n = 5
Output: 32""",
    "starter_code": """#include <iostream>
using namespace std;

long long power(int x, int n) {
    // Write your code here
}

int main() {
    int x, n;
    cin >> x >> n;

    cout << power(x, n);
    return 0;
}"""
},

21: {
    "title": "Factorial Using Recursion",
    "difficulty": "Easy",
    "description": (
        "Given a non-negative integer n, return its factorial using recursion."
    ),
    "example": """Input: n = 5
Output: 120""",
    "starter_code": """#include <iostream>
using namespace std;

long long factorial(int n) {
    // Write your code here
}

int main() {
    int n;
    cin >> n;

    cout << factorial(n);
    return 0;
}"""
},

22: {
    "title": "Bubble Sort",
    "difficulty": "Easy",
    "description": (
        "Given an array of integers, sort the array in ascending order "
        "using Bubble Sort."
    ),
    "example": """Input: nums = [5,1,4,2,8]
Output: [1,2,4,5,8]""",
    "starter_code": """#include <iostream>
#include <vector>
using namespace std;

void bubbleSort(vector<int>& nums) {
    // Write your code here
}

int main() {
    int n;
    cin >> n;

    vector<int> nums(n);
    for (int i = 0; i < n; i++)
        cin >> nums[i];

    bubbleSort(nums);

    for (int i = 0; i < n; i++) {
        if (i) cout << " ";
        cout << nums[i];
    }

    return 0;
}"""
},

23: {
    "title": "Selection Sort",
    "difficulty": "Easy",
    "description": (
        "Sort an array of integers in ascending order using Selection Sort."
    ),
    "example": """Input: nums = [64,25,12,22,11]
Output: [11,12,22,25,64]""",
    "starter_code": """#include <iostream>
#include <vector>
using namespace std;

void selectionSort(vector<int>& nums) {
    // Write your code here
}

int main() {
    int n;
    cin >> n;

    vector<int> nums(n);
    for (int i = 0; i < n; i++)
        cin >> nums[i];

    selectionSort(nums);

    for (int i = 0; i < n; i++) {
        if (i) cout << " ";
        cout << nums[i];
    }

    return 0;
}"""
},

24: {
    "title": "Insertion Sort",
    "difficulty": "Easy",
    "description": (
        "Sort an array of integers in ascending order using Insertion Sort."
    ),
    "example": """Input: nums = [5,2,4,6,1,3]
Output: [1,2,3,4,5,6]""",
    "starter_code": """#include <iostream>
#include <vector>
using namespace std;

void insertionSort(vector<int>& nums) {
    // Write your code here
}

int main() {
    int n;
    cin >> n;

    vector<int> nums(n);
    for (int i = 0; i < n; i++)
        cin >> nums[i];

    insertionSort(nums);

    for (int i = 0; i < n; i++) {
        if (i) cout << " ";
        cout << nums[i];
    }

    return 0;
}"""
},

25: {
    "title": "Merge Sort",
    "difficulty": "Medium",
    "description": (
        "Sort an array of integers in ascending order using the Merge Sort algorithm."
    ),
    "example": """Input: nums = [5,2,3,1]
Output: [1,2,3,5]""",
    "starter_code": """#include <iostream>
#include <vector>
using namespace std;

void mergeSort(vector<int>& nums, int left, int right) {
    // Write your code here
}

int main() {
    int n;
    cin >> n;

    vector<int> nums(n);
    for (int i = 0; i < n; i++)
        cin >> nums[i];

    if (n > 0)
        mergeSort(nums, 0, n - 1);

    for (int i = 0; i < n; i++) {
        if (i) cout << " ";
        cout << nums[i];
    }

    return 0;
}"""
},

26: {
    "title": "Quick Sort",
    "difficulty": "Medium",
    "description": (
        "Sort an array of integers in ascending order using the Quick Sort algorithm."
    ),
    "example": """Input: nums = [10,7,8,9,1,5]
Output: [1,5,7,8,9,10]""",
    "starter_code": """#include <iostream>
#include <vector>
using namespace std;

void quickSort(vector<int>& nums, int low, int high) {
    // Write your code here
}

int main() {
    int n;
    cin >> n;

    vector<int> nums(n);
    for (int i = 0; i < n; i++)
        cin >> nums[i];

    if (n > 0)
        quickSort(nums, 0, n - 1);

    for (int i = 0; i < n; i++) {
        if (i) cout << " ";
        cout << nums[i];
    }

    return 0;
}"""
},

27: {
    "title": "Reverse a String",
    "difficulty": "Easy",
    "description": (
        "Given a string, reverse the characters of the string."
    ),
    "example": """Input: s = "hello"
Output: "olleh" """,
    "starter_code": """#include <iostream>
#include <string>
using namespace std;

string reverseString(string s) {
    // Write your code here
}

int main() {
    string s;
    cin >> s;

    cout << reverseString(s);
    return 0;
}"""
},

28: {
    "title": "Valid Anagram",
    "difficulty": "Easy",
    "description": (
        "Given two strings, determine whether one string is an anagram "
        "of the other."
    ),
    "example": """Input: s = "anagram", t = "nagaram"
Output: true""",
    "starter_code": """#include <iostream>
#include <string>
using namespace std;

bool isAnagram(string s, string t) {
    // Write your code here
}

int main() {
    string s, t;
    cin >> s >> t;

    cout << (isAnagram(s, t) ? "true" : "false");
    return 0;
}"""
},

29: {
    "title": "Longest Common Prefix",
    "difficulty": "Easy",
    "description": (
        "Given an array of strings, find the longest common prefix "
        "shared by all strings."
    ),
    "example": """Input: strs = ["flower","flow","flight"]
Output: "fl" """,
    "starter_code": """#include <iostream>
#include <vector>
#include <string>
using namespace std;

string longestCommonPrefix(vector<string>& strs) {
    // Write your code here
}

int main() {
    int n;
    cin >> n;

    vector<string> strs(n);
    for (int i = 0; i < n; i++)
        cin >> strs[i];

    cout << longestCommonPrefix(strs);
    return 0;
}"""
},

30: {
    "title": "First Non-Repeating Character",
    "difficulty": "Easy",
    "description": (
        "Given a string, find the first character that appears only once. "
        "Return its index."
    ),
    "example": """Input: s = "leetcode"
Output: 0""",
    "starter_code": """#include <iostream>
#include <string>
using namespace std;

int firstUniqChar(string s) {
    // Write your code here
}

int main() {
    string s;
    cin >> s;

    cout << firstUniqChar(s);
    return 0;
}"""
},

31: {
    "title": "Min Stack",
    "difficulty": "Medium",
    "description": (
        "Design a stack that supports push, pop, top, and retrieving "
        "the minimum element in constant time."
    ),
    "example": """Input:
push(3)
push(2)
push(1)
getMin()

Output:
1""",
    "starter_code": """#include <iostream>
#include <stack>
using namespace std;

class MinStack {
private:
    stack<int> st;
    stack<int> minSt;

public:
    void push(int val) {
        // Write your code here
    }

    void pop() {
        // Write your code here
    }

    int top() {
        // Write your code here
    }

    int getMin() {
        // Write your code here
    }
};

int main() {
    MinStack st;
    int n;
    cin >> n;

    while (n--) {
        string operation;
        cin >> operation;

        if (operation == "push") {
            int value;
            cin >> value;
            st.push(value);
        } else if (operation == "pop") {
            st.pop();
        } else if (operation == "top") {
            cout << st.top() << "\n";
        } else if (operation == "getMin") {
            cout << st.getMin() << "\n";
        }
    }

    return 0;
}"""
},

32: {
    "title": "Evaluate Reverse Polish Notation",
    "difficulty": "Medium",
    "description": (
        "Evaluate an arithmetic expression written in Reverse Polish "
        "Notation using a stack."
    ),
    "example": """Input: tokens = ["2","1","+","3","*"]
Output: 9""",
    "starter_code": """#include <iostream>
#include <vector>
#include <string>
#include <stack>
using namespace std;

int evalRPN(vector<string>& tokens) {
    // Write your code here
}

int main() {
    int n;
    cin >> n;

    vector<string> tokens(n);
    for (int i = 0; i < n; i++)
        cin >> tokens[i];

    cout << evalRPN(tokens);
    return 0;
}"""
},

33: {
    "title": "Largest Rectangle in Histogram",
    "difficulty": "Hard",
    "description": (
        "Given an array representing the heights of histogram bars, "
        "find the largest rectangular area that can be formed."
    ),
    "example": """Input: heights = [2,1,5,6,2,3]
Output: 10""",
    "starter_code": """#include <iostream>
#include <vector>
#include <stack>
using namespace std;

int largestRectangleArea(vector<int>& heights) {
    // Write your code here
}

int main() {
    int n;
    cin >> n;

    vector<int> heights(n);
    for (int i = 0; i < n; i++)
        cin >> heights[i];

    cout << largestRectangleArea(heights);
    return 0;
}"""},
34: {
    "title": "Maximum Depth of Binary Tree",
    "difficulty": "Easy",
    "description": (
        "Given the root of a binary tree, find its maximum depth. "
        "The maximum depth is the number of nodes along the longest path "
        "from the root node down to the farthest leaf node."
    ),
    "example": """Input:
    3
   / \\
  9  20
     / \\
    15  7

Output: 3""",
    "starter_code": """#include <iostream>
    #include <vector>
    #include <algorithm>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;

    TreeNode(int x) {
        val = x;
        left = NULL;
        right = NULL;
    }
};

int maxDepth(TreeNode* root) {
    // Write your code here
}

int main() {
    int n;
    cin >> n;

    if (n == 0) {
        cout << 0;
        return 0;
    }

    vector<int> values(n);
    for (int i = 0; i < n; i++) {
        cin >> values[i];
    }

    if (values[0] == -1) {
        cout << 0;
        return 0;
    }

    vector<TreeNode*> nodes(n, nullptr);

    for (int i = 0; i < n; i++) {
        if (values[i] != -1)
            nodes[i] = new TreeNode(values[i]);
    }

    for (int i = 0; i < n; i++) {
        if (nodes[i] == nullptr) continue;

        int left = 2 * i + 1;
        int right = 2 * i + 2;

        if (left < n) nodes[i]->left = nodes[left];
        if (right < n) nodes[i]->right = nodes[right];
    }

    cout << maxDepth(nodes[0]);
    return 0;
}"""
},

35: {
    "title": "Number of Islands",
    "difficulty": "Easy",
    "description": (
        "Given a 2D grid containing '1' representing land and '0' "
        "representing water, count the number of islands. An island is "
        "formed by connected land cells horizontally or vertically."
    ),
    "example": """Input:
11000
11000
00100
00011

Output: 3""",
    "starter_code": """#include <iostream>
#include <vector>
using namespace std;

void dfs(
    vector<vector<char>>& grid,
    int r,
    int c
) {
    // Write your code here
}

int numIslands(vector<vector<char>>& grid) {
    // Write your code here
}

int main() {
    int rows, cols;
    cin >> rows >> cols;

    vector<vector<char>> grid(rows, vector<char>(cols));

    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            cin >> grid[i][j];
        }
    }

    cout << numIslands(grid);
    return 0;
}"""
},

36: {
    "title": "Binary Tree Level Order Traversal",
    "difficulty": "Medium",
    "description": (
        "Given the root of a binary tree, return the values of its nodes "
        "level by level from left to right."
    ),
    "example": """Input:
    3
   / \\
  9  20
     / \\
    15  7

Output:
3 9 20 15 7""",
    "starter_code": """#include <iostream>
#include <vector>
#include <queue>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;

    TreeNode(int x) {
        val = x;
        left = NULL;
        right = NULL;
    }
};

vector<int> levelOrder(TreeNode* root) {
    // Write your code here
}

int main() {
    int n;
    cin >> n;

    if (n == 0) return 0;

    vector<int> values(n);
    for (int i = 0; i < n; i++) {
        cin >> values[i];
    }

    if (values[0] == -1) return 0;

    vector<TreeNode*> nodes(n, nullptr);

    for (int i = 0; i < n; i++) {
        if (values[i] != -1)
            nodes[i] = new TreeNode(values[i]);
    }

    for (int i = 0; i < n; i++) {
        if (nodes[i] == nullptr) continue;

        int left = 2 * i + 1;
        int right = 2 * i + 2;

        if (left < n) nodes[i]->left = nodes[left];
        if (right < n) nodes[i]->right = nodes[right];
    }

    vector<int> ans = levelOrder(nodes[0]);

    for (int x : ans) {
        cout << x << " ";
    }

    return 0;
}"""
},

37: {
    "title": "Lowest Common Ancestor of a Binary Tree",
    "difficulty": "Hard",
    "description": (
        "Given the root of a binary tree and two nodes p and q, find their "
        "lowest common ancestor. The lowest common ancestor is the deepest "
        "node that has both p and q as descendants."
    ),
    "example": """Input:
        3
       / \\
      5   1
     / \\
    6   2

p = 6, q = 2

Output: 5""",
    "starter_code": """#include <iostream>
    #include <vector>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;

    TreeNode(int x) {
        val = x;
        left = NULL;
        right = NULL;
    }
};

TreeNode* lowestCommonAncestor(
    TreeNode* root,
    TreeNode* p,
    TreeNode* q
) {
    // Write your code here
}

int main() {
    int n;
    cin >> n;

    vector<int> values(n);
    for (int i = 0; i < n; i++) {
        cin >> values[i];
    }

    if (n == 0 || values[0] == -1) {
        cout << -1;
        return 0;
    }

    vector<TreeNode*> nodes(n, nullptr);

    for (int i = 0; i < n; i++) {
        if (values[i] != -1)
            nodes[i] = new TreeNode(values[i]);
    }

    for (int i = 0; i < n; i++) {
        if (nodes[i] == nullptr) continue;

        int left = 2 * i + 1;
        int right = 2 * i + 2;

        if (left < n) nodes[i]->left = nodes[left];
        if (right < n) nodes[i]->right = nodes[right];
    }

    int pValue, qValue;
    cin >> pValue >> qValue;

    TreeNode* p = findNode(nodes[0], pValue);
    TreeNode* q = findNode(nodes[0], qValue);

    if (p == nullptr || q == nullptr) {
        cout << -1;
        return 0;
    }

    TreeNode* ans = lowestCommonAncestor(nodes[0], p, q);

    cout << (ans != nullptr ? ans->val : -1);

    return 0;
}"""
},

38: {
    "title": "Course Schedule",
    "difficulty": "Hard",
    "description": (
        "There are numCourses courses and prerequisite relationships. "
        "Determine whether it is possible to finish all courses. A cycle "
        "in the prerequisite graph makes it impossible to complete all courses."
    ),
    "example": """Input:
numCourses = 2
prerequisites = [[1,0]]

Output: true

Input:
numCourses = 2
prerequisites = [[1,0],[0,1]]

Output: false""",
    "starter_code": """#include <iostream>
#include <vector>
using namespace std;

bool canFinish(
    int numCourses,
    vector<vector<int>>& prerequisites
) {
    // Write your code here
}
int main() {
    int numCourses, m;
    cin >> numCourses >> m;

    vector<vector<int>> prerequisites(m, vector<int>(2));

    for (int i = 0; i < m; i++) {
        cin >> prerequisites[i][0] >> prerequisites[i][1];
    }

    cout << (canFinish(numCourses, prerequisites) ? "true" : "false");

    return 0;
}"""},
39: {
    "title": "Minimum Distance Between Tree Nodes",
    "difficulty": "Hard",
    "description": (
        "Given a binary tree and two node values, find the minimum number "
        "of edges between the two nodes. You may convert the tree into an "
        "undirected graph using the parent-child relationships and then "
        "use graph traversal to find the shortest path."
    ),
    "example": """Input:
        1
       / \\
      2   3
     / \\   \\
    4   5   6

Nodes: 4 and 6

Output: 4

Explanation:
The shortest path is:
4 -> 2 -> 1 -> 3 -> 6
which contains 4 edges.""",
    "starter_code": """#include <iostream>
#include <vector>
#include <unordered_map>
#include <queue>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;

    TreeNode(int x) {
        val = x;
        left = nullptr;
        right = nullptr;
    }
};

void buildGraph(
    TreeNode* root,
    TreeNode* parent,
    unordered_map<int, vector<int>>& graph
) {
    // Write your code here
}

int minDistance(TreeNode* root, int start, int target){
    // Write your code here
}
TreeNode* findNode(TreeNode* root, int value) {
    if (root == nullptr) return nullptr;

    if (root->val == value) return root;

    TreeNode* left = findNode(root->left, value);
    if (left != nullptr) return left;

    return findNode(root->right, value);
}
int main() {
    int n;
    cin >> n;

    if (n <= 0) {
        cout << -1;
        return 0;
    }

    vector<int> values(n);
    for (int i = 0; i < n; i++) {
        cin >> values[i];
    }

    if (values[0] == -1) {
        cout << -1;
        return 0;
    }

    vector<TreeNode*> nodes(n, nullptr);

    for (int i = 0; i < n; i++) {
        if (values[i] != -1)
            nodes[i] = new TreeNode(values[i]);
    }

    for (int i = 0; i < n; i++) {
        if (nodes[i] == nullptr)
            continue;

        int left = 2 * i + 1;
        int right = 2 * i + 2;

        if (left < n)
            nodes[i]->left = nodes[left];

        if (right < n)
            nodes[i]->right = nodes[right];
    }

    int start, target;
    cin >> start >> target;

    cout << minDistance(nodes[0], start, target);

    return 0;
}"""
}
}
def get_db_connection():
    return mysql.connector.connect(
        host=st.secrets.get("DB_HOST", "localhost"),
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        database=st.secrets["DB_NAME"]
    )
def get_solved_questions(username):
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT DISTINCT s.question_id
            FROM submissions s
            INNER JOIN users u ON s.user_id = u.id
            WHERE u.username = %s
            AND s.status = 'ACCEPTED'
        """

        cursor.execute(query, (username,))

        solved_ids = {int(row[0]) for row in cursor.fetchall()}

        return solved_ids

    except mysql.connector.Error as e:
        st.error(f"Could not load solved questions: {e}")
        return set()

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
def fetch_submission_history(username):

    history_path = os.path.join(BACKEND_PATH, "history.exe")

    env = os.environ.copy()

    env["DB_HOST"] = st.secrets["DB_HOST"]
    env["DB_USER"] = st.secrets["DB_USER"]
    env["DB_PASSWORD"] = st.secrets["DB_PASSWORD"]
    env["DB_NAME"] = st.secrets["DB_NAME"]

    try:
        result = subprocess.run(
            [history_path, username],
            capture_output=True,
            text=True,
            cwd=BACKEND_PATH,
            timeout=15,
            env=env
        )

        if result.returncode != 0:
            st.error(f"History error: {result.stderr}")
            return []

        import json
        data = json.loads(result.stdout)

        return data["history"]

    except Exception as e:
        return []
bug_questions = [
    {
        "question": "Why does the value of x remain unchanged?",
        "code": """void update(int x) {
    x = 50;
}
int main() {
    int x = 10;
    update(x);
    cout << x;
}""",
        "options": ["Function is not called", "Argument is passed by value", "Incorrect return type", "Variable is not initialized"],
        "answer": "Argument is passed by value"
    },
    {
        "question": "What is the logical error in this recursive function?",
        "code": """int sum(int n) {
    if(n == 0)
        return 0;
    return n + sum(n);
}""",
        "options": ["Wrong return type", "Recursive call does not reduce n", "Missing function parameter", "Incorrect base condition"],
        "answer": "Recursive call does not reduce n"
    },
    {
        "question": "Identify the error in this class.",
        "code": """class Student {
    int marks;
};
int main() {
    Student s;
    s.marks = 90;
}""",
        "options": ["Missing constructor", "Object cannot be created", "marks is private by default", "Class cannot contain integers"],
        "answer": "marks is private by default"
    },
    {
        "question": "What causes the compilation error?",
        "code": """class Student {
public:
    Student(int m) {
        cout << m;
    }
};
int main() {
    Student s;
}""",
        "options": ["Constructor cannot take parameters", "No default constructor is available", "Object name is invalid", "Constructor has no return type"],
        "answer": "No default constructor is available"
    },
    {
        "question": "What is the problem with this inheritance code?",
        "code": """class Parent {
private:
    int x = 10;
};
class Child : public Parent {
public:
    void display() {
        cout << x;
    }
};""",
        "options": ["Derived class cannot contain functions", "Private member cannot be accessed directly in derived class", "Inheritance syntax is incorrect", "Parent class cannot have variables"],
        "answer": "Private member cannot be accessed directly in derived class"
    },
    {
        "question": "Identify the memory management bug.",
        "code": """int main() {
    int *p = new int(20);
    cout << *p;
    p = new int(30);
    delete p;
}""",
        "options": ["Incorrect dereferencing", "Memory leak", "Invalid pointer declaration", "Dangling pointer"],
        "answer": "Memory leak"
    },
    {
        "question": "What is missing when inserting a node at the beginning?",
        "code": """struct Node {
    int data;
    Node* next;
};
void insert(Node*& head, int value) {
    Node* newNode = new Node;
    newNode->data = value;
    head = newNode;
}""",
        "options": ["Linking the new node to the previous head", "Function parameter", "Memory allocation", "Data assignment"],
        "answer": "Linking the new node to the previous head"
    },
    {
        "question": "Why can this linked list traversal crash?",
        "code": """while(head->next != NULL) {
    cout << head->data;
    head = head->next;
}""",
        "options": ["Linked lists cannot use while loops", "head may be NULL before accessing head->next", "The loop uses the wrong operator", "Data cannot be printed in a loop"],
        "answer": "head may be NULL before accessing head->next"
    },
    {
        "question": "What is the stack operation error?",
        "code": """int stack[5];
int top = -1;
void pop() {
    cout << stack[top];
    top--;
}""",
        "options": ["Incorrect decrement", "Stack underflow is not checked", "Wrong array declaration", "Stack overflow"],
        "answer": "Stack underflow is not checked"
    },
    {
        "question": "What is wrong with this queue insertion?",
        "code": """int queue[5];
int rear = -1;
void enqueue(int x) {
    rear++;
    queue[rear] = x;
}""",
        "options": ["Invalid array declaration", "Queue overflow is not checked", "Queue underflow", "Wrong increment operator"],
        "answer": "Queue overflow is not checked"
    },
    {
        "question": "Why might this binary search fail to find an existing element?",
        "code": """int binarySearch(int arr[], int n, int key) {
    int low = 0, high = n;
    while(low <= high) {
        int mid = (low + high) / 2;
        if(arr[mid] == key)
            return mid;
        else if(arr[mid] < key)
            low = mid + 1;
        else
            high = mid - 1;
    }
    return -1;
}""",
        "options": ["Return type should be void", "Initial high value is incorrect", "Mid calculation is invalid", "Array must be sorted"],
        "answer": "Initial high value is incorrect"
    },
    {
        "question": "Why does this bubble sort not sort the array correctly?",
        "code": """for(int i = 0; i < n; i++) {
    for(int j = 0; j < n - 1; j++) {
        if(arr[j] < arr[j + 1]) {
            swap(arr[j], arr[j + 1]);
        }
    }
}""",
        "options": ["Swap cannot be used in sorting", "Wrong comparison for ascending order", "Missing array declaration", "Wrong loop variable"],
        "answer": "Wrong comparison for ascending order"
    },
    {
        "question": "What is the bug in this BST insertion function?",
        "code": """Node* insert(Node* root, int value) {
    if(root == NULL)
        return new Node(value);
    if(value < root->data)
        insert(root->left, value);
    else
        insert(root->right, value);
    return root;
}""",
        "options": ["Missing base condition", "Recursive results are not assigned", "Incorrect comparison", "Wrong return type"],
        "answer": "Recursive results are not assigned"
    },
    {
        "question": "What is the problem with this vector code?",
        "code": """vector<int> v;
v[0] = 10;
v.push_back(20);
cout << v[0];""",
        "options": ["Vector needs a fixed size", "Accessing an element before it exists", "push_back is invalid", "Vector cannot store integers"],
        "answer": "Accessing an element before it exists"
    },
    {
        "question": "Why does this code not correctly compare two strings?",
        "code": """string a = "hello";
string b = "hello";
if(a == b)
    cout << "Same";""",
        "options": ["Missing string header", "Wrong comparison operator", "No error in this code", "Strings cannot be compared"],
        "answer": "No error in this code"
    },
    {
        "question": "What is the indexing error?",
        "code": """int matrix[2][3];
for(int i = 0; i < 3; i++) {
    for(int j = 0; j < 2; j++) {
        cin >> matrix[i][j];
    }
}""",
        "options": ["Rows and columns are interchanged", "Matrix cannot use nested loops", "Missing return statement", "Wrong data type"],
        "answer": "Rows and columns are interchanged"
    },
    {
        "question": "What is missing in this operator overloading code?",
        "code": """class Number {
public:
    int value;
    Number operator+(Number obj) {
        Number temp;
        temp.value = value + obj.value;
    }
};""",
        "options": ["Parameter must be an integer", "Missing return statement", "Class cannot contain operators", "Operator name is invalid"],
        "answer": "Missing return statement"
    },
    {
        "question": "Why might this file reading operation fail?",
        "code": """ifstream fin("data.txt");
int x;
fin >> x;
cout << x;""",
        "options": ["File must have a .cpp extension", "Wrong extraction operator", "File opening success is not checked", "ifstream cannot read integers"],
        "answer": "File opening success is not checked"
    },
    {
        "question": "What is wrong with this linear search?",
        "code": """int search(int arr[], int n, int key) {
    for(int i = 0; i < n; i++) {
        if(arr[i] == key)
            return -1;
    }
    return -1;
}""",
        "options": ["Found element returns the wrong value", "Missing initialization", "Wrong loop condition", "Array cannot be searched"],
        "answer": "Found element returns the wrong value"
    },
    {
        "question": "What is the logical mistake in this code?",
        "code": """int n = 6;
if(n & 1 == 0) {
    cout << "Even";
}
else {
    cout << "Odd";
}""",
        "options": ["Missing else-if", "Bitwise AND has incorrect precedence here", "n must be a float", "Bitwise AND cannot be used with integers"],
        "answer": "Bitwise AND has incorrect precedence here"
    },
    {
        "question": "Why does this code produce a compilation error?",
        "code": """class Test {
    int x = 10;
public:
    friend void display();
};
void display() {
    cout << x;
}""",
        "options": ["Friend functions cannot access private members", "Class cannot contain private variables", "x is not accessible without an object", "Friend function must return int"],
        "answer": "x is not accessible without an object"
    },
    {
        "question": "What is the problem with this code?",
        "code": """class Counter {
public:
    static int count;
};
int main() {
    Counter::count = 10;
    cout << Counter::count;
}""",
        "options": ["Missing constructor", "Static member is declared but not defined", "Static variables cannot be accessed using class name", "Static variables cannot store integers"],
        "answer": "Static member is declared but not defined"
    },
    {
        "question": "Why does this code call the base class function?",
        "code": """class Base {
public:
    void show() {
        cout << "Base";
    }
};
class Derived : public Base {
public:
    void show() {
        cout << "Derived";
    }
};
int main() {
    Base* p = new Derived();
    p->show();
}""",
        "options": ["Derived class cannot redefine functions", "Base function is not virtual", "Pointer cannot point to Derived", "Inheritance is incorrect"],
        "answer": "Base function is not virtual"
    },
    {
        "question": "What is the memory management problem?",
        "code": """class Test {
public:
    int* p;
    Test() {
        p = new int[10];
    }
};
int main() {
    Test t;
}""",
        "options": ["Pointer must be static", "Dynamically allocated memory is never released", "Array allocation is invalid", "Constructor cannot allocate memory"],
        "answer": "Dynamically allocated memory is never released"
    },
    {
        "question": "What is the issue with this copy constructor?",
        "code": """class Test {
public:
    int* p;
    Test(int x) {
        p = new int(x);
    }
    Test(const Test& obj) {
        p = obj.p;
    }
};""",
        "options": ["Constructor must return a value", "Shallow copying causes shared ownership", "Pointer cannot be copied", "Copy constructor cannot accept references"],
        "answer": "Shallow copying causes shared ownership"
    },
    {
        "question": "Why is the exception not caught correctly?",
        "code": """try {
    throw 10;
}
catch(float x) {
    cout << "Caught";
}""",
        "options": ["Missing finally block", "Try block cannot throw integers", "Catch type does not match thrown type", "Integer exceptions cannot be thrown"],
        "answer": "Catch type does not match thrown type"
    },
    {
        "question": "What causes undefined behavior in this code?",
        "code": """vector<int> v = {10, 20, 30};
for(auto it = v.begin(); it != v.end(); it++) {
    if(*it == 20)
        v.erase(it);
}""",
        "options": ["Iterator becomes invalid after erase", "begin() returns an integer", "Vectors cannot use iterators", "erase cannot remove integers"],
        "answer": "Iterator becomes invalid after erase"
    },
    {
        "question": "What is wrong with this code?",
        "code": """map<int, string> students;
students[1] = "Aman";
students[2] = "Ravi";
cout << students[3].length();""",
        "options": ["Map cannot store strings", "length() cannot be used", "Accessing key 3 inserts an empty string", "Map keys must be strings"],
        "answer": "Accessing key 3 inserts an empty string"
    },
    {
        "question": "Which operation is invalid in this code?",
        "code": """deque<int> dq;
dq.pop_front();
dq.push_back(10);""",
        "options": ["Storing integer values", "pop_front on an empty deque", "Creating a deque", "push_back"],
        "answer": "pop_front on an empty deque"
    },
    {
        "question": "Why does this code print the largest element first?",
        "code": """priority_queue<int> pq;
pq.push(10);
pq.push(30);
pq.push(20);
cout << pq.top();""",
        "options": ["top() returns the smallest value", "Default priority_queue is a max heap", "push() reverses elements", "Priority queues always sort in ascending order"],
        "answer": "Default priority_queue is a max heap"
    },
    {
        "question": "What is missing in this BFS implementation?",
        "code": """void BFS(int start) {
    queue<int> q;
    q.push(start);
    while(!q.empty()) {
        int node = q.front();
        q.pop();
        cout << node << " ";
        for(int next : adj[node]) {
            q.push(next);
        }
    }
}""",
        "options": ["Visited array to avoid repeated traversal", "A recursive function", "A stack", "A sorting function"],
        "answer": "Visited array to avoid repeated traversal"
    },
    {
        "question": "Why can this DFS function get stuck in recursion?",
        "code": """void DFS(int node) {
    cout << node << " ";
    for(int next : adj[node]) {
        DFS(next);
    }
}""",
        "options": ["Missing return type", "Adjacency lists cannot store integers", "Missing visited tracking", "DFS cannot use recursion"],
        "answer": "Missing visited tracking"
    },
    {
        "question": "What is wrong with this merge sort splitting logic?",
        "code": """void mergeSort(int arr[], int low, int high) {
    if(low >= high)
        return;
    int mid = (low + high) / 2;
    mergeSort(arr, low, mid);
    mergeSort(arr, mid, high);
}""",
        "options": ["Mid should always be zero", "Second recursive call should start at mid + 1", "Merge sort cannot use recursion", "Wrong base condition"],
        "answer": "Second recursive call should start at mid + 1"
    },
    {
        "question": "What is the bug in this partition function?",
        "code": """int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    for(int j = low; j < high; j++) {
        if(arr[j] <= pivot) {
            i++;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i], arr[high]);
    return i;
}""",
        "options": ["Incorrect final pivot index", "Missing comparison", "Wrong loop condition", "Wrong pivot selection"],
        "answer": "Incorrect final pivot index"
    },
    {
        "question": "What is wrong with this circular queue insertion?",
        "code": """rear = (rear + 1) % size;
queue[rear] = value;""",
        "options": ["Circular queues cannot use arrays", "Queue-full condition is not checked", "Rear cannot be updated", "Modulo operator is invalid"],
        "answer": "Queue-full condition is not checked"
    },
    {
        "question": "What is missing when inserting a node after a given node?",
        "code": """newNode->next = current->next;
current->next = newNode;""",
        "options": ["Deleting current", "Updating the previous pointer of the next node", "Changing the data type", "Allocating an array"],
        "answer": "Updating the previous pointer of the next node"
    },
    {
        "question": "What is the mistake in this matrix multiplication code?",
        "code": """int A[2][3], B[2][3], C[2][3];
for(int i = 0; i < 2; i++) {
    for(int j = 0; j < 3; j++) {
        C[i][j] = 0;
        for(int k = 0; k < 3; k++) {
            C[i][j] += A[i][k] * B[k][j];
        }
    }
}""",
        "options": ["The inner loop should run twice", "Matrices have incompatible dimensions", "Multiplication cannot use three loops", "The output matrix must have 2 rows and 3 columns"],
        "answer": "Matrices have incompatible dimensions"
    },
    {
        "question": "Why is this function overloading invalid?",
        "code": """int calculate(int a, int b) {
    return a + b;
}
float calculate(int a, int b) {
    return a + b;
}""",
        "options": ["Functions cannot differ only by return type", "Float cannot be returned", "Integer parameters are invalid", "Functions cannot have the same name"],
        "answer": "Functions cannot differ only by return type"
    },
    {
        "question": "What causes the compilation error?",
        "code": """void display(const int x) {
    x = 50;
}""",
        "options": ["Missing return statement", "A const variable cannot be modified", "Function cannot accept integers", "Functions cannot assign values"],
        "answer": "A const variable cannot be modified"
    },
    {
        "question": "What is the problem with this postfix evaluation code?",
        "code": """stack<int> st;
st.push(10);
st.push(20);
int a = st.top();
st.pop();
int b = st.top();
st.pop();
st.push(a - b);
cout << st.top();""",
        "options": ["Subtraction cannot be performed using a stack", "Operands are subtracted in the wrong order", "pop() must come before top()", "Stack cannot store integers"],
        "answer": "Operands are subtracted in the wrong order"
    },
    {
        "question": "What is the bug in this code?",
        "code": """int x = 10;
if(x == 10);
{
    cout << "Correct";
}""",
        "options": ["Wrong comparison operator", "Extra semicolon after if", "Wrong variable declaration", "Missing return statement"],
        "answer": "Extra semicolon after if"
    },
    {
        "question": "Identify the error.",
        "code": """int arr[5] = {1, 2, 3, 4, 5};
cout << arr[5];""",
        "options": ["Missing loop", "Array index out of bounds", "Invalid cout statement", "Array is not initialized"],
        "answer": "Array index out of bounds"
    },
    {
        "question": "What is wrong with this loop?",
        "code": """for(int i = 0; i < 5; i--) {
    cout << i;
}""",
        "options": ["Missing semicolon", "Wrong increment direction", "Wrong initialization", "Wrong condition"],
        "answer": "Wrong increment direction"
    },
    {
        "question": "Find the logical error.",
        "code": """int a = 5, b = 10;
if(a > b) {
    cout << "A is smaller";
}""",
        "options": ["Wrong output statement", "Missing braces", "Incorrect condition", "Wrong variable declaration"],
        "answer": "Incorrect condition"
    },
    {
        "question": "What is the bug?",
        "code": """int n = 5;
while(n > 0) {
    cout << n << " ";
    n++;
}""",
        "options": ["Wrong data type", "Infinite loop", "Invalid condition", "Missing initialization"],
        "answer": "Infinite loop"
    },
    {
        "question": "Identify the pointer error.",
        "code": """int *p;
*p = 20;
cout << *p;""",
        "options": ["Missing return", "Pointer is not initialized", "Invalid output statement", "Wrong pointer syntax"],
        "answer": "Pointer is not initialized"
    },
    {
        "question": "What is wrong with this function?",
        "code": """int add(int a, int b) {
    int sum = a + b;
}""",
        "options": ["Missing function call", "Missing return statement", "Wrong parameters", "Wrong variable name"],
        "answer": "Missing return statement"
    },
    {
        "question": "Find the error.",
        "code": """int x = 10;
if(x = 0) {
    cout << "Zero";
}""",
        "options": ["Missing braces", "Assignment instead of comparison", "Invalid condition syntax", "Wrong variable type"],
        "answer": "Assignment instead of comparison"
    },
    {
        "question": "What is the bug in this array code?",
        "code": """int arr[4] = {1, 2, 3, 4};
for(int i = 0; i <= 4; i++) {
    cout << arr[i];
}""",
        "options": ["Missing initialization", "Loop runs one extra time", "Wrong array size", "Wrong data type"],
        "answer": "Loop runs one extra time"
    },
    {
        "question": "Identify the error.",
        "code": """int a = 10;
int b = 0;
cout << a / b;""",
        "options": ["Wrong operator", "Division by zero", "Integer overflow", "Invalid declaration"],
        "answer": "Division by zero"
    },
    {
        "question": "What is the problem with this code?",
        "code": """int x = 5;
if(x > 2 && x < 4) {
    cout << "Valid";
}""",
        "options": ["Wrong variable declaration", "Condition can never be true", "Invalid logical operator", "Missing else block"],
        "answer": "Condition can never be true"
    },
    {
        "question": "Find the bug in this code.",
        "code": """int i;
for(i = 1; i <= 5; i++);
{
    cout << i;
}""",
        "options": ["Wrong loop condition", "Extra semicolon after for loop", "Missing increment", "Uninitialized variable"],
        "answer": "Extra semicolon after for loop"
    },
    {
        "question": "What is wrong with this code?",
        "code": """int x = 10;
if(x > 5) {
    int y = 20;
}
cout << y;""",
        "options": ["Variable y is out of scope", "Missing return", "Invalid integer declaration", "Wrong condition"],
        "answer": "Variable y is out of scope"
    },
    {
        "question": "Identify the error in this code.",
        "code": """int arr[3] = {10, 20, 30};
cout << arr[0 + 3];""",
        "options": ["Wrong output operator", "Array index out of bounds", "Invalid addition", "Missing array declaration"],
        "answer": "Array index out of bounds"
    },
    {
        "question": "What is the bug?",
        "code": """int n = 10;
if(n > 5) {
    cout << "Greater";
}
else if(n > 8) {
    cout << "Very Greater";
}""",
        "options": ["Wrong data type", "Unreachable else-if condition", "Missing else statement", "Invalid comparison"],
        "answer": "Unreachable else-if condition"
    }
]
def show_bug_hunt():

    defaults = {
        "bug_score": 0,
        "bug_question": None,
        "bug_answered": False,
        "bug_selected": None,
        "bug_attempts": 0,
        "bug_correct": 0
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    st.markdown("""
        <style>
        .bug-header {
            background: linear-gradient(120deg, #202020, #303030);
            padding: 22px;
            border-radius: 14px;
            border: 1px solid #383838;
            margin-bottom: 22px;
        }

        .bug-label {
            color: #00e676;
            font-size: 12px;
            font-weight: bold;
            letter-spacing: 1px;
        }

        .bug-title {
            color: white;
            font-size: 30px;
            font-weight: bold;
        }

        .score-panel {
            background: #202020;
            padding: 20px;
            border-radius: 14px;
            border: 1px solid #383838;
            text-align: center;
            margin-bottom: 15px;
        }

        .score-number {
            font-size: 34px;
            color: #00e676;
            font-weight: bold;
        }

        .score-label {
            color: #aaaaaa;
            font-size: 13px;
        }
        </style>
    """, unsafe_allow_html=True)

    question_col, score_col = st.columns([3.2, 1])

    with question_col:

        if st.session_state.bug_question is None:

            st.markdown("### Ready for a challenge?")
            st.write("Generate a random C++ debugging question to begin.")

            if st.button("Generate Random Question",
                         use_container_width=True,
                         type="primary"):

                st.session_state.bug_question = random.choice(bug_questions)
                st.session_state.bug_answered = False
                st.session_state.bug_selected = None
                st.rerun()

        else:

            q = st.session_state.bug_question

            st.markdown("### Identify the Error")
            st.caption("Inspect the following code and find the bug.")

            st.code(q["code"], language="cpp")

            selected = st.radio(
                "Choose the correct answer:",
                q["options"],
                key="bug_mcq_options",
                disabled=st.session_state.bug_answered
            )

            if not st.session_state.bug_answered:

                if st.button("Submit Answer",
                             use_container_width=True,
                             type="primary"):

                    st.session_state.bug_selected = selected
                    st.session_state.bug_answered = True
                    st.session_state.bug_attempts += 1

                    if selected == q["answer"]:
                        st.session_state.bug_score += 10
                        st.session_state.bug_correct += 1

                    st.rerun()

            else:

                if st.session_state.bug_selected == q["answer"]:
                    st.success("Correct! +10 points")
                else:
                    st.error("Incorrect answer!")
                previous_question = st.session_state.bug_question

                available_questions = [
    q for q in bug_questions
    if q != previous_question
                ]

                st.session_state.bug_question = random.choice(
                available_questions or bug_questions
                )

                st.session_state.bug_answered = False
                st.session_state.bug_selected = None
                st.rerun()

    with score_col:

        st.markdown("### Your Stats")

        st.markdown(f"""
            <div class="score-panel">
                <div class="score-label">TOTAL SCORE</div>
                <div class="score-number">
                    {st.session_state.bug_score}
                </div>
                <div class="score-label">POINTS</div>
            </div>
        """, unsafe_allow_html=True)

        st.metric("Attempted",
                  st.session_state.bug_attempts)

        st.metric("Correct",
                  st.session_state.bug_correct)
        accuracy = (
            st.session_state.bug_correct /
            st.session_state.bug_attempts * 100
            if st.session_state.bug_attempts > 0 else 0
        )
        st.metric("Accuracy", f"{accuracy:.1f}%")
        if st.session_state.bug_attempts > 0:
            st.progress(accuracy / 100)
def fetch_progress_data(username):

    if not PROGRESS_PATH.exists():
        return None, "Progress executable not found. Compile progress.cpp first."

    input_data = f"{len(questions)}\n"

    # Send question details to C++
    for qid, question in questions.items():

        topics = question_topics.get(qid, [])

        input_data += f"{qid}\n"
        input_data += f"{question['title']}\n"

        # Send topic count
        input_data += f"{len(topics)}\n"

        # Send each topic separately
        for topic in topics:
            input_data += f"{topic}\n"

        input_data += f"{question['difficulty']}\n"

    # Database environment variables
    env = os.environ.copy()

    env["DB_HOST"] = st.secrets["DB_HOST"]
    env["DB_USER"] = st.secrets["DB_USER"]
    env["DB_PASSWORD"] = st.secrets["DB_PASSWORD"]
    env["DB_NAME"] = st.secrets["DB_NAME"]

    try:

        result = subprocess.run(
            [str(PROGRESS_PATH), username],
            input=input_data,
            text=True,
            capture_output=True,
            cwd=str(BACKEND_PATH),
            timeout=15,
            env=env
        )

        if result.returncode != 0:
            return None, result.stderr or "Progress calculation failed."

        output = result.stdout.strip()

        if not output:
            return None, "C++ returned an empty response."

        try:
            progress_data = json.loads(output)
        except json.JSONDecodeError:
            return None, f"Invalid JSON returned by C++:\n{output}"

        return progress_data, None

    except subprocess.TimeoutExpired:
        return None, "Progress calculation timed out."

    except Exception as e:
        return None, str(e)
def search_questions(query, questions):
    query = query.lower().strip()
    results = []

    for question_no, question in questions.items():
        title = question.get("title", "").lower()
        description = question.get("description", "").lower()
        difficulty = question.get("difficulty", "").lower()

        if (
            query in title
            or query in description
            or query in difficulty
        ):
            results.append((question_no, question))

    return results

def show_progress_page():

    col1, col2, col3 = st.columns([1, 12, 1])

    with col2:

        st.title("My Progress")
        st.caption("Track your coding performance and improve your skills.")

        username = st.session_state.get("username")

        if not username:
            st.warning("Please log in to view your progress.")
            return

        with st.spinner("Calculating your progress..."):
            data, error = fetch_progress_data(username)

        if error:
            st.error(error)
            return

        # Overall Performance
        st.subheader("Overall Performance")

        solved = data["solved_questions"]
        total = data["total_questions"]
        completion = float(data["overall_percentage"])
        accuracy = float(data["accuracy"])

        st.metric(
            "Overall Completion",
            f"{completion:.1f}%",
            f"{solved} out of {total} problems solved"
        )

        st.progress(min(max(completion / 100, 0), 1))

        c1, c2 = st.columns(2)

        with c1:
            st.metric("Problems Solved", f"{solved}/{total}")

        with c2:
            st.metric("Accuracy", f"{accuracy:.1f}%")

        c3, c4 = st.columns(2)

        with c3:
            st.metric(
                "Total Submissions",
                data["total_submissions"]
            )

        with c4:
            st.metric(
                "Accepted Submissions",
                data["accepted_submissions"]
            )

        st.divider()

        # Difficulty-wise Progress
        st.subheader("Difficulty-wise Progress")

        difficulty_data = data["difficulty"]

        easy, medium, hard = st.columns(3)

        for column, level in [
            (easy, "Easy"),
            (medium, "Medium"),
            (hard, "Hard")
        ]:

            solved_count, total_count = difficulty_data[level]

            percentage = (
                solved_count / total_count
                if total_count > 0 else 0
            )

            with column:
                st.write(f"**{level}**")
                st.metric(
                    "Solved",
                    f"{solved_count}/{total_count}"
                )
                st.progress(percentage)
                st.caption(f"{percentage * 100:.1f}% completed")

        st.divider()

        # Topic-wise Progress
        st.subheader("Topic-wise Progress")

        topics = data["topics"]

        if topics:

            for topic in topics:

                name = topic["name"]
                solved_count = topic["solved"]
                total_count = topic["total"]
                percentage = float(topic["percentage"])

                c1, c2 = st.columns([5, 1])

                with c1:
                    st.write(f"**{name}**")

                with c2:
                    st.write(f"{percentage:.1f}%")

                st.progress(
                    min(max(percentage / 100, 0), 1)
                )

                st.caption(
                    f"{solved_count}/{total_count} questions solved"
                )

        else:
            st.info("No topic data available yet.")

        st.divider()

        # Weak Topic Detection
        st.subheader("Weak Topic Detection")

        weakest_topic = data["weakest_topic"]

        if weakest_topic:

            weak_data = next(
                (
                    topic for topic in topics
                    if topic["name"] == weakest_topic
                ),
                None
            )

            if weak_data:

                st.warning(
                    f"Your weakest topic is {weakest_topic}."
                )

                st.write(
                    f"You have solved {weak_data['solved']} "
                    f"out of {weak_data['total']} questions."
                )

                st.caption(
                    "Practice more questions from this topic to improve."
                )

            else:
                st.warning(
                    f"Your weakest topic is {weakest_topic}."
                )

        else:
            st.success("No weak topics detected!")

        st.divider()

        # Recommended Questions
        st.subheader("Recommended Questions")

        st.caption(
            "Questions recommended based on your weaker topics."
        )

        recommendations = data["recommendations"]

        if recommendations:

            for qid in recommendations:

                qid = int(qid)

                if qid not in questions:
                    continue

                question = questions[qid]

                st.write(
                    f"**Q{qid}. {question['title']}**"
                )

                st.caption(
                    f"Difficulty: {question['difficulty']} | "
                    f"Topics: {', '.join(question_topics.get(qid, []))}"
                )

        else:
            st.success(
                "You have solved all available questions!"
            )
if "problem_tab" not in st.session_state:
    st.session_state.problem_tab = "description"
if "submission_output" not in st.session_state:
    st.session_state.submission_output = ""
if "page" not in st.session_state:
    st.session_state.page = "home"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "solved_questions" not in st.session_state:
    st.session_state.solved_questions = set()
active_page = st.session_state.page
if "recovery_email" not in st.session_state:
    st.session_state.recovery_email = ""
if "recovery_username" not in st.session_state:
    st.session_state.recovery_username = ""
st.markdown(f"""
<style>
/* ACTIVE NAVBAR BUTTON */
.st-key-navbar .st-key-{active_page} button {{
    color: #2196F3 !important;
}}

.st-key-navbar .st-key-{active_page} button p {{
    color: #2196F3 !important;
}}
</style>
""", unsafe_allow_html=True)
with st.container(key="navbar"):
    c1,c8,c2,c3,c7,c4,c5,c6=st.columns([1,0.4,0.4,0.4,0.4,0.4,1,0.4])
    with c1:
        st.image("pic.png", width=175)
    with c8:
        st.write(" ")
        if(st.button("🏠︎Home",key='home')):
            st.session_state.page="home"
            st.rerun()    
    with c2:
        st.write("")
        if(st.button("🧩Problems",key='problems')):
            st.session_state.page="problems"
            st.rerun()
    with c3:
        st.write("")
        if(st.button("◴History",key='history')):
            st.session_state.page="history"
            st.rerun()
    with c5:
        st.write("")
        if(st.button("📈Progress",key='progress')):
            st.session_state.page="progress"
            st.rerun()
    with c6:
        st.write("")
        if(st.button("🔒︎Login",key='login')):
            st.session_state.page="login"
            st.rerun()
    with c7:
        st.write("")
        if(st.button("🔍︎Bug Hunt",key='bug_hunt')):
            st.session_state.page="bug_hunt"
            st.rerun()
if st.session_state.page == "home":
    col1, col2, col3, col4 = st.columns([1, 8, 4, 1])
    with col2:
        st.markdown("# CODEPULSE | YOUR CODING SPACE")
        if st.session_state.get("logged_in", False):
            st.write("")
            st.write("")
            username = st.session_state.get("username", "User")
            st.header(f"Welcome back, {username}!")
            st.write("")
            st.subheader("Think smart. Code better. Keep growing.")
            st.write("")
            st.write("Your next coding challenge awaits!")
            c1,c2=st.columns([1,1])
            with c1:
                st.success("✅ Login Successful! Welcome to CodePulse.")
        else:
            st.write("")
            st.write("")
            st.header("Welcome to CodePulse! ")
            st.write("")
            st.subheader("Start your coding journey today.")
            st.write("")
            st.write("Practice, improve, and become a better programmer.")
            c1,c2=st.columns([1,2])
            with c1:
                st.info("🔐 Log in to track your progress.")
                if st.button("Login to Get Started", key="home_login"):
                    st.session_state.page = "login"
                    st.rerun()

    with col3:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.image("img.jpg", width=400)
elif st.session_state.page=='problems':
    st.write(" ")
    st.write(" ")
    col1,col2,col3=st.columns([1,12,1])
    with col2:
        search_query = st.text_input(
    "🔍 Search Problems",
    placeholder="Search by problem name, topic, or difficulty..."
)

        if search_query:
            results = search_questions(search_query, questions)

            if results:
                st.write(f"Found {len(results)} problem(s):")

                for question_no, question in results:
                    st.write(
                f"**{question_no}. {question['title']}** "
                f"— {question['difficulty']}"
            )
            else:
                st.warning("No problems found.")
        st.write("")
        st.write("")
        with st.container(height=500, border=False):  
            with st.container(key="problem1_box"):
                with st.container(key="problem1_title"):
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                        st.write("STATUS")
                    with col2:
                        st.write("TITLE")
                    with col3:
                        st.write("TOPIC")
                    with col4:
                        st.write("DIFFICULTY")
                    with col5:
                        st.write("ㅤACTION")
                with st.container(key="problem1_question"):
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 1 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("1. Two Sum Array")
                    with col3:
                        st.write("Arrays")
                    with col4:
                        st.markdown(
            '<span style="color:#00c853; font-size:16px;">Easy</span>',
            unsafe_allow_html=True
        )

                    with col5:
                        if st.button("Solve", key="problem1", use_container_width=True):
                            st.session_state.question_no = 1
                            st.session_state.submission_output = ""
                            st.session_state.problem_tab = "description"
                            st.session_state.page = "problem"
                            st.rerun()

                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 2 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("2. Reverse a linked list in groups of K")
                    with col3:
                        st.write("Linked List")
                    with col4:
                        st.markdown(
            '<span style="color:#FF0000; font-size:16px;">Hard</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem2", use_container_width=True):
                            st.session_state.question_no = 2
                            st.session_state.submission_output = ""
                            st.session_state.problem_tab = "description"
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)   
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 3 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("3. Valid Parentheses")
                    with col3:
                        st.write("Stack")
                    with col4:
                        st.markdown(
            '<span style="color:#00c853; font-size:16px;">Easy</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem3", use_container_width=True):
                            st.session_state.question_no = 3
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = ""                            
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 4 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("4. Binary Search")
                    with col3:
                        st.write("Binary Search")
                    with col4:
                        st.markdown(
            '<span style="color:#00c853; font-size:16px;">Easy</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem4", use_container_width=True):
                            st.session_state.question_no = 4
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = ""                              
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)
                    
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 5 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("5. Maximum Subarray")
                    with col3:
                        st.write("Arrays")
                    with col4:
                        st.markdown(
            '<span style="color:#00c853; font-size:16px;">Easy</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem5", use_container_width=True):
                            st.session_state.question_no = 5
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = ""                              
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)
                      
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 6 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("6. Merge Two Sorted Lists")
                    with col3:
                        st.write("Linked List")
                    with col4:
                        st.markdown(
            '<span style="color:#00c853; font-size:16px;">Easy</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem6", use_container_width=True):
                            st.session_state.question_no = 6
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = ""                              
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 7 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("7. Number of Islands")
                    with col3:
                        st.write("Graphs")
                    with col4:
                        st.markdown(
            '<span style="color:#ff9800; font-size:16px;">Medium</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem7", use_container_width=True):
                            st.session_state.question_no = 7
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = ""                              
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 8 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("8. Longest Substring Without Repeating Characters")
                    with col3:
                        st.write("Strings")
                    with col4:
                        st.markdown(
            '<span style="color:#ff9800; font-size:16px;">Medium</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem8", use_container_width=True):
                            st.session_state.question_no = 8
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = ""                              
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 9 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("9. Next Greater Element")
                    with col3:
                        st.write("Arrays")
                    with col4:
                        st.markdown(
            '<span style="color:#ff9800; font-size:16px;">Medium</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem9", use_container_width=True):
                            st.session_state.question_no = 9
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = ""                              
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 10 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("10. Binary Tree Level Order Traversal")
                    with col3:
                        st.write("Trees")
                    with col4:
                        st.markdown(
            '<span style="color:#ff9800; font-size:16px;">Medium</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem10", use_container_width=True):
                            st.session_state.question_no = 10
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = ""                              
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 11 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("11. Kth Largest Element")
                    with col3:
                        st.write("Arrays")
                    with col4:
                        st.markdown(
            '<span style="color:#ff9800; font-size:16px;">Medium</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem11", use_container_width=True):
                            st.session_state.question_no = 11
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = ""                              
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 12 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("12. Longest Subarray With Sum K")
                    with col3:
                        st.write("Arrays")
                    with col4:
                        st.markdown(
            '<span style="color:#ff9800; font-size:16px;">Medium</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem12", use_container_width=True):
                            st.session_state.question_no = 12
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = ""                              
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 13 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("13. Detect Cycle in Linked List")
                    with col3:
                        st.write("Linked List")
                    with col4:
                        st.markdown(
            '<span style="color:#ff9800; font-size:16px;">Medium</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem13", use_container_width=True):
                            st.session_state.question_no = 13
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = ""                              
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 14 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("14. Course Schedule")
                    with col3:
                        st.write("Graphs")
                    with col4:
                        st.markdown(
            '<span style="color:#ff9800; font-size:16px;">Medium</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem14", use_container_width=True):
                            st.session_state.question_no = 14
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = ""                              
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 15 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("15. Trapping Rain Water ")
                    with col3:
                        st.write("Stack")
                    with col4:
                        st.markdown(
            '<span style="color:#FF0000; font-size:16px;">Hard</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem15", use_container_width=True):
                            st.session_state.question_no = 15
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = ""                              
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 16 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("16. Fibonacci Number")
                    with col3:
                        st.write("Recursion")
                    with col4:
                        st.markdown(
            '<span style="color:#00c853; font-size:16px;">Easy</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem16", use_container_width=True):
                            st.session_state.question_no = 16
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = ""                              
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)   
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 17 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("17. Sum of Array Using Recursion")
                    with col3:
                        st.write("Arrays & Arrays")
                    with col4:
                        st.markdown(
            '<span style="color:#00c853; font-size:16px;">Easy</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem17", use_container_width=True):
                            st.session_state.question_no = 17
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = ""                              
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)   
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 18 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("18. Reverse a String Using Recursion")
                    with col3:
                        st.write("String & Recursion")
                    with col4:
                        st.markdown(
            '<span style="color:#00c853; font-size:16px;">Easy</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem18", use_container_width=True):
                            st.session_state.question_no = 18
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = ""                              
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)   
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 19 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("19. Check Palindrome Using Recursion ")
                    with col3:
                        st.write("String & Recursion")
                    with col4:
                        st.markdown(
            '<span style="color:#00c853; font-size:16px;">Easy</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem19", use_container_width=True):
                            st.session_state.question_no = 19
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = ""                              
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)   
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 20 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("20. Power of a Number")
                    with col3:
                        st.write("Recursion")
                    with col4:
                        st.markdown(
            '<span style="color:#ff9800; font-size:16px;">Medium</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem20", use_container_width=True):
                            st.session_state.question_no = 20
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = ""                              
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 21 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("21. Factorial Using Recursion")
                    with col3:
                        st.write("Recursion")
                    with col4:
                        st.markdown(
            '<span style="color:#00c853; font-size:16px;">Easy</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem21", use_container_width=True):
                            st.session_state.question_no = 21
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = ""                             
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)     
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 22 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("22. Bubble Sort ")
                    with col3:
                        st.write("Arrays & Sorting")
                    with col4:
                        st.markdown(
            '<span style="color:#00c853; font-size:16px;">Easy</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem22", use_container_width=True):
                            st.session_state.question_no = 22
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = ""                             
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)     
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 23 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("23. Selection Sort ")
                    with col3:
                        st.write("Arrays & Sorting")
                    with col4:
                        st.markdown(
            '<span style="color:#00c853; font-size:16px;">Easy</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem23", use_container_width=True):
                            st.session_state.question_no = 23
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = ""                             
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)     
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 24 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("24. Insertion Sort")
                    with col3:
                        st.write("Arrays & Sorting")
                    with col4:
                        st.markdown(
            '<span style="color:#00c853; font-size:16px;">Easy</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem24", use_container_width=True):
                            st.session_state.question_no = 24
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = ""                             
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)     
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 25 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("25. Merge Sort")
                    with col3:
                        st.write("Arrays & Sorting")
                    with col4:
                        st.markdown(
            '<span style="color:#ff9800; font-size:16px;">Medium</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem25", use_container_width=True):
                            st.session_state.question_no = 25
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = "" 
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)     
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 26 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("26. Quick Sort")
                    with col3:
                        st.write("Arrays & Sorting")
                    with col4:
                        st.markdown(
            '<span style="color:#ff9800; font-size:16px;">Medium</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem26", use_container_width=True):
                            st.session_state.question_no = 26
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = "" 
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)     
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 27 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("27. Reverse a String")
                    with col3:
                        st.write("String")
                    with col4:
                        st.markdown(
            '<span style="color:#00c853; font-size:16px;">Easy</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem27", use_container_width=True):
                            st.session_state.question_no = 27
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = "" 
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)     
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 28 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("28. Valid Anagram")
                    with col3:
                        st.write("String")
                    with col4:
                        st.markdown(
            '<span style="color:#00c853; font-size:16px;">Easy</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem28", use_container_width=True):
                            st.session_state.question_no = 28
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = "" 
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)     
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 29 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("29. Longest Common Prefix")
                    with col3:
                        st.write("Arrays & String")
                    with col4:
                        st.markdown(
            '<span style="color:#00c853; font-size:16px;">Easy</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem29", use_container_width=True):
                            st.session_state.question_no = 29
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = "" 
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)     
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 30 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("30. First Non-Repeating Character ")
                    with col3:
                        st.write("String")
                    with col4:
                        st.markdown(
            '<span style="color:#00c853; font-size:16px;">Easy</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem30", use_container_width=True):
                            st.session_state.question_no = 30
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = "" 
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)     
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 31 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("31. Min Stack")
                    with col3:
                        st.write("Stack")
                    with col4:
                        st.markdown(
            '<span style="color:#ff9800; font-size:16px;">Medium</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem31", use_container_width=True):
                            st.session_state.question_no = 31
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = "" 
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)     
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 32 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("32. Evaluate Reverse Polish Notation")
                    with col3:
                        st.write("Stack")
                    with col4:
                        st.markdown(
            '<span style="color:#ff9800; font-size:16px;">Medium</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem32", use_container_width=True):
                            st.session_state.question_no = 32
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = "" 
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)     
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 33 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("33. Largest Rectangle in Histogram")
                    with col3:
                        st.write("Arrays")
                    with col4:
                        st.markdown(
            '<span style="color:#FF0000; font-size:16px;">Hard</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem33", use_container_width=True):
                            st.session_state.question_no = 33
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = "" 
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)     
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 34 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("34. Maximum Depth of Binary Tree")
                    with col3:
                        st.write("Graph")
                    with col4:
                        st.markdown(
            '<span style="color:#00c853; font-size:16px;">Easy</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem34", use_container_width=True):
                            st.session_state.question_no = 34
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = "" 
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 35 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("35. Number of Islands")
                    with col3:
                        st.write("Trees")
                    with col4:
                        st.markdown(
            '<span style="color:#00c853; font-size:16px;">Easy</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem35", use_container_width=True):
                            st.session_state.question_no = 35
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = "" 
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 36 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("36. Binary Tree Level Order Traversal")
                    with col3:
                        st.write("Trees")
                    with col4:
                        st.markdown(
            '<span style="color:#ff9800; font-size:16px;">Medium</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem36", use_container_width=True):
                            st.session_state.question_no = 36
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = "" 
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True) 
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 37 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("37. Lowest Common Ancestor of a Binary Tree")
                    with col3:
                        st.write("Trees")
                    with col4:
                        st.markdown(
            '<span style="color:#FF0000; font-size:16px;">Hard</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem37", use_container_width=True):
                            st.session_state.question_no = 37
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = "" 
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True) 
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 38 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("38. Course Schedule")
                    with col3:
                        st.write("Graph")
                    with col4:
                        st.markdown(
            '<span style="color:#FF0000; font-size:16px;">Hard</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem38", use_container_width=True):
                            st.session_state.question_no = 38
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = "" 
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)
                    col1, col2, col3, col4,col5 = st.columns([1, 3,3, 3, 0.9])
                    with col1:
                            if 39 in st.session_state.solved_questions:
                                st.write("ㅤ🟩")
                            else:
                                st.write("ㅤ⬜")
                    with col2:
                        st.write("39. Minimum Distance Between Tree Nodes")
                    with col3:
                        st.write("Graph & Trees")
                    with col4:
                        st.markdown(
            '<span style="color:#FF0000; font-size:16px;">Hard</span>',
            unsafe_allow_html=True
        )
                    with col5:
                        if st.button("Solve", key="problem39", use_container_width=True):
                            st.session_state.question_no = 39
                            st.session_state.problem_tab = "description"
                            st.session_state.submission_output = "" 
                            st.session_state.page = "problem"
                            st.rerun()
                    st.markdown("""
        <div style="
            height: 1px;
            background-color: #454d52;
            width: 100%;
            margin: 0;
        "></div>
    """, unsafe_allow_html=True)                                                                                                                                                                                                                                                                                                             
elif st.session_state.page == "history":
    co1,col2,col3=st.columns([1,12,1])
    with col2:
        st.title("Submission History")
        st.caption("Your previous coding submissions")

        history = fetch_submission_history(
        st.session_state.username
    )
        if not st.session_state.logged_in:
            st.warning("Please login first to get history")
        elif not history:
            st.info("No submissions found.")

        else:
            st.success(f"Total submissions: {len(history)}")

            for submission in history:

                status = submission["status"]

                if status == "ACCEPTED":
                    status_label = "🟢 Accepted"
                elif status == "COMPILATION ERROR":
                    status_label = "🔴 Compilation Error"
                else:
                    status_label = "🔴 Not Accepted"

                with st.expander(
                f"Question {submission['question_id']} | "
                f"{status_label} | "
                f"#{submission['submission_id']}"
                ):

                    st.write(f"**Submission ID:** {submission['submission_id']}")
                    st.write(f"**Question ID:** {submission['question_id']}")
                    st.write(f"**Status:** {status_label}")
                    st.write(f"**Date:** {submission['submitted_at']}")

                    st.markdown("**Submitted Code**")

                    st.code(
                        submission["submitted_code"],
                        language="cpp"
                    )
elif st.session_state.page == "bug_hunt":
    co1,col2,col3=st.columns([1,12,1])
    with col2:
        show_bug_hunt()
elif st.session_state.page=='progress':
    show_progress_page()
elif st.session_state.page == "login":
    col1, col2, col3, col4 = st.columns([3, 2, 2.5, 0.5])
    with col2:
        with st.container(key="login_box"):
            st.header("ㅤㅤLOGIN")

            username = st.text_input(
                "Username",
                key="login_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_password"
            )

            st.write("")
            if st.button("Submit", key="login_submit"):
                if not username.strip() or not password:
                    st.error("Please enter your username and password.")

                else:
                    try:
                        env = os.environ.copy()
                        env["PATH"] = (
                r"C:\Program Files\MySQL\MySQL Server 8.0\lib;"
                r"C:\msys64\ucrt64\bin;"
                + env.get("PATH", "")
            )

                        result = subprocess.run(
                [LOGIN_PATH],
                input=f"{username.strip()}\n{password}\n",
                capture_output=True,
                text=True,
                timeout=10,
                cwd=BACKEND_PATH,
                env=env
            )

                        output = result.stdout.strip()
                        error_output = result.stderr.strip()

                        if result.returncode != 0:
                            st.error(
                    f"Login backend error: {error_output or output or 'Unknown error'}"
                )

                        elif output == "LOGIN_FAILED":
                            st.error("Invalid username or password.")

                        elif output.startswith("HASH:"):
                            password_hash = output[len("HASH:"):].strip()

                            if not password_hash:
                                st.error("Password hash was not returned.")

                            elif bcrypt.checkpw(
                    password.encode("utf-8"),
                    password_hash.encode("utf-8")
                ):
                                st.session_state.logged_in = True
                                st.session_state.username = username.strip()
                                st.session_state.solved_questions = get_solved_questions(username)
                                st.session_state.current_user = username.strip()
                                st.session_state.page = "home"
                                st.rerun()

                            else:
                                st.error("Invalid username or password.")

                        else:
                            st.error(
                    f"Unexpected login response: {output or error_output}"
                )

                    except subprocess.TimeoutExpired:
                        st.error("Login timed out. Please try again.")

                    except Exception as e:
                        st.error(f"Login error: {e}")
                        st.write("")

            if st.button(
                "Forgot Username / Forgot Password",
                key="forgot_login"
            ):
                st.session_state.page = "forgotuser"
                st.rerun()

            if st.button("Signup", key="login_signup"):
                st.session_state.page = "signup"
                st.rerun()
elif st.session_state.page == "signup":
    col1, col2, col3, col4 = st.columns([3, 2, 2.5, 0.5])

    with col1:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")

        if st.button("Back"):
            st.session_state.page = "login"
            st.rerun()

    with col2:
        with st.container(key="login_box"):
            st.header("ㅤㅤSIGNUP")

            email = st.text_input("Email", key="signup_email")
            username = st.text_input("Username", key="signup_username")
            password = st.text_input(
                "Password", type="password", key="signup_password"
            )
            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                key="signup_confirm_password"
            )

            if st.button("Submit", key="signup_submit"):
                if not all([
                    email.strip(), username.strip(),
                    password, confirm_password
                ]):
                    st.error("Please enter all details.")

                else:
                    try:
                        env = os.environ.copy()
                        env["DB_PASSWORD"] = st.secrets["DB_PASSWORD"]
                        env["PATH"] = (
                            r"C:\Program Files\MySQL\MySQL Server 8.0\lib;"
                            r"C:\msys64\ucrt64\bin;"
                            + env.get("PATH", "")
                        )
                        result = subprocess.run(
                            [SIGNUP_PATH, "--validate"],
                            input=(
                                f"{email.strip()}\n"
                                f"{username.strip()}\n"
                                f"{password}\n"
                                f"{confirm_password}\n"
                            ),
                            capture_output=True,
                            text=True,
                            timeout=10,
                            cwd=BACKEND_PATH,
                            env=env
                        )
                        message = result.stdout.strip()
                        if result.returncode != 0 or message != "VALID":
                            st.error(message or "Signup validation failed.")
                            if result.stderr.strip():
                                st.code(result.stderr.strip())
                        else:
                            st.write("LOGIN_PATH:", LOGIN_PATH)
                            st.write("BACKEND_PATH:", BACKEND_PATH)
                            st.write("EXE EXISTS:", os.path.exists(LOGIN_PATH))
                            st.write("EXE TIME:", os.path.getmtime(LOGIN_PATH))
                            result = subprocess.run(
                                [SIGNUP_PATH, "--check"],
                                input=f"{email.strip()}\n{username.strip()}\n",
                                capture_output=True,
                                text=True,
                                timeout=10,
                                cwd=BACKEND_PATH,
                                env=env
                            )
                            message = result.stdout.strip()
                            if result.returncode != 0:
                                st.error("Could not check the database.")

                                if result.stderr.strip():
                                    st.code(result.stderr.strip())

                            elif message == "USER_EXISTS":
                                st.error(
                                    "This email or username is already registered."
                                )

                            elif message == "AVAILABLE":
                                st.session_state.email = email.strip()
                                st.session_state.username = username.strip()
                                st.session_state.password = password
                                st.session_state.page = "otp"
                                st.rerun()
                            else:
                                st.error("Unexpected database response.")
                    except subprocess.TimeoutExpired:
                        st.error("Signup operation timed out.")
                    except Exception as e:
                        st.error(f"Signup error: {e}")
elif st.session_state.page == "otp":
    st.write("")
    st.write("")
    st.write("")
    col1, col2, col3, col4 = st.columns([3, 1.2, 2.5, 0.5])
    with col1:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        if st.button("Back", key="otp_back_left"):
            st.session_state.page = "signup"
            st.rerun()
    with col2:
        if "otp" not in st.session_state:
            st.session_state.otp = "".join(
                str(random.randint(0, 9)) for _ in range(6)
            )
            try:
                msg = EmailMessage()
                msg["Subject"] = "CodePulse - OTP Verification"
                msg["From"] = st.secrets["EMAIL_ADDRESS"]
                msg["To"] = st.session_state.email
                msg.set_content(
                    f"Your CodePulse verification OTP is: "
                    f"{st.session_state.otp}\n\n"
                    "Do not share this code with anyone."
                )
                with smtplib.SMTP(
                    "smtp.gmail.com", 587, timeout=20
                ) as server:
                    server.ehlo()
                    server.starttls(
                        context=ssl.create_default_context()
                    )
                    server.ehlo()
                    server.login(
                        st.secrets["EMAIL_ADDRESS"],
                        st.secrets["EMAIL_APP_PASSWORD"]
                    )
                    server.send_message(msg)
                st.session_state.otp_sent = True
            except Exception as e:
                st.session_state.otp_sent = False
                st.session_state.pop("otp", None)
                st.error(f"Could not send OTP: {e}")
        with st.container(key="otp_box"):
            st.subheader("Verification")
            st.write("Check your email for the 6-digit OTP.")
            if st.session_state.get("otp_sent", False):
                entered_otp = st.text_input(
                    "Enter OTP",
                    max_chars=6,
                    key="entered_otp"
                )
                if st.button("Submit", key="otp_submit"):
                    if entered_otp.strip() != st.session_state.otp:
                        st.error("Wrong OTP. Please try again.")
                    else:
                        try:
                            env = os.environ.copy()
                            env["DB_PASSWORD"] = (
                                st.secrets["DB_PASSWORD"]
                            )
                            env["PATH"] = (
                                r"C:\Program Files\MySQL\MySQL Server 8.0\lib;"
                                r"C:\msys64\ucrt64\bin;"
                                + env.get("PATH", "")
                            )
                            password_hash = bcrypt.hashpw(
                                st.session_state.password.encode("utf-8"),
                                bcrypt.gensalt()
                            ).decode("utf-8")

                            result = subprocess.run(
                                [SIGNUP_PATH],
                                input=(
                                    f"{st.session_state.email}\n"
                                    f"{st.session_state.username}\n"
                                    f"{password_hash}\n"
                                ),
                                capture_output=True,
                                text=True,
                                timeout=15,
                                cwd=BACKEND_PATH,
                                env=env
                            )
                            output = result.stdout.strip()

                            if (
                                result.returncode == 0
                                and output == "SIGNUP_SUCCESS"
                            ):
                                st.session_state.logged_in = True
                                st.session_state.current_user = (
                                    st.session_state.username
                                )
                                st.session_state.page = "home"

                                for key in (
                                    "otp",
                                    "otp_sent",
                                    "entered_otp",
                                    "password",
                                    "signup_password",
                                    "email",
                                ):
                                    st.session_state.pop(key, None)

                                st.success("Account created successfully!")
                                st.rerun()

                            else:
                                st.error("Could not create account.")
                                st.write(
                                    "Return code:",
                                    result.returncode
                                )
                                st.write("C++ output:", repr(output))

                                if result.stderr.strip():
                                    st.code(result.stderr.strip())

                        except subprocess.TimeoutExpired:
                            st.error("Database operation timed out.")

                        except Exception as e:
                            st.error(f"Signup error: {e}")

            else:
                st.warning(
                    "OTP was not sent. Return to signup and try again."
                )
elif st.session_state.page == "problem":
    question_no = st.session_state.question_no
    problem = questions[question_no]

    with st.container(key="problem-page"):
        st.markdown("""
        <style>
        .st-key-problem-page {
            position: relative !important;
            top: -2rem !important;
        }
        .st-key-description_box {
            background-color: #1a1a1a !important;
            border: 1px solid #454d52 !important;
            border-radius: 10px !important;
            padding: 20px !important;
        }
        .st-key-submit_solution button {
            background-color: #00c853 !important;
            color: white !important;
            border: 1px solid #00c853 !important;
        }
        .st-key-submit_solution button:hover {
            background-color: #00b248 !important;
        }
        </style>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns([1, 6, 6, 1])

        with col2:
            c1, c2 = st.columns([6, 2])

            with c1:
                st.write("")
                st.write("")
                st.markdown(
                    f'<span style="color:#FFFFFF;font-size:26px;'
                    f'font-weight:bold;">{question_no}. '
                    f'{problem["title"]}</span>',
                    unsafe_allow_html=True
                )

            with c2:
                st.write("")
                st.write("")
                difficulty_colors = {
                    "Easy": "#00c853",
                    "Medium": "#ff9800",
                    "Hard": "#f44336"
                }
                difficulty = problem["difficulty"]

                st.markdown(
                    f'<span style="color:'
                    f'{difficulty_colors.get(difficulty, "#FFFFFF")};'
                    f'font-size:26px;font-weight:bold;">'
                    f'{difficulty}</span>',
                    unsafe_allow_html=True
                )

            if "problem_tab" not in st.session_state:
                st.session_state.problem_tab = "description"

            with st.container(key="description_box"):
                tab1, tab2 = st.columns([0.5, 2])

                with tab1:
                    if st.button("Description", key="description_tab"):
                        st.session_state.problem_tab = "description"
                        st.rerun()

                with tab2:
                    if st.button(
                        "Submitted Code",
                        key="submitted_code_tab"
                    ):
                        st.session_state.problem_tab = "submitted"
                        st.rerun()

                if st.session_state.problem_tab == "description":
                    st.markdown("""
                    <style>
                    .st-key-description_tab button,
                    .st-key-description_tab button p {
                        color: #2196F3 !important;
                    }
                    </style>
                    """, unsafe_allow_html=True)

                    st.write(problem["description"])
                    st.write("**Example:**")
                    st.code(problem["example"])

                else:
                    st.markdown("""
                    <style>
                    .st-key-submitted_code_tab button,
                    .st-key-submitted_code_tab button p {
                        color: #2196F3 !important;
                    }
                    </style>
                    """, unsafe_allow_html=True)

                    st.write("### Submitted Output")

                    if st.session_state.submission_output:
                        submission = st.session_state.submission_output

                        if "🟩" in submission:
                            st.success("🟩 Code executed successfully!")
                            st.code(submission)

                        elif "🟥" in submission:
                            st.error(
                                "🟥 Code was not accepted / execution failed."
                            )
                            st.code(submission)

                        else:
                            st.code(submission)
                    else:
                        st.write("No submission yet.")

        with col3:
            top1, top2, top3, top4 = st.columns([3, 2.5, 1.5, 1])

            with top2:
                language = st.segmented_control(
                    "Language",
                    ["C++"],
                    default="C++",
                    key="language_select"
                )

            with top4:
                st.write("")
                st.write("")

                if st.button("Back", key="back_button"):
                    st.session_state.page = "problems"
                    st.rerun()

            
            text = st_ace(
                    value=problem["starter_code"],
                    language="c_cpp",
                    theme="tomorrow_night",
                    height=450,
                    key=f"cpp_editor_{question_no}",
                    auto_update=True
                )
            
            with top1:
                st.write("")

                with st.container(key="submit_button_box"):
                    st.markdown("""
                    <style>
                    .st-key-submit_button_box div.stButton > button {
                        background-color: #00c853 !important;
                        color: white !important;
                        border: 1px solid #00c853 !important;
                        border-radius: 8px !important;
                    }
                    .st-key-submit_button_box div.stButton > button:hover {
                        background-color: #00b248 !important;
                        color: white !important;
                        border: 1px solid #00b248 !important;
                    }
                    </style>
                    """, unsafe_allow_html=True)

                    if st.button("Submit", key="submit_solution"):
                        if language == "C++":
                            backend_path = (
                                r"C:\Users\saksh\OneDrive\Documents"
                                r"\CodePulse\Backend(C++)"
                            )

                            judge_path = os.path.join(
                                backend_path, "judge.exe"
                            )

                            if not st.session_state.logged_in:
                                st.warning("Please login first to access the Judge.")

                            else:
                                try:
                                    result = subprocess.run(
                                        [
                                            judge_path,
                                            str(question_no),
                                            st.session_state.username
                                        ],
                                        input=text or "",
                                        capture_output=True,
                                        text=True,
                                        cwd=backend_path,
                                        timeout=60,
                                        env=os.environ.copy()
                                    )

                                    output = (result.stdout or "").strip()
                                    error_output = (result.stderr or "").strip()

                                    if error_output:
                                        st.code(error_output)

                                    if (
                                        result.returncode == 0
                                        and "ACCEPTED" in output
                                        and "NOT ACCEPTED" not in output
                                    ):
                                        st.session_state.solved_questions.add(
                                            question_no
                                        )

                                        st.session_state.submission_output = (
                                            "🟩 Problem Solved!\n\n" + output
                                        )

                                    else:
                                        details = (
                                            output
                                            if output
                                            else "No output returned by judge."
                                        )

                                        if "NOT ACCEPTED" in output:
                                            st.session_state.submission_output = (
                                                "🟥 Not Solved\n\n"
                                                "Some test cases failed. "
                                                "Check the details below:\n\n"
                                                + details
                                            )
                                        else:
                                            st.session_state.submission_output = (
                                                "🟥 Execution Failed\n\n"
                                                + details
                                            )

                                except subprocess.TimeoutExpired:
                                    st.session_state.submission_output = (
                                        "🟥 Execution Failed\n\n"
                                        "Submission timed out."
                                    )

                                except Exception as e:
                                    st.session_state.submission_output = (
                                        "🟥 Execution Failed\n\n" + str(e)
                                    )
                                st.session_state.problem_tab = "submitted"
                                st.rerun()

    with st.sidebar:
        codepulse_chatbot(problem)
elif st.session_state.page == "forgotuser":
    col1, col2, col3, col4 = st.columns([3, 2, 2.5, 0.5])

    with col2:
        st.write("")
        st.write("")
        st.write("")
        st.write("")

        with st.container(key="otp_box"):
            st.subheader("Forgot Password")

            email = st.text_input(
                "Registered Email",
                placeholder="Enter your email address",
                key="forgot_password_email"
            )

            if st.button("Continue", key="forgot_password_continue"):
                email = email.strip()

                if not email:
                    st.warning("Please enter your registered email.")

                else:
                    try:
                        env = os.environ.copy()
                        env["DB_PASSWORD"] = st.secrets["DB_PASSWORD"]

                        # Keep your existing MySQL and MSYS2 PATH setup here.
                        env["PATH"] = (
                            r"C:\Program Files\MySQL\MySQL Server 8.0\lib;"
                            r"C:\msys64\ucrt64\bin;"
                            + env.get("PATH", "")
                        )

                        result = subprocess.run(
                            [CHECK_EMAIL_PATH],
                            input=email + "\n",
                            capture_output=True,
                            text=True,
                            timeout=10,
                            cwd=BACKEND_PATH,
                            env=env
                        )

                        output = result.stdout.strip()
                        lines = output.splitlines()

                        if result.returncode != 0:
                            st.error("Could not check the registered email.")
                            st.write("Backend error:", result.stderr.strip())
                        
                        elif "EMAIL_NOT_FOUND" in lines:
                            st.error("No account found with this email.")

                        elif "EMAIL_CHECK_FAILED" in lines:
                            st.error("Database email verification failed.")

                        else:
                            # Extract username independently from email.
                            recovered_username = None

                            for line in lines:
                                if line.startswith("USERNAME:"):
                                    recovered_username = (
                                        line.split(":", 1)[1].strip()
                                    )
                                    break

                            if (
                                "EMAIL_FOUND" in lines
                                and recovered_username
                            ):
                                # Store email and username separately.
                                st.session_state.recovery_email = email
                                st.session_state.recovery_username = (
                                    recovered_username
                                )

                                # Clear previous OTP verification state.
                                st.session_state.pop("reset_otp", None)
                                st.session_state.pop(
                                    "reset_otp_sent", None
                                )
                                st.session_state.pop(
                                    "reset_otp_verified", None
                                )

                                st.session_state.page = (
                                    "forgot_password_otp"
                                )
                                st.rerun()

                            else:
                                st.error(
                                    "The backend did not return both "
                                    "EMAIL_FOUND and USERNAME:<username>. "
                                    "Please check your C++ backend output."
                                )

                    except subprocess.TimeoutExpired:
                        st.error("Recovery request timed out.")

                    except Exception as e:
                        st.error(f"Recovery error: {e}")

    with col1:
        for _ in range(28):
            st.write("")

        if st.button("Back", key="forgot_password_back"):
            st.session_state.page = "login"
            st.rerun()
elif st.session_state.page == "forgot_password_otp":
    col1, col2, col3, col4 = st.columns([3, 2, 2.5, 0.5])
    with col2:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        with st.container(key="otp_box"):
            st.subheader("Enter OTP")

            if "reset_otp" not in st.session_state:
                st.session_state.reset_otp = "".join(
                    str(random.randint(0, 9)) for _ in range(6)
                )

                try:
                    msg = EmailMessage()
                    msg["Subject"] = "CodePulse Password Reset OTP"
                    msg["From"] = st.secrets["EMAIL_ADDRESS"]
                    msg["To"] = st.session_state.recovery_email
                    msg.set_content(
                        f"Your password reset OTP is: "
                        f"{st.session_state.reset_otp}\n"
                        "Do not share this code with anyone."
                    )

                    with smtplib.SMTP(
                        "smtp.gmail.com", 587, timeout=20
                    ) as server:
                        server.ehlo()
                        server.starttls(
                            context=ssl.create_default_context()
                        )
                        server.ehlo()
                        server.login(
                            st.secrets["EMAIL_ADDRESS"],
                            st.secrets["EMAIL_APP_PASSWORD"]
                        )
                        server.send_message(msg)

                    st.session_state.reset_otp_sent = True

                except Exception as e:
                    st.session_state.pop("reset_otp", None)
                    st.session_state.reset_otp_sent = False
                    st.error(f"Could not send OTP: {e}")

            if st.session_state.get("reset_otp_sent", False):
                otp_input = st.text_input(
                    "Enter the OTP sent to your email",
                    max_chars=6,
                    key="reset_otp_input"
                )

                
                if st.button("Verify OTP", key="reset_verify_otp"):
                    if otp_input.strip() == st.session_state.reset_otp:

                        recovered_username = st.session_state.get(
            "recovery_username", ""
        )
                        recovery_email = st.session_state.get(
            "recovery_email", ""
        )

                        if not recovered_username:
                            st.error(
                "Username not found. Please restart account recovery."
            )

                        else:
                            st.session_state.username = recovered_username
                            st.session_state.current_user = recovered_username
                    
                            st.session_state.reset_otp_verified = True
                            st.session_state.pop("reset_otp", None)
                            st.session_state.pop("reset_otp_sent", None)
                            st.session_state.logged_in = True
                            st.session_state.page = "home"

                            st.success(
                f"OTP verified for username: {recovered_username}"
            )
                            st.rerun()

                    else:
                        st.error("Incorrect OTP. Please try again.")

    with col1:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        if st.button("Back"):
            st.session_state.page = "forgotuser"
            st.rerun()