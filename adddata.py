# sudo pip3 install mysql-connector-python

import json
import mysql.connector
from mysql.connector import Error
import os

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as json_file:
            try:
                return json.load(json_file)
            except json.JSONDecodeError:
                return []
    else:
        return []

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='your_host',       # Beispiel: 'localhost'
            database='your_db',     # Beispiel: 'sensordata'
            user='your_username',   # Beispiel: 'root'
            password='your_password' # Dein Passwort
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date DATE,
        LPG INT,
        Hum INT,
        TEMP INT
    )
    ''')
    connection.commit()

def insert_data(connection, data):
    cursor = connection.cursor()
    insert_query = '''
    INSERT INTO sensor_data (date, LPG, Hum, TEMP)
    VALUES (%s, %s, %s, %s)
    '''
    cursor.executemany(insert_query, [(entry['date'], entry['LPG'], entry['Hum'], entry['TEMP']) for entry in data])
    connection.commit()

def main():
    filename = 'data.json'
    data = load_data(filename)
    
    if not data:
        print("Keine Daten gefunden.")
        return

    connection = create_connection()
    if connection is None:
        return
    
    create_table(connection)
    insert_data(connection, data)
    
    print(f"{len(data)} Datensätze wurden erfolgreich in die Datenbank übertragen.")
    
    # Optional: JSON-Datei leeren oder löschen, nachdem die Daten übertragen wurden
    with open(filename, 'w') as json_file:
        json.dump([], json_file)

if __name__ == "__main__":
    main()
