from matplotlib import pyplot as plt
import math,sys
import numpy as np
from scipy import special
def lognormal(sig,mu,x):
   f=1/((2*np.pi)**0.5)/x/sig * np.exp( -(np.log(x)-mu)**2/2/sig**2)
   return f
def lognormaltot(sig,mu,x):
   f= 1/2+ 1/2*special.erf((np.log(x)-mu)/2**.5/sig)
   return f

def lognormalday(sig,mu,day):
   f=0
   if(abs(day)<1.1):
       return 0
   for i in range(101):
       x = day + (0.01*i-0.5)
       f = f + 1/((2*np.pi)**0.5)/x/sig * np.exp( -(np.log(x)-mu)**2/2/sig**2)
   return f/100.

epi=np.array([4.580e+02, 1.793e+03, 2.727e+03, 2.835e+03, 2.691e+03, 2.748e+03, 2.519e+03, \
     2.087e+03, 1.818e+03, 1.431e+03, 1.086e+03, 7.130e+02, 4.590e+02, 3.590e+02, \
     2.540e+02, 2.010e+02, 1.460e+02, 1.040e+02, 5.500e+01, 3.500e+01, 2.300e+01, \
     2.400e+01, 1.400e+01, 1.100e+01, 6.000e+00, 5.000e+00, 7.000e+00, 5.000e+00, \
     6.000e+00, 4.000e+00, 4.000e+00, 3.000e+00, 3.000e+00, 1.000e+00, 2.000e+00, \
     1.000e+00, 1.000e+00, 1.000e+00, 3.000e+00])
#epibin=[ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
# 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39]

totaln=sum(epi)

dt=0.1
t= [] #リストの初期化
x= []
y= []
tdat=0.0
sig=.4
mu=1.73
#convdat=[0]*100
convdat=[0]*30
sss=0
dat=0
for day in range(0,30):
    x.append(day)
    for mid in range(0,day):
        convdat[day]= convdat[day] + epi[day-mid]*lognormalday(sig,mu,mid)/totaln
        #    dat = dat + lognormalday(sig,mu,day)
#    y.append(dat)
#print(day,dat)
#print(x,len(x))
#print(y,len(y))

# ctot=[0]*30
# for i in range(0,30):
#    for day in range(0,30):
#       ctot[day] = ctot[day] + convdat[i+day]
    
# plt.plot(x,ctot, marker='x')
# plt.plot(x,y, marker='o')
plt.plot(x,convdat,marker='o')
#plt.show() 

