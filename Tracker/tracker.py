from flask import Flask
from flask import request

from utils.coding import pack_k

app = Flask(__name__)
PORTS = [8000, 9000, 10000]
mixers = set([f"127.0.0.1:{port}" for port in PORTS])


# mixers = set()  # TODO перевести на List и убедиться что повторений нет.


@app.route("/get-mixers", methods=['GET'])
def get_mixers():
    print("Get mixers")
    print(mixers)
    return {"servers": list(mixers)}, 200


@app.route("/register", methods=['GET'])
def register():
    a = request.environ['REMOTE_ADDR']
    p = request.environ['REMOTE_PORT']
    # print(a, p)
    # print("DATA", request.json)
    mixer_port = request.json["port"]
    mixers.add(f"{request.remote_addr}:{mixer_port}")
    print("MIXERS:", mixers)
    return "OK", 200


if __name__ == '__main__':
    app.run(debug=True)
