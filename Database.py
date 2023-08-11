# coding: utf8
import sqlite3

connection = sqlite3.connect('Splatoon3.db')


cursor = connection.cursor()

"""
cursor.execute('''
CREATE TABLE IF NOT EXISTS teams(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        players TEXT NOT NULL,
        replace TEXT NOT NULL,
        discord_names TEXT NOT NULL,
        roleID TEXT NOT NULL,
        iconURL TEXT NOT NULL,
        image BLOB
    )''')
"""
'''
cursor.execute("""INSERT INTO teams VALUES (
0,
'Team',
'P1 P2',
'R1 R2',
'discordname1 discordname2',
'@354363362',
'https://media.discordapp.net/attachments/994356082313023560/1139184279318958231/9zmu3VCQfSM.png?width=600&height=450',
''
 )""")
'''

cursor.execute("SELECT * FROM teams")
print(cursor.fetchall())


connection.commit()
connection.close()