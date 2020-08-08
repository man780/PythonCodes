#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv

with open('lis.csv', newline='') as fileImport:
    reader = csv.reader(fileImport)
    data = list(reader)

bCandidat = []
bCandidat.append(data[0])
for candidat in data:
    if candidat[5] == 'Бошқарма бошлиғи':
        bCandidat.append(candidat)


with open('export/candidates.csv', 'w') as fileExport:
    writer = csv.writer(fileExport)
    writer.writerows(bCandidat)
