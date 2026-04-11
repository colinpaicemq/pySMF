"""
Take HLASM SYSDATA and extract the symbol records.  Process them in Pandas 
Format (on z/OS):
  python3 adata.py -dsn "//'COLIN.SYSADATA'"

The field names and layout are in the file adata66.py  

"""

import processnew
import  smfobjects as q
#import dumphex
from pyzfile import *
import traceback 


import pandas as pd
import adata66
import struct

import argparse

pd.options.mode.chained_assignment = None # prevent SettingWithCopyWarning: 
# A value is trying to be set on a copy of a slice from a DataFrame.




####################
#  START HERE
####################

# Read the file to get the record type - we are interested in 0x0042
header =[
                q.xu(n="Language",l=1),
                q.xu(n="Type",l=2),
        ]

def readfile(dsn):
    a = 0x0000
    aa = a.to_bytes(2, 'big')
    try:
       #with ZFile("//'COLIN.SYSADATA'", "rb,type=record,noseek") as file:
       with ZFile(dsn, "rb,type=record,noseek") as file:
            for rec in file:
                nrec = rec
                #for n in nrec:
                #    print("==60",n,hex(n))
                yield  nrec
    except ZFileError as e:
        print(e)
        quit()

parser=argparse.ArgumentParser(description='Parse SYSADATA')
parser.add_argument("-dsn",dest='dsn',default="//'COLIN.SYSADATA'")
# parser.add_argument("-n",dest='nrecords',default="9999'")  # number of records to process


args=parser.parse_args()

nth = 0
#    for outerLoop in range(nrecords):
#nrecords = args.nrecords
nrecords = 9999
adata66_data = []  # output
# csect = ""
csect_list = {}
csect_offset = {}
dd66 = adata66.process() # get the definitions for record type 0x0042

for line in readfile(args.dsn):

    nth += 1
    if  nth > nrecords:
        break


    try:
        # find the record type
        data = processnew.processit(header,line,0) #options, line, offset
        # only for the symbols
        if data["Type"] == 66  : #0x42

            data = processnew.processit(dd66,line,0) #options, line, offset b

            # we need to find the symbol name - offset and length in the records
            offset_symbol = data["SymOffset"]
            l_symbol = data["LSymbol"]
            s = f"{l_symbol}s"
            symbol = struct.unpack(s,line[offset_symbol:offset_symbol+ l_symbol])[0]
            m = symbol.decode("cp500")
            e = m.encode('ascii')
            symbol = e.decode("utf-8")
            data["Symbol"] = symbol 

            # Save csect and offset info for DSECTS and CSECTS
            if data["SymType"] in ["CSECT","DSECT"]:
                
                csect_list[data["ESDID"]] = data["Symbol"]
                csect_offset[data["ESDID"]] = data["Offset"]
     
            adata66_data.append(data) # build up the list of records
            
    except Exception as e:
        print("exception79!",e, print("exception 35",e,traceback.format_exc()))
        print("Record:",nth)
        exit()
        raise e

pdD = pd.DataFrame.from_records(adata66_data)
# Select these records

pdSubset = pdD[["ESDID","Symbol","Offset","Length","TypeA","SymType"]]

pd.set_option('display.max_rows', 500)

# We need to update each row with the CSECT name, and offset from start of
# the CSECT
for i, row in pdSubset.iterrows():
    esdid = row["ESDID"]
    pdSubset.at[i,"CSECT"] = csect_list[esdid]
    pdSubset.at[i,"Offset"]  =  row["Offset"] - csect_offset[esdid] 
#  Sort field by CSECT and offset within CSECT 

pdSubsetSorted = pdSubset.sort_values(by=["CSECT","Offset"])
# and print without row numbers
print(pdSubsetSorted.to_string(index=False))

