'''
Define "objects/classes" for common SMF fields
invoked as
 ... x.xu(ln="field name",c="comment",l=length,x="field exit name",p=value,t=triplet,o=offset)
 where
 print value p can be True, False or function name which returns true or false
 triplet is the name of a definition of an SMF triplet block
 offset can be specified to help check the definitions are correct
'''
import datetime
import struct
def lookup(data,d,dummy):
    '''
    Simple lookup of value in a list
    '''
    #  print("====15",data,type(d),d)
    v = d.get(data,"?")
    if v =="?":
        v = "Unknown type:"+ str(data)
    #print("==19",data,v)
    return v

def bitmask(data,ll,dummy):
    '''
    Simple lookup of value in a list
    Each list element is [mask,value,description]
    We and the value with the mask, and compare it with the value - if it matches use the
    description

    '''
    output = []
    for l in ll:
        if (data & l[0] ) & l[1] == l[1]:
            output.append(l[2])
    return output



class common:
    '''
    Common processing for all types
    Methods
    __init__
    check_offset
    get_struct  -value needed for the struct....
    get_value
    get_name
    display
    set
    __str__
    '''
    def __init__(self,n=None,c=None,l=None,x=None,t=None,p=None,o=None,x0=None,x1=None,v=None,i=False):

        # print("==3",self.__class__)
        if l is None:
            raise ValueError("SMF:length value (l) is not set")
        if n is None:
            raise ValueError("SMF:name value (n) is not set")
        self.x = x
        self.x0 = x0
        self.x1 = x1
        self.t = t
        self.p = p
        self.name  = n
        self.comment = c
        self.value = None
        self.struct = None
        self.offset = o
        self.type = self.__class__.__name__
        self.length = l
        self.constant = v
        self.ignore = i
        self.strip = False

    def check_offset(self,current_length):
        '''

        Ensure the we have not got it wrong, by checking the
        actual offset with expected offset
        '''
        if self.offset is None:
            self.offset = current_length
            return True
        #print("Checkoffset:",self.name +",","o="+     
        #        str(self.offset),"actual="+str(current_length ))
        if self.offset != current_length:
            raise ValueError("Bad offset found for "+
                self.name +",","o="+
                # self.name +","+self.comment,"o="+
                str(self.offset),"actual="+str(current_length ))

    def __len__(self):
        return self.length
    def get_struct(self):
        '''
        Return the value for struct eg H for halfword
        '''
        if self.struct is None:
            raise ValueError("invalid struct value for " + self.name +"," +self.comment )
        return self.struct

    def get_name(self):
        '''
        return the name of the field
        '''
        return self.name
    def get_value(self):
        '''
        return the value
        '''
        return self.value

    def xdisplay(self):
        '''
        Display the object for passing on
        '''
        if self.p == "no":
            return
        if self.p == "NZ" and self.value == 0:

            return
        dv =str(self.value)
        p ={}

        p["v"] = dv
        # = {"n":dn,"c":dc,"v":dv}
        #if self.__class__.__name__ == "SMFTime":
        #    print("====60",self.value,dv,p)

        return dv
    def set(self,value):  #super.set
        '''
        save the value
        '''
        self.value = value
        if self.x is not None:
            self.value = self.x(value,self.x0,self.x1)
        if self.constant is not None:
            if self.constant != value:
                name = self.name
                raise ValueError("SMF: Value does not match the v=value in"+name,self.value,self.constant)

    def __str__(self):
        print("smfo158",self.value,type(self.value))
        super().__str__(self.value)
        #return str(self.value)
        #return f"{self.value}"
    #def __repr__(self):
    #    print("===178",self.name)
    #    #x =   super()._repr__(self)
    #    return self.value
class xs(common):
    '''
    String or character
    '''
    def __init__(self,n=None,c=None,l=None,x=None,p=None,o=None,v=None,debug=None,i=False,strip=False):
        super().__init__(n=n,c=c,l=l,x=x,p=p,o=o,i=i)
        if l <= 0 or l > 1024:
            raise ValueError("invalid length value(l).  It needs to be in range 1 to 1024")
        s = f"{l}s"

        self.struct = s
        self.length = l
        self.debug = debug
        self.strip = strip

    def set(self,value):
        if not isinstance(value, bytes):
            raise ValueError("invalid data passed to xs. Expecting bytes, passed "+type(value))
        #print("==84")
        #print(''.join(format(x, '02x') for x in value))
        # print("????",self.name,len(value),dumphex.dumphex(value))
        try:
            if value[0] == 0:
                self.value = "NULL"
            elif value[0] == 255:  # 0xff
                self.value = "NULL"
            else:
                m = value.decode("cp500")
                e = m.encode('ascii')
                value = e.decode("utf-8") 
                # print("=====179",value, ".", value.rstrip(),"!",len(value.rstrip( " ")))
                #if self.name == "DSN":
                #    print("DSN", self.strip)
                if self.strip  is True:
                    value = value.rstrip(" ")
                self.value = value
        except Exception as e:
            print("exception","Element name:",self.name,e, "offset",self.offset)
            print(''.join('{:02x}'.format(x) for x in value))
            #dumphex.dumphex(value)
            self.value = None
            raise e


class xu(common):
    '''
    Unsigned integer
    '''
    def __init__(self,n=None,c=None,l=None,x=None,x0=None,p=None,o=None,v=None,x1=None,i=False):
    # def __init__(self,name,comment,**kw):
    #
        # print("====92 o",o, "n",n,"c",c)
        super().__init__(n=n,c=c,l=l,x=x,p=p,o=o,x0=x0,x1=x1,i=i)
        struct_codes = {1:"B",2:"H",4:"I",8:"Q"}
        if l in struct_codes:
            self.struct = struct_codes[l]
        else:
            raise ValueError("SMF: invalid length value(l).  It needs to be one of 1,2,4,8. Name=",n)
    def set(self,value):
        super().set(value)
        #print("smfo xu 216A",self.value,type(self.value),self.name)
        # if the definition had  a constant thene check
        # for example the length of a control block
        #if self.constant is not None:
        #    if self.constant != value:
        #        name = self.name
        #        raise ValueError("Value does not match the v=value in"+
        #                         name,self.value,self.constant)

class xp(common):
    '''
    packed yyyydddF
    '''
    def __init__(self,n=None,c=None,l=None,x=None,x0=None,p=None,o=None,v=None,x1=None,i=False):
    # def __init__(self,name,comment,**kw):
    #
        super().__init__(n=n,c=c,l=l,x=x,p=p,o=o,x0=x0,x1=x1,i=i)
        struct_codes = {1:"B",2:"H",4:"I",8:"Q"}
        if l in struct_codes:
            self.struct = struct_codes[l]
        else:
            raise ValueError("SMF: invalid length value(l).  It needs to be one of 1,2,4,8, Name=",n)
    def set(self,value):
      if value == 15 : #  value 0000000F  ... a packed 0 value
        date = "**********"
      else:
        yyyy = value >> 16 # convert yyyyxxxx to 0000yyyy
        y1 = (yyyy  &0x0000f000 ) >> 12
        y2 = (yyyy  &0x00000f00 ) >> 8
        y3 = (yyyy  &0x000000f0 ) >> 4
        y4 = (yyyy  &0x0000000f ) >> 0
        yy = y1 * 1000 + y2 * 100 +y3 * 10   +y4
        d1 = (value &0x0000f000) > 12
        d2 = (value &0x00000f00) > 8
        d3 = (value &0x000000f0) > 4
        dd = 100 * d1 + 10 * d2 + d3
        d  = f"{yy} {dd:{3}}"  # string version of the date eg 2025 014
        date  = datetime.datetime.strptime(d,"%Y %j")  # this produces date and time
        date = date.date() #just take the date
        date = date.strftime('%Y/%m/%d')
      self.value = date
      super().set(date )

class xb(common):
    '''
    byte stream (not a string)
    '''
    def __init__(self,n=None,c=None,l=None,x=None,x0=None,p=None,o=None,v=None,x1=None,i=False):

        super().__init__(n=n,c=c,l=l,x=x,p=p,o=o,x0=x0,x1=x1,i=i)
        s = f"{l}s"
        self.struct = s
        self.length = l

    def set(self,value):
        super().set(value)
        #ba = bytearray(value)
        # if the definition had  a constant thene check
        # for example the length of a control block
        #if self.constant is not None:
        #    if self.constant != value:
        #        name = self.name
        #        raise ValueError("SMF: Value does not match the v=value in"+name,self.value,self.constant)
class ig(xb):  # 
    '''
    ignore ... do not produce any output - used as spacing in structure
    treat as a byte string
    '''
    def __init__(self,n=None,c=None,l=None,x=None,x0=None,p=None,o=None,v=None,x1=None,i=False):
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>291")
        super().__init__(n=n,c=c,l=l,x=x,p=p,o=o,i=i)
        self.ignore=True
    def set(self,value):
        super().set(value)    


class ig2(common):  # 
    '''
    ignore ... do not produce any output - used as spacing in structure
    '''
    def __init__(self,n=None,c=None,l=None,x=None,x0=None,p=None,o=None,v=None,x1=None,i=False):
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>291")
        super().__init__(n=n,c=c,l=l,x=x,p=p,o=o,x0=x0,x1=x1,i=i)
        self.ignore=True
        s = f"{l}s"
        self.struct = s
        self.length = l
        #print("+====292 set ignore",self.ignore)
    def set(self,value):
        super().set(value)    

class x128(common):
    '''
    Units of 128 microseconds
    '''
    def __init__(self,n=None,c=None,x=None,x0=None,p=None,o=None,i=False):
        super().__init__(n=n,c=c,l=4,x=x,p=p,o=o,i=i)
        self.struct = "I" # length 4
    def set(self,value):
        self.value = value *128/1000000.0 # in seconds

class xx(common):
    '''
    Unsigned integer formatted as a hex value
    '''
    def __init__(self,n=None,c=None,l=None,x=None,p=None,o=None,i=False):
    # def __init__(self,name,comment,**kw):
        super().__init__(n=n,c=c,l=l,x=x,p=p,o=o,i=i)
        struct_codes = {1:"B",2:"H",4:"I",8:"Q"}
        if l in struct_codes:
            self.struct = struct_codes[l]
        else:
            raise ValueError("invalid length value(l).  It needs to be one of 1,2,4,8 Name=",n)
    def __str__(self):
        return hex(self.value)
        
class SMFTime(common):
    '''
    Convert packed time to time value
    '''
    def __init__(self,n=None,c=None,x=None,p=None,o=None,l=4,i=False):
        if l != 4:
            raise ValueError("invalid length value(l). l must be 4",n)
        super().__init__(n=n,c=c,l=4,x=x,p=p,o=o,i=i)
        self.struct = "I"
    def set(self,value):
        if value == 0:
            self.value = None
        else:
            hundreds = value%100
            hhmmss = value //100
            ss = hhmmss  % 60
            hhmm = hhmmss//60
            mm = hhmm %60
            hh = hhmm//60
            if hh > 23 :
                raise ValueError("SMF: Time problem,hh",hh, self.value,self.name,self.offset)
            dt = datetime.time(hour=hh,minute=mm,second=ss,microsecond= hundreds * 10000)

            self.value = dt.strftime("%H:%M:%S.%f")[0:11]
     

    def __str__(self):

        return hex(self.value)
class SMFDate(common):
    '''
    convert SMF time to a date object
    '''
    def __init__(self,n=None,c=None,x=None,p=None,o=None,l=4,i=False):
        if l != 4:
            raise ValueError("invalid length value(l). l must be 4",n)
        super().__init__(n=n,c=c,l=4,x=x,p=p,o=o,i=i)
        self.struct = "I" #
    def set(self,value):

        # we need to convert the internal date format to a string yyyy dddd
        # then parse this to a date timeobject
        # then take the date
        # format is 0cyydddf as packed decimal
        # we need to isolate each digit and *10 to build the decimal date
        value =  value >> 4 # get rid of the trailing F
        if value == 0:
            self.value = None
        else:
            #print("===155",value)
            d3 = value &0x0000000f
            d2 = (value &0x000000f0 ) >>4
            d1 = (value &0x00000f00 ) >> 8
            days = d1 * 100 + d2 * 10  + d3

            y2 = (value &0x0000f000 ) >> 12
            y1 = (value &0x000f0000 )>> 16
            yy = 10 * y1 + y2
            d  = f"20{yy} {days:{3}}"  # string version of the date eg 2025 014
            date  = datetime.datetime.strptime(d,"%Y %j")  # this produces date and time
            date = date.date() #just take the date
            date = date.strftime('%Y/%m/%d')
            self.value = date


class xhun(common):
    '''
    Number in hundreds of a second.
    '''

    def __init__(self,n=None,c=None,l=None,x=None,p=None,o=None,i=False):
    # def __init__(self,name,comment,**kw):
    #
        # print("====92 o",o, "n",n,"c",c)
        super().__init__(n=n,c=c,l=l,x=x,p=p,o=o,i=i)
        struct_codes = {1:"B",2:"H",4:"I",8:"Q"}
        if l in struct_codes:
            self.struct = struct_codes[l]
        else:
            raise ValueError("invalid length value(l).  It needs to be one of 1,2,4,8 Name=",n)
    def set(self,value):
        self.value = value/100

class xtimehun(common):
    '''
    Time since midnight in in hundreds of a second.
    '''

    def __init__(self,n=None,c=None,l=None,x=None,p=None,o=None,i=False):
    # def __init__(self,name,comment,**kw):
    #
        # print("====92 o",o, "n",n,"c",c)
        super().__init__(n=n,c=c,l=l,x=x,p=p,o=o,i=i)
        struct_codes = {1:"B",2:"H",4:"I",8:"Q"}
        if l in struct_codes:
            self.struct = struct_codes[l]
        else:
            raise ValueError("invalid length value(l).  It needs to be one of 1,2,4,8 Name=",n)
    def set(self,value):
        #if value == 0 :
        #    print("===266 xtimehun is zero",self.name)
        hundreds = value%100
        allseconds  = value //100
        ss = allseconds%60 # convert to minutes
        allminutes = ss//60
        mm = allminutes %60
        hh = allminutes//60

        self.value = datetime.time(hour=hh,minute=mm,second=ss,microsecond= hundreds * 10000)





class xSTCK(common):
    '''
    Handle store clock
    '''
    def __init__(self,n=None,c=None,x=None,p=None,o=None,l=8,i=False):
        if l != 8:
             raise ValueError("invalid length value(l).  It needs to be one of 8 Name=",n)
        else:
            super().__init__(n=n,c=c,l=8,x=x,p=p,o=o,i=i)
            self.struct = "Q" #  8 bytes
    def set(self,value):
        if value == 0:
            self.value = None
        else:

            t = value/4096 #  remove the bottom 12 bits to get value in micro seconds
            tsm = (t /1000000 ) -  2208988800 # // number of seconds from Jan 1 1970
            ts = datetime.datetime.fromtimestamp(tsm)
            self.value = ts

    def xdisplay(self):
        '''
        Display the object for passing on
        '''

        if self.p == "no":
            return
        return self.value
        #dv =str(self.value)

class xSTCKE(common):
    '''
    standin
    '''
    def __init__(self,n=None,c=None,x=None,p=None,o=None,l=None,i=False):
    # def __init__(self,name,comment,**kw):
    #
        # print("====92 o",o, "n",n,"c",c)
        #print("==409 abuut")
        super().__init__(n=n,c=c,l=16,x=x,p=p,o=o,i=i)
        self.struct = "16s" #  18 bytes

        #else:
        #    raise ValueError("invalid length value(l).  It needs to be one of 1,2,4,8 Name=",n)
    def set(self,value):
        if value == 0:
            self.value = None
        else:
            #  print("===273",value)
            v  = struct.unpack(">Q",value[1:9])
            # print("stcke",value[1:9])
            # raise ValueError("iCheck stcke")
            if v[0] == 0:
                print("xSTCK is 0")
            value = v[0]
            # print("value",value,type(value))
            t = value/4096 #  remove the bottom 12 bits to get value in micro seconds
            tsm = (t /1000000 ) -  2208988800 # // number of seconds from Jan 1 1970
            # print("==????",dir(datetime))
            ts = datetime.datetime.fromtimestamp(tsm)
            printable = ts.isoformat()
            #print("TS",tsm,ts.isoformat())
            self.value = printable    #
    def __len__(self):
       #l  = self.structs[self.type][1]
        return self.length

class xoffset(common):
    '''
    Used for smf 42 record where we are just given an offset of a section
    we point use t= to point to the template
    specify ol as the length of the block being pointed to
    '''
    def __init__(self,n=None,c=None,x=None,p=None,o=None,t=None,ol=None,i=False):
        if t is None:
            raise ValueError("SMF: Type xoffset needs a T=value")
        if ol is None:
            raise ValueError("SMF: Type xoffset needs an length of the block  in ol=")
        super().__init__(n=n,c=c,l=4,x=x,p=p,o=o,t=t,i=i)
        self.triplet = t
        self.struct = "I"
        self.offsetlen =ol
    def set(self,value):
        #print("===332 xoffset",value)
        self.value = [value,self.offsetlen]
    def get_triplet(self):
        '''
        return the data
        '''
        return self.triplet


class xtriplet(common):
    '''
     Just like a triplet, except the offset, to record, length, and count
    '''
    def __init__(self,n=None,c=None,x=None,p=None,o=None,t=None,i=False):
        if t is None:
            raise ValueError("Type triplet needs a T=value")

        super().__init__(n=n,c=c,l=8,x=x,p=p,o=o,t=t,i=i)
        self.triplet = t
        self.struct = "Q"
    def set(self,value):

        oln = value
        ol  = oln  >> 16 # remove the offset
        n   = value - (ol  <<16)
        offset  = ol >>16
        l = ol - (offset  <<16)
        self.value = [l,n,offset]

    def get_triplet(self):
        '''
        return the data
        '''
        return self.triplet

class xarray(common):
    '''
     We get an 8 byte number first 4 bytes number , second 4 is length,
     the offset is the field following - so current_length+8
    '''
    def __init__(self,n=None,c=None,x=None,p=None,o=None,t=None,i=False):
        if t is None:
            raise ValueError("Type xarray needs a T=value")
        if o is None:
            raise ValueError("Type xarray needs a o=value")


        super().__init__(n=n,c=c,l=8,x=x,p=p,o=o,t=t,i=i)
        self.triplet = t
        self.struct = "Q"
    def set(self,value):

        oln = value
        n = oln  >> 32 # move the 8 bytes and take top 4  bytes

        l = value - ( n <<32) # residue
        offset = self.offset + 8
        print("xarray",l,n,offset,self.length)
        self.value = [l,n,offset]

    def get_triplet(self):
        '''
        return the data
        '''
        return self.triplet
