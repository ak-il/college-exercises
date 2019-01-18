#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

def open_policy_table():
    table = []
    with open('./firewall-policy.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            table.append({
                'src_address': row[0],
                'src_port': row[1],
                'dest_ip': row[2],
                'sodest_port': row[3],
                'port': row[4],
                'action': row[5]
            })
    return table

def open_traffic_table():
    table = []
    with open('./firewall-traffic.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            table.append({
                'src_address': row[0],
                'src_port': row[1],
                'dest_ip': row[2],
                'sodest_port': row[3],
                'port': row[4]
            })
    return table

def start_simulation(policy, traffic):
    for traffic_entry in traffic:
        print_action(policy, traffic_entry)

def print_action(policy, traffic_entry):
    pass

def main():
    policy = open_policy_table()
    traffic = open_traffic_table()
    start_simulation(policy, traffic)

if __name__ == "__main__":
   main()
