from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from enum import Enum, auto
import json

clients = []
scheduleList = []


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


class Simulator(WebSocket):
    def handleMessage(self):
        print(self.address, 'sent', self.data)
        j = json.loads(self.data)
        rqtType = j['type'] + 1
        data = j['data']
        dataDict = {}

        if DataType(rqtType) == DataType.DATA_SCHEDULE_ADD:
            if 'enabled' not in data.keys():
                data['enabled'] = True
            if 'id' not in data.keys():
                data['id'] = len(scheduleList)
            if 'ratio' not in data.keys():
                data['ratio'] = 0

            dataDict = {
                'type': j['type'],
                'data': {
                    'hour': data['hour'],
                    'minute': data['minute'],
                    'enabled': data['enabled'],
                    'id': data['id'],
                    'ratio': data['ratio']
                }
            }

            scheduleList.append({'hour': data['hour'], 'minute': data['minute'], 'enabled': data['enabled'], 'ratio': data['ratio']})
        elif DataType(rqtType) == DataType.DATA_SCHEDULE_REMOVE:
            if data['id'] <= len(scheduleList):
                del scheduleList[data['id']]

            dataDict = j
        elif DataType(rqtType) == DataType.DATA_SCHEDULE_ENABLE:
            if data['id'] <= len(scheduleList):
                scheduleList[data['id']]['enabled'] = data['value']

                dataDict = j

        sendData = json.dumps(dataDict)

        print('replying', sendData)
        for client in clients:
                client.sendMessage(sendData)

    def handleConnected(self):
        print(self.address, 'connected')
        clients.append(self)

    def handleClose(self):
        clients.remove(self)
        print(self.address, 'closed')


server = SimpleWebSocketServer('', 8000, Simulator)
server.serveforever()