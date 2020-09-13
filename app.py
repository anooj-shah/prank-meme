from twilio.rest import Client
import os
import pymongo
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request, redirect

app = Flask(__name__)

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)


@app.route('/')
def main():
    return 'Message Forwarding System'

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    number = request.values.get('From', None)
    body = request.values.get('Body', None)
    print(body)
    # Start our TwiML response
    resp = MessagingResponse()
    if body is None:
        resp.message("Invalid: Enter your name, class, and session# separated by spaces as shown (one student at a time). Examples:\nAvi Patel grade1 session1\nRavi Rao PreK session1\nMira Singh KG session2")
        return str(resp)
    body = body.lower()
    body = body.strip()
    body_arr = body.split()
    class_name = ""
    name = ""
    if len(body_arr) == 4:
        first_name = body_arr[0]
        last_name = body_arr[1]
        name = first_name + " " + last_name
        class_name = body_arr[2] + body_arr[3]
    elif len(body_arr) == 6:
        first_name = body_arr[0]
        last_name = body_arr[1]
        name = first_name + " " + last_name
        class_name = body_arr[2] + body_arr[3] + body_arr[4] + body_arr[5]
    else:
        resp.message("Invalid: Enter your name, class, and session# separated by spaces as shown (one student at a time). Examples:\nAvi Patel grade1 session1\nRavi Rao PreK session1\nMira Singh KG session2")
        return str(resp)

    # forward_message(class_name, number, name)

    return str(resp)
    
# def forward_message(class_name, number, name):
#         message = client.messages.create(body=message_body, from_='+15122014739', to=i[1])
#         print(message.sid)

if __name__ == '__main__':
    app.run()