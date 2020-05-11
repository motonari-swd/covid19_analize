#chenge directory
#renamed from corona_graph6.2.py for github

import csv
import numpy as np
import sys
import re,os

#import seaborn as sns
import matplotlib.pyplot as plt
import japanize_matplotlib
import matplotlib.cm as cm


##### Date edit def #####
def date_sort(date_list):     #date_list=["15/04/2020","09/04/2020","15/03/2020"]
        new_date_list=[]
        #print(date_list)
        for d in date_list:
                new_date=d.split("/")[2]+"/"+d.split("/")[1]+"/"+d.split("/")[0] # d/m/y >>>y/m/d
                new_date_list.append(new_date)
        sorted_list=sorted(new_date_list)  
        #print(sorted_list)                                      # sort
        return sorted_list

def dmy_to_ymd(date_list):
        new_date_list=[]
        for d in date_list:
                new_date=d.split("/")[2]+"/"+d.split("/")[1]+"/"+d.split("/")[0] # d/m/y >>>y/m/d
                new_date_list.append(new_date)  
        return  new_date_list 

def Calendar(start_date,currentdate):
        month_date={1:31,2:29,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}  
        day_list=[]        
      
        s_year=int(start_date.split("/")[0])
        s_month=int(start_date.split("/")[1])
        s_day=int(start_date.split("/")[2])

        c_year=int(currentdate.split("/")[0])
        c_month=int(currentdate.split("/")[1])
        c_day=int(currentdate.split("/")[2])
        
        for year in range(s_year,c_year+1):
                for month in range(1,13):
                        for day in range(1,month_date[month]+1):
                                day_list.append(str(year)+"/"+str(month)+"/"+str(day))
        ###cut
        effectiv_date=False
        effectiv_list=[]
        for date in day_list:
                if date==start_date:
                        effectiv_date=True

                if effectiv_date:
                        effectiv_list.append(date)

                if date==currentdate:
                        effectiv_date=False                        
                        
        f_list=[]
        for date in effectiv_list:
                if len(str(date).split('/')[1])==1:
                        n_month='0'+str(date).split('/')[1]
                else:n_month=str(date).split('/')[1]

                if len(str(date).split('/')[2])==1:
                        n_day="0"+str(date).split('/')[2]
                else:n_day=str(date).split('/')[2]

                ndate=str(date).split('/')[0]+"/"+n_month+"/"+n_day
                f_list.append(ndate)
        return f_list
 
       

def date_reduction(cal):  #ex 2020/01/02 >>> 2
                          #   2020/01/01 >>> 2020/01/01
                          #   2020/02/01 >>> 2/1
        new_major=[]
        firstday_check=[]
        sunday_point=[] 
        for i,m in enumerate(cal):
                year =m.split("/")[0]
                month=m.split("/")[1]
                day  =m.split("/")[2]

                #if i==0:
                #        new_major.append(year+"/"+month.lstrip("0")+"/"+day.lstrip("0"))
                #        continue
                #if i==len(cal)-1:
                #        new_major.append(year+"/"+month.lstrip("0")+"/"+day.lstrip("0"))
                #        continue


                #sunday point
                #2020 01 05 is sunday
                if "2020/01/05" in cal and "2019/12/31" in cal:
                        if (i-5)%7==0:
                                sunday_point.append(i)


                                               
                if day=="01" and month=="01" :
                        new_major.append(year+"/"+month.lstrip("0")+"/"+day.lstrip("0"))
                        continue
                elif day=="01":
                        new_major.append(month.lstrip("0")+"/"+day.lstrip("0"))
                        firstday_check.append(i)
                        continue
                elif day=="30":
                        new_major.append("") 
                elif int(day)%5==0:
                        new_major.append(day.lstrip('0'))
                else:
                        #new_major.append(day.lstrip("0"))
                        new_major.append("")   
        return new_major,firstday_check ,sunday_point






##### Analize def #####
def infectivity(y_list,range_date):
        base=range_date
        
        new=[None]*len(y_list)

        """  
        for i in range(base,len(new)):
                base_list=[item for item in y_list[i-4:i-1] if not item==None]
                if (sum(base_list))==0:
                        new[i]=None
                        continue
                if y_list[i]==None:
                        new[i]=None
                        continue
        
                new[i]=y_list[i]*len(base_list)/(sum(base_list))
        """
        ave_list=range_average(y_list,range_date)
        for i in range(len(new)):
                if ave_list[i]==0 or ave_list[i]==None or y_list[i]==None:
                        new[i]=None   
                        continue    
                                 
                new[i]=y_list[i]/ave_list[i]
                #if new[i]==5:
                #        print(y_list[i],ave_list[i])
                #        sys.exit()
        
        return new           

def infectivity_w8(y_list,range_date):
        base=range_date
        
        new=[None]*len(y_list)


        ave_list=range_average_w8(y_list)
        for i in range(len(new)):
                if ave_list[i]==0 or ave_list[i]==None or y_list[i]==None:
                        new[i]=None   
                        continue    
                                 
                new[i]=y_list[i]/ave_list[i]
        return new

def infectivity_w8_2(y_list):  #### important culcuration 
        delay=9
        base=7
        new=[None]*len(y_list)
        ave_list=range_average_w(y_list)

        for i in range(3,len(new)-delay):
                #if ave_list[i]==0 or ave_list[i]==None or y_list[i+delay]==None:
                #        new[i]=None   
                #        continue  
  
                if ave_list[i]==0:
                        #new[i]=1000  
                        #continue 
                        ave_list[i]=0.00001
                if ave_list[i]==None or y_list[i+delay]==None:
                        new[i]=None   
                        continue
                #new[i]=y_list[i+delay]/ave_list[i]

                value=y_list[i+delay]/ave_list[i]
                if value>=1000:
                        value=1000
                new[i]=value
        return new 


def range_average(y_list,range_date):
        base=range_date
        new=[None]*len(y_list)  
        for i in range(base,len(new)):
                base_list=[item for item in y_list[i-7:i-1] if not item==None]
                #print("blist",base_list)
                if (sum(base_list))==0:
                        new[i]=0
                        continue
                #if y_list[i]==None:
                #        new[i]=None
                #        continue
                new[i]=(sum(base_list))/len(base_list)
        return new  

def range_average_w8(y_list):
        base=7
        
        ave=[None]*len(y_list)  
        for i in range(3,len(ave)-3):
                base_list=[item for item in y_list[i-3:i+3] if not item==None]
                #print("blist",base_list)
                if (sum(base_list))==0:
                        ave[i]=0
                        continue

                ave[i]=(sum(base_list))/len(base_list)

        ## 8 days delay
        new=[None]*8+ave
        new=new[:len(y_list)]
        return new 
    
def range_average_w(y_list):
        base=7
        
        ave=[None]*len(y_list)  
        for i in range(3,len(ave)-3):
                base_list=[item for item in y_list[i-3:i+3] if not item==None]
                if sum(base_list)==0:
                        ave[i]=0
                        continue
                ave[i]=(sum(base_list))/len(base_list)
        return ave 

def fill_in_missing(calendar,missingdate_dict):
        missing_date=list(set(calendar)-set(missingdate_dict.keys()))
        #missingdate_dict.update([(key,None) for key in missing_date])
        missingdate_dict.update([(key,0) for key in missing_date])
        return missingdate_dict













### Paramaters ###

#today="2020/4/29"
today=input("What day is it Today \nex 2020/4/20\n")
#langage="j"
langage=input("Select language in Japanese or English\n type e or j\n")

if today=="":today="2020/5/3"
        
formula=False
darkcolor=False

#dataset_type="europ"
#dataset_type="toyokei"
eort=input("Select dataset in the European Union or toyokeizai dataset.\ntype e or t\n")
print(eort)
if   eort is "e":dataset_type="europ"
elif eort is "t":dataset_type="toyokei"
else:
        print("type e or t")
        sys.exit()


color_list=[(1,0,0),(0,1,0),(0,0,1),(0.5,0.5,0)]*4


infective_analize=True
#analizes=["cases","average","infective","average_w8","infective_w8","average_w","infective_w8_2"]
#analizes=["cases"]
#analizes=["cases","average_w","infective_w8_2"]
#analizes=["cases","average_w","infective_w8_zoom","infective_w8_2"]
#analizes=["cases","average_w","infective_w8_zoom","infective_w8_2","inf_zoominout"]
analizes=["cases","average_w","infective_w8_2"]


range_date=7



if dataset_type is "europ":
        print("DATA europ")
        ### import data ###
        DATA = []
        #dataset="./Downloads/ダウンロード"
        #dataset="./European_Centre_data"
        dataset="./csv"
        with open(dataset) as d:
                #print(d)
                content=d.read()
                lines=content.split("\n")

                for line in lines:
                        _data=re.split(r',',line)
                        data=[]
                        for p in _data:
                                try:p=float(p)
                                except:pass
                                
                                data.append(p)
                        #if len(data)==1:continue
                        DATA.append(data)

        ### take data ###
        contaner={}
        for line in DATA[1:]:
                country=  line[6]
                date=     line[0]
                case=     line[4]
                death=    line[5]
                pop=      line[9]
                continent=line[7]

                if not country in contaner.keys():
                        contaner[country]=[[],[],[],[],[]] #{country:[ date list ],[value list]}
                #date_list=[]
                #value_list=[]
                
                contaner[country][0].append(date)
                contaner[country][1].append(case)
                contaner[country][2].append(death)
                contaner[country][3].append(pop)
                contaner[country][4].append(continent)

        """        
        ### data revers
        for key in contaner.keys():    
                contaner[key][0].reverse()
                contaner[key][1].reverse()
                contaner[key][3].reverse()
                contaner[key][2].reverse()
        """

nostack_select_countries=["Japan","South_Korea","Taiwan","Vietnam","Philippines","Indonesia","Thailand","Malaysia","Mongolia","Myanmar","Laos",
                          "Cambodia","Singapore","Timor_Leste","Italy","Germany","China","United_States_of_America","France","United_Kingdom","Brazil","Egypt","Sweden"]
japanes_countries=["日本","韓国","台湾","ベトナム","フィリピン","インドネシア","タイ","マレーシア","モンゴル","ミャンマー","ラオス",
                    "カンボジア","シンガポール","東ティモール","イタリア","ドイツ","中国","アメリカ","フランス","イギリス","ブラジル","エジプト","スウェーデン"]


if dataset_type is "toyokei":
        print("DATA toyokei")
        select_countries= ["Japan"]
        japanes_countries=["日本"]
        ### import data ###
        DATA = []
        #dataset="./toyokei_data"
        dataset="./summary.csv"
        with open(dataset) as d:
                content=d.read()
                lines=content.split("\n")

                for line in lines:
                        _data=re.split(r',',line)
                        data=[]
                        for p in _data:
                                try:p=int(p)
                                except:pass
                                
                                data.append(p)
                        if len(data)==1:continue
                        DATA.append(data)

        ### take data ###
        contaner={}
        for il,line in enumerate(DATA[1:]):
                country=  "Japan"

                #print("\n",line)
                for i in range(3):
                        if line[i]<10:
                                line[i]="0"+str(line[i])
                        else:
                                line[i]=str(line[i])
                #print(line)

                date=     line[2]+"/"+line[1]+"/"+line[0]

                #print(line[3])
                if il==0:
                        case=line[3]
                else:
                        #print("pre",case)
                        case=line[3]-sum(contaner[country][1])#cansel ruiseki 
                        #print(case)
                #death=    line[5]
                pop=     125960000 
                #continent=line[7]

                if not country in contaner.keys():
                        contaner[country]=[[],[],[],[],[]] #{country:[ date list ],[value list]}
                #date_list=[]
                #value_list=[]
                
                contaner[country][0].append(date)
                contaner[country][1].append(case)
                #contaner[country][2].append(death)
                contaner[country][3].append(pop)
                #contaner[country][4].append(continent)


 
print(contaner["Japan"][1])
### GRAF ###

cal=Calendar("2019/12/31",today)
xlim=[30,len(cal)+1]
model=[0]*len(cal)
print(cal)
for i_country,i_japanes in zip(nostack_select_countries,japanes_countries):
        select_countries=[i_country]
        japanes_countries=[i_japanes]
        print("\n################\n",select_countries,japanes_countries)




        fig = plt.figure(figsize=(15*1.618,5*len(analizes)))

        #fig, ax = plt.subplots(figsize=(20,10*len(analizes)),facecolor=(1,1,1),edgecolor=(0,0.2,0),linewidth=2)
        #ax = plt.gca()

        import japanize_matplotlib

        axlist=[]
        for a,analize in enumerate(analizes):
                max_value=0
                print("\n",analize,a,len(analizes))


                if not "infective_w8_2" in analizes:
                        axlist.append(plt.subplot(len(analizes),1,a+1)) 
                else:
                        if not analize=="infective_w8_2":
                                axlist.append(plt.subplot((len(analizes)-1)*2,1,a+1))
                        else:
                                axlist.append(plt.subplot(2,1,2))





                ### axis plot 
                cal=Calendar("2019/12/31",today)
                model=[0]*len(cal)
                axlist[a].plot(cal, model, linewidth=0.01)


                ### analize and plot ###
                for i,country in enumerate(select_countries) : 
                        print("\n",country)
                        
                        x_list=dmy_to_ymd(contaner[country][0]) #date
                        y_list=contaner[country][1] #cases
                        population=contaner[country][3][0]

                        #print(x_list)
                        ### sort date with cases
                        sort_dic={}
                        for x,y in zip(x_list,y_list):
                                sort_dic[x]=y
                        #print(sort_dic)

                        sort_dic=fill_in_missing(cal,sort_dic)  #fill in missing date by None
                        x_list=sorted(sort_dic.keys())
                        #print("#4",sort_dic.keys())
                        y_list=[sort_dic[date] for date in x_list]

                        #print(x_list,y_list)
                        #sys.exit()

                        if analize=="cases":
                                #print(x_list,y_list)
                                #print(len(x_list),len(y_list))
                                #sys.exit()
                                pass

                        if analize=="average":
                                y_list=range_average(y_list,range_date)
                        if analize=="average_w8":
                                y_list=range_average_w8(y_list)
                        if analize=="average_w":
                                y_list=range_average_w(y_list)
                        if analize=="infective":
                                y_list=infectivity(y_list,range_date)
                                delay=4         
                                y_list=y_list[delay:]+[None]*delay
                        if analize=="infective_w8":
                                y_list=infectivity_w8(y_list,range_date)
                                delay=4         
                                y_list=y_list[delay:]+[None]*delay
                        if analize=="infective_w8_2" or analize=="infective_w8_zoom" or analize=="inf_zoominout":
                                y_list=infectivity_w8_2(y_list)


                        #print('\nx=',x_list,"\ny=",y_list)
                        #ax.plot(x_list, y_list, linewidth=2, color=color_list[i%11],label=country,alpha=0.8,marker=".")
                        #plt.plot(x_list, y_list, linewidth=1.5,label=japanes_countries[i],alpha=1,marker=None,linestyle = "solid",color=cm.nipy_spectral(i/(len(select_countries))))

                        c_lab=japanes_countries[i]
                        if langage is "e":
                                c_lab=select_countries[i]

                        if len(select_countries)==1:
                                if not darkcolor:
                                        plt.plot(x_list, y_list, linewidth=2,label=c_lab,alpha=1,marker='.',linestyle = "solid",color=(0.4,0,0.9))
                                else:
                                        plt.plot(x_list, y_list, linewidth=2,label=c_lab,alpha=1,marker='.',linestyle = "solid",color=(0.87,0.9,0.8))

                                    
                                        

                        else:
                                plt.plot(x_list, y_list, linewidth=2,label=c_lab,alpha=1,marker='.',linestyle = "solid",color=cm.nipy_spectral((i+0.1)/(len(select_countries))))

                        _max=float(max([i for i in y_list if i is not None]))
                        if max_value<=_max: max_value=_max


                print("plot finish")






                if analize=="cases":
                        #ax.set_ylabel('New cases par day',fontsize=20)
                        axlist[a].set_ylabel("新規感染者数"+r"$N$"+"[人/日]",fontsize=30)
                        if langage is "e":
                                #axlist[a].set_ylabel(r"$N$"+"[person/day]",fontsize=30)
                                axlist[a].set_ylabel(r"$N^{\rm{obs}}$"+"\n[person/day]",fontsize=22)                                
                        plt.ylim([0,max_value*6/5])


                if analize=="average":
                        axlist[a].set_ylabel(str(range_date)+"日前までの平均値"+r"$\overline{N}$"+" [人]",fontsize=30)
                        plt.text(15,max_value*4/5,r"$\overline{N}(i)=\frac{1}{7}\sum^{i-1}_{k=i-7}N(k)$", size=30,bbox={"facecolor":(0.98,0.98,0.98)})
                        #plt.text(15,max_value*4/5,r"$N^{W8}(i)=\frac{1}{7}\sum_{k=-11}^{k-5}N(k)$", size=30,bbox={"facecolor":(0.98,0.98,0.98)})
                        plt.ylim([0,max_value*6/5])

                if analize=="average_w8":
                        axlist[a].set_ylabel("8日を中心とする一週間平均値"+r"$N^{W8}$"+" [人]",fontsize=30)
                        plt.text(15,max_value*4/5,r"$N^{W8}(i+8)=\frac{1}{7}\sum_{k=i-11}^{i-5}N(k)$", size=30,bbox={"facecolor":(0.98,0.98,0.98)})
                        plt.ylim([0,max_value*6/5])

                if analize=="average_w":
                        axlist[a].set_ylabel("一週間平均値"+r"$N^{\rm{W}}$"+" [人/日]",fontsize=30)
                        #axlist[a].set_ylabel("一週間平均値"+r"$N\rm{W}$"+" [人/日]",fontsize=30)
                        if langage is "e":
                                #axlist[a].set_ylabel(r"$N^{\rm{W}}$"+" [person/day]",fontsize=30)
                                #axlist[a].set_ylabel(r"$N^{\rm{W}}$"+"\n[person/day]",fontsize=25)
                                axlist[a].set_ylabel(r"$N^{\rm{obs,W}}$"+"\n[person/day]",fontsize=22)

                        if formula:
                                plt.text(40,max_value*4/5,   r"$N^{\rm{W}}(i)=\frac{1}{7}\sum_{k=i-3}^{i+3}N(k)$", size=30,bbox={"facecolor":(0.98,0.98,0.98)})
                                #_plt.text(40,max_value*4/5,   r"$N\rm{W}(i)=\frac{1}{7}\sum_{k=i-3}^{i+3}N(k)$", size=30,bbox={"facecolor":(0.98,0.98,0.98)})

                        plt.ylim([0,max_value*6/5])



                if analize=="infective":
                        #ax.set_ylabel('infectivity',fontsize=20)
                        axlist[a].set_ylabel('感染力'+r'$I$',fontsize=30)
                        plt.text(15,5,r"$I(i)=\frac{N(i+4)}{\overline{N}(i+4)}$", size=30,bbox={"facecolor":(0.98,0.98,0.98)})
                        #plt.text(15,5,r"$I^{W8}(i)=\frac{N(i+4)}{\overline{N}(i+4)}$", size=30,bbox={"facecolor":(0.98,0.98,0.98)})
                        axlist[a].hlines(1, xlim[0], xlim[1],color=(1,0,0))
                        plt.ylim([0,6])

                if analize=="infective_w8":
                        axlist[a].set_ylabel('感染力'+r'$I^{W8}$',fontsize=30)

                        plt.text(15,5,    r"$I^{W8}(i)=\frac{N(i+4)}{N^{W8}(i+4)}$", size=30,bbox={"facecolor":(0.98,0.98,0.98)})
                        axlist[a].hlines(1, xlim[0], xlim[1],color=(1,0,0))
                        plt.ylim([0,6])

                if analize=="infective_w8_2":
                        #axlist[a].set_ylabel('感染力'+r'$I^{\rm{W8}}$',fontsize=30)
                        axlist[a].set_ylabel('実効再生産数'+r'$R^{\rm{W8}}$',fontsize=30)
                        #axlist[a].set_ylabel('実効再生産数'+r'$R\rm{W8}$',fontsize=30)  
                        if langage is "e":                      
                                #axlist[a].set_ylabel(r'$R^{\rm{W8}}$',fontsize=30)  
                                axlist[a].set_ylabel(r'$R^{\rm{W9}}$',fontsize=30)  


                        if formula:
                                #plt.text(40,5,    r"$I^{\rm{W8}}(i)=\frac{N(i+8)}{N^{\rm{W}}(i)}$", size=30,bbox={"facecolor":(0.98,0.98,0.98)})
                                plt.text(40,5,    r"$R^{\rm{W8}}(i)=\frac{N(i+8)}{N^{\rm{W}}(i)}$", size=30,bbox={"facecolor":(0.98,0.98,0.98)})
                                #_plt.text(40,5,    r"$R\rm{W8}(i)=\frac{N(i+8)}{N\rm{W}(i)}$", size=30,bbox={"facecolor":(0.98,0.98,0.98)})

                        axlist[a].hlines(1, xlim[0], xlim[1],color=(1,0,0))
                        #plt.ylim([0,6])
                        #plt.ylim([0,3])
                        plt.ylim([0,10])
                
                        ## filling
                        y_list_forfill=y_list
                        for i,item in enumerate(y_list):
                                if item is None:
                                        y_list_forfill[i]=-1000
                        if not darkcolor:
                                plt.fill_between(x_list,y_list_forfill,facecolor='b',alpha=0.1) #fill
                        else:
                                plt.fill_between(x_list,y_list_forfill,facecolor=(0,1,1),alpha=0.4) #fill
                       
                if analize=="infective_w8_zoom":
                        #axlist[a].set_ylabel('感染力'+r'$I^{\rm{W8}}$',fontsize=30)
                        axlist[a].set_ylabel('実効再生産数'+r'$R^{\rm{W8}}$',fontsize=30)
                        #axlist[a].set_ylabel('実効再生産数'+r'$R\rm{W8}$',fontsize=30)
                        if langage is "e":
                                axlist[a].set_ylabel(r'$R^{\rm{W8}}$',fontsize=30)
                        
                        if formula:
                                #plt.text(40,5,    r"$I^{\rm{W8}}(i)=\frac{N(i+8)}{N^{\rm{W}}(i)}$", size=30,bbox={"facecolor":(0.98,0.98,0.98)})
                                plt.text(40,max_value*4/5,    r"$R^{\rm{W8}}(i)=\frac{N(i+8)}{N^{\rm{W}}(i)}$", size=30,bbox={"facecolor":(0.98,0.98,0.98)})
                                #_plt.text(40,max_value*4/5,    r"$R\rm{W8}(i)=\frac{N(i+8)}{N\rm{W}(i)}$", size=30,bbox={"facecolor":(0.98,0.98,0.98)})
                        axlist[a].hlines(1, xlim[0], xlim[1],color=(1,0,0))
                        plt.ylim([0,max_value*10.5/10])
                        ## filling
                        y_list_forfill=y_list
                        for i,item in enumerate(y_list):
                                if item is None:
                                        y_list_forfill[i]=-1000
                        if not darkcolor:
                                plt.fill_between(x_list,y_list_forfill,facecolor='b',alpha=0.1) #fill
                        else:
                                plt.fill_between(x_list,y_list_forfill,facecolor=(0,1,1),alpha=0.4) #fill
                

                if analize=="inf_zoominout":

                        ## Right ##
                        ### "infective_w8_zoom"
                        #axlist[a].set_ylabel('感染力'+r'$I^{\rm{W8}}$',fontsize=30)
                        axlist[a].set_ylabel('実効再生産数'+r'$R^{\rm{W8}}$',fontsize=30)
                        #axlist[a].set_ylabel('実効再生産数'+r'$R\rm{W8}$',fontsize=30)
                        if langage is "e":
                                axlist[a].set_ylabel(r'$R^{\rm{W8}}$',fontsize=30)
                        
                        if formula:
                                #plt.text(40,5,    r"$I^{\rm{W8}}(i)=\frac{N(i+8)}{N^{\rm{W}}(i)}$", size=30,bbox={"facecolor":(0.98,0.98,0.98)})
                                plt.text(40,max_value*4/5,    r"$R^{\rm{W8}}(i)=\frac{N(i+8)}{N^{\rm{W}}(i)}$", size=30,bbox={"facecolor":(0.98,0.98,0.98)})
                                #_plt.text(40,max_value*4/5,    r"$R\rm{W8}(i)=\frac{N(i+8)}{N\rm{W}(i)}$", size=30,bbox={"facecolor":(0.98,0.98,0.98)})
                        axlist[a].hlines(1, xlim[0], xlim[1],color=(1,0,0))
                        plt.ylim([0,max_value*10.5/10])
                        ## filling
                        y_list_forfill=y_list
                        for i,item in enumerate(y_list):
                                if item is None:
                                        y_list_forfill[i]=-1000
                        if not darkcolor:
                                plt.fill_between(x_list,y_list_forfill,facecolor='b',alpha=0.1) #fill
                        else:
                                plt.fill_between(x_list,y_list_forfill,facecolor=(0,1,1),alpha=0.4) #fill

                        plt.yticks(fontsize=30)

                        #plt.twinx()
                        ax2=plt.twinx()
                        #plt.plot(x_list, y_list, linewidth=2,label=c_lab,alpha=1,marker='.',linestyle = "solid",color=(0.87,0.9,0.8))  
                        ax2.plot(x_list, y_list, linewidth=2,label=c_lab,alpha=1,marker='.',linestyle = "solid",color=(0.,0.4,0.7))  

                        ## Left ##

                        #axlist[a].set_ylabel('感染力'+r'$I^{\rm{W8}}$',fontsize=30)
                        axlist[a].set_ylabel('実効再生産数'+r'$R^{\rm{W8}}$',fontsize=30)
                        #axlist[a].set_ylabel('実効再生産数'+r'$R\rm{W8}$',fontsize=30)  
                        if langage is "e":                      
                                axlist[a].set_ylabel(r'$R^{\rm{W8}}$',fontsize=30)  

                        if formula:
                                #plt.text(40,5,    r"$I^{\rm{W8}}(i)=\frac{N(i+8)}{N^{\rm{W}}(i)}$", size=30,bbox={"facecolor":(0.98,0.98,0.98)})
                                plt.text(40,5,    r"$R^{\rm{W8}}(i)=\frac{N(i+8)}{N^{\rm{W}}(i)}$", size=30,bbox={"facecolor":(0.98,0.98,0.98)})
                                #_plt.text(40,5,    r"$R\rm{W8}(i)=\frac{N(i+8)}{N\rm{W}(i)}$", size=30,bbox={"facecolor":(0.98,0.98,0.98)})

                        #axlist[a].hlines(1, xlim[0], xlim[1],color=(1,0,0))
                        plt.hlines(1, xlim[0], xlim[1],color=(1,0,0))

                        #plt.ylim([0,6])
                        plt.ylim([0,3])
                
                        ## filling
                        y_list_forfill=y_list
                        for i,item in enumerate(y_list):
                                if item is None:
                                        y_list_forfill[i]=-1000
                        if not darkcolor:
                                plt.fill_between(x_list,y_list_forfill,facecolor=(0,1,1),alpha=0.1) #fill
                        else:
                                plt.fill_between(x_list,y_list_forfill,facecolor=(0,0.5,0.7),alpha=0.6) #fill


                

                #axlist[0].set_title("東アジアコロナウィルス感染力の推移(＊中国を除く)",fontsize=20)
                axlist[0].set_title("コロナウィルスの感染力推移"+"(〜"+today+")",fontsize=40)
                if langage is "e":
                        if not darkcolor:
                                #axlist[0].set_title("Reproduction index "+r"$R^{\rm{W8}}$"+"(〜"+today+")",fontsize=40)
                                axlist[0].set_title("Reproduction index "+r"$R^{\rm{W9}}$"+"(〜"+today+")",fontsize=40)
                        else:
                                #axlist[0].set_title("Reproduction index "+r"$R^{\rm{W8}}$"+"(〜"+today+")",fontsize=40,color="w")
                                axlist[0].set_title("Reproduction index "+r"$R^{\rm{W9}}$"+"(〜"+today+")",fontsize=40,color="w")                                
                plt.rcParams['axes.xmargin'] = 0        #(0,0)point
                #ax.set_xlabel('Date',fontsize=20)


                if a==len(analizes)-1:
                        axlist[a].set_xlabel('日付',fontsize=30)
                        if langage is "e":
                                axlist[a].set_xlabel('Date',fontsize=30)
                        #x ticks
                        xlocs,xlabs=plt.xticks(np.arange(len(cal)),date_reduction(cal)[0],fontsize=30,rotation=None) 
                else:
                        plt.xticks(np.arange(len(cal)),[""]*len(cal),color=None,fontsize=30,rotation=None) 

                if a==0:
                        plt.legend(prop={'size':40,},title=None,title_fontsize=15,loc='upper left', ncol=1,labelspacing=0,borderpad=0,framealpha=0.7,facecolor=(0.94,0.97,0.95),borderaxespad=0.3)
                        #print("max",max_value)
                if analize is "cases":
                        if dataset_type is "europ":
                                #plt.text(sum(xlim)/2, max_value*3.5/4, "European Centre for Disease Prevention and Control\n An agency of the European Union", alpha=0.7, size=40, ha="center", va="center",color="g")
                                plt.text(sum(xlim)/2, max_value*3.5/4, "European Centre for Disease Prevention and Control\n An agency of the European Union", alpha=0.7, size=30, ha="center", va="center",color="g")                                
                                #plt.text(sum(xlim)/2, max_value*2.2/4, "\n https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide", alpha=0.5, size=25, ha="center", va="center",color="g")
                                plt.text(sum(xlim)/2, max_value*2.2/4, "\n https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide", alpha=0.5, size=15, ha="center", va="center",color="g")

                        if dataset_type is "toyokei":
                                if not darkcolor:
                                        plt.text(sum(xlim)/2, max_value*3.5/4, "TOYOKEIZAI ONLINE", alpha=0.7, size=50, ha="center", va="center",color=(0.1,0.1,0.15))
                                        plt.text(sum(xlim)/2, max_value*2.2/4, "https://github.com/kaz-ogiwara/covid19/blob/master/data/summary.csv", alpha=0.5, size=25, ha="center", va="center",color=(0.1,0.1,0.15))
                                else:
                                        plt.text(sum(xlim)/2, max_value*3.5/4, "TOYOKEIZAI ONLINE", alpha=1, size=50, ha="center", va="center",color=(0.97,1,0.97))
                                        plt.text(sum(xlim)/2, max_value*2.2/4, "https://github.com/kaz-ogiwara/covid19/blob/master/data/summary.csv", alpha=1, size=25, ha="center", va="center",color=(0.97,1,0.97))  



                #y ticks
                if not analize is "infective_w8_2" and not analize is "inf_zoominout":
                        locs,labs=plt.yticks(fontsize=25)
                        #print( [ lab.get_text() for lab in labs ] )

                        labs=[str(int(item)) for item in locs]
                        for i in range(len(labs)):
                                if not i%3==0:
                                        labs[i]=""
                        #print(labs)

                        plt.yticks(locs,labs,fontsize=30)
                else:plt.yticks(fontsize=30)


                if analize in ["cases","average_w"]:
                        plt.twinx()
                        #if analize is "cases":ana=r"$N$"
                        if analize is "cases":ana=r"$N^{\rm{obs}}$"        
                        elif analize is "average_w": ana=r"$N^{\rm{obs,W}}$"

                        #plt.ylabel(ana+"/populataion\n["+r"$\times10^{-3}$"+"%]",fontsize=30)
                        plt.ylabel(ana+"/populataion\n["+r"$\times10^{-3}$"+"%]",fontsize=22)

                        #print(labs,population)

                        for i,l in enumerate(labs):
                                #print(i,l)
                                if l is "":continue
                                labs[i]=round(int(l)/population*100*1000,2)
                                #print(labs[i])
                        #print(labs)

                        plt.yticks(locs,labs,fontsize=30)
                        plt.tick_params(axis='y')



                axlist[a].grid(which="both")

                axlist[a].tick_params(direction = "inout", length = 15,width=1, colors = (0,0.1,0.04),which="major")

                for xpoint in date_reduction(cal)[1]:
                        axlist[a].vlines(xpoint, 0, max_value*7/5,color=(0.08,0.1,0.08),alpha=0.7,linewidth=2.5,linestyles="dashed")

                #draw sunday line
                for sunday in date_reduction(cal)[2]:
                        axlist[a].vlines(sunday  ,0,max_value*7/5,color=(1,0,0),alpha=0.9,linewidth=2,linestyles="dotted")
                        axlist[a].vlines(sunday-1,0,max_value*7/5,color=(0.2,0,1),alpha=0.9,linewidth=1.5,linestyles="dotted")# sutuday line

                plt.xlim(xlim)
                plt.subplots_adjust(hspace=0.4)
                #plt.tight_layout()
                plt.subplots_adjust(wspace=0.4, hspace=0.1)

                
        if darkcolor:
                for i in range(len(axlist)):
                        axlist[i].tick_params(color=(1,1,1),labelcolor="w",grid_color="w")
                        axlist[i].xaxis.label.set_color("w")
                        axlist[i].yaxis.label.set_color("w")
                        axlist[a].set_facecolor((0.1,0.15,0.23))
                plt.savefig(__file__.split(".")[0]+'_{para}_dark.png'.format(para=dataset_type+"_"+re.sub(r"\/",r"_",today)+str(select_countries)+str(analizes)+"langage="+langage+"_formula="+str(formula)), pad_inches=1.0 ,format="png",facecolor=(0,0.05,0.1))
        else:
                for i in range(len(axlist)):
                        axlist[i].set_facecolor((0.94,0.99,0.94))
                
                
                try:
                        #os.mkdir("./Pictures/"+__file__.rsplit(".",1)[0]+'_{para}/'.format(para=dataset_type+"_"+re.sub(r"\/",r"_",today)+str(analizes)+"langage="+langage+"_formula="+str(formula)))
                        #os.mkdir("./covid19_analize/figures/{p}".format(p=re.sub(r"\/",r"_",today)))
                        os.mkdir("./figures/{p}".format(p=re.sub(r"\/",r"_",today)))
                        print("try")

                except:pass
                #plt.savefig("./Pictures/"+__file__.rsplit(".",1)[0]+'_{para}/'.format(para=dataset_type+"_"+re.sub(r"\/",r"_",today)+str(analizes)+"langage="+langage+"_formula="+str(formula))+str(select_countries).strip('[\'').strip("\']")+'.png', pad_inches=1.0 ,format="png")
                #plt.savefig("./covid19_analize/figures/{p}/".format(p=re.sub(r"\/",r"_",today))+str(select_countries).strip('[\'').strip("\']")+'.png', pad_inches=1.0 ,format="png")
                plt.savefig("./figures/{p}/".format(p=re.sub(r"\/",r"_",today))+str(select_countries).strip('[\'').strip("\']")+'.png', pad_inches=1.0 ,format="png")
                
                print("save fig\n")
        
