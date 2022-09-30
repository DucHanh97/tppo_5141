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

def setParams(canvas, lightflow):
    illumin = str(setIllumination(int(canvas), int(lightflow)))
    device = open('Device.txt','w')
    device.writelines("canvas="+canvas+"\nlightflow="+lightflow+"\nillumination="+illumin)
    device.close()

# def setLightFlow(value):
#     device = open('Device.txt','r')
#     buff = device.readline()
#     device.close()
#     for i in range(len(buff)):
#         if buff[i] == '=':
#             canvas = int(buff[i+1:])
#     illumin = str(setIllumination(canvas, int(value)))
#     device = open('Device.txt','w')
#     device.write(buff+"lightflow="+value+'\n'+"illumination="+illumin)
    # device.write("lightflow="+value+'\n')
    # device.write("illumination="+illumin)

def setIllumination(canvas, light):
    return int((canvas * light) / 10000 * 50000)
