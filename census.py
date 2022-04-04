import re
import paho.mqtt.client as mqtt
from datetime import datetime
from MySQLdb import connect, Error
import config


def db_query(query_string):
    """Execute a database query."""
    print(query_string)
    try:
        with connect(
            host="localhost",
            user=config.sqlusername,
            password=config.sqlpassword,
            database=config.sqldatabase,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query_string)
                connection.commit()
                return cursor.fetchall()
    except Error as e:
        print("Database error: ", e)
        return None


def mac_to_int(mac):
    """Convert a MAC address to an integer."""
    res = re.match('^((?:(?:[0-9a-f]{2}):){5}[0-9a-f]{2})$', mac.lower())
    if res is None:
        raise ValueError('invalid mac address')
    return int(res.group(0).replace(':', ''), 16)


def on_connect(client, userdata, flags, rc):
    """Callback for when mqtt client connects."""
    print("Connected with result code "+str(rc))
    # Just get the firehose
    client.subscribe("#")

def on_message(client, userdata, msg):
    """Callback for when mqtt client receives a message."""
    payload = str(msg.payload.decode("utf-8"))
    print(msg.topic+" "+payload)

    if (msg.topic == "Connect/NUSTEM/MOOD"):
        # Act on mood
        print("Mood receive", payload)
        query_string = """
        INSERT INTO moods (mood_name, mood_count)
        VALUES ('"""+payload+"""', 1)
        ON DUPLICATE KEY UPDATE mood_count = mood_count + 1;"""
        db_query(query_string)
    elif (msg.topic.startswith("/management/from")):
        if (payload == "255"):
            # Trigger the device watching function with the MAC address
            # i_see_you(msg.topic[17:29])
            now=datetime.now()
            query_string = """
            INSERT INTO devices (mac_address, last_seen)
            VALUES ('"""+mac_to_int(msg.topic[17:29])+"""', '"""+now.strftime("%Y-%m-%d %H:%M:%S")+"""')
            ON DUPLICATE KEY UPDATE
            last_seen = '"""+now.strftime("%Y-%m-%d %H:%M:%S")+"""',
            ping_count = ping_count + 1;"""

    elif (msg.topic.startswith("/management/to")):
        device = mac_to_int(msg.topic[17:29])
        query_string = """
        UPDATE devices SET flash_count = flash_count + 1
        WHERE mac_address = '"""+device+"""'
        """
        db_query(query_string)
    else:
        print("Unknown message: ", msg.topic, payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(config.mqttUsername, config.mqttPassword)

def do_connect():
    try:
        client.connect("connect.nustem.uk", 1883, 60)
        print("Connection successful")
    except:
        print("Failed to connect to MQTT server")
        exit(1)


if __name__ == "__main__":
    do_connect()
    client.loop_forever()
