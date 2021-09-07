from datetime import datetime
import time
# import daqmx
import matplotlib.pyplot as plt
import socket
import numpy as np
import sys
import winsound
from threading import Thread

import pandas as pd
import scipy.signal as sci
# import nidaqmx
# from plot_data_stream import PlotDataStream
#from thread import start_new_thread

#*************************************************************************
#*********************** Communication details ***************************
#*************************************************************************
# Create UDP stuff

UDP_IP = "127.0.0.1"
UDP_PORT = 8787

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))


#*************************************************************************
#************************** Define user functions ************************
#*************************************************************************

def init_readForce(tsk1,S2,times,bias=np.zeros(6)):
        data  = tsk1.read()
        data_cal = np.array(CalibrateForce(data[0][0],S2)) - bias

        return data_cal


def readForce(tsk1,S2,times,bias=np.zeros(6)):
        data  = tsk1.read()
        data = np.array(data[0][0])
        return data 


def CalibrateForce(rawForce,S2):
        fx = np.divide(np.dot(rawForce,np.transpose(S2[0,[0,1,2,3,4,5]])),S2[0,6])
        fy = np.divide(np.dot(rawForce,np.transpose(S2[1,[0,1,2,3,4,5]])),S2[1,6])
        fz = np.divide(np.dot(rawForce,np.transpose(S2[2,[0,1,2,3,4,5]])),S2[2,6])
        tx = np.divide(np.dot(rawForce,np.transpose(S2[3,[0,1,2,3,4,5]])),S2[3,6])
        ty = np.divide(np.dot(rawForce,np.transpose(S2[4,[0,1,2,3,4,5]])),S2[4,6])
        tz = np.divide(np.dot(rawForce,np.transpose(S2[5,[0,1,2,3,4,5]])),S2[5,6])

        forces_cal = [fx, fy, fz, tx, ty, tz]
        return forces_cal


def beepSound():
        frequency = 1000  # Set Frequency in Hertz
        duration = 100  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)


def ReadPosition(skt,headerVal,bufsize):
        pos_data, pos_addr_rec = skt.recvfrom(bufsize)
        posgnd = np.array((pos_data.split(', '))).astype(float)
        if posgnd[0] == headerVal:
                return posgnd[1::]
        # else: 
        #       return np.zeros(12)
        # return np.array((pos_data.split(', '))).astype(float)

        # return np.array((pos_data.split('\t'))).astype(float)


def ReadExperiment(skt1):
        expData, exp_addr_rec = skt1.recvfrom(128)
        # print expData 
        return expData
        # return np.array((expData.split(', '))).astype(int)


def SaveData(txWriter1,data):
        #txWriter1.write(str(data.save) + "\n") # format to a better way
        # print type(data)
        # print data.shape
        np.savetxt(txWriter1, data, delimiter='\t')


def column(arr, i):
        return [row[i] for row in arr]











import asyncio
import qtm

data_path = "C:/Users/galeaj/admin/Documents/Projects/QTM_py/qualisys_python_sdk/examples/"
pos_onlyre, marker_only, probeForce, touch_force, gnd_plate, pos_only, frc_time, pos_time, time_elapsed = [],[],[],[],[],[],[],[],[]
trigger = 0 

participantID = 'MyGroup_' # Ollie to change 
condition = 1
fname = 'test'
f5 = data_path + "data_x.json"

def on_packet(packet):
    """ Callback function that is called everytime a data packet arrives from QTM """
    # print("Framenumber: {}".format(packet.framenumber))
    header, markers = packet.get_3d_markers()
    # print("Component info: {}".format(header))
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
    # pos_only.append(ReadPosition(sock,99999,bufSizes))
    rawQuestMessage, addr = sock.recvfrom(1024*2) # buffer size is 1024 bytes
    questMessage = rawQuestMessage.decode("utf-8")

    questData = questMessage.split(',')
    # print("Msg: " ,message)

    # xPos = float(questData[0])
    # yPos = float(questData[1])
    # zPos = float(questData[2])
    # timeX = float(questData[3])
    # trigger = int(questData[4])

    trialName = float(questData[0])
    timeX = float(questData[1])
    trigger = int(questData[2])

    pos_only.append(np.array([trialName, timeX, trigger]))
    print(trialName, timeX, trigger)

    # i = 0
    # for marker in markers:
    #     Xmpos = marker[0]
    #     Ympos = marker[1]
    #     Zmpos = marker[2]
    #     # print("Marker", i, "Positions: ", Xmpos, " ", Ympos, " ", Zmpos)
    #     marker_only.append(np.array([Xmpos, Ympos, Zmpos, time.time()]))
    #     i = i+1


    if trigger == 2:

        xMPositions = [row[0] for row in marker_only]
        yMPositions = [row[1] for row in marker_only]
        zMPositions = [row[2] for row in marker_only]
        tMyme = [row[3] for row in marker_only]
        markerIdx = [row[4] for row in marker_only]


        pos_onlyre = sci.resample(pos_only, len(marker_only))

        # trialPosition = np.asarray(pos_only)
        xPositions = [row[0] for row in pos_onlyre]
        yPositions = [row[1] for row in pos_onlyre]
        zPositions = [row[2] for row in pos_onlyre]
        tyme = [row[3] for row in pos_onlyre]

        timeDatP = np.asarray(tyme)
        timeDatMP = np.asarray(tMyme)

        tmpResampledp = list(zip(xPositions,timeDatP))
        tmpResp = pd.DataFrame(tmpResampledp,columns=['XUnityPos','UnityTime'])
        tmpResp.insert(0, "YUnityPos", yPositions , True) # Add x position to dataframe
        tmpResp.insert(0, "ZUnityPos", zPositions , True) 
        tmpResp.insert(0, "XMoCapPos", xMPositions , True) 
        tmpResp.insert(0, "YMoCapPos", yMPositions , True) 
        tmpResp.insert(0, "ZMoCapPos", zMPositions , True) 
        tmpResp.insert(0, "MoCapTime", timeDatMP , True) 
        tmpResp.insert(0, "MarkerID", markerIdx , True) 

        # tmpResp.insert(0, "XPosition", xPositions , True) # Add x position to dataframe
        # tmpResp.insert(0, "Trial", trialNump , True) # Add trial number to the dataframe 
        # tmpResp.insert(0, "Group_ID", participantIDxp , True) # Add participant id to dataframe

        # Save to file 
        outfile2 = open(str(time.time())+'test.json', "w")
        jsonTextp = tmpResp.to_json(orient="columns")
        outfile2.writelines(jsonTextp)
        outfile2.close()

		trigger = 3
        print("File saved!!!", trigger)
    	



# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
    i = 0
    for marker in markers:
        Xmpos = marker[0]
        Ympos = marker[1]
        Zmpos = marker[2]
        # print("Marker", i, "Positions: ", Xmpos, " ", Ympos, " ", Zmpos)
        marker_only.append(np.array([Xmpos, Ympos, Zmpos, time.time(), i]))
        i = i+1

    # i = 0
    # for marker in markers:
    #     # print("\t", marker)
    #     Xmpos = marker[0]
    #     Ympos = marker[1]
    #     Zmpos = marker[2]

    #     print("Marker", i, "Positions: ", Xmpos, " ", Ympos, " ", Zmpos)

    #     i = i+1



async def setup():
    """ Main function """
    connection = await qtm.connect("127.0.0.1")
    if connection is None:
        return

    await connection.stream_frames(components=["3d"], on_packet=on_packet)


if __name__ == "__main__":

    # marker_only, probeForce, touch_force, gnd_plate, pos_only, frc_time, pos_time, time_elapsed = [],[],[],[],[],[],[],[]
    asyncio.ensure_future(setup())
    asyncio.get_event_loop().run_forever()








# currentTrial = 0
# numTrials = 1

# trs = range(currentTrial, numTrials)

# for tr in trs:

#         probeForce, touch_force, gnd_plate, pos_only, frc_time, pos_time, time_elapsed = [],[],[],[],[],[],[]

#         sampleRate_pos = 200.0 # this number should be the same as set in Unity 

#         pos_frac = 1.0/sampleRate_pos

#         trialDuration = 5.0 # seconds
#         sC_frc = 0
#         sC_pos = 0

#         # raw_input("Enter when ready ...")

#         tocbuf = 0
#         ticbuf = time.time()

#         # print "\n \n Waiting to receive experiment info ...\n "
#         # expInfo.append(ReadExperiment(sock2))
#         # expInfoVar = ReadExperiment(sock2)

#         beepSound()
#         print ("\n \n *** Start Task Now ***\n \n")


#         toc = 0
#         tic = time.time()
        
#         # Main Thread runs experiment 
#         while toc < trialDuration:
#                 toc = time.time()-tic 
#                 try: 
#                         # # Force reading
#                         # if toc > (sC_frc * frc_frac):
#                         #         touch_force.append(readForce(task,S2_plate,time.time(),ft_bias_plate))
#                         #         # print(np.shape(readForce(task,S2_plate,time.time(),ft_bias_plate)))

#                         #         sC_frc += 1
#                         #         frc_time.append(time.time())

#                         # Position reading 
#                         if toc > (sC_pos * pos_frac):
#                                 # pos_only.append(ReadPosition(sock,99999,bufSizes))
#                                 data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
#                                 message = data.decode("utf-8")

#                                 positions = message.split(',')
#                                 # print("Msg: " ,message)

#                                 xPos = float(positions[0])
#                                 yPos = float(positions[1])
#                                 zPos = float(positions[2])
#                                 timeX = float(positions[3])
                                
#                                 pos_only.append(np.array([xPos, yPos, zPos, timeX]))
#                                 print(xPos)
                                
#                                 #print(type(pos_only))
#                                 #print(type(touch_force))

#                                 # print("zPos: " ,zPos)

#                                 sC_pos += 1
#                                 # pos_time.append(time.time())

#                         time_elapsed.append(time.time())                
#                 except Exception as e:
#                         print (e)
#                 except KeyboardInterrupt:
#                         sock.close()
#                         print ("\n \nSockets cleaned!!! \n \n ")


#         print ("\n \nTotal force samples collected:", sC_frc, " samples")
#         print ("Total position samples collected:", sC_pos, " samples")
#         print ("Time elapsed", toc, " seconds")
#         # print "\n \nObserved Force Frequency", sC_frc/toc, " Hz"
#         print ("Observed Position Frequency", sC_pos/toc, " Hz \n \n")
#         beepSound()
#         time.sleep(0.25)
#         beepSound()
#         task.stop()
#         print ("\n \n *** Stop Now ***\n \n")

        # Plot data here after every trial to check validity and ask for user response 
        # Responding for participant 

        # Prep data before saving to file 
participantID = 'MyGroup_' # Ollie to change 
condition = 1
fname = 'test'
f4 = data_storage + fname + "ID" + "_" + str(participantID) + "_Condition_" + str(condition) + "_Tr_" + str(tr) + "force.json"
f5 = data_storage + fname + "ID" + "_" + str(participantID) + "_Condition_" + str(condition) + "_Tr_" + str(tr) + "position.json"

# Positions
xPositions = np.asarray(pos_only[0:,0])
yPositions = np.asarray(pos_only[0:,1])
zPositions = np.asarray(pos_only[0:,2])
posTime = np.asarray(pos_only[0:,3])

plt.figure()
plt.plot(pos_only[0:,0],'r-o')
plt.plot(pos_only[0:,1],'g-o')
plt.plot(pos_only[0:,2],'b-o')
# plt.legend([len(xPositions), len(pos_only[0:,1]), len(pos_only[])])
plt.show()

timeDatP = np.asarray(posTime)
trialNump = np.repeat(str(tr),len(timeDatP),axis=None)
participantIDxp = np.repeat(participantID,len(timeDatP),axis=None)

tmpResampledp = list(zip(xPositions,timeDatP))
tmpResp = pd.DataFrame(tmpResampledp,columns=['Force','Time'])
# tmpResp.insert(0, "XPosition", xPositions , True) # Add x position to dataframe
tmpResp.insert(0, "YPosition", yPositions , True) # Add x position to dataframe
tmpResp.insert(0, "ZPosition", zPositions , True) # Add x position to dataframe
tmpResp.insert(0, "Trial", trialNump , True) # Add trial number to the dataframe 
tmpResp.insert(0, "Group_ID", participantIDxp , True) # Add participant id to dataframe

# Save to file 
outfile2 = open(f5, "w")
jsonTextp = tmpResp.to_json(orient="columns")
# jsonFile = json.dumps(jsonText, indent=4)  
outfile2.writelines(jsonTextp)
outfile2.close()


## Cleanup tasks
# try: 
sock.close()

# except: 
# print "Force sensor task objects cleaned up."