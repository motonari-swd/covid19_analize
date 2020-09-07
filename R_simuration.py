import sys
from matplotlib import pyplot as plt
#def Rm_to_N(R_model_list):

# open file
dataset="R_simulation_model"
with open(dataset) as d:
        R_model_list=[float(r) for r in d.read().split("\n") if not r==""]

import plotlognormal1 as lognormal
import covidepi2 as epi
import plotserial_1 as serial
#print(serial.y)
#print(serial.t)

S=serial.y
R=R_model_list
N=[0]*len(R)

print("S",S)
print("R",R)
print("N",N)

print("S",len(S))
print("R",len(R))
print("N",len(N))

for j in range(len(R)):
        for k in range(len(S)):
                i=j-k
                if i<0:N_input=1
                else:  N_input=N[i]
                
                if (j-i)>=len(S):continue
                try:N[j]+=R[j]*S[j-i]*N_input
                except:
                        print("j=",j,"i=",i)
                        sys.exit()
                print(N[j])
print("output N=",N)

import plotconv as conv
N_obs=[0]*len(R)
C=conv.convdat
for j in range(len(R)):
        for i in range(len(C)):
                if j-i<0:N_input=1
                else    :N_input=N[j-i]
                N_obs[j]+=C[i]*N_input

import covid19_graph as cg
delay=8
RW8=cg.infectivity_w8_2(N_obs,delay)
print("RW8 ",RW8)






### plot fig 1
import seaborn as sns
sns.set()
plt.figure(figsize=(15*1.618,5*4))

##fill in blanck with zeros
def fillin_withzero(alist,len_range):
        zeros=[0]*len_range
        print("alist",len(alist))
        for i in range(len(alist)):
                if i >=len_range:break
                zeros[i]=alist[i]
        newlist=zeros
        return newlist
#1-a
ax=plt.subplot(4,1,1)
#plt.ylabel("serial")
S=fillin_withzero(S,31)
plt.plot(S, marker='o')
plt.xlim([0,30])
#plt.ylim([0,2.5])
plt.text(0,max(S)*0.9,"(a)",fontsize=30)
plt.text(20,max(S)*0.5,"Serial interval",fontsize=40)
plt.xticks(fontsize=30)
plt.yticks(fontsize=20)
plt.ylabel("probability\ndensity per day",fontsize=30)

#1-b
ax=plt.subplot(4,1,2)
#plt.title("fig.1")
#plt.ylabel("lognormal")
o_i=fillin_withzero(lognormal.y,31)
plt.plot(o_i, marker='o')
plt.xlim([0,30])
#plt.ylim([0,2.5])
plt.text(0,max(o_i)*0.9,"(b)",fontsize=30)
plt.text(20,max(o_i)*0.5,"Onset - Infected",fontsize=40)
plt.xticks(fontsize=30)
plt.yticks(fontsize=20)
plt.ylabel("probability\ndensity per day",fontsize=30)

#1-c
ax=plt.subplot(4,1,3)
#plt.ylabel("confimed-onset")
c_o=fillin_withzero(epi.data,31)
#plt.plot(c_o, marker='o')
plt.bar(range(31),c_o,width=1)
plt.xlim([0,30])
#plt.ylim([0,2.5])
plt.text(0,max(c_o)*0.9,"(c)",fontsize=30)
plt.text(20,max(c_o)*0.5,"Confirmed - Onset",fontsize=40)
plt.xticks(fontsize=30)
plt.yticks(fontsize=20)
plt.ylabel("person",fontsize=30)

#1-d
ax=plt.subplot(4,1,4)
#plt.ylabel("covolution")
C=fillin_withzero(C,31)
plt.plot(C, marker='o')
plt.xlim([0,30])
#plt.ylim([0,2.5])
plt.text(0,max(C)*0.9,"(d)",fontsize=30)
plt.text(20,max(C)*0.5,"Confirmed - Infected",fontsize=40)
plt.xticks(fontsize=30)
plt.yticks(fontsize=20)
plt.ylabel("probability\ndensity per day",fontsize=30)
plt.xlabel("Day",fontsize=30)




plt.savefig("fig1.png")


### plot fig 2
import seaborn as sns
sns.set()
plt.figure(figsize=(15*1.618,5*4))
#xlim=[1,len(RW8)]
xlim=[11,72]
#xlim=[-9,62]
axlist=[]

#2-a
axlist.append(plt.subplot(4,1,1))
#plt.title("fig.2")
#plt.ylabel("R model")
plt.plot(R, marker='o')
#plt.grid()
plt.text(11,1.48,"(a)",fontsize=30)
#plt.text(60,1.5,r"$R(i)$",fontsize=40)
plt.text(60,1.1,r"$R(i)$",fontsize=40)
plt.xticks(range(0,90,10),range(-20,70,10),fontsize=30)
plt.yticks(fontsize=30)
plt.xlim(xlim)
#plt.ylim([0,2.5])
plt.ylim([0.9,1.6])


#2-b
axlist.append(plt.subplot(4,1,2))
#plt.ylabel("N")
plt.plot(N, marker='o')
#plt.grid()
plt.text(11,20,"(b)",fontsize=30)
plt.text(60,10,r"$N(i)$",fontsize=40)
plt.xticks(range(0,90,10),range(-20,70,10),fontsize=30)
plt.yticks(fontsize=30)
plt.xlim(xlim)
plt.ylim([0,25])

#2-c
axlist.append(plt.subplot(4,1,3))
#plt.ylabel("N obs")
plt.plot(N_obs, marker='o')
#plt.grid()
plt.text(11,20,"(c)",fontsize=30)
plt.text(60,8,r"$N^{\rm{obs}}(i)$",fontsize=40)
plt.xticks(range(0,90,10),range(-20,70,10),fontsize=30)
plt.yticks(fontsize=30)
plt.xlim(xlim)
plt.ylim([0,25])

#2-d
axlist.append(plt.subplot(4,1,4))
#plt.ylabel("RW8")
plt.plot(RW8, marker='o')
#plt.grid()
#plt.ylim([0,2.5])
plt.ylim([0.9,1.6])
#plt.text(11,2,"(d)",fontsize=30)
plt.text(11,1.48,"(d)",fontsize=30)
#plt.text(60,1.5,r"$R^{\rm{W8}}(i)$",fontsize=40)
plt.text(60,1.1,r"$R^{\rm{W8}}(i)$",fontsize=40)
plt.xticks(range(0,90,10),range(-20,70,10),fontsize=30)
plt.yticks(fontsize=30)
plt.xlim(xlim)
plt.xlabel("Day",fontsize=30)

for i in range(len(axlist)):
        ax=axlist[i]
        axlist[i]
        ax.vlines(20,-5,30)
        ax.vlines(50,-5,30)
        
#print(RW8)
plt.savefig("fig2.png")


