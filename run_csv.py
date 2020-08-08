#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv

with open('lis.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
