

class RequestParser():
    
    def parse_inference_request(self, _json):
        model = _json["model"]
        data = _json["data"]
        return model, data