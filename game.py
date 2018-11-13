'''
Game.py

'''
import requests, json

STATUS = {
    'PLAYING':      'PLAYING',
    'GAME_OVER':    'GAME_OVER',
    'NONE':         'NONE',
    'FINISHED':     'FINISHED'
}

ACTION = {
    'UP':     'UP',
    'DOWN':   'DOWN',
    'LEFT':   'LEFT',
    'RIGHT':  'RIGHT'
}

RESULT = {
    'WALL':           'WALL',
    'SUCCESS':        'SUCCESS',
    'OUT_OF_BOUNDS':  'OUT_OF_BOUNDS',
    'END':            'END'
}

class Game:
    def __init__(self, server_url, uid):       
        action = '/session'
        data = {'uid': uid}
        res = requests.post(url=server_url+action, data=data).json()
        self.token = res['token']
        self.server_url = server_url

    def get_state(self):
        action = '/game'
        params = {'token': self.token}
        res = requests.get(url=self.server_url+action, params=params).json()
        return res

    def do_action(self, gameAction):
        action = '/game'
        params = {'token': self.token}
        data = {'action': gameAction}
        res = requests.post(url=self.server_url+action, params=params, data=data).json()
        return res
