import re
import paho.mqtt.client as mqtt
from datetime import datetime
from MySQLdb import connect, Error
from netaddr import *
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


def on_connect(client, userdata, flags, rc):
    """Callback for when mqtt client connects."""
    print("Connected with result code "+str(rc))
    # Just get the firehose
    client.subscribe("#") # TODO: QoS setting

def on_message(client, userdata, msg):
    """Callback for when mqtt client receives a message."""
    payload = str(msg.payload.decode("utf-8"))
    print(msg.topic+" "+payload)

    if (msg.topic == "Connect/NUSTEM/MOOD"):
        # Act on mood
        # TODO: Should we not just log this to a file, and rotate the logs?
        #       Timestamped granularity vs. manual database snapshots.
        #       Yes, but likely also do this, for JSON/AJAX purposes.
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
            mac = EUI(msg.topic[17:29])
            query_string = """
            INSERT INTO devices (mac_address, last_seen, pings)
            VALUES ('"""+str(int(mac))+"""', '"""+now.strftime("%Y-%m-%d %H:%M:%S")+"""', 1)
            ON DUPLICATE KEY UPDATE
            last_seen = '"""+now.strftime("%Y-%m-%d %H:%M:%S")+"""',
            pings = pings + 1;"""
            db_query(query_string)

    elif (msg.topic.startswith("/management/to")):
        device = int(EUI(msg.topic[17:29]))
        query_string = """
        UPDATE devices SET times_flashed = times_flashed + 1
        WHERE mac_address = '"""+device+"""'
        """
        db_query(query_string)
    elif ('msg.topic.startswith("Connect/NUSTEM/hello_my_name_is")'):
        device = int(EUI(payload))
        now = datetime.now()
        # Update logins count
        query_string = """
        INSERT INTO devices (mac_address, logins, last_seen)
        VALUES ('"""+str(device)+"""', 1, '"""+now.strftime("%Y-%m-%d %H:%M:%S")+"""')
        ON DUPLICATE KEY UPDATE
        logins = logins + 1,
        last_seen = '"""+now.strftime("%Y-%m-%d %H:%M:%S")+"""';"""
        db_query(query_string)
        # TODO: handle days active here (separate query?) Or do we do this via MQTT logs?
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
