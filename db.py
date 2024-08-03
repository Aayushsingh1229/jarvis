import sqlite3

#import pywhatkit
conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()
# query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
# cursor.execute(query)
# query = "INSERT INTO sys_command VALUES (null,'music','C:\\Users\\srija singh\\Music')"
#cursor.execute(query)
# conn.commit()

# query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO web_command VALUES (null,'google','https://www.google.com')"

# Connect to the SQLite database
# Create a cursor object

# Define the table name to be deleted
# query = "CREATE TABLE IF NOT EXISTS events ( id integer primary key,title text not null,start_date text not null,end_date text not null,description text)"

# query ="CREATE TABLE IF NOT EXISTS reminders (id INTEGER PRIMARY KEY,event_id INTEGER,reminder_date TEXT NOT NULL,message TEXT, FOREIGN KEY (event_id) REFERENCES events (id))"


#cursor.execute()
#conn.commit()
#import pywhatkit

#pywhatkit.sendwhatmsg_instantly('+917903798357', 'hi', 10)

#desired_columns_indices = [0, 32]
#cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')
#import csv
#with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
 #   csvreader = csv.reader(csvfile)
  #  for row in csvreader:
   #     selected_data = [row[i] for i in desired_columns_indices]
    #    cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# # Commit changes and close connection
conn.commit()
conn.close()

