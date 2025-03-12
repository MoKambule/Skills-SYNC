from my_script import db

# def get_mentor():
#     mentor_ref = db.collection("users").stream()

#     for user in mentor_ref:
#         mentor_data = user.to_dict()
#         if mentor_data.get("role") == "mentor":
#             print(mentor_data)
#             return mentor_data
        
#     print('No available mentors')   

def get_available_mentors():
    mentors_ref = db.collection("users").where("role", "==", "mentor").stream()

    mentors = []
    for mentor in mentors_ref:
        mentor_data = mentor.to_dict()
        mentors.append({
            "id": mentor.id,
            "name": mentor_data.get("name", "Unknown"),
            "expertise": mentor_data.get("expertise", []),
            "availability": mentor_data.get("availability", [])
        })

    return mentors  # Return instead of print

if __name__=="__main__":
     get_available_mentors()
    # get_mentor() 
       
