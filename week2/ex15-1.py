# read the mailbox data (mbox.txt)
# count the number of email messages per organization (domain)
# store the counts in a database relation with the following structure:
# org TEXT, count INTEGER

import sqlite3 as sq
import re

conn = sq.connect('ex15-1.sqlite')

cur = conn.cursor()

cur.execute('drop table if exists counts')
cur.execute('create table counts (org TEXT, count INTEGER)')

fname = 'mbox.txt'
fh = open(fname)

for line in fh :

    if not line.startswith('From: ') : continue
    domainSearch = re.findall('@(\S+?)\s', line)
    domain = domainSearch[0]

    cur.execute('select count from counts where org like ?', (domain,))
    row = cur.fetchone()

    if row is None:
        cur.execute('insert into counts (org, count) values (?, 1)', (domain,))
    else:
        cur.execute('update counts set count = count + 1 where org like ?', (domain,))

    conn.commit()

sqlstr = 'select org, count from counts order by count desc limit 10'

for row in cur.execute(sqlstr) :
    print(row)

cur.close()
