

from lotusops.speedtest.jsonformat import string2datetime,msg2sectorId
# in:  2021-07-26T11:32:54.442
# out: datetime.datetime(2021, 7, 26, 11, 32, 54)
# import datetime
# def string2datetime(st):
#     return datetime.datetime.strptime(st, "%Y-%m-%dT%H:%M:%S.%f")

from lotusops.speedtest.sectorstatus import strfdelta
import datetime

def analyzeFile(filepaths,filters):
    total_cnt,total_sum=0,datetime.timedelta(0)
    start,finish=string2datetime("2089-01-01T00:00:00.000"),string2datetime("1989-01-01T00:00:00.000")
    for filepath in filepaths:
        sector,sectors={},{}
        with open(filepath,"r") as f:
            lines=f.readlines()
            for line in lines:
                if any(filter not in line for filter in filters): continue
                # structed=line.strip("\t")
                msg = line.rstrip("\n")
                if not any(mark in msg for mark in ["start","finish"]): continue
                time=string2datetime(msg.split()[0])
                # in case of precommit2
                if any("seal_pre_commit_phase2" in filter for filter in filters):
                    if "start" in msg: sector["start"]=time; start=start if time > start else time;continue
                    if "finish" in msg: sector["finish"]=time; finish=finish if time < finish else time
                    if all(key in sector for key in ["start","finish"]): 
                        sector["period"]=sector["finish"]-sector["start"]
                        print("DURATION:{0}    START:{1} FINISH:{2}".format(strfdelta(sector["period"]),sector["start"].strftime("%Y-%m-%d %H:%M:%S"),sector["finish"].strftime("%Y-%m-%d %H:%M:%S")))
                        sectors[sector["start"]]=sector
                    sector={};continue
                # in case of precommit1, commit2
                id = msg2sectorId(msg)
                if id < 0: continue
                if id not in sectors.keys(): sectors[id]={}
                if "start" in msg: sectors[id]["start"]=time; start=start if time > start else time; continue
                if "finish" in msg: sectors[id]["finish"]=time; finish=finish if time < finish else time
                if all(key in sectors[id] for key in ["start","finish"]): 
                    sectors[id]["period"]=sectors[id]["finish"]-sectors[id]["start"]
                    print("SectorId({0})- DURATION:{1}    START:{2} FINISH:{3}".format(id,strfdelta(sectors[id]["period"]),sectors[id]["start"].strftime("%Y-%m-%d %H:%M:%S"),sectors[id]["finish"].strftime("%Y-%m-%d %H:%M:%S")))
            # analyze
            
            ## max, min, mean
            max_=datetime.timedelta(0)
            min_=datetime.timedelta(days=10)
            mean_=datetime.timedelta(0)
            ## initialize
            sum=datetime.timedelta(0)
            cnt=0
            for k,v in sectors.items():
                if "period" not in v.keys(): continue
                cnt+=1
                if v["period"] < min_: min_= v["period"]
                if v["period"] > max_: max_= v["period"]
                sum+=v["period"]
            mean_=sum/cnt if cnt!=0 else sum
            total_cnt+=cnt
            total_sum+=sum
            print("*******************************************")  
            print("MIN:  {0}".format(strfdelta(min_)))
            print("MAX:  {0}".format(strfdelta(max_)))
            print("MEAN: {0}".format(strfdelta(mean_)))
            print("*******************************************")
    # speed calculation
    if total_cnt == 0: return
    duration=(finish-start).total_seconds()/(24*3600.0)#days
    meantime=(total_sum/total_cnt).total_seconds()/(24*3600.0)#days
    sector_size = 32#GiB
    _as_terabyte = sector_size/1000.0
    dspeed = total_cnt*_as_terabyte/duration
    mspeed = len(filepaths) *_as_terabyte/meantime
    print("SectorSize: 32GiB, SectorCnt: {0}, MeanTime: {1}".\
        format(total_cnt,\
              "%.1f hours"%(meantime*24) if any("seal_pre_commit_phase1" in filter for filter in filters) else \
              "%.1f mins"%(meantime*24*60)))
    print("DURATION:{0} START: {1}, FINISH: {2}".\
        format(strfdelta(finish-start),\
            start.strftime("%Y-%m-%d %H:%M:%S"),\
            finish.strftime("%Y-%m-%d %H:%M:%S")))
    if any("seal_pre_commit_phase1" in filter for filter in filters):
        print("MINING RATE: {0}".format("%.1fTiB/D"%dspeed))
    else:
        print("MINING RATE: {0}|{1}TiB/D".format("%.1f"%dspeed,"%.1f"%mspeed))

