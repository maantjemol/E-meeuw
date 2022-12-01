import json
import uuid

def addUser(email:str, password:str):
    """Adds a user to the database and generates a unique UserID for them

    Args:
        email (str): The email of the new user
        password (str): The password of the new user
    """
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
            "password": "asjdkflaslkdf"
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
    """Gets the userID from an username and password

    Args:
        email (str): The username you're trying to find
        password (str): The password you're trying to find

    Returns:
        (str / None): Returns the userID or nothing if it isn't found
    """
    with open("./database/database.json", "r") as f:
        fileCont = f.read()
    database = json.loads(fileCont)

    for user in database["users"]:
        if user["email"] == email:
            if user["password"] == password:
                return user["id"]
    
    return None


def addRecievedEmail(from_email:str, uid:str, to_email:str, subject:str, contents:str):
    """Adds a recieved email to the database

    Args:
        from_email (str): The emailaddress the email came from
        uid (str): The userID of the user
        to_email (str): The emailaddress the email was for
        subject (str): The subject of the email
        contents (str): The contents of the email
    """
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
    """Adds a send email to the database

    Args:
        from_email (str): The emailaddress the email came from
        uid (str): The userID of the user
        to_email (str): The emailaddress the email was for
        subject (str): The subject of the email
        contents (str): The contents of the email
    """
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
    """Gets all emails recieved by an user

    Args:
        id (str): userID

    Returns:
        list: list of emails
    """
    all_mails = []

    with open("./database/database.json", "r") as f:
        fileCont = f.read()
    database = json.loads(fileCont)

    for email in database["recieved_emails"]:
        if email["uid"] == id:
            all_mails.append(email)
    
    return all_mails


def getSendMail(id:str):
    """Gets all emails send by an user

    Args:
        id (str): userID

    Returns:
        list: list of emails
    """
    all_mails = []

    with open("./database/database.json", "r") as f:
        fileCont = f.read()
    database = json.loads(fileCont)

    for email in database["send_emails"]:
        if email["uid"] == id:
            all_mails.append(email)
    
    return all_mails
