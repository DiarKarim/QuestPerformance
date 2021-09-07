# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

path = "C:/Users/galeaj-admin/AppData/LocalLow/DefaultCompany/QuestHandTrackingTest/"

fileName = "test008_Target_row_C6_Trial_7_.json"

df = pd.read_json(path + fileName)

#plt.plot(df.time[480:790])
plt.plot(df.zPos,'r')
plt.plot(df.time,'g')
#plt.legend(['Hand','Target'])