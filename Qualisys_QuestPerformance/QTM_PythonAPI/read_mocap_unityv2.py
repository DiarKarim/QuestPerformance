from datetime import datetime
import time
import socket
import numpy as np
import pandas as pd
import scipy.signal as sci
import asyncio
import qtm

#*********************** Communication details ***************************
# Create UDP stuff

UDP_IP = "127.0.0.1"
UDP_PORT = 8787

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))


#************************** Define user functions ************************
def on_packet(packet, marker_only=[]):

    rawQuestMessage, addr = sock.recvfrom(256) # buffer size is 1024 bytes
    questMessage = rawQuestMessage.decode("utf-8")
    questData = questMessage.split(',')
    trialName = questData[0]
    timeX = float(questData[1])
    trigger = int(questData[2])
    print(trialName, timeX, trigger)
    
    header, markers = packet.get_3d_markers()
	
    i = 0
    for marker in markers:
        Xmpos = marker[0]
        Ympos = marker[1]
        Zmpos = marker[2]
        marker_only.append(np.array([Xmpos, Ympos, Zmpos, time.time(), i]))
        i = i+1

    if trigger == 2:
        xMPositions = [row[0] for row in marker_only]
        yMPositions = [row[1] for row in marker_only]
        zMPositions = [row[2] for row in marker_only]
        tMyme = [row[3] for row in marker_only]
        markerIdx = [row[4] for row in marker_only]
        timeDatMP = np.asarray(tMyme)

        tmpResampledp = list(zip(xMPositions,timeDatMP))
        tmpResp = pd.DataFrame(tmpResampledp,columns=['XUnityPos','MoCapTime'])
        tmpResp.insert(0, "YMoCapPos", yMPositions , True) 
        tmpResp.insert(0, "ZMoCapPos", zMPositions , True) 
        tmpResp.insert(0, "MarkerID", markerIdx , True) 

        # Save to file 
        outfile2 = open(str(time.time())+ trialName +'.json', "w")
        jsonTextp = tmpResp.to_json(orient="columns")
        outfile2.writelines(jsonTextp)
        outfile2.close()

        trigger = 3
        marker_only = []
        print("File saved!!!", trigger)

# ------------------------------------------------------------------------------------
    # i = 0
    # for marker in markers:
    #     Xmpos = marker[0]
    #     Ympos = marker[1]
    #     Zmpos = marker[2]
    #     # print("Marker", i, "Positions: ", Xmpos, " ", Ympos, " ", Zmpos)
    #     marker_only.append(np.array([Xmpos, Ympos, Zmpos, time.time(), i]))
    #     i = i+1
# ------------------------------------------------------------------------------------

async def setup():
    """ Main function """
    connection = await qtm.connect("127.0.0.1")
    if connection is None:
        return

    await connection.stream_frames(components=["3d"], on_packet=on_packet)


if __name__ == "__main__":
    data_path = "C:/Users/galeaj/admin/Documents/Projects/QTM_py/qualisys_python_sdk/examples/"
    pos_only, pos_time, time_elapsed = [],[],[]
    # global marker_only
    marker_only  = []

    trigger = 0 

    participantID = 'MyGroup_' # Ollie to change 
    condition = 1
    fname = 'test'
    f5 = data_path + "data_x.json"

    asyncio.ensure_future(setup())
    asyncio.get_event_loop().run_forever()

    sock.close()