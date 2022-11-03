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

def setIllumination(canvas, light):
    return int((canvas * light) / 10000 * 50000)

if(__name__=="__main__"):
    setParams(str(100),str(100))
