import firebase_admin
from firebase_admin import auth, credentials, firestore
import pyrebase


cred = credentials.Certificate(r"C:\Users\Mokgethwa\Skills-SYNC\skill-sync-19755-firebase-adminsdk-fbsvc-d2ed3fab9b.json")  
firebase_admin.initialize_app(cred)
  

db = firestore.client()

firebase_configuration = {
  "apiKey": "AIzaSyB7tkgWJv7q_UYeovuTB1nKf-IPdk-zuis",
  "authDomain": "skill-sync-19755.firebaseapp.com",
  "databaseURL":"https://skill-sync-19755-default-rtdb.firebaseio.com/",
  "projectId": "skill-sync-19755",
  "storageBucket": "skill-sync-19755.appspot.com",
  "messagingSenderId": "409434407561",
  "appId": "1:409434407561:web:1feeb6db192b5b6478bc58",
  "measurementId": "G-X6H90SZ9DW"
}

def sign_up():
  
    try:
        name = input("enter your name: ")
        role = input("role? (mentor/peer): ")
        email = input("email adress: ")
        password = input("enter password: ")
        if role=='mentor':
            expertise= input("list your expertise: ")
        else:
            expertise = None    

        user = auth.create_user(email=email, password=password, display_name = name)
        print(f'user created')

        db.collection('users').document(user.uid).set({"name":name,
                                                              "email": email,
                                                              "role":role,
                                                              "expertise":expertise})
        print("user created")                                                      
    except Exception as e:
        print(f' Error creating user: {e}')


firebase = pyrebase.initialize_app(firebase_configuration)
auth_client = firebase.auth()

def get_user_data():
  while True:
    try:
        user_id= input("enter user id: (uid/exit- to quit)")
        if user_id.lower() == "exit":  # Allow user to exit
            print("Exiting program...")
            break
      
        ref = db.collection("users").document(user_id)
        user_data = ref.get()
        if user_data.exists:
            print("User Found: ", user_data.to_dict())
            return user_data.to_dict()
        else:
            print("User not found!")    
        
    except Exception as e:
        print(f"error getting user: {e}")

def store_user_data(): #store a user after signing up using uid
    user_id= input("enter user id:")
    name, role, email, password, expertise = sign_up()
    ref = db.reference(f"users: {user_id}")
    ref.set({
        "name": name,
        "role": role,
        "expertise": expertise.split(", "),  # Store expertise as a list
        
    })
    print("User data stored successfully!")


def login():
    try:
        email = input("enail adress:")
        password = input("enter password:")
        #authenticate the user
        user = auth_client.sign_in_with_email_and_password(email, password)
        token = user['idToken']
        print("login successful")

        decoded_token = auth_client.get_account_info(token)
        user_id = decoded_token['users'][0]['localId']

        user_d = db.collection("users").document(user_id).get()
        if user_d.exists:
                user_data = user_d.to_dict()
                print(f' Welcome,')
                return {"user_id": user_id, "role": user_data["role"], "email": user_data["email"]}
        else:
            print('user not found')        
            return None

    except Exception as e:
        print(f' login failed: {e}')
        return None
    



if __name__=="__main__":
    sign_up()
    # get_user_data()
    store_user_data()
    # login()  
      