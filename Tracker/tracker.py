from flask import Flask
from flask import request

from utils.coding import pack_k

app = Flask(__name__)


@app.route("/get-mixers", methods=['GET'])
def get_public_key():
    PORTS = [8000, 9000, 10000]
    return {"servers": [f"http://127.0.0.1:{port}" for port in PORTS]}, 200


if __name__ == '__main__':
    app.run(debug=True)
