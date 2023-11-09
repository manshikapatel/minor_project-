import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-c0d6b-default-rtdb.firebaseio.com/"
})

ref =db.reference('Students')

data = {

    "097":
        {
            "name": "Manshi Kumari",
            "branch": "CSE",
            "Class":"CS-B",
            "id":"097",
            "semester":"5th",
            "Year":"3-Year",
            "Total_Attendance":10,
            "Last_attendance_time":"2023-11-01  00:54:34" 
        },      
    "098":
        {
            "name": "Manshika Patel",
            "branch": "CSE",
            "Class":"CS-B",
            "id":"098",
            "semester":"5th",
            "Year":"3-Year",
            "Total_Attendance":10,
            "Last_attendance_time":"2023-11-01  00:54:34"       
        },
    "099":
        {
            "name": "pooja Gour",
            "branch": "CSE",
            "Class":"CS-B",
            "id":"099",
            "semester":"5th",
            "Year":"3-Year",
            "Total_Attendance":11,
            "Last_attendance_time":"2023-11-02  00:54:34"       
        },
    "100":
        {
            "name": "Gitika Birla",
            "branch": "Hotal Management",
            "Class":"HM",
            "id":"100",
            "semester":"5th",
            "Year":"3-Year",
            "Total_Attendance":20,
            "Last_attendance_time":"2023-11-02  00:54:20"       
        },
    "101":
        {
            "name": "Palak Sharma",
            "branch": "CSE",
            "Class":"CS-B",
            "id":"101",
            "semester":"5th",
            "Year":"3-Year",
            "Total_Attendance":15,
            "Last_attendance_time":"2023-11-01  00:54:34"       
        },
    "102":
        {
            "name": "Anshika Solanki",
            "branch": "CSE",
            "Class":"CS-A",
            "id":"102",
            "semester":"5th",
            "Year":"3-Year",
            "Total_Attendance":20,
            "Last_attendance_time":"2023-11-01  00:54:34"       
        },
    "103":
        {
            "name": "Arundhati Pawar",
            "branch": "CSE",
            "Class":"CS-A",
            "id":"103",
            "semester":"5th",
            "Year":"3-Year",
            "Total_Attendance":20,
            "Last_attendance_time":"2023-11-01  00:54:34"       
        }
}

for key,value in data.items():
    ref.child(key).set(value)