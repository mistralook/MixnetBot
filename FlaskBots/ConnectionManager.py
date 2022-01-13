import datetime
import time
from threading import Thread
import sys

sys.path.append('../')
import requests

from FlaskBots.Network import get_all_servers
from utils.coding import unpack_pub_k


class ConnectionManager:
    def __init__(self):
        self.connections = {}
        for server in get_all_servers():
            self.connections[server] = ConnectionInfo(datetime.datetime(1980, 1, 1), None)

    def start(self):
        thread = Thread(target=self.background_updater, daemon=True)
        thread.start()
        return self

    def background_updater(self):
        while True:
            for mixer in get_all_servers():
                try:
                    response = requests.get(f"{mixer}/public-key")
                    pub_k = unpack_pub_k(response.json()['public_key'])
                    self.connections[mixer] = ConnectionInfo(last_online_dt=datetime.datetime.now(),
                                                             pub_k=pub_k)
                    time.sleep(1)
                except requests.exceptions.RequestException:
                    pass  # TODO log

    def get_online_servers(self):
        res = [s for s, server_info in self.connections.items() if server_info.is_online()]
        if not res:
            raise Exception(f"{self.connections.items()}")
        return res

    def get_server_pub_k(self, server):
        server_info = self.connections[server]
        if server_info.is_online():
            return server_info.pub_k
        else:
            raise Exception("Attempt to get pub_k of offline server")

    def get_all_servers(self):
        return list(self.connections.keys())


class ConnectionInfo:
    def __init__(self, last_online_dt, pub_k):
        self.last_online_dt = last_online_dt
        self.pub_k = pub_k

    def __str__(self):
        return f"{self.last_online_dt, self.is_online()}"

    def __repr__(self):
        return self.__str__()

    def is_online(self):
        now = datetime.datetime.now()
        delta = now - self.last_online_dt
        return delta.total_seconds() < 5
