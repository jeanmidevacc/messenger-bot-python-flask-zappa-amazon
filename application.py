import requests
from flask import Flask, request
import json
import time


# Variables to
app = Flask(__name__)
# Token of the bot
access_token=""
verify_token=""

# Quick replies example
replies = [
    {
        "content_type": "text",
        "title": "1",
        "payload": "CHOICE1",
    },
    {
        "content_type": "text",
        "title": "2",
        "payload": "CHOICE2",
    },
    {
        "content_type": "text",
        "title": "3",
        "payload": "CHOICE3",
    },
]

def log(message):
    """
    Function to log message in the console

    :param message:
    """
    try:
        print(message)
    except Exception as e:
        print("ERROR:"+str(e))


def send_typing(recipient_id,action):
    """
    Function to send one of the three types of elements link to the typing

    :param recipient_id:
    :param action:
    :return:
    """
    params = {
        "access_token": access_token
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "sender_action":action
    })

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def send_message(recipient_id, message_text):
    """
    Function to send message_text to recipient_id

    :param recipient_id:
    :param message_text:
    :return:
    """
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    timer3dot(recipient_id,2)
    params = {
        "access_token": access_token
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    send_typing(recipient_id,"TYPING_OFF")
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_quickreply(recipient_id,text,replies):
    """
    Function to send quick reply commands to recipient_id

    :param recipient_id:
    :param text:
    :param replies:
    :return:
    """
    timer3dot(recipient_id,2)
    params = {
        "access_token": access_token
    }
    headers = {
        "Content-Type": "application/json"
    }


    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": text,
            "metadata":"test",
            "quick_replies":replies
        }
    })
    send_typing(recipient_id,"TYPING_OFF")
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def timer3dot(recipient_id,timer=1):
    """
    Function to send the Mark seen marker and the 3 dots during timer seconds

    :param recipient_id:
    :param timer:
    :return:
    """
    send_typing(recipient_id,"MARK_SEEN")
    send_typing(recipient_id, "TYPING_ON")
    time.sleep(timer)

def talkuser(messaging_event):
    """
    Function to manage the result of the webhook

    :param messaging_event:
    :return:
    """

    if "message" in messaging_event and "quick_reply" in messaging_event["message"]:#In the case that the user has clikc on a quick reply button
        recipient_id = messaging_event["sender"]["id"]
        text=messaging_event["message"]["quick_reply"]["payload"]
        send_message(recipient_id,text)

    elif "message" in messaging_event and "text" in messaging_event["message"]:#In the case that the user send a message
        recipient_id = messaging_event["sender"]["id"]
        text = messaging_event["message"]["text"]
        if text=="qr":#If the message is qr , send quick replies
            send_quickreply(recipient_id,"Quick replies",replies)
        else:
            send_message(recipient_id,text)
    else:
        text = "Hummm i don't understand, click on the followings links to know more about Jean-Michel."
        recipient_id = messaging_event["sender"]["id"]  # the recipient's ID, which should be your page's facebook ID
        send_message(recipient_id,text)



"""
Application request
"""

#To check if the application is on
@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == verify_token:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


# To collect the webhooks
@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                log(messaging_event)
                if messaging_event.get("message") :  # someone sent us a message
                   talkuser(messaging_event)
    return "ok", 200

#Flask application
if __name__ == '__main__':
    app.run(debug=True)
