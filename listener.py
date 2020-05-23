import paho.mqtt.client as mqtt
import subprocess

class Listener:
    def __init__(self, server):
        self.broker = subprocess.check_output('hostname').decode().rstrip('\n')
        self.port = 8883
        self.client = mqtt.Client()
        self.target = server
        self.connect_to_broker()


    def process_message(self, client, userdata, message):
        message = (str(message.payload.decode("utf-8"))).split(".")

        if message[0] == 'connected':
            self.target.add_terminal(message[1], message[2])
        elif message[0] == 'disconnected':
            self.target.remove_terminal(message[1])
        elif message[0] == 'action':
            self.target.gate_update(message[1], message[2])


    def connect_to_broker(self):
        self.client.tls_set("/etc/mosquitto/certs/ca.crt")
        # Authorization 
        self.client.username_pw_set(username='client', password='password')
        # Connect to the broker.
        self.client.connect(self.broker, self.port)
        # Send message about conenction.
        self.client.on_message = self.process_message
        # Starts client and subscribe.
        self.client.loop_start()
        self.client.subscribe("worker/name")


    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
