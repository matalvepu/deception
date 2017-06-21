import csv
import glob
import os
import sys

def compute_feature_change(f_name,i_e,w_s,lag,window):
	if (i_e-window) < 0:
		left=0
	else:
		left=i_e-window

	right_s=i_e+lag
	right_e=right_s+window

	if right_s > w_s:
		right_s=w_s

	if right_e > w_s+window:
		right_e=w_s+window

	s_l=[0]*17
	c_l=0
	s_r=[0]*17
	c_r=0

	with open(f_name) as f:
		header = f.readline()
		for line in f:
			line=line[:-1].split(',')
			a=line[396:]
			a.pop(-2) #remove au28_c because file does not have au28_r
			a=[float(x) for x in a]
			time=float(line[1])	
			if time>=left and time<i_e:
				c_l+=1
				for i in range(len(s_l)):
					# s_l[i]+=a[i+17]
					#s_l[i]+=(a[i]*a[i+17])/float(5)
					s_l[i]+=a[i] #only au_r
			if time>=right_s and time<=right_e:
				c_r+=1
				for i in range(len(s_r)):
					#s_r[i]+=a[i+17]
					#s_r[i]+=(a[i]*a[i+17])/float(5)
					s_r[i]+=a[i] 	#only au_r

	s_l=[float(x/c_l) for x in s_l]
	s_r=[float(x/c_r) for x in s_r]

	diff=[0.]*17
	for i in range(len(s_l)):
		diff[i]=s_r[i]-s_l[i]

	return diff



def get_feature_diff(f_name,time_intervals,lag,window):
	feature=[]
	for i in range(0,len(time_intervals),2):
		i_e=time_intervals[i]
		w_s=time_intervals[i+1]
		diff=compute_feature_change(f_name,i_e,w_s,lag,window)
		feature.append(diff)
	return feature	


			
def get_time_interval(root,time_intervals):
	for interval in time_intervals:
		if root in interval:
			return interval[1:]

	return []

def write_csv(root,feature,lag,window):
	file_name="out_baseline_diff/au_r/baseline_diff_features_l_"+str(lag)+"_w_"+str(window)+".csv"
	with open(file_name, 'a') as out_f:
		wr = csv.writer(out_f)
		feature.insert(0,root)
		wr.writerow(feature)


f_name="baseline_annotations.csv"
time_intervals=[]
root_names=[]
with open(f_name) as f:
	header = f.readline()
	for line in f:
		line=line.split(',')
		line=line[:-1]
		root_names.append(line[0])
		interval=[line[0],float(line[2]),float(line[3]),float(line[6]),float(line[7]),float(line[10]),float(line[11]),float(line[14]),float(line[15]),float(line[18]),float(line[19])]
		time_intervals.append(interval)

f_name="silent_intervals.csv"
root_names_s=[]
with open(f_name) as f:
	for line in f:
		line=line.split(',')
		line=line[:-1]
		root_names_s.append(line[0])

s1_map={}

with open("list_s1_s2.csv") as f:
	header=f.readline()
	for line in f:
		line=line.split(',')
		root=line[0]
		s1_map[root]=float(line[1])

new50_files = glob.glob("/localdisk/deception/new50/OpenFace/*-W-*.txt")
classic61_files=glob.glob("/localdisk/deception/classic61/OpenFace/*-W-*.txt")
new_april=glob.glob("/localdisk/deception/new_april/OpenFace/*-W-*.txt")
april_2=glob.glob("/localdisk/deception/april2/OpenFace/*-W-*.txt")
open_face_files=new50_files+classic61_files+new_april+april_2

lag=float(sys.argv[1])
window=float(sys.argv[2])

for file in open_face_files:
	file_name=file[file.rfind('/')+1:]
	root=file_name[:file_name.rfind('-')-4]
	if root in s1_map and root in root_names and root in root_names_s:		
		intervals=get_time_interval(root,time_intervals)
		if not intervals:
			continue
		s1=s1_map[root]
		intervals=[x+s1 for x in intervals]
		if intervals:
			feature=get_feature_diff(file,intervals,lag,window)
			write_csv(root,feature,lag,window)






