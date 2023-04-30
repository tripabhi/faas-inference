from flask import Flask, request
from src.sched.scheduler import InferenceScheduler
from src.parser.requestparser import RequestParser


app = Flask(__name__)
scheduler = InferenceScheduler()
parser = RequestParser()

@app.route("/")
def welcome():
    return "<h1>Welcome to zerocopy experiments!</h2>"

def inference(model, data):
    return f"This is inference job for {model} and the data is {data}"

@app.route("/serve", methods=["POST"])
def serve():
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        __r_json = request.json
        _model_id, _data = parser.parse_inference_request(__r_json)
        __fut = scheduler.submit(inference, _model_id, _data)
        return {'labels' : __fut.result()}
    else:
        return "Content-Type not supported!"


if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as e:
        print("Exception occurred : ", e)
    finally:
        print("Shutting down Scheduler")
        scheduler.shutdown()