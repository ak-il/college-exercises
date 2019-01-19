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
                'dest_port': row[3],
                'protocol': row[4],
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
                'dest_port': row[3],
                'protocol': row[4]
            })
    return table

def start_simulation(policy, traffic):
    for traffic_entry in traffic:
        if is_allowed(policy, traffic_entry):
            print("allow traffic:")
        else:
            print("drop traffic:")
        print(traffic_entry)

def is_allowed(policy, traffic_entry):
    for policy_entry in policy:
        if (policy_entry['src_address'] == traffic_entry['src_address'] or
            policy_entry['src_address'] == 'any') and \
            (policy_entry['src_port'] == traffic_entry['src_port'] or
            policy_entry['src_port'] == 'any') and \
            (policy_entry['dest_ip'] == traffic_entry['dest_ip'] or
            policy_entry['dest_ip'] == 'any') and \
            (policy_entry['dest_port'] == traffic_entry['dest_port'] or
            policy_entry['dest_port'] == 'any') and \
            (policy_entry['protocol'] == traffic_entry['protocol'] or
             policy_entry['protocol'] == 'any'):
                if policy_entry['action'] == 'allow':
                    return True
                else:
                    return False
    # Drop by default
    return False

def main():
    policy = open_policy_table()
    traffic = open_traffic_table()
    start_simulation(policy, traffic)

if __name__ == "__main__":
   main()
