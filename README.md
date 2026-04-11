# pySMF
A suite of Python programs to rocess SMF data to create Python objects which can be used in mfpandas and other Python programs.

This suite of Python programs reads and SMF datasets and processes the dat as defined by Python definitons of the record layout.

The output is a list of rows of Python dictionaries.
This list can be fed into Pandas for processing, or your own Python programs.

## Support for HLAsM SYSADATA

This has support for HLASM SYSADATA format


    python3 adata.py -dsn "//'COLIN.SYSADATA'""


## Define a  record layout.
You define the record layout in Python dictionaries.  For example in the main program which reads the records from the dataset you may have

    if data["RecordType"] == 30 and  data["RecordSubType"] ==1 : 
        data = processnew.processit(smf30st1.process(),line,0) 
        #options, line, offset    


This says if the record type is 30 and subtype is 
1 then process the data using the tables in 
smf30st1.process()

smf30st1.process() has

    opts = [q.xu(n="RecLen",c="RecordLength",l=2,i=True),
            q.xu(n="Seg",c="Segment",l=2,o=2,i=True),
            q.xx(n="Flag",c="",l=1),
            q.xu(n="RecordType",c="",l=1),
            q.SMFTime(n="Time",c=""),
            q.SMFDate(n="Date",c=""),
            q.xs(n="SID",c="",l=4),
            q.xs(n="Subsys",c="",l=4),
            q.xu(n="RecordSubType",c="",l=2,o=22),
            q.xtriplet(n="Subsystem",o=24,t=subsystem),
            q.xtriplet(n="Identification",o=32,t=id_self),
            q.xtriplet(n="IOActivity",o=40,t=io_self),
            q.xtriplet(n="Return code ",t=return_code),
            q.xtriplet(n="ProcessorAccounting",t=processor_accounting),
            q.xx(n="AccountingTriplet",l=8,p="no"),
            ...
        gg]   

The layout of the data  is in the format of q.type(values)
Where values can be 

n 
:  The name of dat field

l 
: the length of the field

i 
: True ignore this field when creating the data 
t 
: the name of a triplet defintion.   A triplet is of the format

Field types are

q.xu 
: Unsigned integer 
q.xx 
: Unsigned integer formatted as a hex value
q.SMFTime
: Takes the value in the record and creates a Python time object
q.SMFDate
:  Takes the value in the record and creates a Python date object
q.xtriplet
:  Handles nested data in a triplet.
q.xp 
: takes a field of format yyyydddf and converts it to a Python date object

q.xb 
: Treats the data as a byte stream (not a character string)
q.x128 
: Time unit in units of 128 microseconds - converted to time
q.xhun
:  Converts hundedths of a second to time object
q.xtimehun
:  Time since midnights in hundreds of a second
q.xSTCK 
: converts a stck value into a Python Date Time object
q.xSTCKE
: converts a stcke value into a Python Date Time object
q.xoffset 
: SMF 42 section. Used for smf 42 record where we are just given an offset of a section.
    we point use t= to point to the template
    specify ol as the length of the block being pointed to

q.xtriplet
: the offset to teh data, length, and count
q.xarray
:  We get an 8 byte number first 4 bytes number, 
second 4 is length, 
the offset is the field following - so current_length+8



Parameters

## lookup list

compare the data with the value in the list.  If it matches, use the value

     q.xu(n="datasetType",l=1,x=q.lookup,x0=typelist),
     
For example

    typelist ={0:"Other",
        1:"PS",
        2:"PDS",
        3:"PDSE",
        4:"DA",
        5:"ISAM",
        6:"EXCP",
        7:"Extended physical sequential data set",
        10:"HFS",
        16:"KSDS data component",
        17:"KSDS index component",
        18:"Variable RRDS data component",
        19:"Variable RRDS index component",
        20:"Fixed length RRDS",
        21:"Linear",
        22:"ESDS"}


q.xu(n="entryDescriptor",l=1,x=q.bitmask,x0=entrydesc),

## Bit mask

    entrytype = [[0xc0,0xc0,"GSR"],
                 [0xc0,0x80,"LSR"],
                 [0xc0,0x40,"RLS"],
                 [0xc0,0x00,"NSR"],
                 [0x10,0x10,"Open for EXCP"],
                 [0x80,0x80,"Non VSAM fixed length"],
                 [0x40,0x40,"Program library"],
                 [0x20,0x20,"Extended format"],
                 [0x01,0x01,"Compressed format"]
                 ]

take the field, and do a logical and with the field field.
Now compare with the second field.  
If it matches then use the third value.

## References
A field like

              q.xoffset(n="ODataset",t=dataset,ol=112),
the t points to 

    dataset =[q.xu(n="offset",l=4),
              q.xs(n="datasetName",l=44,strip=True,),
              q.xu(n="datasetType",l=1,x=q.lookup,x0=typelist),
              q.xu(n="entryDescriptor",l=1,x=q.bitmask,x0=entrydesc),
              q.xu(n="datasetDescriptor",l=1,x=q.bitmask,x0=entrytype),
              q.xb(n="Reserved",l=1,i=True,),
              q.xoffset(n="odsio",t=datasetIO,ol=152),
              q.xoffset(n="oams",t=ams,ol=88,o=56),
        ]






