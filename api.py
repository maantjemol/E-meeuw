
from database import * 
from mail_lib import * 

def handleLogin(request):
    request_data = json.loads(request.body)
    
    session = getSession(email=request_data["username"], password=request_data["password"])
    
    resp = {
        "error": "Username or password not correct",
        "success": False
    }

    if session:
        resp = {
            "cookie": session,
            "success": True
        }

    return resp

def handleSendMail(request):
    request_data = json.loads(request.body)
    user_data = getUser(request_data["uid"])

    if not user_data:
        return {"success": False, "error": "uid not found"}
    
    from_email = user_data["email"]

    to_email = request_data["to_email"]
    subject = request_data["subject"]
    uid = request_data["uid"]
    contents = request_data["contents"]

    addSendEmail(
        from_email = from_email,
        to_email = to_email,
        subject = subject,
        uid = uid,
        contents = contents,
    )
    # session = getSession(email=request_data["username"], password=request_data["password"])
    server_address = to_email.split("@")[-1]
    port = 25

    if("e-meeuw.de" in server_address):
        server_address = "localhost"
        port = 1114

    status = sendEmail(
        mail_from = from_email, 
        mail_to = to_email, 
        message = contents, 
        server_address = server_address, 
        subject=subject,
        port=port
    )

    if status["success"] == False:
        return status

    resp = {
        "success": True
    }

    return resp

def handleGetMail(request):
    request_data = json.loads(request.body)

    if not request_data["uid"]:
        return {"success": False, "error": "no UID"}

    emails = getMail(request_data["uid"])

    resp = {
        "success": True,
        "emails": emails
    }

    return resp

def handleGetSendMail(request):
    request_data = json.loads(request.body)

    if not request_data["uid"]:
        return {"success": False, "error": "no UID"}

    emails = getSendMail(request_data["uid"])

    resp = {
        "success": True,
        "emails": emails
    }

    return resp