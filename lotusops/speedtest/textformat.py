

from lotusops.speedtest.jsonformat import string2datetime,msg2sectorId
# in:  2021-07-26T11:32:54.442
# out: datetime.datetime(2021, 7, 26, 11, 32, 54)
import datetime
def string2datetime(st):
    return datetime.datetime.strptime(st, "%Y-%m-%dT%H:%M:%S.%f")

def analyzeFile(filepath,filters):
    sectors={}
    with open(filepath,"r") as f:
        lines=f.readlines()
        for line in lines:
            if any(filter not in line for filter in filters): continue
            # structed=line.strip("\t")
            msg = line.rstrip("\n")
            if not any(mark in msg for mark in ["start","finish"]): continue
            id = msg2sectorId(msg)
            time=string2datetime(msg.split()[0])
            if "start" in msg: sectors[id]={};sectors[id]["start"]=time
            if "finish" in msg: sectors[id]["finish"]=time
            if all(key in sectors[id] for key in ["start","finish"]): 
                sectors[id]["period"]=sectors[id]["finish"]-sectors[id]["start"]
                print("SectorId({0})- duration:{1} start:{2} finish:{3}".format(id,sectors[id]["period"],sectors[id]["start"],sectors[id]["finish"]))
