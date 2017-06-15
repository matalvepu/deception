import csv
import glob
import os
import sys

import numpy as np

import numpy as np
from sklearn import preprocessing
from random import shuffle

lags=[0.0,0.1,0.2,0.3,0.4,0.5]
# lags=[0.1]
windows=[0.8,0.9,1.0,1.1,1.2,1.3,1.5]
# windows=[0.8,0.9,1.0,1.1,1.2,1.3,1.5]

for lag in lags:
	for window in windows:
		os.system("python baseline_diff_features.py "+str(lag)+" "+str(window))
		os.system("python relevant_diff_features.py "+str(lag)+" "+str(window))
		os.system("python count_cosine.py "+str(lag)+" "+str(window))
		print(lag)
		print(window)
		print("******************")


print("test 2 finished ")