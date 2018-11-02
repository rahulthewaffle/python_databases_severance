import re

fname = 'mbox.txt'
fh = open(fname)
i = 0

for line in fh :
    if i >= 10 : break
    if not line.startswith('From: ') : continue

    print(re.findall('@(\S+?)\s', line))

    i += 1
