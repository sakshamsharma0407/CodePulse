import streamlit as st
import mysql.connector
import re
import bcrypt
import random
import smtplib
from email.message import EmailMessage

@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )
st.markdown("""
<style>
.block-container {
    padding-top: 2.3rem;
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
div.stButton > button {
    background-color: #222222;
    color: white;
    border: 1px solid #444444;
    border-radius: 8px;
}

div.stButton > button:hover {
    background-color: #333333;
    color: white;
}
</style>
""", unsafe_allow_html=True)
if "page" not in st.session_state:
    st.session_state.page="home"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None
c1,c8,c2,c3,c7,c4,c5,c6=st.columns([1,0.4,0.4,0.4,0.4,0.7,0.7,0.7])
with c1:
    st.image("pic.png", width=175)
with c8:
    st.write(" ")
    if(st.button("Home",key='home')):
        st.session_state.page="home"
        st.rerun()    
with c2:
    st.write("")
    if(st.button("Problems",key='problems')):
        st.session_state.page="problems"
        st.rerun()
with c3:
    st.write("")
    if(st.button("History",key='history')):
        st.session_state.page="history"
        st.rerun()
with c4:
    st.write("")
    if(st.button("Interview",key='interview')):
        st.session_state.page="interview"
        st.rerun()
with c5:
    st.write("")
    if(st.button("Progress",key='progress')):
        st.session_state.page="progress"
        st.rerun()
with c6:
    st.write("")
    if(st.button("Login",key='login')):
        st.session_state.page="login"
        st.rerun()
with c7:
    st.write("")
    if(st.button("Debug",key='debug')):
        st.session_state.page="debug"
        st.rerun()
if st.session_state.page=='home':
    st.title("Home Page")
elif st.session_state.page=='problems':
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    col1,col2,col3,col4,col5,col6,col7,col8,col9=st.columns([5,2,2,2,2,2,2,2,5])
    with col2:
        if st.button("Array"):
            st.session_state.page='array'
            st.rerun()
        st.write("")
        st.write("")
        st.write("")
        text=st.text_input("Search Question")
        st.write("")
        st.write("")        
    with col3:
        if st.button("Linked List"):
            st.session_state.page='ll'
            st.rerun() 
    with col4:
        if st.button("Sorting"):
            st.session_state.page='sorting'
            st.rerun()
    with col5:
        if st.button("Queue"):
            st.session_state.page='queue'
            st.rerun() 
    with col6:
        if st.button("Recursion"):
            st.session_state.page='recursion'
            st.rerun()   
    with col7:
        if st.button("String"):
            st.session_state.page='string'
            st.rerun()
    with col8:
        if st.button("Trees"):
            st.session_state.page='trees'
            st.rerun()                                            
    st.write(" ")
    
    with st.sidebar:
        if st.button("Library"): 
            st.session_state.page='problems'
            st.rerun()              
        if st.button("Quest"):
            st.session_state.page='quest'
            st.rerun()  
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write("-------------")
        st.button("Favourites⭐")
    co1,co2=st.columns([0.76,3])
    with co2:
        if st.button("1. Two SetㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤEASY"):
            st.session_state.page='twoset'
            st.rerun()        
    if st.button("Back"):
        st.session_state.page='home'
        st.rerun()
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
    col1,col2,col3,col4=st.columns([3,1,2.5,0.5])
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
        st.header("Login")
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
                        stored_hash.encode("utf-8")
                    ):
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
    col1,col2,col3,col4=st.columns([3,1,2.5,0.5])
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
        st.header("Signup")
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
    col1,col2,col3,col4=st.columns([3,1,2.5,0.5])
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
                st.session_state.otp +=str(random.randint(0,9))
            msg=EmailMessage()
            from_mail="sakshamsharma.0407@gmail.com"
            msg['Subject']='OTP Verification'
            msg['From']=from_mail
            msg['To']=st.session_state.email
            msg.set_content(f"Your OTP is:{st.session_state.otp}")
            server.send_message(msg)
            server.quit()
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
    col1,col2,col3,col4=st.columns([3,1,2.5,0.5])
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
        st.header("CodePulse")
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
elif st.session_state.page=='twoset':
    col1,col2=st.columns([1,1])
    with col1:
        st.write("""You are given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

Example 1:
Input: nums = [2,7,11,15],target = 9

Output: [0,1]

Explanation: Because nums[0] + nums[1] == 9, 
we return [0, 1].

Example 2:

Input: nums = [3,2,4],target = 6

Output: [1,2]

Example 3:

Input: nums = [3,3], target = 6

Output: [0,1]

Constraints:

2 <= nums.length <= 104

-109 <= nums[i] <= 109

-109 <= target <= 109

Only one valid answer exists.

Follow-up: Can you come up with an algorithm that is less than O(n2) time complexity?""")
    with col2:
        text=st.text_area("Enter your code",height=450)
        if st.button("Submit"):
            st.write("done")