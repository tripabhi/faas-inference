from flask import Flask, request
from gevent.pywsgi import WSGIServer
from src.sched.scheduler import InferenceScheduler
#from src.sched.scheduler_process import InferenceScheduler
from src.parser.requestparser import RequestParser
from src.inference.inference import infer

app = Flask(__name__)
scheduler = InferenceScheduler()
parser = RequestParser()

@app.route("/")
def welcome():
    return "<h1>Welcome to zerocopy experiments!</h2>"

def inference(data):
    return infer(data)

@app.route("/serve", methods=["POST"])
def serve():
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        __r_json = request.json
        #_model_id, _data = parser.parse_inference_request(__r_json)
        _data = __r_json["data"]
        __fut = scheduler.submit(inference, _data)
        return {'labels' : __fut.result()}
    else:
        return "Content-Type not supported!"


if __name__ == "__main__":
    try:
        #app.run(host="0.0.0.0", debug=True, port=5000)
        http_server = WSGIServer(('0.0.0.0', 5000), app)
        http_server.serve_forever()
    except Exception as e:
        print("Exception occurred : ", e)
    finally:
        print("Shutting down Scheduler")
        scheduler.shutdown()