# serial interval 
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

dt=1
t= [.0]#リストの初期化
x= [.0]
y= []
tdat=0.0
mu  = np.log(4.7**2/(2.9**2 + 4.7**2)**.5) #see https://jp.mathworks.com/help/stats/lognstat.html
sig = np.log(2.9**2/4.7**2 + 1.0)**.5 #
sss=0
dat=0
while tdat < 20:
   tdat = tdat+dt
   t.append( tdat ) #リストへの追加
   dat = lognormal(sig,mu,tdat)
   sss=sss+dat
   x.append(dat)
   print(tdat,sss)
y=[x[i]/sss for i in range(len(x))]
print(sum(y))
#print(y)
#plt.plot(t,x)#, marker='o')
plt.plot(t,y, marker='o')
#plt.show() 
