from sklearn.cluster import KMeans
import numpy as np
import csv
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing
from sklearn.multiclass import OneVsRestClassifier
from sklearn import svm
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsOneClassifier
from sklearn import datasets
from sklearn.metrics.pairwise import cosine_similarity
import math
import sys


def get_baseline_features(root_name,baseline_features):
	for features in baseline_features:
		if features[0]==root_name:
			return features[1:]

	return []

def get_truth_label(root_name,truth_labels):
	for line in truth_labels:
		if line[0]==root_name:
			return line[1]
	return None

def write_csv(root_name,truth_label,count,lag,window):
	l=[]
	file_name="data/cosine_similarity/count_diff_l_"+str(lag)+"_w_"+str(window)+".csv"
	with open(file_name, 'a') as out_f:
		wr = csv.writer(out_f)
		l.append(root_name)
		l.append(truth_label)
		for c in count:
			l.append(c)
		wr.writerow(l)
	
def min_cosine_distance_index(feature,b_feature):
	similarities=cosine_similarity([feature], b_feature)
	max_val=max(similarities[0])
	return similarities[0].tolist().index(max_val)

lag=float(sys.argv[1])
window=float(sys.argv[2])

file_name="out_baseline_diff/baseline_diff_features_l_"+str(lag)+"_w_"+str(window)+".csv"
f = open(file_name)
csv_f = csv.reader(f)
baseline_features=[]
for line in csv_f:
	feature=[]
	feature.append(line[0])
	for i in range(1,len(line)):
		q=line[i]
		q=q[1:len(q)-1]
		q=q.split(',')
		q=[float(x)for x in q]
		feature.append(q)
	baseline_features.append(feature)

file_name="out_relevant_diff/relevant_diff_features_l_"+str(lag)+"_w_"+str(window)+".csv"
f = open(file_name)
csv_f = csv.reader(f)
relevant_features=[]
for line in csv_f:
	feature=[]
	feature.append(line[0])
	for i in range(1,len(line)):
		q=line[i]
		q=q[1:len(q)-1]
		q=q.split(',')
		q=[float(x)for x in q]
		feature.append(q)
	relevant_features.append(feature)

f = open("silent_intervals.csv")
csv_f = csv.reader(f)
truth_labels=[]
for line in csv_f:
	truth_labels.append([line[0],line[1]])


for r_features in relevant_features:
	root_name=r_features[0]
	r_features=r_features[1:]
	c=[0]*5
	b_feature=get_baseline_features(root_name,baseline_features)
	if not b_feature:
		continue
	truth_label=get_truth_label(root_name,truth_labels)
	if not truth_label:
		continue
	for feature in r_features:
		index=min_cosine_distance_index(feature,b_feature)
		c[index]+=1

	write_csv(root_name,truth_label,c,lag,window)





	