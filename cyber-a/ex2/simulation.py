#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv

def print_usage(script_name):
    print('%s a b c' % script_name)

def open_worm_table():
    with open('./worm-table.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(', '.join(row))

def start_simulation(a, b, c):
    pass

def main(script_name, argv):
    try:
        a = int(argv[0])
        b = int(argv[1])
        c = int(argv[2])
        open_worm_table()
        start_simulation(a, b, c)
    except:
        print_usage(script_name)
        sys.exit(2)

if __name__ == "__main__":
   main(sys.argv[0], sys.argv[1:])
