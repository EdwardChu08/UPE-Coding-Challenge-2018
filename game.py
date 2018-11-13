'''
Game.py

'''
import requests, json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

STATUS = {
    'PLAYING':      'PLAYING',
    'GAME_OVER':    'GAME_OVER',
    'NONE':         'NONE',
    'FINISHED':     'FINISHED'
}

ACTION = {
    'DOWN':   'DOWN',
    'RIGHT':  'RIGHT',
    'LEFT':   'LEFT',
    'UP':     'UP'
}

RESULT = {
    'WALL':           'WALL',
    'SUCCESS':        'SUCCESS',
    'OUT_OF_BOUNDS':  'OUT_OF_BOUNDS',
    'END':            'END'
}

RETRIES = Retry(total=5, backoff_factor=0.3, status_forcelist=[ 429, 502, 503, 504 ])

class Game:
    def __init__(self, server_url, uid):       
        action = '/session'
        data = {'uid': uid}
        session = requests.Session()
        session.mount('http://', HTTPAdapter(max_retries=RETRIES))
        res = session.post(url=server_url+action, data=data).json()
        self.token = res['token']
        self.server_url = server_url

    def get_state(self):
        action = '/game'
        params = {'token': self.token}
        session = requests.Session()
        session.mount('http://', HTTPAdapter(max_retries=RETRIES))
        res = session.get(url=self.server_url+action, params=params)
        return res.json()

    def do_action(self, gameAction):
        action = '/game'
        params = {'token': self.token}
        data = {'action': gameAction}
        session = requests.Session()
        session.mount('http://', HTTPAdapter(max_retries=RETRIES))
        res = session.post(url=self.server_url+action, params=params, data=data)
        return res.json()
