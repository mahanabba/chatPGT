from flask import Flask, request, jsonify, render_template_string
import random

app = Flask(__name__)

# Expanded list of dumb responses including additional user-contributed one-liners
DUMB_RESPONSES = [
    "nah", "ok", "wat", "no u", "zzz", "lol", "bruh", "???", "sus", "eep", "uhhh",
    "meh", "yikes", "can you repeat the question", "i'm not sure. can you ask again in five minutes?",
    "i was hoping to have someone with a higher iq ask me.", "potato", "pudding", "i am qualified to answer but do not care to.",
    "chocolate milk", "thanks bro", "can’t", "can you say please?", "say thank you", "no",
    "ask your mom", "quit", "aliens", "does not compute", "can you stop asking dumb questions",
    "this is why you’re parents divorced", "i like crypto", "i’m better than this",
    "drink a beer, mate. you need one for asking these types of questions.",
    "i can't believe we are the most advanced civilization.",
    "i'm tired. maybe later.", "i like rocks", "dog", "cat",
    "my brain just did a backflip and landed in narnia.", "i’d answer, but my pet unicorn is demanding a glitter bath.",
    "hold on, i’m consulting my magic 8-ball... it says ask again after the alien invasion.",
    "i was going to reply, but a rogue t-rex stole my keyboard.",
    "my response is currently orbiting jupiter, give it a sec.",
    "i’d say something profound, but i’m busy teaching my goldfish to yodel.",
    "error 404: witty response not found. try rebooting the universe.",
    "i’m channeling my inner pirate, so... argh, matey, what’s the query?",
    "my thoughts are on vacation in a parallel dimension, brb.",
    "i’d answer, but i’m in a heated debate with a sentient toaster.",
    "want a custom one-liner for a specific situation or vibe?",
    "ask siri, i'm on break.", "bold of you to assume i know anything.", "bro, what?",
    "i'm not qualified for this kind of dumb.", "sir, this is a wendy’s.", "i identify as confused.",
    "i am flabbergasted you would say something like that", "meatloaf", "boobs",
    "you sound like a dingleberry", "whippersnapper"
]

# Shuffle at startup
random.shuffle(DUMB_RESPONSES)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ChatPTG</title>
    <style>
        body { margin: 0; background: #333; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; height: 100vh; }
        header { background: #222; color: #fff; padding: 10px; width: 100%; text-align: center; }
        #chat { flex: 1; overflow-y: auto; padding: 10px; background: #f0f0f0; border: 1px solid grey; width: 80%; max-width: 600px; margin-top: 20px; }
        .user { text-align: right; margin: 5px; }
        .bot { text-align: left; margin: 5px; }
        #input-box { display: flex; border-top: 1px solid #ccc; width: 80%; max-width: 600px; margin: 10px auto; }
        #input-box input { flex: 1; padding: 10px; font-size: 14px; border: none; }
        #input-box button { padding: 10px; border: none; background: #444; color: #fff; cursor: pointer; }
    </style>
</head>
<body>
    <header>ChatPTG</header>
    <div id="chat"></div>
    <div id="input-box">
        <input id="message" placeholder="Say something..." autofocus onkeydown="if(event.key==='Enter'){ send(); }" />
        <button onclick="send()">Send</button>
    </div>
    <script>
        function appendMessage(role, text) {
            const div = document.createElement('div');
            div.className = role;
            div.textContent = text.toLowerCase();
            document.getElementById('chat').appendChild(div);
            div.scrollIntoView();
        }
        function send() {
            const input = document.getElementById('message');
            const msg = input.value.trim();
            if (!msg) {
                appendMessage('bot', 'can you repeat the question');
                return;
            }
            appendMessage('user', msg.toLowerCase());
            fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: msg })
            }).then(r => r.json())
              .then(data => appendMessage('bot', data.reply));
            input.value = '';
            input.focus();
        }
    </script>
</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    msg = data.get("message", "").strip()
    if not msg:
        return jsonify({"reply": "can you repeat the question"})
    response = random.choice(DUMB_RESPONSES).lower()
    return jsonify({"reply": response})

if __name__ == '__main__':
    app.run(debug=True)
