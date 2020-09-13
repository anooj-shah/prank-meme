from twilio.rest import Client
import os
import pymongo
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request, redirect
from twilio.twiml.voice_response import Play, VoiceResponse
from flask_cors import CORS, cross_origin
import random

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

@app.route('/', methods=['GET'])
def main():
    return {
        "api_stuff": "success",
    }

@app.route('/image', methods=['GET', 'POST'])
@cross_origin()
def image():
    images = ["https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSZCdzyXGUg2Gbcdc3fujKiLchsBxFVGpvNNA&usqp=CAU", "https://static.wikia.nocookie.net/arresteddevelopment/images/d/d1/2017_Lego_Batman_Premiere_-_Michael_Cera_01.jpg/revision/latest/top-crop/width/360/height/450?cb=20170624164358"]
    random_number = random.randint(0,1)
    content = request.json
    phone = content["phone"]
    message = client.messages.create(
        body='',
        from_='+15122014739',
        media_url=[images[random_number]],
        to='+1' + phone
    )

    print(message.sid)
    return str(message.sid)

@app.route("/call", methods=['GET', 'POST'])
@cross_origin()
def outgoing_call():
    """Send a dynamic phone call"""
    content = request.json
    type_of_message = content["type"]
    # phone_number = request.data.phone
    # mp3_url="http://prank-meme.herokuapp.com/answer"

    if type_of_message == "johncena":
        call = client.calls.create (
            to="+1" + content["phone"],
            from_="+15122014739",
            url="http://prank-meme.herokuapp.com/johncena"
        )
    elif type_of_message == "howuare":
        call = client.calls.create(
            to="+1" + content["phone"],
            from_="+15122014739",
            url="http://prank-meme.herokuapp.com/askyouhowyouare"
        )
    elif type_of_message == "road":
        call = client.calls.create(
            to="+1" + content["phone"],
            from_="+15122014739",
            url="http://prank-meme.herokuapp.com/road"
        )
    elif type_of_message == "car":
        call = client.calls.create(
            to="+1" + content["phone"],
            from_="+15122014739",
            url="http://prank-meme.herokuapp.com/car"
        )
    print(call.sid)
    return str(call.sid)
    
@app.route("/askyouhowyouare", methods=['GET', 'POST'])
def askyouhowyouare():
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiML response
    response = VoiceResponse()
    response.play('https://youcustomizeit.s3.us-east-2.amazonaws.com/how-are-you-meme.mp3')
    # Read a message aloud to the caller
    # response.say("Thank you for calling! Have a great day.")

    return str(response)

@app.route("/johncena", methods=['GET', 'POST'])
def johncena():
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiML response
    response = VoiceResponse()
    response.play('https://youcustomizeit.s3.us-east-2.amazonaws.com/John+Cena+Meme+Original+Remastered+HD.mp3')
    # Read a message aloud to the caller
    # response.say("Thank you for calling! Have a great day.")

    return str(response)

@app.route("/road", methods=['GET', 'POST'])
def road():
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiML response
    response = VoiceResponse()
    response.play('https://youcustomizeit.s3.us-east-2.amazonaws.com/road.mp3')
    # Read a message aloud to the caller
    # response.say("Thank you for calling! Have a great day.")

    return str(response)

@app.route("/car", methods=['GET', 'POST'])
def car():
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiML response
    response = VoiceResponse()
    response.play('https://youcustomizeit.s3.us-east-2.amazonaws.com/car.mp3')
    # Read a message aloud to the caller
    # response.say("Thank you for calling! Have a great day.")

    return str(response)
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