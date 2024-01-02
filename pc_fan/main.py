import sys, serial, time
from serial.tools import list_ports


def analyze_ports(message):
    print(message)
    com_ports = list_ports.comports()  # 列出当前所有串口
    for com in com_ports:  # com[0]，串口号
        try:
            print(com[0])
            ser = serial.Serial(com[0], 115200)
            if ser.is_open:
                print(f'串口{com[0]}已打开')
                for i in range(10):
                    ser.write(f'{message}'.encode('utf-8'))
                    time.sleep(1)

                # bytes = ser.readline()
                # print(f'Read 10 bytes: {bytes}')
                ser.close()
            else:
                print(f'串口{com[0]}未打开')
        except serial.SerialException as e:
            print(f'打开串口{com[0]}时出错: {e}')

