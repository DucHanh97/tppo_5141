from tkinter import Canvas


def getCanvas():
    device = open('Device.txt', 'r')
    CanLine = device.readline()
    device.close()
    for i in range(len(CanLine)):
        if CanLine[i] == '=':
            return int(CanLine[i+1:])

def getLightFlow():
    device = open('Device.txt', 'r')
    device.readline()
    LightFlow = device.readline()
    device.close()
    for i in range(len(LightFlow)):
        if LightFlow[i] == '=':
            return int(LightFlow[i+1:])

def getIllumination():
    device = open('Device.txt', 'r')
    device.readline()
    device.readline()
    Illumination = device.readline()
    device.close()
    for i in range(len(Illumination)):
        if Illumination[i] == '=':
            return int(Illumination[i+1:])

def setCanvas(value):
    device = open('Device.txt','r')
    device.readline()
    buff = device.readline()
    device.close()
    for i in range(len(buff)):
        if buff[i] == '=':
            light = int(buff[i+1:])
    illumin = str(setIllumination(int(value), light))
    device = open('Device.txt','w')
    device.write("canvas="+value+'\n')
    device.write(buff)
    device.write("illumination="+illumin)

    

def setLightFlow(value):
    device = open('Device.txt','r')
    buff = device.readline()
    device.close()
    for i in range(len(buff)):
        if buff[i] == '=':
            canvas = int(buff[i+1:])
    illumin = str(setIllumination(canvas, int(value)))
    device = open('Device.txt','w')
    device.write(buff)
    device.write("lightflow="+value+'\n')
    device.write("illumination="+illumin)

def setIllumination(canvas, light):
    return int((canvas * light) / 10000 * 50000)

setLightFlow('95')