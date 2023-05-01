from flask import Flask, request
from src.sched.scheduler import InferenceScheduler
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
        app.run(debug=True, port=5000)
    except Exception as e:
        print("Exception occurred : ", e)
    finally:
        print("Shutting down Scheduler")
        scheduler.shutdown()