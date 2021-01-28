# -*- coding: utf-8 -*-
"""
write configuration
dictionary --> json

read configuration
json --> dictionary
"""

import json

class JsonConfig(object):
    def __init__(self, filepath):

        self.filepath = filepath
        self.data = {}

    def get_data(self, pyfirmata_format = False): # 'dictionary' /'pyfirmata'
        with open(self.filepath) as json_file:
            self.data = json.load(json_file)
            # print(self.data)

        if pyfirmata_format:
            # format so pyfirmata pin can be directly configured/created
            pyfirmata_data = []
            for pin in self.data['io_pins']:
                # print(pin)
                #     pin = data['io_pins'][i]
                pin_type = pin['type']
                pin_number = pin['number']
                pin_mode = pin['mode']
                # type:number:mode (a:0:i)
                string = pin_type+':'+pin_number+':'+pin_mode
                pyfirmata_data.append(string)
            return pyfirmata_data
        else:
            return self.data

    def set_data(self, dictionary):
        with open(self.filepath, 'w') as outfile:
            json.dump(dictionary, outfile)

    def get_default(self):
        # read data from default configuration file
        default_file = 'default_config.txt'
        with open(default_file) as json_file:
            self.data = json.load(json_file)

        return self.data


def write_test():
    # 'mode': 'i', # ‘i’,‘o’ input/output ‘p’ for pwm).
    data = {}
    data['io_pins'] = []
    """
    usual-pyfermata config = 'd:3:o', type:number:mode
    data['io_pins'].appendd({
        'name': '' #D0..D13,A0..A5
        'type': '', #digital = ‘d’, analog =‘a’
        'mode': 'i', # ‘i’,‘o’ input/output ‘p’ for pwm).
        'is_pwm': True # True/False
        'is_analog':
    })
    """
    # create default data
    pin_name = ['D2',
                   'D3',
                   'D4',
                   'D5',
                   'D6',
                   'D7',
                   'D8',
                   'D9',
                   'D10',
                   'D11',
                   'D12',
                   'D13',
                   'A0',
                   'A1',
                   'A2',
                   'A3',
                   'A4',
                   'A5']

    pin_mode = ['i',
                'i',
                'i',
                'i',
                'i',
                'i',
                'i',
                'i',
                'i',
                'i',
                'i',
                'i',
                'i',
                'i',
                'i',
                'i',
                'i',
                'i']

    pin_number = ['2',
                  '3',
                  '4',
                  '5',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10',
                  '11',
                  '12',
                  '13',
                  '0',
                  '1',
                  '2',
                  '3',
                  '4',
                  '5']

    pin_type = ['d',
                'd',
                'd',
                'd',
                'd',
                'd',
                'd',
                'd',
                'd',
                'd',
                'd',
                'd',
                'a',
                'a',
                'a',
                'a',
                'a',
                'a']

    is_pwm = [False,
             True,
             False,
             True,
             True,
             False,
             False,
             True,
             True,
             True,
             False,
             False,
             False,
             False,
             False,
             False,
             False,
             False]

    is_analog = [False,
             False,
             False,
             False,
             False,
             False,
             False,
             False,
             False,
             False,
             False,
             False,
             True,
             True,
             True,
             True,
             True,
             True]
    
    enabled = [True,
             True,
             True,
             True,
             True,
             True,
             True,
             True,
             True,
             True,
             True,
             True,
             True,
             True,
             True,
             True,
             True,
             True]
    # type:number:mode (a:0:i)
    for i in range(len(pin_name)):
        pin = {}
        pin['type'] = pin_type[i]
        pin['number'] = pin_number[i]
        pin['mode'] = pin_mode[i]
        pin['name'] = pin_name[i]
        pin['is_pwm'] = is_pwm[i]
        pin['is_analog'] = is_analog[i]
        pin['enabled'] = enabled[i]
        data['io_pins'].append(pin)

    # print(data)
    configuration.set_data(data)

def read_test():
    print(configuration.get_data(False))
#-----------------------------
if __name__ == "__main__":
    configuration = JsonConfig('configuration.txt')

    write_test()
    # read_test()