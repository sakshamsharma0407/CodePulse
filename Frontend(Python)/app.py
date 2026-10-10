import streamlit as st
import mysql.connector
import re
import bcrypt
import random
import smtplib
from email.message import EmailMessage
import subprocess
import tempfile
import os
import subprocess
import sys
from streamlit_ace import st_ace
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
username = "saksham"
password = "1234"
import os
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

backend_path = os.path.join(BASE_DIR, "Backend(C++)")
login_path = os.path.join(backend_path, "login.exe")

print("PATH:", login_path)
print("EXISTS:", os.path.exists(login_path))

if not os.path.exists(login_path):
    st.error("login.exe not found!")
else:
    result = subprocess.run(
        [login_path, username, password],
        capture_output=True,
        text=True,
        cwd=backend_path
    )

    print("C++ OUTPUT:", result.stdout)
    print("C++ ERROR:", result.stderr)
@st.cache_resource
@st.cache_data
def get_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )
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

vector<int> twoSet(vector<int>& nums, int target) {
    // Student writes solution here
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
if "problem_tab" not in st.session_state:
    st.session_state.problem_tab = "description"

if "submission_output" not in st.session_state:
    st.session_state.submission_output = ""

if "page" not in st.session_state:
    st.session_state.page = "home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state.username = None

if "solved_questions" not in st.session_state:
    st.session_state.solved_questions = set()

active_page = st.session_state.page


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
    with c4:
        st.write("")
        if(st.button("💼Interview",key='interview')):
            st.session_state.page="interview"
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
        if(st.button("🔍︎Debug",key='debug')):
            st.session_state.page="debug"
            st.rerun()
if st.session_state.page=='home':
    col1,col2,col3=st.columns([1,12,1])
    with col2:
        st.title("CodePulse: A Coding Practice and Evaluation Platform")
        st.write("")
        st.header("""Practice DSA. Write Code.Build Better Problem-Solving Skills.""")
        st.write("CodePulse is an interactive DSA practice platform designed to help you solve coding problems, test your solutions, track your performance, and improve your weak areas.")
        col1,col2=st.columns([1,1])
        with col1:
            with st.container(key="description_box"):
                st.subheader("""Why CodePulse?""")
                st.write("""
•Practice — Solve problems across different DSA topics.

•Code & Judge — Write your solution and test it instantly.

•Learn from History — Review your previous attempts.

•Improve Weak Areas — Identify topics that need more practice.""")
                st.subheader("""Made By:""")
                st.write("""
Saksham Sharma

Lokesh Farswan

Prateek Pratap Singh

Shorya Pratap""")
elif st.session_state.page=='problems':
    st.write(" ")
    st.write(" ")
    co1,col2,col3=st.columns([0.5,6,0.5])
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
    # Question 1
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
            
    # Divider
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
                                                                                                                                                                                                                                                                                                      
elif st.session_state.page=='history':
    st.title("History Page")
    if st.button("Back"):
        st.session_state.page='home'
        st.rerun()
elif st.session_state.page=='interview':
    st.title("Interview Page")
    if st.button("Back"):
        st.session_state.page='home'
        st.rerun()
elif st.session_state.page=='progress':
    st.title("Progress Page")
    if st.button("Back"):
        st.session_state.page='home'
        st.rerun()
elif st.session_state.page=='login':
    st.write(" ")
    st.write(" ")
    col1,col2,col3,col4=st.columns([3,2,2.5,0.5])
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
        if st.button("Back"):
                st.session_state.page='home'
                st.rerun()                               
    with col2:
        with st.container(key="login_box"):
            st.header("ㅤㅤLOGIN")
            st.write(" ")
            st.write(" ")
            username=st.text_input("Username")
            st.write(" ")
            password=st.text_input("Password")
            st.write(" ")
            if st.button("Submit"):
                if username==None or password==None:
                    st.error("Please enter all details")
                else:
                    connection=get_connection()
                    cursor=connection.cursor()
                    cursor.execute(
                    "SELECT id, password_hash FROM USERS WHERE username = %s",
                    (username,))
                    user = cursor.fetchone()
                    if user:
                        user_id = user[0]
                        stored_hash = user[1]
                        if bcrypt.checkpw(
                            password.encode("utf-8"),
                            stored_hash.encode("utf-8")):
                            st.success("Login successful!")
                            st.session_state.logged_in = True
                            st.session_state.user_id = user_id
                            st.session_state.username = username
                            st.session_state.page = "home"                   
                            st.rerun()
                        else:
                            st.error("Sorry, incorrect password.")
                    else:
                        st.error("Sorry, username not found.")
            if st.button("Forgot Username"):
                st.session_state.page="forgotuser"
                st.rerun()
            if st.button("Forgot Password"):
                st.session_state.page="forgotpass"
                st.rerun()
    with col4:
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
        if st.button("Signup"):
            st.session_state.page='signup'
            st.rerun()
elif st.session_state.page=='signup':
    st.write(" ")
    st.write(" ")
    col1,col2,col3,col4=st.columns([3,2,2.5,0.5])
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
        if st.button("Back"):
            st.session_state.page='login'
            st.rerun()
    with col2:
        with st.container(key="login_box"):
            st.header("ㅤㅤSIGNUP")
            st.write(" ")
            email=st.text_input("Email")
            password=st.text_input("Password")
            confirm_password=st.text_input("Confirm Password")
            st.write(" ")
            if st.button("Submit"):
                if password==None or confirm_password==None or email==None:
                    st.error("Please enter all details")
                elif not re.fullmatch(r"[A-Za-z0-9._%+-]+@gmail\.com",email):
                    st.error("Please enter a valid Gmail address.")
                elif(confirm_password!=password):
                    st.error("Confirm Password and Password didnt match")
                elif(len(password)<8):
                    st.error("lenght of password should be greater than 8")
                elif not re.search(r"[A-Z]",password):
                    st.error("password should contain atleast one uppercase letter")
                elif not re.search(r"[^A-Za-z0-9\s]", password):
                    st.error("Password must contain at least one special character.")
                else:
                    connection=get_connection()
                    cursor=connection.cursor()
                    cursor.execute("""SELECT id from users where email=%s""",(email,))
                    existing_email=cursor.fetchone()
                    if existing_email:
                        st.error("Account has already made in this email")
                    else:
                        st.session_state.email = email
                        st.session_state.password = password   
                        st.session_state.page="otp"
                        st.rerun()
elif st.session_state.page=='otp':
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    col1,col2,col3,col4=st.columns([3,1.2,2.5,0.5])
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
        if st.button("Back"):
            st.session_state.page='signup'
            st.rerun()
    with col2:
        if "otp" not in st.session_state:
            st.session_state.otp = ""
            server=smtplib.SMTP("smtp.gmail.com",587)
            server.starttls()
            server.login("sakshamsharma.0407@gmail.com",'hedz kbbu zhmo yidq')
            for i in range(0,6):
                st.session_state.otp+=str(random.randint(0,9))
            msg=EmailMessage()
            from_mail="sakshamsharma.0407@gmail.com"
            msg['Subject']='OTP Verification'
            msg['From']=from_mail
            msg['To']=st.session_state.email
            msg.set_content(f"Your OTP is:{st.session_state.otp}")
            server.send_message(msg)
            server.quit()
        with st.container(key="otp_box"):
            st.subheader("Verification")
            st.write("")
            st.write("")
            st.write("Check your email")
            otp1=st.text_input("Enter OTP")
            st.write("")
            st.write("") 
            if st.button("Submit"):
                if st.session_state.otp==otp1:
                    st.session_state.page="user"
                    st.rerun()
                else:
                    st.error("Wrong OTP")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    if st.button("Back"):
                st.session_state.page='signup'
                st.rerun()
if st.session_state.page=='user':
    st.write(" ")
    st.write(" ")
    col1,col2,col3,col4=st.columns([3,2,2.5,0.5])
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
        if st.button("Back"):
            st.session_state.page='signup'
            st.rerun()
    with col2:
        with st.container(key="otp_box"):
            st.header("ㅤCODEPULSE")
            st.write(" ")
            st.write(" ")
            username=st.text_input("Create your Username")
            st.write(" ")
            if st.button("Submit"):
                if len(username)<=4:
                    st.error("Choose username more than 4 letters")
                elif ' ' in username:
                    st.error("Username should not contain space")
                else:
                    try:
                        connection=get_connection()
                        cursor=connection.cursor()                    
                        cursor.execute("SELECT id FROM users WHERE username = %s",(username,))
                        existing_user = cursor.fetchone()
                        if existing_user:
                            st.error("Sorry, username already exists.")
                        else:
                            password_hash = bcrypt.hashpw(
                            st.session_state.password.encode("utf-8"),
                            bcrypt.gensalt()
                            ).decode("utf-8")
                            connection=get_connection()
                            cursor=connection.cursor()
                            cursor.execute("""INSERT INTO USERS (username,password_hash,email) VALUES (%s,%s,%s)""",(username,password_hash,st.session_state.email))
                            existing_user=cursor.fetchone()
                            connection.commit()
                            st.session_state.logged_in =True
                            st.session_state.page='home'
                            st.rerun()
                    except mysql.connector.Error as e:
                        st.error(f"Database error: {e}")
                    finally:
                        if "cursor" in locals():
                            cursor.close()
                        if "connection" in locals() and connection.is_connected():
                            connection.close()
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
                    f'<span style="color:#FFFFFF;font-size:26px;font-weight:bold;">'
                    f'{question_no}. {problem["title"]}</span>',
                    unsafe_allow_html=True
                )
            with c2:
                st.write("")
                st.write("")
                difficulty_colors = {"Easy": "#00c853",    "Medium": "#ff9800",  "Hard": "#f44336"     }
                difficulty = problem["difficulty"]
                st.markdown(
    f'<span style="color:{difficulty_colors.get(difficulty, "#FFFFFF")};'
    f'font-size:26px;font-weight:bold;">'
    f'{difficulty}</span>',
    unsafe_allow_html=True
)
            if "problem_tab" not in st.session_state:
                st.session_state.problem_tab = "description"
            with st.container(key="description_box"):
                tab1, tab2 = st.columns([0.5, 2])
                with tab1:
                    if st.button(
                        "Description",
                        key="description_tab"
                    ):
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
                    .st-key-description_tab button {
                        color: #2196F3 !important;
                    }

                    .st-key-description_tab button p {
                        color: #2196F3 !important;
                    }
                    </style>
                    """, unsafe_allow_html=True)

                    st.write(problem["description"])

                    st.write("**Example:**")

                    st.code(problem["example"])

                    st.write("**Constraints:**")

                    st.write(
                        """2 ≤ nums.length ≤ 10⁴

-10⁹ ≤ nums[i] ≤ 10⁹

-10⁹ ≤ target ≤ 10⁹"""
                    )
                    st.write(
                        "**Challenge:** Try to solve the problem in "
                        "better than O(n²) time complexity."
                    )
                else:
                    st.markdown("""
                    <style>
                    .st-key-submitted_code_tab button {
                        color: #2196F3 !important;
                    }

                    .st-key-submitted_code_tab button p {
                        color: #2196F3 !important;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    st.write("### Submitted Output")
                    if st.session_state.submission_output:
                        if "🟩" in st.session_state.submission_output:
                            st.success("🟩 Code executed successfully!")
                        elif "🟥" in st.session_state.submission_output:
                            st.error("🟥 Code was not accepted / execution failed.")
                        st.code(st.session_state.submission_output)
                    else:
                        st.write("No submission yet.")
        with col3:
            top1, top2, top3,top4 = st.columns([3, 2.5,1.5, 1])
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
                if st.button(
                    "Back",
                    key="back_butto"
                ):
                    st.session_state.page = "problems"
                    st.rerun()
            if language == "C++":
                text = st_ace(
                    value=problem["starter_code"],
                    language="c_cpp",
                    theme="tomorrow_night",
                    height=450,
                    key=f"cpp_editor_{question_no}",
                    auto_update=True
                )
            else:
                text = st_ace(
                    value="# Write your Python code here",
                    language="python",
                    theme="tomorrow_night",
                    height=450,
                    key=f"python_editor_{question_no}",
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
                    if st.button("Submit",key="submit_solution"):
                        if language == "C++":
                            backend_path = r"C:\Users\saksh\OneDrive\Documents\CodePulse\Backend(C++)"
                            judge_path = os.path.join(backend_path, "judge.exe")
                            try:
                                result = subprocess.run(
                [judge_path, str(question_no)],
                input=text,
                capture_output=True,
                text=True,
                cwd=backend_path,
                timeout=60
            )

                                output = (result.stdout or "").strip()
                                error_output = (result.stderr or "").strip()

                                if (
                result.returncode == 0
                and "ACCEPTED" in output
                and "NOT ACCEPTED" not in output
            ):
                                    st.session_state.solved_questions.add(question_no)
                                    st.session_state.submission_output = (
                    "🟩 Problem Solved!\n\n" + output
                )
                                else:
                                    details = output if output else "No output returned by judge."

                                    if "NOT ACCEPTED" in output:
                                        st.session_state.submission_output = (
            "🟥 Not Solved\n\n"
            "Some test cases failed. Check the details below:\n\n"
            + details
        )
                                    else:
                                        st.session_state.submission_output = (
            "🟥 Execution Failed\n\n" + details
        )


                                st.session_state.problem_tab = "submitted"
                                st.rerun()

                            except subprocess.TimeoutExpired as e:
                                partial_output = e.stdout or ""
                                partial_error = e.stderr or ""

                                st.session_state.submission_output = (
                "🟥 Timed out after 60 seconds.\n\n"
                f"Partial output:\n{partial_output}\n\n"
                f"Partial error:\n{partial_error}"
            )
                                st.session_state.problem_tab = "submitted"
                                st.rerun()

                            except Exception as e:
                                st.session_state.submission_output = (
                f"🟥 Error: {e}"
            )
                                st.session_state.problem_tab = "submitted"
                                st.rerun()
    with st.sidebar:
        codepulse_chatbot(problem)