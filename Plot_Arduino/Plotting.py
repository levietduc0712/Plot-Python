import serial
import matplotlib.pyplot as plt
import numpy as np

ser = serial.Serial('COM4',9600)
plt.close('all')
plt.figure()
plt.ion()
plt.show()

ser.close()
ser.open()

data = np.array([])
data2 = np.array([])

i = 1


while True:
    a = ser.readline()
    a.decode()
    # print(a)
    b = float(a[0:6])
    if (i%2):
        data = np.append(data,b)
    else:
        data2 = np.append(data2,b)

    plt.cla()
    plt.subplot(2, 2, 1)
    plt.plot(data2, c='red')
    plt.title('Cos()')
    plt.grid()

    plt.subplot(2, 2, 2)
    plt.plot(data, c='blue')
    plt.title('Sin()')
    plt.grid()

    plt.subplot(2, 1, 2)
    plt.plot(data, c='blue')
    plt.plot(data2, c='red')
    plt.title('Cos() and Sin()')
    plt.grid()

    plt.pause(0.01)
    i = i + 1
