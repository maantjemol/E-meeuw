# importeert een hoop shit
import glob
import re
import socket
import ssl
import threading
import json

def getSSLSocket():
    return ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), ssl_version=ssl.PROTOCOL_SSLv23)

def getEmailUid(email:str):
    with open("./database/database.json", "r") as f:
        fileCont = f.read()
    database = json.loads(fileCont)

    for user in database["users"]:
        if user["email"] in email:
            return user["id"]
    
    return None

def sendEmail(mail_from:str, mail_to:str, message:str, server_address:str, subject:str, port:int = 25):
    print("Yessss")
    sock = getSSLSocket()
    sock.connect((server_address, port))
    sock.send("HELO".encode())
    response = sock.recv(2048).decode()
    print(response)
    
    if "OK" in response:
        sock.send(f"MAIL FROM: <{mail_from}>".encode())
    else:
        print(f"could not connect to server. error: {response}")
        return
    response = sock.recv(2048).decode()
    print(response)
    
    if "OK" in response:
        sock.send(f"RCPT TO: <{mail_to}>".encode())
    else:
        print(f"could not connect to server. error: {response}")
        return
    response = sock.recv(2048).decode()
    print(response)
    
    if "OK" in response:
        sock.send("DATA\r\n".encode())
    else:
        print(f"could not connect to server. error: {response}")
        return
    response = sock.recv(2048).decode()

    sock.send(f"{message}\r\n".encode())

    response = sock.recv(2048).decode()

    fullStop = '\r\n.\r\n'
    sock.send(fullStop.encode('utf-8'))

    response = sock.recv(2048).decode()

    if "250" in response:
        sock.send("QUIT".encode())
    else:
        print(f"could not connect to server. error: {response}")
        return
    
    response = sock.recv(2048).decode()


def fprint(s:str):
    print(f"> {s}")

def acceptEmail(connstream):
    
    email = ''

    print("got connection!")

    request = connstream.recv(1024).decode()

    fromEmail = ""
    rcptEmail = ""

    if "HELO" in request:
        fprint(request)
        connstream.sendall("250 OK".encode())
    else:
        connstream.sendall("450".encode())
        connstream.close()
        return

    request = connstream.recv(1024).decode()
    if "MAIL FROM" in request:
        regex = r"(?<=<).*?(?=>)" # Everything between < >
        fromEmail = re.findall(regex, request)[0]
        fprint(request)
        print(fromEmail)
        connstream.sendall("250 OK".encode())
    else:
        connstream.sendall("450".encode())
        connstream.close()
        return

    request = connstream.recv(1024).decode()
    if "RCPT TO" in request:
        regex = r"(?<=<).*?(?=>)" # Everything between < >
        rcptEmail = re.findall(regex, request)[0]

        if not getEmailUid(rcptEmail):
            connstream.sendall("450".encode())
            print(rcptEmail, "doesn't exists in database")
            connstream.close()
            return

        fprint(request)
        print(rcptEmail)
        connstream.sendall("250 OK".encode())
    else:
        connstream.sendall("450".encode())
        connstream.close()
        return
    
    request = connstream.recv(1024).decode()
    if "DATA" in request:
        fprint(request)
        connstream.sendall("354 End data with <CR><LF>.<CR><LF>".encode())
    else:
        connstream.sendall("450".encode())
        connstream.close()
        return
    
    while True:
        request = connstream.recv(1024).decode()
        if '\r\n.\r\n' in request:
            connstream.sendall("250 OK: queued as 12345".encode())
            break
        else:
            connstream.sendall("250 OK".encode())
            email += request
    
    request = connstream.recv(1024).decode()
    if request == "QUIT":
        connstream.sendall("221 Bye".encode())
        connstream.close()
    
    uid = getEmailUid(rcptEmail)

    if not uid:
        return

    addRecievedEmail(
        from_email=fromEmail,
        to_email=rcptEmail,
        subject="none",
        contents=email,
        uid=uid,
    )


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