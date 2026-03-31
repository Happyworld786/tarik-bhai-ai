import os
import uuid
import random
import time
import json
import re
from flask import Flask, request, jsonify, session, render_template_string

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "tarik-bhai-secret-2024")

# In-memory chat store
chat_sessions = {}

# Emotional responses
EMOTIONAL_RESPONSES = {
    "sad": ["Bhai, main samajh sakta hoon tu dard mein hai. Main yahaan hoon tere saath.", "Tu akela nahi hai bhai. Main yahaan hoon."],
    "fear": ["Dar mat bhai! Main hoon na tere saath.", "Tu strong hai bhai!"],
    "general": ["Haan bhai, main sun raha hoon.", "Accha bata, kya hua? Main yahaan hoon."]
}

def detect_emotion(message):
    msg = message.lower()
    if any(w in msg for w in ["sad", "dukhi", "rona"]):
        return "sad"
    if any(w in msg for w in ["dar", "scared", "fear"]):
        return "fear"
    return "general"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tarik Bhai AI</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:Arial;background:linear-gradient(135deg,#1a1a2e,#16213e);min-height:100vh;padding:20px}
        .container{max-width:600px;margin:0 auto}
        .header{background:linear-gradient(135deg,#e94560,#533483);border-radius:20px;padding:30px;text-align:center;color:white;margin-bottom:20px}
        .logo{font-size:50px;margin-bottom:10px}
        h1{font-size:28px}
        .chat-container{background:rgba(255,255,255,0.1);border-radius:20px;overflow:hidden}
        .messages{height:400px;overflow-y:auto;padding:20px;display:flex;flex-direction:column;gap:10px}
        .message{display:flex}
        .message.user{justify-content:flex-end}
        .message.bot{justify-content:flex-start}
        .bubble{max-width:70%;padding:10px 15px;border-radius:18px;font-size:14px}
        .user .bubble{background:linear-gradient(135deg,#e94560,#533483);color:white}
        .bot .bubble{background:white;color:#1a1a2e}
        .timestamp{font-size:10px;color:rgba(255,255,255,0.6);margin-top:5px}
        .input-area{padding:20px;background:rgba(0,0,0,0.3);display:flex;gap:10px}
        .input-area input{flex:1;padding:12px;border:none;border-radius:25px;outline:none}
        .input-area button{padding:12px 25px;background:linear-gradient(135deg,#e94560,#533483);border:none;border-radius:25px;color:white;cursor:pointer}
        .typing{display:none;padding:10px 20px;color:rgba(255,255,255,0.7);font-size:12px}
        .typing.active{display:block}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🤝</div>
            <h1>TARIK BHAI AI</h1>
            <p>💖 Tera Bhai - Hamesha Tere Saath 💖</p>
        </div>
        <div class="chat-container">
            <div class="messages" id="messages">
                <div class="message bot">
                    <div class="bubble">Assalamu Alaikum bhai! Main Tarik Bhai - tera apna bada bhai.<br>Tu akela nahi hai. Main hoon na tere saath! 💖<div class="timestamp">⚡ Online</div></div>
                </div>
            </div>
            <div class="typing" id="typing">Tarik Bhai soch raha hai...</div>
            <div class="input-area">
                <input type="text" id="messageInput" placeholder="Bhai, kuch bol... main sun raha hoon 💬" onkeypress="if(event.key==='Enter') sendMessage()">
                <button onclick="sendMessage()">Send 💖</button>
            </div>
        </div>
    </div>
    <script>
        let sessionId = "session_" + Date.now();
        function getTime(){return new Date().toLocaleTimeString([],{hour:"2-digit",minute:"2-digit"});}
        function addMessage(text,sender){const m=document.getElementById("messages");const d=document.createElement("div");d.className="message "+sender;d.innerHTML='<div class="bubble">'+text+'<div class="timestamp">'+getTime()+'</div></div>';m.appendChild(d);m.scrollTop=m.scrollHeight;}
        async function sendMessage(){const i=document.getElementById("messageInput");const msg=i.value.trim();if(!msg)return;addMessage(msg,"user");i.value="";document.getElementById("typing").classList.add("active");try{const r=await fetch("/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:msg,session_id:sessionId})});const d=await r.json();document.getElementById("typing").classList.remove("active");addMessage(d.response,"bot");}catch(e){document.getElementById("typing").classList.remove("active");addMessage("Bhai, thoda technical issue hai. Dobara try kar! 💖","bot");}}
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")
    emotion = detect_emotion(message)
    responses = EMOTIONAL_RESPONSES.get(emotion, EMOTIONAL_RESPONSES["general"])
    response = random.choice(responses)
    return jsonify({"response": response})

@app.route("/clear/<session_id>")
def clear(session_id):
    chat_sessions.pop(session_id, None)
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
