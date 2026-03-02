'''
Process SMF 30 subtype 1 SMF records
'''
#import struct
import  smfobjects as q

zzzz = {"AAA":"KW1","B":"KW2"}


def xxx(value,x0,x1) :
    #print("In xxxx",value,x0,x1)
    pass

def process():
    '''
    main ( and only ) processing
    '''

    subsystem = [q.xu(n="SubsystemType",l=2,x=xxx,x0=zzzz),
                 q.xu(n="Reserved",l=1),
                 q.xu(n="flags",l=1,o=3),
                 q.xu(n="Version",l=2,o=4),
                 q.xs(n="SubsystemName",l=8,o=6),
                 q.xs(n="OpSysLvl",l=8),
                 q.xs(n="SystemName",l=8),
                 q.xs(n="SysplexName",l=8,o=30),
    ]

    return_code = [ q.xx(n="CompletionCode",l=2),
                    q.xx(n="CompletionIndicator",l=2),
                    q.xx(n="Reason",l=4),

    ]
    id_self   = [q.xs(n="Jobname",l=8),
                 q.xs(n="PgmName",l=8),
                 q.xs(n="StepName",l=8),
                 q.xs(n="Userid",l=8),
                 q.xs(n="JESID",l=8),
                 q.xu(n="StepNumber",l=2,o=40),
                 q.xs(n="JobClass",l=1),
                 q.xx(n="Flag",l=1,o=43),
                 q.xu(n="ignored",l=2),
                 q.xu(n="JesPriority",l=2),
                 q.SMFTime(n="DevAllocTime"),
                 q.SMFTime(n="probProgStartTime"),
                 q.SMFTime(n="InitSelTime",o=56),
                 q.SMFDate(n="InitSelDate"),
                 q.SMFTime(n="JobReadTime",o=64),
                 q.SMFDate(n="JobReadDate"),
                 q.SMFTime(n="JobEndTime",o=72),
                 q.SMFDate(n="JobEndDate"),
                 q.xs(n="ProgName",l=20),
                 q.xs(n="RACFGROUP",l=8),
                 q.xs(n="RACFUserid",l=8,o=108),
                 q.xs(n="RACFTerminid",l=8),
                 q.xs(n="TermSymName",l=8),
                 q.xs(n="StepName",l=8),
                 q.xs(n="JobClass",l=8),
                 q.xSTCK(n="intStartStck",l=8,o=148),
                 q.xSTCK(n="intEndStck",l=8,o=156),
                 q.xu(n="Substep",l=4,o=164),
                 q.xs(n="Unix Program Name",l=16,o=168),
                 q.xu(n="ASID",l=2),
                 q.xs(n="Jes Correlator",l=64,o=186),
    ]

    io_self = [q.xu(n="CardsRead",l=4,p="NZ"),
               q.xu(n="blocks",l=4),
               q.xu(n="tputs",l=4,p="NZ"),
               q.xu(n="tgets",l=4,p="NZ"),
               q.xu(n="readerDeviceClass",l=1),
               q.xu(n="readerDeviceType",l=1),
               q.x128(n="TotalConnect time",p="NZ"),
               q.xu(n="flags",l=4,p="NZ"),
               q.xu(n="reserved",l=2,o=26,p="no"),
               q.xu(n="reread",l=4,p="NZ"),
               q.x128(n="DASD IO connect time",p="NZ"),
               q.x128(n="DASD disconnect time",p="NZ"),
               q.x128(n="Pending",p="NZ"),
               q.x128(n="StartSubChannel",p="NZ"),
               q.x128(n="connectTimeIEnclaves",p="NZ"),
               q.x128(n="DASDDiscIEnclaves",p="NZ"),
               q.x128(n="DASDPend+CUQIenclaves",p="NZ"),
               q.x128(n="DASDSSubChIEnclaves",o=60,p="NZ"),
               q.xu(n="TotalBlocksExcp",l=4,p="NZ"),
               q.xu(n="DDAcctSupressed",l=4,p="NZ") 
    ]
    processor_accounting = [
                q.xu(n="Reserved",l=2,p="NZ"),
                q.xu(n="InvalidTimer",l=2,p="NZ"),
                q.xhun(n="TotalCPU",l=4),
                q.xhun(n="SRBCPU",l=4),
                q.xhun(n="InitTCBCPU",l=4,p="NZ"),
                q.xhun(n="InitSRBCPU",l=4,o=16,p="NZ"),
                q.xhun(n="StepVectorCPU",l=4,p="NZ"),
                q.xhun(n="InitVectorCPU",l=4,p="NZ"),
                q.xhun(n="StepVectorAffinity",l=4,p="NZ"),
                q.xhun(n="InitVectorAffinity",l=4,o=32,p="NZ"),
                q.xtimehun(n="IntervalStartTime",l=4),
                q.SMFDate(n="IntervalStartDate"),
                q.xhun(n="CPU IO interrupts",l=4,p="NZ"),
                q.xhun(n="CPU RCT",l=4,o=48,p="NZ"),
                q.xhun(n="CPU IO Hiperspace",l=4,p="NZ"),
                q.xu(n="ICSF count",l=4,o=56,p="NZ"),
                q.xu(n="Count of ADMF write pages",l=4,p="NZ"),
                q.xu(n="Count of ADMF read pages",l=4,p="NZ"),
                q.xhun(n="CPU Preempt SRB",l=4,p="NZ"),
                q.xhun(n="CPU Independant enclave",l=4,p="NZ"),
                q.xhun(n="CPU Dependant enclave",l=4,o=76,p="NZ"),
                q.xu(n="Enqueue Promote",l=4,p="NZ"),
                q.xx(n="Timer Flags",l=1,p="NZ"),
                q.xx(n="Failure flags",l=1,p="NZ"),
                q.xx(n="More Failure flags",l=1,o=86,p="NZ"),
                q.xx(n="Boost",l=1,p="NZ"),
                q.xhun(n="CPU ZAAP" ,l=4,p="NZ"),
                q.xhun(n="Enclave ZAAP",l=4,p="NZ"),
                q.xhun(n="Dep Enclave ZAAP",l=4,o=96,p="NZ"),
                q.xhun(n="ZAAP work on CP",l=4,p="NZ"),
                q.xhun(n="ZAAP Enclave work on CP",l=4,p="NZ"),
                q.xhun(n="ZAAP Dep Enclave work on CP",l=4,p="NZ"),
                q.xu(n="Enqueue promote",l=4,o=112,p="NZ"),
                q.xhun(n="CPU ZIIP" ,l=4,p="NZ"),
                q.xhun(n="Enclave ZIIP",l=4,p="NZ"),
                q.xhun(n="Dep Enclave ZIIP",l=4,o=124,p="NZ"),
                q.xhun(n="ZIIP work on CP",l=4,p="NZ"),
                q.xhun(n="ZIIP Enclave work on CP",l=4,p="NZ"),
                q.xhun(n="ZIIP Dep Enclave work on CP",l=4,p="NZ"),
      ]
    excp = [ q.xx("Device class",l=1),
            q.xx(n="Unit type",l=1),
            q.xx(n="Device Number",l=2),     
            q.xs(n="DDName",l=8),
            q.xu(n="Blocks",l=4),
            q.xu(n="Largest  Blocksize",l=2),
            q.x128(n="Device ConnectTime"),
            q.xx(n="block size value",l=8),
            ]   
    unix = [ q.xu(n="UNIX process id",l=4),
            q.xu(n="Unix group id",l=4),
            q.xu(n="Unix userid",l=4),
            q.xu(n="Unix process user group id",l=4,o=12),
            q.xu(n="Unix session id",l=4),
            q.xu(n="Unix services calls",l=4),
            q.xhun(n="Total CPU time",l=4),
            q.xu(n="Dir reads",l=4),
            q.xu(n="read file count",l=4),
            q.xu(n="write file count",l=4,o=36),
            q.xu(n="reserved",l=4,p="no"),
            q.xu(n="reserved",l=4,p="no"),
            q.xu(n="pathname lookups logical",l=4),
            q.xu(n="pathname lookups physical",l=4),
            q.xu(n="pathname generates physical",l=4),
            q.xu(n="pathname generates physical",l=4),
            q.xu(n="parent process id",l=4)

    ] 

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
            q.xx(n="StorageTriplet",l=8,o=72,p="no"),
            q.xx(n="PerformanceTriplet",l=8,o=80,p="no"),
            q.xx(n="OperatorTriplet",l=8,o=88,p="no"),
            q.xtriplet(n="EXCP",t=excp,o=96),
            q.xu(n="Old EXCP in other records",c="",l=2,o=104),
            q.xu(n="Reserved",c="",l=2),
            q.xu(n="EXCP in other records",c="",l=4),
            q.xx(n="APPCCumulativeTriplet",l=8,o=112,p="no"),
            q.xx(n="APPCCumulative",l=8,o=120,p="no"),
            q.xtriplet(n="OMVS",t=unix),
    ]
    return opts   
def type_subType():
        ''' 
        Return type/subtype
        '''
        return  "30/"


def init():
    s= smf()
    return s 
class smf():
    '''
    base class
    '''
    def __init__(self):
        self.name = ""
        self.rows = []

    def process(self):
        return process()

    def type_subType(self):
        return  "92/11"

    def doit(self,data):
        ofields = ["ID.JobName","Data.pathname","Data.Reads","Data.Writes",
                   "Data.DirBlocks","Data.FileType","Data.FlagByte"]
        
        o = pick.pick(data,ofields)
        self.rows.extend(o)
    def  end(self):

        if len(self.rows)  == 0 :
            return
        pd.set_option("display.max_columns", None)
        pd.set_option('max_colwidth', 70)
        pd.set_option('display.max_rows', None)
        pd.options.display.width = 1000
        df = pd.DataFrame.from_records(self.rows)
        #df2 = df.sort_values('pathname',axis=0)
        print(df)


