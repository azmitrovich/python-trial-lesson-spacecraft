# @title 🚀 Launch the Space Runner server
from flask import Flask, render_template
import threading
from google.colab import output

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

def run_app():
    app.run(host="0.0.0.0", port=5008, use_reloader=False, threaded=True)

threading.Thread(target=run_app, daemon=True).start()

output.serve_kernel_port_as_iframe(5008)