# create a SQLite db that contains a user, course, and member table
# read roster data from roster_data.json
# populate db with data from json
# print the first row of an ascending ordered hex of user.name, course.title, member.role

import sqlite3 as sql
import json

createDBString = '''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
'''

conn = sql.connect('ex15-3.sqlite')
cur = conn.cursor()

cur.executescript(createDBString)

fname = 'roster_data.json'
fh = open(fname)

data = json.loads(fh.read())

for entry in data :
    user = entry[0]
    course = entry[1]
    role = entry[2]
    # debugging: print(user, course, role)

    cur.execute('''insert or ignore into user (name)
    values (?)''', (user,))
    userID = cur.execute('select id from user where name = ?', (user,)).fetchone()[0]
    # debugging: print(userID)

    cur.execute('''insert or ignore into course (title)
    values (?)''', (course,))
    courseID = cur.execute('select id from course where title = ?', (course,)).fetchone()[0]
    # debugging: print(courseID)

    cur.execute('''insert or ignore into member (user_id, course_id, role)
    values (?, ?, ?)''', (userID, courseID, role))

    conn.commit()

enrollment_hex = cur.execute('''SELECT hex(User.name || Course.title || Member.role ) AS X FROM
    User JOIN Member JOIN Course
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY X''').fetchone()[0]

print(enrollment_hex)
