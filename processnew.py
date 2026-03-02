"""
take the structure of data, and the input record and create the structure with the record data
"""
import struct
from collections import OrderedDict
import dumphex

def processit(opts,line,position):
    '''
    We are passed a list of the parameters, and the data.
    process it and return the dict to the caller
    '''
    sformat = ">"
    current_length = 0
    # calculate the length of our data, and the specified offset matches where we are
    lline= len(line)
    #for o1 in opts:
    for n, o1 in enumerate(opts):
        sformat = sformat + o1.get_struct()
        o1.check_offset(current_length)
        current_length += len(o1)  # and accumulate past the current element
        if current_length < lline:
            current_n = n
        elif current_length == lline:
           current_n = n
           break
        else : #  current_length > lline:
            raise ValueError("Definition mismatch with record length. ",o1.get_name(),
                             "offset instructure",current_length,"record length",lline)

    l_needed =struct.calcsize(sformat)
    #print("====22==",l_needed,lline)
    try:
        #print("dump it")
        output1 = struct.unpack(sformat,line[position:position+l_needed])
    except Exception as e:
        print("exception 31",e)
        for o1 in opts:
            print("name",o1.get_name())
        print(sformat)
        print("Length",len(line),position,position+l_needed,l_needed)
        dumphex.dumphex(line)
        for o1 in opts:
            print(o1.get_name(),o1.get_struct())

        raise e
    data1 = OrderedDict()
    for n1, o1 in enumerate(opts):
        # we need to tie up the value in output with the structure of variables in opts
        # if we have more defintions than data .... crete them as None
        if n1 > current_n:
             #print("===52=", n,current_n,o1.get_name())
             data1[o1.get_name()] = None
             continue #
        if o1.ignore is True : # do not produce any output
            continue
        v1= output1[n1] # get the value
        o1.set(v1)
        if o1.__class__.__name__ ==  "xtriplet":
            triplet_parms = o1.get_value() # length number offset
            #print(o1.get_name())
            offset = triplet_parms[2]
            nz = triplet_parms[1]
            l = triplet_parms[0]
            triplet_data = []

            for iz in range(nz):
                ioffset = offset + iz * l
                #print("====50 loop=",iz,"length=",l,"offset=",offset)
                # print("===60  triplet")
                ret = processit(o1.get_triplet(),line,position+ioffset)
                #print("/==60 tpriplet")
                #print("==triplet returned",ret)
                triplet_data.append(ret)
            if nz == 1:  # just the one
                #print("====51 count1",o1.get_name())
                data1[o1.get_name()] = ret
            elif nz ==0:
                #print("====51 count0",o1.get_name())
                data1[o1.get_name()] = None
            else:
                #print("====51 counttriplet",o1.get_name())
                data1[o1.get_name()] = triplet_data
        elif o1.__class__.__name__ ==  "xoffset":
        #    print("xoffset69")
            toffsetLen = o1.get_value() # length number offset
            myOffset = toffsetLen[0]
            #print("===80",myOffset,type(myOffset),o1.name,position )
            triplet_data = []
            count = 0
            while myOffset != 0  and myOffset <  65535: # 0xffff
                count += 1
                ret = processit(o1.get_triplet(),line,myOffset )
                # print("==57 offset",ret)
                if "offset" in ret:
                    myOffset  = int(ret["offset"])  # of next
                else:
                    myOffset = 0
                triplet_data.append(ret)
            #if count == 1:
            #    data1[o1.get_name()] = ret
            if count ==0:
                data1[o1.get_name()] = None
            else:
                data1[o1.get_name()] = triplet_data
        else:
            o1.set(v1)
            #if v1 is not None:
            data1[o1.get_name()] = o1.get_value()

    return data1

