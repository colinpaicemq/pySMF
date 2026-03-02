"""
Program to process SMF data, and process create python structures out of it.
"""

import processnew
import  smfobjects as q
import dumphex
from pyzfile import *
import smf30st1
import pandas as pd 
import smf42st6
import pickle


####################
#  START HERE
####################

# we need the basis shape of an SMF header, so we can see if it has subtypes or not            
headerSubtype =[
                q.xu(n="RecLen",c="RecordLength",l=2),
                q.xu(n="Seg",c="Segment",l=2,o=2),
                q.xu(n="Flag",c="",l=1),
                q.xu(n="RecordType",c="",l=1),
                q.SMFTime(n="Time",c=""),
                q.SMFDate(n="Date",c=""),
                q.xs(n="SID",c="",l=4),
                q.xu(n="Subsys",c="",l=4,i=True), # Not in type 0,or smf 80 ( RACF records)
                q.xu(n="RecordSubType",c="",l=2,o=22),
]

def readfile():
    a = 0x0000
    aa = a.to_bytes(2, 'big')
    try:
        with ZFile("//'IBMUSER.SMF'", "rb,type=record,noseek") as file:
            for rec in file:
                l = len(rec)
                bl = l.to_bytes(2, 'big') 
                
                nrec = bl+  aa + rec # length + segment
                #for n in nrec:
                #    print("==60",n,hex(n))
                yield  nrec
    except ZFileError as e:
        print(e)

nth = 0  
#    for outerLoop in range(nrecords):
nrecords = 500
smf30_1_list = []
smf42_6_list = []
for line in readfile():
    nth += 1
    if  nth > nrecords:
        break
    if len(line)<= 16:
        continue

    try:
        #data = processit.processit(headerOld,line,line)
        data = processnew.processit(headerSubtype,line,0) #options, line, offset

        if (data["Flag"] &0x40 ) != 0x40:
            #print("subtype reset",data["Flag"] )
            data["RecordSubType"] = None
        # print(data["RecordType"],data["RecordSubType"])    
        #for kw,v in data.items():
        #        print(kw,v)    
        if data["RecordType"] == 30 and  data["RecordSubType"] ==1 : 
            data = processnew.processit(smf30st1.process(),line,0) #options, line, offset    
            #for kw,v in data.items():
            #    print(kw,v)
            #print("Time",nth,data["Time"])
            smf30_1_list.append(data) 
        if data["RecordType"] == 42 and  data["RecordSubType"] ==6 : 
            data = processnew.processit(smf42st6.process(),line,0) #options, line, offset    
            #for kw,v in data.items():
            #    print(kw,v)
            smf42_6_list.append(data)     

    except Exception as e:
        print("exception!",e)
        print("Record:",nth)
        exit()
        raise e
#pd301= pd.DataFrame.from_records(smf30_1_list)    
#print(pd301) 
#print("len",len(smf42_6_list))
pd426 = pd.DataFrame.from_records(smf42_6_list) 
print(list(pd426.columns.values))
print(pd426) 
fPickle = open('smf426.pickle', 'wb')    
#    # source, destination
pickle.dump(pd426,fPickle)    