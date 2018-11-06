# Just as a note, the 'correct' answer is wrong from the get go.

# You're required to use the database schema provided by the prompt, but the issue is the usage of the unique constraint.
# I understand that the unique constraint is used to trigger a conflict which in turn is supposed to prompt desired behaviour from the Insert or Ignore statement.

# However, putting a unique constraint on individual columns simply makes the table unable to accept rows with repeat values in each of those particular columns.
# Hence, you can't have albums with the same title but with different artists! (A very common issue in the real world) This holds true of the other tables with unique constraints on individual columns.
# This in turn results in insert statements that necessitate tracks being inserted with the incorrect albumID, which violates the theoretical and normalized object hierarchy.
# For instance, a song from Frank Sinatra's album "greatest hits" will instead be associated with Queen's album 'greatest hits' since a track on Queen's 'greatest hits' was read from the xml first.

# The solution to this issue is to place your unique constraint around multiple columns, forming a unique index that represents a hash key composited of multiple columns' values.
# e.g. : create table album ( id integer not null primary key autoincrement unique, artistID integer, title text, unique (artistID, title) on conflict ignore)
# Obviously you'd want to repeat this step for your other tables that have unique collections of attributes rather than individually unique attributes.
# This allows you to support both rows that are unique as a sum of the relevant criteria, and it allows you to preserve 3NF and not have composite key columns in the table.
# In addition, it means that the on conflict or ignore logic is stored in the table, not the CRUD statement.

# With all this being said, in order to submit an sqlite file that the autograder will accept, you have to generate the incorrect database as is done in the tracks.py example code.
# So if you're having trouble because of this issue, you'll have to bite the bullet in order to pass, but you can at least be happy now that you know how to avoid this issue with future sqlite db architecture! :)

# Read an iTunes export file in XML
# Create a properly normalized database
# Populate said database with xml data

import sqlite3 as sql
import xml.etree.ElementTree as ET

createDBString = '''drop table if exists artist;
drop table if exists genre;
drop table if exists album;
drop table if exists track;

create table artist (
    id integer not null primary key autoincrement unique,
    name    text unique
);

create table genre (
    id integer not null primary key autoincrement unique,
    name    text unique
);

create table album (
    id integer not null primary key autoincrement unique,
    artist_id  integer,
    title   text unique
);

create table track (
    id integer not null primary key autoincrement unique,
    title text unique,
    album_id integer,
    genre_id integer,
    len integer,
    rating integer,
    count integer
);'''

def lookup(d, key):
    found = False
    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == key :
            found = True
    return None

conn = sql.connect('ex15-2.sqlite')
cur = conn.cursor()

cur.executescript(createDBString)

fname = 'Library.xml'

all = ET.parse(fname)
tracks = all.findall('dict/dict/dict')

print('Dict Count:', len(tracks))

for track in tracks :
    if (lookup(track, 'Track ID') is None) : continue

    title = lookup(track, 'Name')
    if (title is None) : continue

    artist = lookup(track, 'Artist')
    if (artist is None) : continue

    album = lookup(track, 'Album')
    if (album is None) : continue

    genre = lookup(track, 'Genre')
    if (genre is None) : continue

    length = lookup(track, 'Total Time')
    if (length is None) : continue

    count = lookup(track, 'Track Count')
    if (count is None) : continue

    rating = lookup(track, 'Rating')
    if (rating is None) : continue

    # debugging: print(title, artist, album, genre, count, rating, length)

    cur.execute('''insert or ignore into artist (name)
        values ( ? )''', (artist,) )
    artistID = cur.execute('select id from artist where name like ? ', (artist,)).fetchone()[0]

    cur.execute('''insert or ignore into genre (name)
        values ( ? )''', (genre,))
    genreID = cur.execute('select id from genre where name like ? ', (genre,)).fetchone()[0]

    cur.execute('''insert or ignore into album (artist_ID, title)
        values ( ?, ? )''', (artistID, album))
    albumID = cur.execute('select id from album where title like ?', (album,)).fetchone()[0]

    cur.execute('''insert or ignore into track (title, album_id, genre_id, len, rating, count)
        values ( ?, ?, ?, ?, ?, ? )''', (title, albumID, genreID, length, rating, count))

    conn.commit()
