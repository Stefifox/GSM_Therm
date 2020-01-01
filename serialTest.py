import serial
from time import sleep

# Enable Serial Communication
port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)


def rcv():
    sleep(0.5)
    recive = port.readline(10)
    print(recive)

port.write("AT\r\n".encode())
rcv()
sleep(1)
port.write("AT+CNMI=2,2,0,0,0\r\n".encode())
sleep(1)
rcv()
port.write("AT+CCID\r\n".encode())
rcv()
port.write("AR+CREG?\r\n")
rcv()

while True:

    rcv()
