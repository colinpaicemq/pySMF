
# program to parse a pasearch map and output put it as yaml
"""
Program to parse the pasearch output from z/OS to generate YAML of the non default options
"""


import struct

#import  ../smfobjects as q
#import /home/colin/git/pySMF/smfobjects
from .. import smfobjects
from collections import OrderedDict

######################################
# import readfile
def zz(name):
    x = name()
    print(x)
            
dl2 = []

# record_count =1000

####################
#  START HERE
####################


fIn = open("DCOLLECT.bin","rb")
lline = fIn.read(2)
output = struct.unpack(">H",lline) # get the length
line = fIn.read(output[0] - 2) # ignore the first
line = lline + line
headerold  = [q.xu(n="RecLen",c="RecordLength",l=2),
              q.xu(n="Seg",c="Segment",l=2,o=2),
              q.xu(n="Flag",c="",l=1),
              q.xu(n="RecordType",c="",l=1),
              q.SMFTime(n="Time",c=""),
              q.SMFDate(n="Date",c=""),
              q.xs(n="SID",c="",l=4),
              #q.xs(n="Subsys",c="",l=4), # Not in type 0
              #q.xu(n="RecordSubType",c="",l=2,o=22),
              ]



for outerLoop in range(1):
    lline = fIn.read(2)  # getonly what we need
    if len(lline) == 0:
        break

    output = struct.unpack(">H",lline) # get the length
    print("Line 56",output)
    '''
    line = fIn.read(output[0]-2) # ignore the length field
    #   print("length", output)
    line = lline + line # rebuild the line with the length on the front
    if output[0]<= 16:
        continue # record too short
    #print("===record:",outerLoop)
    try:
        data = processit(headerSubtype,line)
    except Exception as e:
        print("exception",e)
        dumphex.dumphex(line)
        raise e
'''