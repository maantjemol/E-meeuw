# importeert een hoop shit
import glob
import json
import re
import socket
import ssl
import threading
from database import *



def getSSLSocket():
    return ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), ssl_version=ssl.PROTOCOL_SSLv23)

def getEmailUid(email:str):
    """Gets the userID by email

    Args:
        email (str): email string

    Returns:
        uid: an userID
    """
    with open("./database/database.json", "r") as f:
        fileCont = f.read()
    database = json.loads(fileCont)

    for user in database["users"]:
        if user["email"] in email:
            return user["id"]
    
    return None

def sendEmail(mail_from:str, mail_to:str, message:str, server_address:str, subject:str, port:int = 26):
    """Sends an email from our mail server to the recipients mail server.

    Args:
        mail_from (str): the from email
        mail_to (str): the recipients email
        message (str): the contentents of the email
        server_address (str): the address of the server
        subject (str): The subject of the email
        port (int, optional): the port of the server. Defaults to 26.

    Returns:
        dict: {success: True/False, "error": "error"}
    """
    try:
        sock = getSSLSocket()
        sock.settimeout(5)
        sock.connect((server_address, port))
        sock.send("HELO".encode())
        response = sock.recv(2048).decode()
        
        if "OK" in response:
            sock.send(f"MAIL FROM: <{mail_from}>".encode())
        else:
            print(f"could not connect to server. error: {response}")
            return {"success": False, "error": "could not connect to server"}
        response = sock.recv(2048).decode()
        
        if "OK" in response:
            sock.send(f"RCPT TO: <{mail_to}>".encode())
        else:
            print(f"could not connect to server. error: {response}")
            return {"success": False, "error": "could not connect to server"}
        response = sock.recv(2048).decode()
        
        if "OK" in response:
            sock.send("DATA\r\n".encode())
        else:
            print(f"could not connect to server. error: {response}")
            return {"success": False, "error": "could not connect to server"}
        response = sock.recv(2048).decode()

        sock.send(f"subject:{subject}\r\n".encode())
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
            return {"success": False, "error": "Could not connect to server"}
        
        response = sock.recv(2048).decode()
        return {"success": True}  
    except Exception as e:
        print("Error in Email server (send):", e)
        return {"success": False, "error": "An error occurred"}


def fprint(s:str):
    """fancy print

    Args:
        s (str): string you want to fancy print
    """
    print(f"> {s}")

def acceptEmail(connstream):
    """function that accepts and handles emails

    Args:
        connstream (socket): the socket of the incomming email connection
    """
    try:
        email = ''

        request = connstream.recv(1024).decode()

        fromEmail = ""
        rcptEmail = ""

        if "HELO" in request:
            connstream.sendall("250 OK".encode())
        else:
            connstream.sendall("450".encode())
            connstream.close()
            return

        request = connstream.recv(1024).decode()
        if "MAIL FROM" in request:
            regex = r"(?<=<).*?(?=>)" # Everything between < >
            fromEmail = re.findall(regex, request)[0]
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
            connstream.sendall("250 OK".encode())
        else:
            connstream.sendall("450".encode())
            connstream.close()
            return
        
        request = connstream.recv(1024).decode()
        if "DATA" in request:
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
        
        print(email)

        
        request = connstream.recv(1024).decode()
        if request == "QUIT":
            connstream.sendall("221 Bye".encode())
            connstream.close()
        
        uid = getEmailUid(rcptEmail)

        if not uid:
            return

        contents = ''.join(str(e) for e in email.split("\r\n")[1:])

        addRecievedEmail(
            from_email=fromEmail,
            to_email=rcptEmail,
            subject=email.split("\r\n")[0].split("subject:")[1],
            contents=contents,
            uid=uid,
        )
    
    except Exception as e:
                print("Error in Email server (recieve):", e)
