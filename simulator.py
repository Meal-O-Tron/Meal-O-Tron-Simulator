from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from enum import Enum, auto
import json

clients = []


class DataType(Enum):
    DATA_SCHEDULE_START = auto()
    DATA_SCHEDULE_ADD = auto()
    DATA_SCHEDULE_REMOVE = auto()
    DATA_SCHEDULE_ENABLE = auto()
    DATA_SCHEDULE_DATE = auto()
    DATA_SCHEDULE_RATIO = auto()
    DATA_SCHEDULE_END = auto()

    DATA_DOG_START = auto()
    DATA_DOG_NAME = auto()
    DATA_DOG_WEIGHT = auto()
    DATA_DOG_REGULATION_ENABLE = auto()
    DATA_DOG_REGULATION_VALUE = auto()
    DATA_DOG_END = auto()


class SimpleChat(WebSocket):
    def handleMessage(self):
        print(self.address, 'sent', self.data)
        j = json.loads(self.data)
        type = j['type'] + 1
        data = ''

        if DataType(type) == DataType.DATA_SCHEDULE_ADD:
            if j['data']['enabled'] is None:
                j['data']['enabled'] = True
            if j['data']['id'] is None:
                j['data']['id'] = 0
            if j['data']['ratio'] is None:
                j['data']['ratio'] = 0

            dataDict = {
                'type': j['type'],
                'data': {
                    'hour': j['data']['hour'],
                    'minute': j['data']['minute'],
                    'enabled': j['data']['enabled'],
                    'id': j['data']['id'],
                    'ratio': j['data']['ratio']
                }
            }

            data = json.dumps(dataDict)

        print('replying', data)
        for client in clients:
                client.sendMessage(data)

    def handleConnected(self):
        print(self.address, 'connected')
        clients.append(self)

    def handleClose(self):
        clients.remove(self)
        print(self.address, 'closed')


server = SimpleWebSocketServer('', 8000, SimpleChat)
server.serveforever()