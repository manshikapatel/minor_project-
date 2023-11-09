import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-c0d6b-default-rtdb.firebaseio.com/",
    "storageBucket": "faceattendancerealtime-c0d6b.appspot.com"
})

bucket = storage.bucket()
#Webcam
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

#Graphics
imgBackground = cv2.imread('C:/Users/YUGANK/Desktop/Manshika_File/project/minor_project/Face_Recognition_Real_Time_Databases/Resource/Background.jpeg')

#Importing the mode images into a list 
folderModePath = 'C:/Users/YUGANK/Desktop/Manshika_File/project/minor_project/Face_Recognition_Real_Time_Databases/Resource/mode'
modePathList = os.listdir(folderModePath)
imgModeList = []

for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))
# print(len(imgModeList))

#load the encoding file
print("Loading Encode File...")
file = open('C:/Users/YUGANK/Desktop/Manshika_File/project/minor_project/Face_Recognition_Real_Time_Databases/EncodedFile.p','rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown,studentIds = encodeListKnownWithIds
# print(studentIds)
print("Encode File Loaded")

modeType = 0
counter = 0
id = -1
imgStudent =[]

while True:
    success, img = cap.read()

    imgS  = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS,faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
            for encodeFace, faceLoc in zip(encodeCurFrame,faceCurFrame):
            #Check if the current face encoding is not None
                if encodeFace is not None and len(encodeListKnown) > 0:
            # Ensure that known encodings are loaded
                # if len(encodeListKnown) > 0:
                    matches =[]
                    faceDis = []
                    for known_encoding in encodeListKnown:
                    # encodeFace = [encodeFace]
                        if known_encoding is not None:
                            match = face_recognition.compare_faces([known_encoding], encodeFace)
                        #Extract the match result from the list
                            matches.append(match[0])
                            distance = face_recognition.face_distance([known_encoding],encodeFace)
                        #Extract the distance value from the list
                            faceDis.append(distance[0])
                        else :
                            #Handle the case where a known encoding is none
                            matches.append(None)
                            faceDis.append(None)

                        # faceDis = face_recognition.face_distance(encodeListKnown,encodeFace[0])
                    print("matches",matches)
                    print("faceDis",faceDis)

                    filtered_faceDis = [distance for distance in faceDis if distance is not None] 

                    if filtered_faceDis:
                        matchIndex = filtered_faceDis.index(min(filtered_faceDis))
                    print("Match Index:", matchIndex)

                    # matchIndex = np.argmin(faceDis)
                    # print("Match Index", matchIndex)

                    if matches [matchIndex] is not None:
                        if matches[matchIndex]:
                            # print("KNOEN FACE IS DETECTED")
                            # print(studentIds[matchIndex])
                            y1, x2, y2, x1 = faceLoc
                            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                            imgBackground = cvzone.cornerRect(imgBackground,bbox,rt=0)
                            id = studentIds[matchIndex]
                            print(id)

                            if counter == 0:
                                cvzone.putTextRect(imgBackground,"Loading",(275,400))
                                cv2.imshow("Face Attendence", imgBackground)
                                cv2.waitKey(1)
                                counter = 1
                                modeType = 1
                        else:
                            print("NO KNOWN FACE DETECTED IN THE CURRENT FRAME")
                    else:
                        print("NO known face  detected in the current frame")
                    
                    if counter!= 0:

                        if counter ==1:
                            studentInfo = db.reference(f'Students/{id}').get()
                            print(studentInfo)

                            #Get the images from storage
                            blob = bucket.get_blob(f'Images/{id}.jpeg')
                            if blob is not None:
                                image_data = blob.download_as_string()
                                if image_data:
                                    array = np.frombuffer(image_data,np.uint8)
                                    if len(array)>0:
                                        imgStudent = cv2.imdecode(array,cv2.IMREAD_COLOR)
                                else:
                                    imgStudent = None
                            else:
                                imgStudent = None
                            # imgStudent = cv2.imdecode(array,cv2.IMREAD_COLOR)

                            #updata data of attendence
                            datetimeObject = datetime.strptime(studentInfo['Last_attendance_time'],
                                                            "%Y-%m-%d %H:%M:%S")
                            secondElapsed = (datetime.now()-datetimeObject).total_seconds()
                            print(secondElapsed)
                            if secondElapsed > 30:
                                ref = db.reference(f'Students/{id}')
                                studentInfo['Total_Attendance'] +=1
                                ref.child('Total_Attendance').set(studentInfo['Total_Attendance'])
                                ref.child('Last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            else:
                                modeType = 3
                                counter = 0
                                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                        if modeType != 3:        
                            if 10<counter<20: 
                                modeType =2

                            
                            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                            if counter<=10:

                                cv2.putText(imgBackground,str(studentInfo['Total_Attendance']),(861,125),
                                            cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255), 1)
                                cv2.putText(imgBackground,str(studentInfo['name']),(810,445),
                                            cv2.FONT_HERSHEY_COMPLEX,1,(50,50,50), 1)
                                cv2.putText(imgBackground,str(studentInfo['branch']),(1006,550),
                                            cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                                cv2.putText(imgBackground,str(studentInfo['id']),(1006,493),
                                            cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                                cv2.putText(imgBackground,str(studentInfo['Class']),(910,625),
                                            cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                                cv2.putText(imgBackground,str(studentInfo['semester']),(1002,625),
                                            cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                                cv2.putText(imgBackground,str(studentInfo['Year']),(1125,625),
                                            cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                                if imgStudent is not None:
                                    imgBackground[175:175+216,909:909+216] = imgStudent

                        counter+=1

                        if counter >=20:
                            counter = 0
                            modeType =0
                            studentInfo = []
                            imgStudents =[]
                            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                elif len (encodeListKnown) == 0:
                    print("No KNown face encodings loaded")
                else:
                    print("No face encoding detected in the current frame")

    else:
        modeType = 0
        counter = 0
    # cv2.imshow("Webcam",img)
    cv2.imshow("Face Attendance",imgBackground)
    k=cv2.waitKey(1)

    if k == ord('q'):
        break