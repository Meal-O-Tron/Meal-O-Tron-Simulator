from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from enum import Enum, auto
import json
import os
import random

clients = []
scheduleList = []
dogData = {}
food_array = []
arrival_array = []
weight_array = []


class DataType(Enum):
    DATA_GLOBAL_RELOAD = auto()

    DATA_STATS_START = auto()
    DATA_STATS_WEIGHT = auto()
    DATA_STATS_REMAINING_FOOD = auto()
    DATA_STATS_DOG_ARRIVAL = auto()
    DATA_STATS_END = auto()

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
        rqt_type = j['type'] + 1
        data = j['data']
        data_dict = j

        if DataType(rqt_type) == DataType.DATA_SCHEDULE_ADD:
            if 'enabled' not in data.keys():
                data['enabled'] = True
            if 'id' not in data.keys():
                data['id'] = len(scheduleList)
            if 'ratio' not in data.keys():
                data['ratio'] = 0

            data_dict = {
                'type': j['type'],
                'data': {
                    'hour': data['hour'],
                    'minute': data['minute'],
                    'enabled': data['enabled'],
                    'id': data['id'],
                    'ratio': data['ratio']
                }
            }

            scheduleList.append({'hour': data['hour'], 'minute': data['minute'], 'enabled': data['enabled'],
                                 'ratio': data['ratio']})
        elif DataType(rqt_type) == DataType.DATA_SCHEDULE_REMOVE:
            if data['id'] <= len(scheduleList):
                del scheduleList[data['id']]
        elif DataType(rqt_type) == DataType.DATA_SCHEDULE_ENABLE:
            if data['id'] <= len(scheduleList):
                scheduleList[data['id']]['enabled'] = data['value']
        elif DataType(rqt_type) == DataType.DATA_SCHEDULE_DATE:
            if data['id'] <= len(scheduleList):
                current_item = scheduleList[data['id']]
                current_item['hour'] = data['value']['hour']
                current_item['minute'] = data['value']['minute']
        elif DataType(rqt_type) == DataType.DATA_SCHEDULE_RATIO:
            if data['id'] <= len(scheduleList):
                current_item = scheduleList[data['id']]
                current_item['ratio'] = data['value']
        elif DataType(rqt_type) == DataType.DATA_DOG_NAME:
            dogData['name'] = data['value']
        elif DataType(rqt_type) == DataType.DATA_DOG_REGULATION_ENABLE:
            dogData['weight_reg'] = data['value']
        elif DataType(rqt_type) == DataType.DATA_DOG_REGULATION_VALUE:
            dogData['weight_reg_value'] = data['value']
        elif DataType(rqt_type) == DataType.DATA_DOG_WEIGHT:
            new_weight = random.randint(1, 60)

            dogData['weight'] = new_weight
            data_dict['data']['value'] = new_weight
        elif DataType(rqt_type) == DataType.DATA_STATS_WEIGHT:
            weight_array.clear()
            for i in range(random.randint(1, 30)):
                weight_array.append(random.randint(30, 40))

            data_dict['data']['values'] = weight_array
        elif DataType(rqt_type) == DataType.DATA_STATS_REMAINING_FOOD:
            food_array.clear()
            for i in range(random.randint(1, 30)):
                food_array.append(random.random())

            data_dict['data']['values'] = food_array
        elif DataType(rqt_type) == DataType.DATA_STATS_DOG_ARRIVAL:
            arrival_array.clear()
            for i in range(random.randint(1, 30)):
                arrival_array.append(random.randint(1, 5))

            data_dict['data']['values'] = arrival_array
        elif DataType(rqt_type) == DataType.DATA_GLOBAL_RELOAD:
            stats_dict = {}
            stats_dict['weight'] = weight_array
            stats_dict['food'] = food_array
            stats_dict['arrival'] = arrival_array

            data_dict['data']['stats'] = stats_dict
            data_dict['data']['dog'] = dogData
            data_dict['data']['schedule'] = scheduleList

        send_data = json.dumps(data_dict)

        print('replying', send_data)
        for client in clients:
                client.sendMessage(send_data)

    def handleConnected(self):
        print(self.address, 'connected')
        clients.append(self)

    def handleClose(self):
        clients.remove(self)
        print(self.address, 'closed')


if os.path.exists('data/dog.json'):
    dog_file = open('data/dog.json')
    dogData = json.load(dog_file)
    dog_file.close()

if os.path.exists('data/schedule_list.json'):
    schedule_file = open('data/schedule_list.json')
    scheduleList = json.load(schedule_file)
    schedule_file.close()

for i in range(random.randint(1, 30)):
    weight_array.append(random.randint(30, 40))
    food_array.append(random.random())
    arrival_array.append(random.randint(1, 5))

server = SimpleWebSocketServer('', 8000, Simulator)
server.serveforever()
