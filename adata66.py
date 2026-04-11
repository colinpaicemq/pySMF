'''
Process HLASM SYSDATA definition for symbols.
'''

import  smfobjects as q

def process():
    '''
    main (and only ) processing
    '''
    # map values to the description
    typelist ={0:"Undefined",1:"CSECT",2:"DSECT",3:"CommonSection",4:"DummyExternalDSect",
               5:"VCON",6:"QUalifier",7:"EXTRN/WXTRN",8:"LOCTR",9:"Duplicate",
               10:"Literal",11:"*InLiteralName",12:"EQU",13:"OrdinaryLabel",
               14:"Unresolvable EQU,DC,DS"}

    opts = [
                q.xu(n="Language",l=1),  # unsigned integer of length 1
                q.xx(n="Type",l=2),      # hex value of length 2 
                q.xu(n="Arch",l=1),
                q.xu(n="flag",l=1),
                q.xu(n="Edition",l=1),
                q.xu(n="Reserved",l=4),
                q.xu(n="ADFLen",l=2,),
                q.xu(n="ESDID",l=4,o=12),
                q.xu(n="Statement",l=4),
                q.xu(n="Offset",l=4),
                q.xu(n="SymType",l=1,x=q.lookup,x0=typelist), # map the values to a description
                q.xu(n="Dup",l=4),
                q.xs(n="TypeA",l=1,ea="E"),  # do Ebcdic to ASCII
                q.xs(n="AsmType",l=4,ea="E"),
                q.xs(n="ProgType",l=4,ea="E"),
                q.xu(n="Length",l=4),
                q.xu(n="IntA",l=2),
                q.xu(n="ScaleA",l=2),
                q.xu(n="SymFlag",l=1),
                q.xs(n="reserver2",l=7,i=True),
                q.xu(n="SymOffset",l=4,), # cannot be ignored because used
                q.xu(n="LSymbol",l=4,),  # cannot be ignored because used
                 #q.xs(n="Symbol",l=4,ea="E"), # generated afterwards

            ]
    return opts