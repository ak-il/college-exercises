#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
import random
import matplotlib.pyplot as plt
import time

def print_usage(script_name):
    print('%s a b c' % script_name)

def open_worm_table():
    table = {}
    with open('./worm-table.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            table[row[0]] = {
                'is_reachable': row[1] == 'Y',
                'is_vulnerable': row[2] == 'Y',
                'is_infected': row[3] == 'Y'
            }
    return table

def start_simulation(table, a, b, c):
    actions = {}
    for ip, value in table.iteritems():
        actions[ip] = reset_action()
    infected_by_time = do_iterations(table, actions, a, b, c)
    print infected_by_time
    save_graph(infected_by_time, a, b, c)

def do_iterations(table, actions, a, b, c):
    infected_by_time = []
    while not simulation_finished(table):
        infected_by_time.append(len(list(filter(lambda x: x['is_infected'], \
                                                  table.values()))))
        for ip, value in actions.iteritems():
            value['try_access_left'] -= 1
            value['test_vulnerable_left'] -= 1
            value['exploit_left'] -= 1
            if value['target'] == None:
                ips = table.keys()
                ips.remove(ip)
                value['target'] = random.choice(ips)
                value['try_access_left'] = a
            elif value['try_access_left'] == 0:
                if table[value['target']]['is_reachable']:
                    value['test_vulnerable_left'] = b
                else:
                    actions[ip] = reset_action()
            elif value['test_vulnerable_left'] == 0:
                if table[value['target']]['is_vulnerable']:
                    value['exploit_left'] = c
                else:
                    actions[ip] = reset_action()
            elif value['exploit_left'] == 0:
                table[value['target']]['is_infected'] = True
                actions[ip] = reset_action()
    return infected_by_time

def reset_action():
    return {
        'target': None,
        'try_access_left': -1,
        'test_vulnerable_left': -1,
        'exploit_left': -1,
    }

def simulation_finished(table):
    for ip, value in table.iteritems():
        if value['is_reachable'] and value['is_vulnerable'] and \
        not value['is_infected']:
            return False
    return True

def save_graph(infected_by_time, a, b, c):
    x = range(len(infected_by_time))
    plt.plot(x, infected_by_time)
    plt.xlabel('time')
    plt.ylabel('infected computers')
    plt.title('Worm infections by time, a=%s b=%s c=%s' % (a, b, c,))
    plt.grid(True)
    plt.savefig("%s.png" % time.strftime("%d%m%Y-%H%M%S"))
    plt.show()

def main(script_name, argv):
    try:
        a = int(argv[0])
        b = int(argv[1])
        c = int(argv[2])
        if a > 0 and b > 0 and c > 0:
            table = open_worm_table()
            start_simulation(table, a, b, c)
        else:
            raise ValueError('Arguments should be integers bigger than zero!')
    except Exception as e:
        print(e)
        print_usage(script_name)
        sys.exit(2)

if __name__ == "__main__":
   main(sys.argv[0], sys.argv[1:])
