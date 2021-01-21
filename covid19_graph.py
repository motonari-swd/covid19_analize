#chenge directory
#renamed from corona_graph6.2.py for github

### import section ###
import csv
import numpy as np
import sys
import re,os
#import seaborn as sns
import matplotlib.pyplot as plt
import japanize_matplotlib
import matplotlib.cm as cm

import module_text_contena as tx


##### Date edit def #####
#########################
def date_sort(date_list):            #date_list=["15/04/2020","09/04/2020","15/03/2020"]
        new_date_list=[]
        for d in date_list:
                new_date=d.split("/")[2]+"/"+d.split("/")[1]+"/"+d.split("/")[0] # d/m/y >>>y/m/d
                new_date_list.append(new_date)
        sorted_list=sorted(new_date_list)  
        return sorted_list

def dmy_to_ymd(date_list):            # trance day/month/year >>> year/month/day
        new_date_list=[]
        for d in date_list:
                new_date=d.split("/")[2]+"/"+d.split("/")[1]+"/"+d.split("/")[0] # d/m/y >>>y/m/d
                new_date_list.append(new_date)  
        return  new_date_list 

def Calendar(start_date,currentdate):  # create no missing date list 
        month_date={1:31,2:29,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}  
        day_list=[]        
      
        s_year=int(start_date.split("/")[0])
        s_month=int(start_date.split("/")[1])
        s_day=int(start_date.split("/")[2])

        c_year=int(currentdate.split("/")[0])
        c_month=int(currentdate.split("/")[1])
        c_day=int(currentdate.split("/")[2])
        
        for year in range(s_year,c_year+1):#day_list is complete date for setting year range
                for month in range(1,13):
                        for day in range(1,month_date[month]+1):
                                day_list.append(str(year)+"/"+str(month)+"/"+str(day))
        ###cutting
        effectiv_date=False
        effectiv_list=[]   #comp datelist for setting range 
        for date in day_list:
                if date==start_date:
                        effectiv_date=True
                if effectiv_date:
                        effectiv_list.append(date)
                #if date==currentdate:
                if date==str(c_year)+"/"+str(c_month)+"/"+str(c_day):
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

def date_reduction(cal): #for tick date label
        #ex 2020/01/02 >>> 2
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
                        firstday_check.append(i)
                        continue
                elif day=="01":
                        new_major.append(month.lstrip("0")+"/"+day.lstrip("0"))
                        firstday_check.append(i)
                        continue
                #elif day=="30":
                elif day=="30" or day=="05":
                        new_major.append("") 
                elif int(day)%10==0:
                        new_major.append(day.lstrip('0'))
                else:
                        #new_major.append(day.lstrip("0"))
                        new_major.append("")   
        return new_major,firstday_check ,sunday_point

def restrict_line(langage):
        langage="e"
        if PR: langage="j"
        from matplotlib.patches import ArrowStyle
        ### import data ###
        DATA = []
        restrict="./japan_restrict"
        with open(restrict) as d:
                content=d.read()
        lines=content.split("\n")
        for line in lines:
                if line =="":continue
                _data=line.split()
                sdate=_data[0]+"/"+_data[1]+"/"+_data[2]
                fdate=_data[0]+"/"+_data[3]+"/"+_data[4]
                data=[]
                data.append(sdate)
                data.append(fdate)
                data.append(_data[5])
                data.append(_data[6])
                DATA.append(data)
        def date_to_ax(date,cal):
                for i ,idate in enumerate(cal):
                        if date==idate:
                                return i
        restrict_name_list=[]
        sdate_list=[]
        fdate_list=[]
        for irest in DATA:
                if langage=="j":restrict_name_list.append(irest[2]) 
                else:           restrict_name_list.append(re.sub(r"_",r" ",irest[3])) 
                        
                sdate_list.append(date_to_ax(irest[0],cal))  
                fdate_list.append(date_to_ax(irest[1],cal)) 
        #for i in range(len(axlist)):
        #        for j in range(len(restrict_name_list)):                
        #                axlist[i].vlines(float(xdate_list[j])  ,0,max_value*7/5,color=(1,0.4,0.8),alpha=0.9,linewidth=5,linestyles="dotted")
        
        #arrow_color=(0.99,0.,0.85)
        arrow_color=(0.99,0.,0.2)
        arrow_style=ArrowStyle('|-|', widthA=1.5, widthB=1.5)
        for j in range(len(restrict_name_list)):  
                """
                if j==2:
                        axlist[1].annotate("",xy=(sdate_list[j],4),xytext=(fdate_list[j],4)
                                                ,arrowprops=dict(arrowstyle=arrow_style,edgecolor=arrow_color,facecolor='#0000ff'))
                        axlist[1].annotate("",xy=(sdate_list[j],4),xytext=(fdate_list[j],4)
                                                ,arrowprops=dict(edgecolor=arrow_color,facecolor='#0000ff',width=8))
                        axlist[1].text(float(sdate_list[j]),4.5, restrict_name_list[j]  , size=20,color=arrow_color)

                else:
                        axlist[1].annotate("",xy=(sdate_list[j],8),xytext=(fdate_list[j],8)
                                                ,arrowprops=dict(arrowstyle=arrow_style,edgecolor=arrow_color,facecolor='#0000ff'))
                        axlist[1].text(float(sdate_list[j]),8.5, restrict_name_list[j]  , size=30,color=arrow_color)
                """
                #__
                y_point=8.5-(8.5-2)/len(restrict_name_list)*j
                if PR:
                        y_point=2.5-(2.5-1)/len(restrict_name_list)*j
                #axlist[1].annotate("",xy=(fdate_list[j],y_point),xytext=(sdate_list[j],y_point),arrowprops=dict(edgecolor=arrow_color,facecolor=(0,0,1),width=8))
                axlist[-1].text(float(sdate_list[j]),y_point+0.1, restrict_name_list[j]  , size=30,color=arrow_color)  
                axlist[-1].hlines(y_point,fdate_list[j] ,sdate_list[j] ,color=(1,0,0.2),alpha=0.7,linewidth=20)

##### Analyzing def #####
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

def infectivity_w8_2(y_list,delay):  #### important culcuration 
        base=7
        new=[None]*len(y_list)
        ave_list=range_average_w(y_list)
        for i in range(3,len(new)-delay):
                #if ave_list[i]==0 or ave_list[i]==None or y_list[i+delay]==None:
                #        new[i]=None   
                #        continue  
  
                if ave_list[i+3]==0:
                        ave_list[i+3]=0.00001
                if ave_list[i+3]==None or y_list[i+delay]==None:
                        new[i]=None   
                        continue
                value=y_list[i+delay]/ave_list[i+3]
                if value>=1000:
                        value=1000
                new[i]=value
        if delay==15:
                _new=[None]*len(new)
                for i in range(len(new)):
                        if new[i] == 0:
                                _new[i]=0
                                continue
                        #if new[i] ==1000:
                        #        _new[i]=new[i]
                        #        continue
                        if new[i] == None:
                                _new[i]=None
                                continue
                        if new[i]<0:
                                _new[i]=None
                                continue
                        xxx=new[i]**(8/15)
                        #if xxx>1000:_new[i]=1000
                        #else:_new[i]=xxx
                        _new[i]=xxx
                new=_new
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

        for end in range(len(y_list)):
                if y_list[-(end+1)]!=None:break
        if end:
                _list=y_list[:-end]
        else:  _list=y_list
        _ave=[None]*len(_list) 
        for i in range(3,len(_list)-3):
                base_list=[item for item in _list[i-3:i+4] if not item==None]
                
                if sum(base_list)==0:
                        _ave[i]=0
                        continue
                _ave[i]=(sum(base_list))/7
        for i in range(len(_ave)):
                ave[i]=_ave[i]
        return ave

#def fill_in_missing(calendar,missingdate_dict):
#        missing_date=list(set(calendar)-set(missingdate_dict.keys()))
#        #missingdate_dict.update([(key,None) for key in missing_date])
#        missingdate_dict.update([(key,0) for key in missing_date])
#        return missingdate_dict

def fill_in_missing(missingdate_dict,start_date):#update to do not fill carrent day
        currentdate=sorted(missingdate_dict.keys())[-1]
        calendar=Calendar(start_date,currentdate)
        missing_date=list(set(calendar)-set(missingdate_dict.keys()))
        #missingdate_dict.update([(key,None) for key in missing_date])
        missingdate_dict.update([(key,0) for key in missing_date])
        return missingdate_dict

def CW8(cases_list):
        cases_list  =cases_list
        ave_list=range_average_w(cases_list)
        new=[None]*len(y_list)
        up=[None]*len(y_list)
        down=[None]*len(y_list)
        for i in range(0,len(new)-8):
                if ave_list[i+8]==0:
                        ave_list[i+8]=0.00001
                if ave_list[i+8]==None or cases_list[i+9]==None:
                        new[i]=None   
                        continue
                if ave_list[i+8]<0:
                        new[i]=None   
                        continue
                #cw8=(cases_list[i+9]-ave_list[i+8])/(ave_list[i+8])**0.5
                cw8=(cases_list[i+8]-ave_list[i+8])/ave_list[i+8]
                gap=ave_list[i+8]**0.5
                print("gaps",gap,cases_list[i+8],ave_list[i+8])

                up_cw8=(cases_list[i+8]-ave_list[i+8]+gap)/ave_list[i+8]
                down_cw8=(cases_list[i+8]-ave_list[i+8]-gap)/ave_list[i+8]

                #if value>=1000:
                #        value=1000
                new[i]=cw8
                up[i]=up_cw8
                down[i]=down_cw8
        for i in range(len(y_list)):
                print(new[i],up[i],down[i])
        return new ,up,down

def import_koroshodata():
        with open("pcr_positive_daily.csv") as f:
                data=f.read()
        lines=data.split("\n")[1:-1]
        print(lines)
        _date=[lines[i].split(",")[0] for i in range(len(lines))]
        positive=[int(lines[i].split(",")[1]) for i in range(len(lines))]

        date=[]
        for i in range(len(_date)):
                new_date=_date[i]
                date_split=_date[i].split("/")
                if len(date_split[1])==1:
                        new_date=date_split[0]+"/0"+date_split[1]
                else:
                        new_date=date_split[0]+"/"+date_split[1]
                if len(date_split[2])==1:
                        new_date+="/0"+date_split[2]   
                else:
                        new_date+="/"+date_split[2]
                date.append(new_date)
                                            
        print(date)
        print(positive)
        
        if len(date)!=len(positive):
                print("!!!check kouroughou data")
        return date,positive

if __name__=="__main__":
        ### Paramaters ###
        ##################

        ### setting Date range
        #today="2020/4/29"
        #today=input("What day is it Today \nex 2020/4/20\n")
        year="2021"
        year=input("What year")
        month=input("What month")
        day=input("What day")
        today=year+"/"+month+"/"+day

        ### setting langage
        #langage=input("Select language in Japanese or English\n type e or j\n")
        langage="e"
        #langage="j"

        ### setting 
        #dataset_type="europ"
        #dataset_type="toyokei"
        #eort=input("Select dataset in the European Union or toyokeizai dataset.\ntype e or t\n")
        eort=input("Select analized data,e or t or j\ne >>> ECDC\nt >>> Toyokeizai\nj >>>jag japan\nk >>>Koseirodousyo")
        print(eort)
        if   eort is "e":dataset_type="europ"
        elif eort is "t":dataset_type="toyokei"
        elif eort is "j":dataset_type="jag-japan"
        elif eort is "k":dataset_type="DATA kourou"
        else:
                print("Select analized data,e or t or j\ne >>> ECDC\nt >>> Toyokeizai\nj >>>jag japan")
                sys.exit()

        ### setting option
        formula=False
        darkcolor=False
        pile_up_nw=True
        delay=8#15
        #delay=int(input("dalay .ex8,15"))
        plot_kourou=False
        PR=True

        color_list=[(1,0,0),(0,1,0),(0,0,1),(0.5,0.5,0)]*4
        range_date=7
        infective_analize=True

        ### Analysis setting
        #analizes=["cases","average","infective","average_w8","infective_w8","average_w","infective_w8_2"]
        #analizes=["cases"]
        #analizes=["cases","average_w","infective_w8_2"]
        #analizes=["cases","average_w","infective_w8_zoom","infective_w8_2"]
        #analizes=["cases","average_w","infective_w8_zoom","infective_w8_2","inf_zoominout"]
        #analizes=["cases","average_w","infective_w8_2","CW8"]
        #analizes=["cases","average_w","infective_w8_2"]#until 2020 Oct 5
        analizes=["cases","average_w","N_log","Nw_log","infective_w8_2"]#new
        if PR:analizes=["cases","average_w","infective_w8_2"]

        ### Country list
        nostack_select_countries=["Japan","South_Korea","Taiwan","Vietnam","Philippines","Indonesia","Thailand","Malaysia","Mongolia","Myanmar","Laos",
                                  "Cambodia","Singapore","Timor_Leste","Italy","Germany","China","United_States_of_America","France","United_Kingdom","Brazil","Egypt","Sweden","Norway","Australia","Austria","Spain"]
        japanes_countries=["日本","韓国","台湾","ベトナム","フィリピン","インドネシア","タイ","マレーシア","モンゴル","ミャンマー","ラオス",
                            "カンボジア","シンガポール","東ティモール","イタリア","ドイツ","中国","アメリカ","フランス","イギリス","ブラジル","エジプト","スウェーデン","ノルウェー","オーストラリア","オーストリア","スペイン"]
        ### Data inport
        if dataset_type is "europ":
                print("DATA europ")
                ### import data ###
                DATA = []
                #dataset="./Downloads/ダウンロード"
                dataset="./European_Centre_data"
                #dataset="./csv"
                with open(dataset) as d:
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
                        if len(line)==1: continue
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
                        date=     line[2]+"/"+line[1]+"/"+line[0]

                        if il==0:
                                case=line[3]
                        else:
                                case=line[3]-sum(contaner[country][1])#cansel ruiseki 
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

        if dataset_type is "jag-japan":
                print("DATA Jag japan")
                select_countries= ["Japan"]
                japanes_countries=["日本"]
                contaner={}
                contaner["Japan"]=[[],[],[],[],[]] #{country:[ date list ],[value list]}
                import jag_japan_import as jj
                contaner["Japan"][0]=jj.date
                contaner["Japan"][1]=jj.confirm
                pop=     125960000
                contaner["Japan"][3].append(pop)

        if dataset_type is "DATA kourou":
                print("DATA kourou")
                kourou_data=import_koroshodata()
                select_countries= ["Japan"]
                japanes_countries=["日本"]
                contaner={}
                contaner["Japan"]=[[],[],[],[],[]] #{country:[ date list ],[value list]}
                contaner["Japan"][0]=kourou_data[0]
                contaner["Japan"][1]=kourou_data[1]   
                pop=     125960000  
                contaner["Japan"][3].append(pop) 


        ### setting fgraph ###
        ######################
        cal=Calendar("2019/12/31",today)
        xlim=[30,len(cal)+1]
        model=[0]*len(cal)

        for i_country,i_japanes in zip(nostack_select_countries,japanes_countries):
                select_countries=[i_country]
                japanes_countries=[i_japanes]

                if PR:          graph_num=3
                elif pile_up_nw:  graph_num=len(analizes)-2    
                else:           graph_num=len(analizes)

                fig = plt.figure(figsize=(15*1.618,5*graph_num))
                #fig, ax = plt.subplots(figsize=(20,10*len(analizes)),facecolor=(1,1,1),edgecolor=(0,0.2,0),linewidth=2)

                axlist=[]
                i_graph=1
                a_gap=0  #initial False for switch after pile up graph
                import japanize_matplotlib
                for a,analize in enumerate(analizes):
                        max_value=0
                        log=False
                        print("\n",analize,a,len(analizes)) 
                        if analize in ["N_log","Nw_log"]:
                                if analize is "N_log":
                                        print("N log >> cases")
                                        analize="cases"
                                if analize is "Nw_log":
                                        analize="average_w"
                                        print("Nw    >> acerage_W")
                                log=True

                        #switch analize symbol which is ram str
                        analize_symbol="?"
                        if analize is "cases":
                                analize_symbol=r"$N^{\rm{obs}}$"
                        if analize is "average_w":
                                analize_symbol=r"$N^{\rm{obs,W}}$"
                                if PR: analize_symbol=r"$N^{\rm{obs}}$(週平均)"
                        if analize is "infective_w8_2":
                                if delay==8:
                                        analize_symbol=r'$R^{\rm{W8}}$'
                                if delay==9:
                                        analize_symbol=r'$R^{\rm{W9}}$'
                                if delay==15:
                                        #analize_symbol=r'$R^{\rm{W15}}$'
                                        analize_symbol=r'$R^{\rm{W15}}**\frac{8}{15}$'
                        print(analize_symbol)


                        # set axs
                        if PR:
                                if analize=="cases":
                                        if a_gap:   #after pile up 
                                                a=a-a_gap
                                        axlist.append(plt.subplot(3,1,1))
                                elif analize=="average_w":
                                        a_gap+=1
                                        a=a-a_gap
                                        pass
                                elif analize=="infective_w8_2":
                                        if a_gap:   #after pile up 
                                                a=a-a_gap
                                        axlist.append(plt.subplot(3,1,(2,3)))

                        elif pile_up_nw:    #for pile up N graph and NW graph 
                                if analize=="average_w":
                                        a_gap+=1
                                        a=a-a_gap
                                else:
                                        if a_gap:   #after pile up 
                                                a=a-a_gap
                                        #axlist.append(plt.subplot(2,1,a+1))     #for pile up N on NW graph and RW8 
                                        axlist.append(plt.subplot(graph_num,1,a+1))
                                        
                        else:
                                if not "infective_w8_2" in analizes:
                                        axlist.append(plt.subplot(len(analizes),1,a+1)) 
                                else:
                                        if not analize=="infective_w8_2":
                                                axlist.append(plt.subplot((len(analizes)-1)*2,1,a+1))
                                        else:
                                                axlist.append(plt.subplot(2,1,2))




                        ### date shaft plot 
                        cal=Calendar("2019/12/31",today)   #make date list for setting range
                        model=[0]*len(cal)
                        axlist[a].plot(cal, model, linewidth=0.01)

                        ### analize and plot ###
                        ########################
                        for i,country in enumerate(select_countries) : 
                                print("\n",country)
                                if dataset_type is "DATA kourou":
                                        x_list=contaner[country][0]
                                else:
                                        x_list=dmy_to_ymd(contaner[country][0]) #sort "year,month,day"
                                y_list=contaner[country][1]             #cases list
                                population=contaner[country][3][0]      #population

                                # sort date with cases data
                                sort_dic={}
                                for x,y in zip(x_list,y_list):
                                        sort_dic[x]=y           
                                sort_dic=fill_in_missing(sort_dic,"2019/12/31")  #fill in missing date of xy list by None
                                x_list=sorted(sort_dic.keys())
                                y_list=[sort_dic[date] for date in x_list]


                                #if dataset_type is "DATA kourou":
                                #        y_list=y_list[1:]#delay one day
                                #        x_list=x_list[:-1]

                                # cutting today-1 data
                                x_list=x_list[:len(cal)-1]
                                y_list=y_list[:len(cal)-1]

                                ### analize ###
                                ###############
                                if analize=="cases":
                                        print(x_list,y_list)
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
                                        y_list=infectivity_w8_2(y_list,delay)
                                if analize=="CW8":
                                        y_list=CW8(y_list)
                                        

                                ### plot ###
                                ############
                                #print('\nx=',x_list,"\ny=",y_list)
                                #ax.plot(x_list, y_list, linewidth=2, color=color_list[i%11],label=country,alpha=0.8,marker=".")
                                #plt.plot(x_list, y_list, linewidth=1.5,label=japanes_countries[i],alpha=1,marker=None,linestyle = "solid",color=cm.nipy_spectral(i/(len(select_countries))))

                                c_lab=japanes_countries[i]
                                if langage is "e":
                                        c_lab=select_countries[i]

                                if len(select_countries)==1:
                                        if darkcolor:   plt.plot(x_list, y_list, linewidth=2,label=c_lab,alpha=1,marker='.',linestyle = "solid",color=(0.87,0.9,0.8))  #for dark color
                                        else:# normal color
                                                if analize in ["cases","infective_w8_2"]:
                                                        plot_color=(0.3,0.2,1)
                                                else:   
                                                        #plot_color=(0.2,0.6,0.2)
                                                        plot_color=(1,0.3,0.2)
                                                if pile_up_nw:
                                                        c_lab=analize_symbol
                                                if analize=="CW8":
                                                        plt.plot(x_list, y_list[0], linewidth=2,label=c_lab,alpha=1,marker='.',linestyle = "solid",color=plot_color)
                                                        plt.plot(x_list, y_list[1], linewidth=2,label=c_lab,alpha=0.75,marker='.',linestyle = "solid",color=(1,0.5,0.5))
                                                        plt.plot(x_list, y_list[2], linewidth=2,label=c_lab,alpha=0.75,marker='.',linestyle = "solid",color=(1,0.5,0.5))
                                                        print(y_list[0])
                                                        print(max([i for i in y_list if i is not None]))
                                                        plt.ylim([min([i for i in y_list[0] if i is not None]),max([i for i in y_list[0] if i is not None])])
                                                        y_list=y_list[0]
                                                #elif analize=="N_logscale":pass
                                                else: plt.plot(x_list, y_list, linewidth=2,label=c_lab,alpha=1,marker='.',linestyle = "solid",color=plot_color)
                                else: plt.plot(x_list, y_list, linewidth=2,label=c_lab,alpha=1,marker='.',linestyle = "solid",color=cm.nipy_spectral((i+0.1)/(len(select_countries))))

                                _max=float(max([i for i in y_list if i is not None]))
                                if max_value<=_max: max_value=_max
                        print("plot finish")
                        if pile_up_nw and analize=="cases":
                                cases_max_value=max_value



                        ### edit layout ###
                        ##############axis#
                        if analize=="cases":   ## @latest
                                if pile_up_nw:    #for pile up N graph and NW graph 
                                        axlist[a].set_ylabel("新規感染者数"+r"$N$"+"[人/日]",fontsize=30)
                                        if langage is "e":
                                                axlist[a].set_ylabel(r"$N^{\rm{obs}}$"+"\n[person/day]",fontsize=22)                                
                                        plt.ylim([0,max_value*6/5])

                                        if plot_kourou: #plot kourou positive data
                                                kourou_data=import_koroshodata()
                                                plt.plot(kourou_data[0],kourou_data[1],label="kouseiroudoushow",color=(0,1,1),alpha=1,marker='.',linestyle = "solid", linewidth=2)
                                else:
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

                        if analize=="average_w":  ## @latest
                                if pile_up_nw:    #for pile up N graph and NW graph 
                                        if formula:
                                                plt.text(40,max_value*4/5,   r"$N^{\rm{W}}(i)=\frac{1}{7}\sum_{k=i-3}^{i+3}N(k)$", size=30,bbox={"facecolor":(0.98,0.98,0.98)})
                                        plt.ylim([0,max_value*6/5])
                                else:
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
                                #Oct 5
                                Rw8_ave=range_average_w(y_list)

                                if PR:
                                        legend_lab=r'$R^{\rm{W8}}$(週平均)'
                                else:
                                        legend_lab=r'$R^{\rm{W8,W}}$'
                                plt.plot(x_list,Rw8_ave,label=legend_lab,color=(1,0.3,0.2),alpha=1,marker='.',linestyle = "solid", linewidth=2)

                                #axlist[a].set_ylabel('感染力'+r'$I^{\rm{W8}}$',fontsize=30)
                                axlist[a].set_ylabel('実効再生産数'+r'$R^{\rm{W8}}$',fontsize=30)
                                #axlist[a].set_ylabel('実効再生産数'+r'$R\rm{W8}$',fontsize=30)  
                                if langage is "e":                      
                                        #axlist[a].set_ylabel(r'$R^{\rm{W8}}$',fontsize=30)  
                                        #axlist[a].set_ylabel(r'$R^{\rm{W9}}$',fontsize=30)  
                                        axlist[a].set_ylabel(analize_symbol,fontsize=30)  

                                if formula:
                                        #plt.text(40,5,    r"$I^{\rm{W8}}(i)=\frac{N(i+8)}{N^{\rm{W}}(i)}$", size=30,bbox={"facecolor":(0.98,0.98,0.98)})
                                        plt.text(40,5,    r"$R^{\rm{W8}}(i)=\frac{N(i+8)}{N^{\rm{W}}(i)}$", size=30,bbox={"facecolor":(0.98,0.98,0.98)})
                                        #_plt.text(40,5,    r"$R\rm{W8}(i)=\frac{N(i+8)}{N\rm{W}(i)}$", size=30,bbox={"facecolor":(0.98,0.98,0.98)})

                                axlist[a].hlines(1, xlim[0], xlim[1],color=(0.4,0.6,0),alpha=0.8,linewidth=3)
                                #plt.ylim([0,6])
                                #plt.ylim([0,3])
                                plt.ylim([0,10])

                                if PR:
                                        plt.ylim([0,3])
                        
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


                        if analize is "CW8":
                                plt.hlines(1,xlim[0], xlim[1],color=(1,0,0))
                                plt.hlines(0,xlim[0], xlim[1],color=(0.2,0.2,0.2))
                                axlist[a].set_ylabel(r'$C^{\rm{W8}}$',fontsize=30)


                        ### set title ###
                        #################
                        #axlist[0].set_title("東アジアコロナウィルス感染力の推移(＊中国を除く)",fontsize=20)
                        axlist[0].set_title("コロナウィルスの感染力推移"+"(〜"+today+")",fontsize=40)
                        if langage is "e":
                                if not darkcolor:
                                        #axlist[0].set_title("Reproduction index "+r"$R^{\rm{W8}}$"+"(〜"+today+")",fontsize=40)
                                        #axlist[0].set_title("Reproduction index "+r"$R^{\rm{W9}}$"+"(〜"+today+")",fontsize=40)
                                        #axlist[0].set_title(select_countries[0]+"  Reproduction index "+r"$R^{\rm{W9}}$"+"(〜"+today+")",fontsize=40)
                                        #axlist[0].set_title(select_countries[0]+"  Reproduction index "+analize_symbol+"(〜"+today+")",fontsize=40)                                
                                        #axlist[0].set_title("Reproduction index "+analize_symbol+"(〜"+today+")",fontsize=40)  
                                        axlist[0].set_title("Reproduction index "+analize_symbol,fontsize=40)  
                                                                              

                                else:
                                        #axlist[0].set_title("Reproduction index "+r"$R^{\rm{W8}}$"+"(〜"+today+")",fontsize=40,color="w")
                                        axlist[0].set_title("Reproduction index "+r"$R^{\rm{W9}}$"+"(〜"+today+")",fontsize=40,color="w")  
                        
                        print("finish title")
                        

                        ### x ticks ###                                            
                        plt.rcParams['axes.xmargin'] = 0        #(0,0)point
                        #ax.set_xlabel('Date',fontsize=20)
                        #if a==len(analizes)-1:
                        print("a=",a,graph_num)
                        if PR and a==1:
                                axlist[a].set_xlabel('Date',fontsize=30)
                                xlocs,xlabs=plt.xticks(np.arange(len(cal)),date_reduction(cal)[0],fontsize=25,rotation=None)
                                plt.setp(axlist[a].get_xticklabels(), rotation=-30,rotation_mode="anchor")
                        elif a==graph_num-1:
                                axlist[a].set_xlabel('日付',fontsize=30)
                                if langage is "e":
                                        axlist[a].set_xlabel('Date',fontsize=30)
                                #x ticks
                                #xlocs,xlabs=plt.xticks(np.arange(len(cal)),date_reduction(cal)[0],fontsize=30,rotation=None) 
                                xlocs,xlabs=plt.xticks(np.arange(len(cal)),date_reduction(cal)[0],fontsize=25,rotation=None)
                        else:
                                plt.xticks(np.arange(len(cal)),[""]*len(cal),color=None,fontsize=30,rotation=None) 

                        #### y ticks ###
                        if not analize is "infective_w8_2" and not analize is "inf_zoominout":
                                locs,labs=plt.yticks(fontsize=25)
                                #print( [ lab.get_text() for lab in labs ] )

                                labs=[str(int(item)) for item in locs]
                                for i in range(len(labs)):
                                        if not i%3==0:
                                                labs[i]=""
                                plt.yticks(locs,labs,fontsize=30)
                        else:plt.yticks(fontsize=30)

                        print("finish ticks")


                        #if analize in ["cases","average_w"]:            ###for right label
                        #if analize is "cases" or (analize is "average_w" and not pile_up_nw):            ###for right label
                        if (not pile_up_nw and analive in ["cases","average_w"]) or (pile_up_nw and analize=="average_w") and not PR :            ###for right label
                                if log:pass
                                else:
                                        plt.twinx()
                                        if analize is "cases":ana=r"$N^{\rm{obs}}$"        
                                        elif analize is "average_w": ana=r"$N^{\rm{obs,W}}$"

                                        for i,l in enumerate(labs):
                                                if l is "":continue
                                                labs[i]=round(int(l)/population*100*1000,2)

                                        #plt.ylabel(ana+"/populataion\n["+r"$\times10^{-3}$"+"%]",fontsize=30)
                                        plt.ylabel(ana+"/populataion\n["+r"$\times10^{-3}$"+"%]",fontsize=22)
                                        plt.yticks(locs,labs,fontsize=30)
                                        plt.tick_params(axis='y')



                        # draw grid ticks
                        if pile_up_nw and analize=="average_w":pass
                        else:
                                line_length=max_value*7/5
                                if log: line_length=100000
                                axlist[a].grid(which="both")
                                axlist[a].tick_params(direction = "inout", length = 15,width=1, colors = (0,0.1,0.04),which="major")

                                for xpoint in date_reduction(cal)[1]:
                                        axlist[a].vlines(xpoint, 0, line_length,color=(0.08,0.1,0.08),alpha=0.7,linewidth=2.5,linestyles="dashed")# month sepalate line

                                #draw weekend line
                                for sunday in date_reduction(cal)[2]:
                                        axlist[a].vlines(sunday  ,0,line_length,color=(1,0,0),alpha=0.9,linewidth=2,linestyles="dotted")# draw sunday line
                                        axlist[a].vlines(sunday-1,0,line_length,color=(0.2,0,1),alpha=0.9,linewidth=1.5,linestyles="dotted")# draw sutuday line

                        ### legend ###
                        ##############
                        """
                        if pile_up_nw:
                                #if analize=="cases":
                                if analize=="average_w":
                                        plt.legend(prop={'size':40,},title=None,title_fontsize=15,loc='upper left', ncol=1,labelspacing=0,borderpad=0,framealpha=0.7,facecolor=(0.94,0.97,0.95),borderaxespad=0.3)

                        else:
                                if a==0:
                                        plt.legend(prop={'size':40,},title=None,title_fontsize=15,loc='upper left', ncol=1,labelspacing=0,borderpad=0,framealpha=0.7,facecolor=(0.94,0.97,0.95),borderaxespad=0.3)
                                        print("max",max_value)
                        """


                        ### label for datasets ###
                        if analize is "cases" and not log:
                                if dataset_type is "europ":
                                        #plt.text(sum(xlim)/2, max_value*3.5/4, "European Centre for Disease Prevention and Control\n An agency of the European Union", alpha=0.7, size=40, ha="center", va="center",color="g")
                                        #plt.text(sum(xlim)/2, max_value*3.5/4, "European Centre for Disease Prevention and Control\n An agency of the European Union", alpha=0.7, size=30, ha="center", va="center",color="g")                                
                                        #plt.text(sum(xlim)*2/3, max_value*3.5/4, "EUROPIAN CDC CDC", alpha=0.7, size=30, ha="center", va="center",color="g")                                                
                                        plt.text(xlim[1]-0.05*(xlim[1]-xlim[0]), max_value*3.5/4, "EUROPIAN CDC", alpha=0.7, size=50, ha="right", va="bottom",color="g")
                                        #plt.text(sum(xlim)/2, max_value*2.2/4, "\n https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide", alpha=0.5, size=25, ha="center", va="center",color="g")
                                        #plt.text(sum(xlim)/2, max_value*2.2/4, "\n https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide", alpha=0.5, size=15, ha="center", va="center",color="g")

                                if dataset_type is "toyokei":
                                        if not darkcolor:
                                                #plt.text(sum(xlim)/2, max_value*3.5/4, "TOYOKEIZAI ONLINE", alpha=0.7, size=50, ha="center", va="center",color=(0.1,0.1,0.15))
                                                #plt.text(sum(xlim)/2, max_value*3.5/4, "TOYO KEIZAI ONLINE", alpha=0.7, size=50, ha="center", va="center",color=(0.1,0.1,0.15))
                                                plt.text(xlim[1]-0.05*(xlim[1]-xlim[0]), max_value*3.5/4, "TOYO KEIZAI ONLINE", alpha=0.7, size=50, ha="right", va="bottom",color=(0.1,0.1,0.15))
                                                #plt.text(sum(xlim)/2, max_value*2.2/4, "https://github.com/kaz-ogiwara/covid19/blob/master/data/summary.csv", alpha=0.5, size=25, ha="center", va="center",color=(0.1,0.1,0.15))
                                        else:
                                                #plt.text(sum(xlim)/2, max_value*3.5/4, "TOYOKEIZAI ONLINE", alpha=1, size=50, ha="center", va="center",color=(0.97,1,0.97))
                                                plt.text(sum(xlim)*2/3, max_value*3.5/4, "TOYO KEIZAI ONLINE", alpha=1, size=50, ha="center", va="center",color=(0.97,1,0.97))
                                                #plt.text(sum(xlim)/2, max_value*2.2/4, "https://github.com/kaz-ogiwara/covid19/blob/master/data/summary.csv", alpha=1, size=25, ha="center", va="center",color=(0.97,1,0.97))  
                                if dataset_type is "jag-japan":
                                        plt.text(xlim[1]-0.05*(xlim[1]-xlim[0]), max_value*3.5/4,"J.A.G Japan", alpha=0.7, size=50, ha="right", va="bottom",color=(0.75,0,0))
                                if dataset_type is "DATA kourou":
                                        plt.text(xlim[1]-0.05*(xlim[1]-xlim[0]), max_value*3.5/4,"厚生労働省オープンデータ", alpha=0.7, size=40, ha="right", va="bottom",color=(0,0,0.75))

                        print("finish label")
                        #plt.tight_layout()
                        plt.subplots_adjust(wspace=0.4, hspace=0.1)
                        plt.xlim(xlim)
                        if log:      
                                if 9000<max_value: 
                                        plt.ylim([0.1,100000])
                                else:
                                        plt.ylim([0.1,10000])
                                plt.yscale("log")                               
                                


                #country label
                axlist[0].text(xlim[0]+0.05*(xlim[1]-xlim[0]), cases_max_value*3.5/4, country, alpha=0.7, size=40, ha="left", va="bottom",color=(0.1,0.4,0.1),bbox={"facecolor":(0.98,0.98,0.98)})                                                
                ### legend ###
                if pile_up_nw:
                        axlist[0].legend(prop={'size':40,},title=None,title_fontsize=15,loc='lower left', ncol=1,labelspacing=0,borderpad=0,framealpha=0.7,facecolor=(0.94,0.97,0.95),borderaxespad=0.3)
                else :
                        axlist[0].legend(prop={'size':40,},title=None,title_fontsize=15,loc='upper left', ncol=1,labelspacing=0,borderpad=0,framealpha=0.7,facecolor=(0.94,0.97,0.95),borderaxespad=0.3)

                #axlist[2].legend(prop={'size':40,},title=None,title_fontsize=15,loc='upper right', ncol=1,labelspacing=0,borderpad=0,framealpha=0.7,facecolor=(0.94,0.97,0.95),borderaxespad=0.3)
                axlist[-1].legend(prop={'size':40,},title=None,title_fontsize=15,loc='upper right', ncol=1,labelspacing=0,borderpad=0,framealpha=0.7,facecolor=(0.94,0.97,0.95),borderaxespad=0.3)
                ### restrict line 
                restrict_view=True
                if dataset_type in ["toyokei","jag-japan","DATA kourou"] and restrict_view:
                        restrict_line(langage)

                ## finaly edit and save figure ##
                #################################
                if darkcolor:
                        for i in range(len(axlist)):
                                axlist[i].tick_params(color=(1,1,1),labelcolor="w",grid_color="w")
                                axlist[i].xaxis.label.set_color("w")
                                axlist[i].yaxis.label.set_color("w")
                                axlist[a].set_facecolor((0.1,0.15,0.23))
                        plt.savefig(__file__.split(".")[0]+'_{para}_dark.png'.format(para=dataset_type+"_"+re.sub(r"\/",r"_",today)+str(select_countries)+str(analizes)+"langage="+langage+"_formula="+str(formula)), pad_inches=1.0 ,format="png",facecolor=(0,0.05,0.1))
                else:# normal color
                        for i in range(len(axlist)):
                                axlist[i].set_facecolor((0.94,0.99,0.94))
                        try:
                                #os.mkdir("./Pictures/"+__file__.rsplit(".",1)[0]+'_{para}/'.format(para=dataset_type+"_"+re.sub(r"\/",r"_",today)+str(analizes)+"langage="+langage+"_formula="+str(formula)))
                                #os.mkdir("./covid19_analize/figures/{p}".format(p=re.sub(r"\/",r"_",today)))
                                #os.mkdir("./figures/{p}".format(p=re.sub(r"\/",r"_",today)))
                                os.mkdir("./figures/{p}_Rw{d}".format(p=re.sub(r"\/",r"_",today),d=delay))
                                print("try")
                        except:pass
                        if PR:
                                plt.tight_layout()
                        print("start save")
                        #plt.savefig("./Pictures/"+__file__.rsplit(".",1)[0]+'_{para}/'.format(para=dataset_type+"_"+re.sub(r"\/",r"_",today)+str(analizes)+"langage="+langage+"_formula="+str(formula))+str(select_countries).strip('[\'').strip("\']")+'.png', pad_inches=1.0 ,format="png")
                        #plt.savefig("./covid19_analize/figures/{p}/".format(p=re.sub(r"\/",r"_",today))+str(select_countries).strip('[\'').strip("\']")+'.png', pad_inches=1.0 ,format="png")
                        #plt.savefig("./figures/{p}/".format(p=re.sub(r"\/",r"_",today))+str(select_countries).strip('[\'').strip("\']")+'.png', pad_inches=1.0 ,format="png")
                        plt.savefig("./figures/{p}_Rw{d}/".format(p=re.sub(r"\/",r"_",today),d=delay)+str(select_countries).strip('[\'').strip("\']")+'.png', pad_inches=1.0 ,format="png")
                        print("save fig\n")




        
