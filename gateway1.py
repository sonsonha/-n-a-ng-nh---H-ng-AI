import serial.tools.list_ports
import random
import time
import  sys
from  Adafruit_IO import  MQTTClient

AIO_FEED_IDS = ["humi", "temp", "fan", "led", "door"]
AIO_USERNAME = "sonsonha"
AIO_KEY = "aio_uQxn48r43SoIaxueitarvD8MqKko"

# def uart_write(data):
#     ser.write((str(data) + "#").encode())
#     return

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB-SERIAL" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort

ser = serial.Serial( port=getPort(), baudrate=115200)

def  connected(client):
    print("Ket noi thanh cong...")
    # client.subscribe("fan")
    # client.subscribe("led")
    for feed in AIO_FEED_IDS :
        client.subscribe(feed)
        print("Ket noi thanh cong...")


def  disconnected(client):
    print("Ngat ket noi...")
    sys.exit (1)

def subscribe(client, userdata, mid, granted_qos):
    print("Subscribe thành công...")

def  message(client, feed_id, payload):
    print("Nhan du lieu: " + feed_id + ", Payload: " + payload)
    if(feed_id == "fan"):
        print("Nhan du lieu fan: " + payload)
        ser.write(("!set_fan:" + payload + "#").encode())
    if (feed_id == "led"):
        print("Nhan du lieu led: " + payload)
        ser.write(("!set_led:" + payload + "#").encode())
    if (feed_id == "door"):
        print("Nhan du lieu led: " + payload)
        ser.write(("!open_door:" + payload + "#").encode())

# def  message(client, userdata, msg):
#     print("Nhan du lieu: " + msg.topic + " " + str(msg.payload.decode()))
#     if(msg.topic == "fan"):
#         print("Nhan du lieu fan: " + str(msg.payload.decode()))
#         ser.write(("!set_fan:" + str(msg.payload.decode()) + "#").encode())
#     if (msg.topic == "led"):
#         print("Nhan du lieu led: " + str(msg.payload.decode()))
#         ser.write(("!set_led:" + str(msg.payload.decode()) + "#").encode())

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()


def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    if splitData[0] == "TEMP":
        time.sleep(0.3)
        client.publish("temp", splitData[1])
    if splitData[0] == "HUMI":
        time.sleep(0.3)
        client.publish("humi", splitData[1])


mess = ""
def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

# client.loop_start()
while True:
    # print("a")
    readSerial()
    time.sleep(1)