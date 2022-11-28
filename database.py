import json
import uuid

def addUser(email:str, password:str):
    user = {
        "id": str(uuid.uuid4()),
        "email": email,
        "password": password
    }
    with open("./database/database.json", "r") as f:
        fileCont = f.read()
    
    database = json.loads(fileCont)
    database["users"].append(user)
    json_database = json.dumps(database)
    
    with open("./database/database.json", "w") as f:
        f.write(json_database)


def getUser(id:str):
    """Gets User

    Args:
        id (uid): A uid: b3d19da8-c681-47da-8736-25cbb97f3512

    Returns:
        {
            "id": "b3d19da8-c681-47da-8736-25cbb97f3512",
            "email": "maan@e-meeuw.de",
            "password": "lolpower"
        }
    """
    with open("./database/database.json", "r") as f:
        fileCont = f.read()
    database = json.loads(fileCont)

    for user in database["users"]:
        if user["id"] == id:
            return user
    
    return None


def getSession(email:str, password:str):
    with open("./database/database.json", "r") as f:
        fileCont = f.read()
    database = json.loads(fileCont)

    for user in database["users"]:
        if user["email"] == email:
            if user["password"] == password:
                return user["id"]
    
    return None


def addRecievedEmail(from_email:str, uid:str, to_email:str, subject:str, contents:str):
    email = {
        "from_email": from_email,
        "uid": uid,
        "to_email": to_email,
        "subject": subject,
        "contents": contents
    }

    with open("./database/database.json", "r") as f:
        fileCont = f.read()
    
    database = json.loads(fileCont)
    database["recieved_emails"].append(email)
    json_database = json.dumps(database)
    
    with open("./database/database.json", "w") as f:
        f.write(json_database)


def addSendEmail(from_email:str, uid:str, to_email:str, subject:str, contents:str):
    email = {
        "from_email": from_email,
        "uid": uid,
        "to_email": to_email,
        "subject": subject,
        "contents": contents
    }

    with open("./database/database.json", "r") as f:
        fileCont = f.read()
    
    database = json.loads(fileCont)
    database["send_emails"].append(email)
    json_database = json.dumps(database)
    
    with open("./database/database.json", "w") as f:
        f.write(json_database)


def getMail(id:str):
    all_mails = []

    with open("./database/database.json", "r") as f:
        fileCont = f.read()
    database = json.loads(fileCont)

    for email in database["recieved_emails"]:
        if email["uid"] == id:
            all_mails.append(email)
    
    return all_mails

def getSendMail(id:str):
    all_mails = []

    with open("./database/database.json", "r") as f:
        fileCont = f.read()
    database = json.loads(fileCont)

    for email in database["send_emails"]:
        if email["uid"] == id:
            all_mails.append(email)
    
    return all_mails

if __name__ == "__main__":
    print(getSendMail("b3d19da8-c681-47da-8736-25cbb97f3512"))