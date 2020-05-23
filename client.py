import paho.mqtt.client as mqtt
import subprocess

terminal_id = input("Enter terminalID: ")
place = input("Enter terminal place(in/out): ")
place = place if place in ('in', 'out') else 'in'
broker = subprocess.check_output('hostname').decode().rstrip('\n')
port = 8883


# The MQTT client.
client = mqtt.Client()

def call_worker(RFID_num):
    client.publish("worker/name", 'action.' + terminal_id + "." + RFID_num,)


def connect_to_broker():
    client.tls_set("/etc/mosquitto/certs/ca.crt")
    # authorization
    client.username_pw_set(username='client', password='password')
    # connect to the broker.
    client.connect(broker, port)
    # Send message about connection.
    client.publish("worker/name", 'connected.'+terminal_id+'.'+place)


def disconnect_from_broker():
    
    # Send message about disconenction.
    client.publish("worker/name", 'disconnected.'+terminal_id+'.'+place)
    # Disconnet the client.
    client.disconnect()


def run_sender():
    RFID = input("Enter RFID number (registered employees have values 1-10): ")
    while RFID != 'quit':
        call_worker(RFID)
        RFID = input("Enter RFID number (registered employees have values 1-10): ")


if __name__ == "__main__":
    connect_to_broker()
    run_sender()
    disconnect_from_broker()
