from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice():
    resp = VoiceResponse()
    gather = Gather(num_digits=1, action="/handle-key", method="POST")
    gather.say("Welcome. Press 1 for Sales. Press 2 for our virtual assistant.")
    resp.append(gather)
    resp.redirect("/voice")
    return Response(str(resp), mimetype="text/xml")

@app.route("/handle-key", methods=["POST"])
def handle_key():
    digit = request.form.get("Digits")
    resp = VoiceResponse()
    
    if digit == "1":
        resp.say("Transferring to Sales.")
        resp.dial("+1234567890")  # Replace with real number
    elif digit == "2":
        resp.say("Connecting to the assistant.")
        resp.redirect("/voicebot")
    else:
        resp.say("Invalid input. Try again.")
        resp.redirect("/voice")

    return Response(str(resp), mimetype="text/xml")

@app.route("/voicebot", methods=["POST"])
def voicebot():
    resp = VoiceResponse()
    resp.say("Hi. I am your assistant. Please speak after the beep.")
    resp.record(timeout=3, transcribe=True, max_length=10, action="/process")
    return Response(str(resp), mimetype="text/xml")

@app.route("/process", methods=["POST"])
def process():
    transcript = request.form.get("TranscriptionText", "")
    print("User said:", transcript)
    reply = "You said: " + transcript
    resp = VoiceResponse()
    resp.say(reply)
    resp.hangup()
    return Response(str(resp), mimetype="text/xml")

@app.route("/")
def home():
    return "Voicebot is running!"

if __name__ == "__main__":
    app.run(debug=True)