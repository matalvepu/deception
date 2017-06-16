import csv
import glob
import os
import sys

def get_diff_fetaure(f_name,interval,lag,window):

	i_e=float(interval[0])
	w_s=float(interval[1])
	
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
			a.pop(-2)
			a=[float(x) for x in a]
			time=float(line[1])	
			if time>=left and time<i_e:
				c_l+=1
				for i in range(len(s_l)):
					if i>0:
						s_l[i]+=(a[i]*a[i+17])/float(5)
					else:
						s_l[i]+=a[i]
			if time>=right_s and time<=right_e:
				c_r+=1
				for i in range(len(s_r)):
					if i>0:
						s_r[i]+=(a[i]*a[i+17])/float(5)
					else:
						s_r[i]+=a[i]

	if c_l==0 or c_r==0:
		return []
	s_l=[float(x/c_l) for x in s_l]
	s_r=[float(x/c_r) for x in s_r]

	diff=[0.]*17
	for i in range(len(s_l)):
		diff[i]=s_r[i]-s_l[i]

	return diff

			
def get_time_interval(root,time_intervals):
	for interval in time_intervals:
		if root in interval:
			return interval[1:]

	return []

def write_csv(root,features,lag,window):
	file_name="out_relevant_diff/relevant_diff_features_l_"+str(lag)+"_w_"+str(window)+".csv"
	with open(file_name,'a') as out_f:		
	    wr = csv.writer(out_f)
	    features.insert(0,root)          
	    wr.writerow(features)

  
def get_q2(root_name,q2_list):
    for [root,q2] in q2_list:
        if root==root_name:
            return float(q2)
    return -1

def get_all_q2_time(filename):
    f = open(filename)
    csv_f = csv.reader(f)
    q2_list=[]
    for row in csv_f:
        if row[21]:
            q2_list.append([row[0],row[21]])

    return q2_list[1:]

   
filename="baseline_annotations.csv"
q2_list=get_all_q2_time(filename)

f_name="silent_intervals.csv"
time_intervals=[]
root_names_s=[]
f = open(f_name)
csv_f = csv.reader(f)
for line in csv_f:
	root_names_s.append(line[0])
	interval=line[2:]
	interval.insert(0,line[0])
	time_intervals.append(interval)


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
april2=glob.glob("/localdisk/deception/april2/OpenFace/*-W-*.txt")
open_face_files=new50_files+classic61_files+new_april+april2

lag=float(sys.argv[1])
window=float(sys.argv[2])

for file in open_face_files:
	file_name=file[file.rfind('/')+1:]
	root=file_name[:file_name.rfind('-')-4]
	if root in s1_map and root in root_names_s:		
		intervals=get_time_interval(root,time_intervals)
		if not intervals:
			continue
		s1=s1_map[root]
		q2=get_q2(root,q2_list)
		q2=q2+s1

		if intervals:
			feature_list=[]
			for interval in intervals:
				if(len(interval)<2):
					continue
				interval=interval.split(':')
				if float(interval[0])>q2:							
					feature=get_diff_fetaure(file,interval,lag,window)
					if feature:
						feature_list.append(feature)

			write_csv(root,feature_list,lag,window)

print("finish")