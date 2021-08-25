import pyrebase

firebaseConfig = {
    'apiKey': "AIzaSyAbECtqqhusDd0zZABg3h678gIpHJCHiyA",
    'authDomain': "groupby-136a4.firebaseapp.com",
    'databaseURL': "https://groupby-136a4-default-rtdb.firebaseio.com",
    'projectId': "groupby-136a4",
    'storageBucket': "groupby-136a4.appspot.com",
    'messagingSenderId': "645587650151",
    'appId': "1:645587650151:web:9f2d7f1b9d8fa685b076c2",
    'measurementId': "G-L6J17ERCQ3"
}


firebase = pyrebase.initialize_app(firebaseConfig)




def add_to_user(data,id):
    db = firebase.database()
    db.child('user').child(str(id)).set(data)

def add_to_userinfo(data,id):
    db = firebase.database()
    db.child('userinfo').child(str(id)).set(data)

