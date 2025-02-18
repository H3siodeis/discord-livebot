from flask import Flask
from threading import Thread

app = Flask(__name__)


@app.route('/')
def home():
    return "Le bot est en ligne !"


def run():
    app.run(host="0.0.0.0", port=8080, threaded=True)


def keep_alive():
    thread = Thread(target=run, daemon=True)  # Utilisation d'un thread daemon
    thread.start()
