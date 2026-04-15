from flask import Flask, render_template, Response
import threading
from proctoring import proctoringAlgo, stop_proctoring, data_record

app = Flask(__name__)

proctor_thread = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start')
def start():
    global proctor_thread
    try:
        if proctor_thread is None or not proctor_thread.is_alive():
            proctor_thread = threading.Thread(target=proctoringAlgo)
            proctor_thread.start()
            return "Proctoring Started"
        else:
            return "Proctoring already running"
    except Exception as e:
        import traceback
        return traceback.format_exc(), 500

@app.route('/stop')
def stop():
    stop_proctoring()
    return "Proctoring Stopped"

@app.route('/logs')
def logs():
    return "<br>".join([str(i) for i in data_record])

if __name__ == '__main__':
    app.run(debug=True)
