import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

def myConvolve(signal1, signal2, m, n):
    if m == 0:
        raise ValueError('signal1 boş olamaz')
    if n == 0:
        raise ValueError('signal2 boş olamaz')
    convLen = m + n - 1
    y = np.zeros(convLen, dtype=float)
    for i in range(convLen):  # signal 2 yi terslemeyi tercih ettim
        signal2_start = max(0, i - m + 1)
        signal2_end = min(i + 1, n)
        signal1_start = min(i, m - 1)
        for j in range(signal2_start, signal2_end):
            y[i] = y[i] + signal1[signal1_start] * signal2[j]
            signal1_start = signal1_start - 1
    return y

def initialize(index, length):
    x = []
    for i in range(length):
        x.append(index)
        index = index + 1
    return x

def graph_versus(signalX, signalY, zeroIndexX, zeroIndexY):
    
    conv_ary = myConvolve(signalX, signalY, len(signalX), len(signalY))
    convolution = np.convolve(signalX, signalY)

    maxY = max(signalX) * max(signalY) * 2
    minY = maxY * -1 / 2
    maxX = max(len(signalX), len(signalY)) * 2
    minX = min(-zeroIndexX, -zeroIndexY) - max(len(signalX), len(signalY))
    startX = initialize(-zeroIndexX, len(signalX))
    startY = initialize(-zeroIndexY, len(signalY))
    startConv = initialize(-(zeroIndexX + zeroIndexY), len(signalX) + len(signalY) - 1)

    fig = plt.figure(figsize=(13, 7), dpi=80, facecolor='w', edgecolor='k')
    plt.subplot(2, 2, 1)
    plt.stem(startX, signalX, "ro")
    plt.xlabel('Sample Index - n')
    plt.ylabel('Sample Value - signal1[n]')
    plt.ylim([minY, maxY])
    plt.xlim([minX, maxX])

    plt.subplot(2, 2, 2)
    plt.stem(startY, signalY, 'c')
    plt.xlabel('Sample Index - n')
    plt.ylabel('Sample Value - signal2[n]')
    plt.ylim([minY, maxY])
    plt.xlim([minX, maxX])

    plt.subplot(2, 2, 3)
    plt.stem(startConv, conv_ary, 'g')
    plt.xlabel('Sample Index - n')
    plt.ylabel('Sample Value - my_conv[n]')
    plt.ylim([minY, maxY])
    plt.xlim([minX, maxX])

    plt.subplot(2, 2, 4)
    plt.stem(startConv, convolution, 'g')
    plt.xlabel('Sample Index - n')
    plt.ylabel('Sample Value - convolution[n]')
    plt.ylim([minY, maxY])
    plt.xlim([minX, maxX])

    plt.show()

def vector_versus(signalX, signalY):
    conv_ary = myConvolve(signalX, signalY, len(signalX), len(signalY))
    convolution = np.convolve(signalX, signalY)

    print(signalX)
    print(signalY)
    print(conv_ary)
    print(convolution)

def audiorecord(duration):
    freq = 44100
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)
    print("Recording...")
    sd.wait(duration)
    print("Recording is over")
    rec1 = np.array(recording).flatten()
    sd.play(rec1, blocking=True)
    return rec1

def newAudioWithMyConvolve(record, M):
    h = np.zeros(M*400+1, dtype=float)
    h[0] = 1
    k = 1
    for i in range(k,M+1):
        j = i * 400
        h[j] = 0.8
    print("Processing...")
    myAudioConv = myConvolve(record,h,len(record),len(h))
    return myAudioConv

def newAudioWithNumpyConvelve(record, M):
    h = np.zeros(M*400+1, dtype=float)
    h[0] = 1
    k = 1
    for i in range(k,M+1):
        j = i * 400
        h[j] = 0.8
    print("Processing...")
    myAudioConv = np.convolve(record,h)
    return myAudioConv

len1 = int(input("1.sinyal dizisinin eleman uzunluğunu giriniz:"))
signalX = np.zeros(len1)
for i in range(0,len1):
    signalX[i] = input("Eleman:")
len2 = int(input("2.sinyal dizisinin eleman uzunluğunu giriniz:"))
signalY = np.zeros(len2)
for i in range(0,len2):
    signalY[i] = input("Eleman:")
zeroIndexX = int(input("1.Dizinin sıfır noktasını giriniz:"))
zeroIndexY = int(input("2.Dizinin sıfır noktasını giriniz:"))

graph_versus(signalX, signalY, zeroIndexX, zeroIndexY)
vector_versus(signalX, signalY)
record5 = audiorecord(5)
record10 = audiorecord(10)

Y1 = newAudioWithNumpyConvelve(record5, 2)
sd.play(Y1, blocking=True)
Y2 = newAudioWithNumpyConvelve(record10, 2)
sd.play(Y2, blocking=True)

my_Y1 = newAudioWithMyConvolve(record5, 3)
sd.play(my_Y1, blocking=True)
my_Y2 = newAudioWithMyConvolve(record10, 3)
sd.play(my_Y2, blocking=True)