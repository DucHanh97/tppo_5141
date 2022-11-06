import Device as device
from socket import SocketIO
import threading
from flask_socketio import SocketIO
from flask import Flask, request, abort
import os
from sys import argv

cur_Canvas  = str(device.getCanvas())
cur_Light   = str(device.getLightFlow())
cur_Illumin = str(device.getIllumination())
Dv_Params = [{"canvas":cur_Canvas}, {"lightflow":cur_Light}, {"illumination":cur_Illumin}]

print(cur_Canvas, type(cur_Canvas))
print(cur_Light, type(cur_Light))
print(cur_Illumin, type(cur_Illumin))

app = Flask(__name__)
socketio = SocketIO(app, cors_allower_origins="*", logger=True, engineio_logger=True, async_handlers=True)

#----------- Set route for REST APIs ------------
@app.route('/blinds/infor')
def main():
    return Dv_Params

@app.route('/blinds')       #Query String, http://ip_host/blinds?<parameter>=<value>
def get_query_string():
    global cur_Canvas
    global cur_Light
    global cur_Illumin
    global Dv_Params
    canvas = request.args.get('canvas')
    light = request.args.get('light')
    
    if((canvas != None) & (light == None)):
        device.setParams(canvas, cur_Light)
        cur_Canvas = str(device.getCanvas())
        cur_Light = str(device.getLightFlow())
        cur_Illumin = str(device.getIllumination())
        Dv_Params = [{"canvas":cur_Canvas}, {"lightflow":cur_Light}, {"illumination":cur_Illumin}]
        return Dv_Params
    elif((light != None) & (canvas == None)):
        device.setParams(cur_Canvas, light)
        cur_Canvas = str(device.getCanvas())
        cur_Light = str(device.getLightFlow())
        cur_Illumin = str(device.getIllumination())
        Dv_Params = [{"canvas":cur_Canvas}, {"lightflow":cur_Light}, {"illumination":cur_Illumin}]
        return Dv_Params
    elif((canvas != None) & (light != None)):
        device.setParams(canvas, light)
        cur_Canvas = str(device.getCanvas())
        cur_Light = str(device.getLightFlow())
        cur_Illumin = str(device.getIllumination())
        Dv_Params = [{"canvas":cur_Canvas}, {"lightflow":cur_Light}, {"illumination":cur_Illumin}]
        return Dv_Params
    else:
        abort(404)
#---------------- Handle socketio event ----------------
@socketio.on('connect')
def client_connect(auth):
    print("A client connected to the server")
    global notifDeviceChange
    if not notifDeviceChange.is_alive():
        notifDeviceChange.start()

@socketio.on('disconnect')
def client_disconnect():
    print("A client disconnected")

#----------- Notify device changes to clients ----------
def notifDeviceChange_handle():
    global socketio
    global cur_Canvas
    global cur_Light
    global cur_Illumin
    global Dv_Params
    time_cache = os.stat("Device.txt").st_mtime
    while True:
        time_change = os.stat("Device.txt").st_mtime
        if time_change != time_cache:
            time_cache = time_change
            
            cur_Canvas  = str(device.getCanvas())
            cur_Light   = str(device.getLightFlow())

            if (cur_Canvas != Dv_Params[0]["canvas"]) or (cur_Light != Dv_Params[1]["lightflow"]):
                print("Device had changed")
                device.setParams(cur_Canvas, cur_Light)
                Dv_Params[0]["canvas"] = str(device.getCanvas())
                Dv_Params[1]["lightflow"] = str(device.getLightFlow())
                Dv_Params[2]["illumination"] = str(device.getIllumination())
                print(Dv_Params)
                socketio.emit("DeviceChanged", Dv_Params, broadcast=True)
                print("Sent data to clients")

notifDeviceChange = threading.Thread(target=notifDeviceChange_handle, args=())
notifDeviceChange.start()

if(__name__ == "__main__"):
    socketio.run(app, host=argv[1], port=int(argv[2]), debug=False)
