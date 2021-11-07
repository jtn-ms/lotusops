
import os

sectors_log_dir = os.path.abspath("./sectors.logs") if os.name != 'nt' else os.path.abspath(".\\Calibnet\\sectors.logs")

#################
# line analysis #
#################
# in:  [event;sealing.SectorStartCC]
# out: SectorPreCommit1
def line2event(line):
    prefix="event;sealing."
    s = line.find(prefix) + len(prefix)
    return line[s:line.find("]")]

# in:  0.	2021-06-21 23:52:25 +0800 CST:	[event;sealing.SectorStartCC]	{"User":{"ID":30,"SectorType":8}}
# out: ['0.', '2021-06-21 23:52:25 +0800 CST:', '[event;sealing.SectorStartCC]', '{"User":{"ID":30,"SectorType":8}}']
def line2list(line):
    return line.split('\t')

import datetime
import time

# in:  2021-06-21 23:52:25 +0800 CST:
# out: datetime.datetime(2021, 6, 21, 23, 52, 25)
def string2datetime(st):
    return datetime.datetime.strptime(st, "%Y-%m-%d %H:%M:%S +0800 CST:")

#################
# file analysis #
#################

events=[
        "SectorStartCC",
        "SectorPacked",
        "SectorTicket",
        "SectorPreCommit1",
        "SectorPreCommit2",
        "SectorPreCommitBatch",
        "SectorPreCommitBatchSent",
        "SectorPreCommitLanded",
        "SectorSeedReady",
        "SectorCommitted",
        "SectorSubmitCommitAggregate",
        "SectorCommitAggregateSent",
        "SectorProving",
        "SectorFinalized",
        "SectorSealPreCommit1Failed",
        "SectorRetrySealPreCommit1",
]

def file2events(logfile):
    with open(logfile,"r") as f:
        lines=f.readlines()
        return lines2events(lines)

def lines2events(lines):
    sector_report={}
    previous=0
    for line in lines:
        items=line2list(line.rstrip("\n"))
        if len(items) < 4: continue
        now=string2datetime(items[1])
        if "SectorStartCC" in items[2]: previous=now
        sector_report[line2event(items[2])] = {
                                                "order":items[0].rstrip("."),   
                                                "time":now,
                                                "log":items[3],
                                                "period":now-previous
                                                }
        previous=now
    return sector_report

stages = ["SectorPacked","SectorPreCommit1","SectorPreCommit2","SectorSeedReady","SectorCommitted"]

def printReport(report):
    if "SectorStartCC" in report.keys(): print("SectorStartCC     {0}".format(report["SectorStartCC"]["time"]))
    if "SectorPacked" in report.keys():  print("SectorPacked:     {0}".format(report["SectorPacked"]["period"].strftime("%H:%M:%S")))
    if "SectorPreCommit1" in report.keys(): print("SectorPreCommit1: {0}".format(report["SectorPreCommit1"]["period"].strftime("%H:%M:%S")))
    if "SectorPreCommit2" in report.keys(): print("SectorPreCommit2: {0}".format(report["SectorPreCommit2"]["period"].strftime("%H:%M:%S")))
    # if "SectorSeedReady" in report.keys(): print("SectorSeedReady:  {0}".format(report["SectorSeedReady"]["period"])
    if "SectorCommitted" in report.keys(): print("SectorCommitted:  {0}".format(report["SectorCommitted"]["period"].strftime("%H:%M:%S")))
    if "SectorFinalized" in report.keys(): print("SectorFinalized:  {0}".format(report["SectorFinalized"]["time"]))

#################
#  dir analysis #
#################

def makeReport(start_id,end_id,issectorprinted=False):
    reports=[]
    for idx in range(start_id,end_id):
        logfile=os.path.join(sectors_log_dir,"%d.log"%idx)
        issectorprinted: print(logfile)
        if not os.path.exists(logfile): continue
        sector_report=file2events(logfile)
        printReport(sector_report)
        reports.append(sector_report)
        
    return reports

from string import Template

class DeltaTemplate(Template):
    delimiter = "%"

def strfdelta(tdelta, fmt="%H:%M:%S"):
    d = {"D": tdelta.days}
    hours, rem = divmod(tdelta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    d["H"] = '{:02d}'.format(hours)
    d["M"] = '{:02d}'.format(minutes)
    d["S"] = '{:02d}'.format(seconds)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)

def analyzeReport(reports):
    print("*******************************************")
    for stage in stages:        
        ## max, min, mean
        max_=datetime.timedelta(0)
        min_=datetime.timedelta(days=10)
        mean_=datetime.timedelta(0)
        ## initialize
        sum=datetime.timedelta(0)
        cnt=0
        for report in reports:
            if stage not in report.keys(): continue
            if "period" not in report[stage].keys(): continue
            if report[stage]["period"] > max_: max_=report[stage]["period"]
            if report[stage]["period"] < min_: min_=report[stage]["period"]
            sum+= report[stage]["period"]
            cnt+=1
        mean_=sum/cnt if cnt!=0 else sum
        print("[%s]"%stage)
        print("MIN:  {0}".format(min_))
        print("MAX:  {0}".format(max_))
        print("MEAN: {0}".format(strfdelta(mean_)))
        print("*******************************************")

    ## calc
    start=reports[0]["SectorStartCC"]["time"]
    end=start
    for report in reports:
        last=end
        if "SectorStartCC" in report.keys(): last=report["SectorStartCC"]["time"]
        if "SectorFinalized" in report.keys(): last=report["SectorFinalized"]["time"]
        if last>end: end=last
    duration=(end-start).total_seconds()/(24*3600.0)#days
    sector_size = 32#GiB
    _as_terabyte = sector_size/1000.0
    p1_cnt,p2_cnt,c2_cnt,fin_cnt=0,0,0,0
    for report in reports:
        if "SectorPreCommit1" in report.keys(): p1_cnt+=1
        if "SectorPreCommit2" in report.keys(): p2_cnt+=1
        if "SectorCommitted" in report.keys(): c2_cnt+=1
        if "SectorFinalized" in report.keys(): fin_cnt+=1
    print("DURATION: {0}  START: {1}, FINISH: {2}".format("%.1f days"%duration,start,end))
    print("SECTOR SIZE: %d(GiB)"%sector_size)
    print("PC1: %.2fT, PC2: %.2fT, C: %.2fT, FIN: %.2fT"%(\
                p1_cnt*_as_terabyte/duration,\
                p2_cnt*_as_terabyte/duration,\
                c2_cnt*_as_terabyte/duration,\
                fin_cnt*_as_terabyte/duration))

from lotusops.cli.lotuspledge import runscript

# lotusspeed miner 110 300
# argv=[110,300]
# lotusspeed miner 110
# arv [110]
# lotusspeed miner detail
# argv=['detail']
def AnalyzeSectorLogs(argv):
    
    try:
        output=runscript("lotus-miner sectors list",isansible=False)
        candidates = [line.split()[0] for line in output[1:]]
        sector_ids = [int(candidate) for candidate in candidates if candidate.isdigit()]
    except:
        return
    # start:end
    start = int(argv[0]) if len(argv)>0 and argv[0].isdigit() else sector_ids[0]
    end = int(argv[1]) if len(argv)>1 and argv[1].isdigit() else sector_ids[-1]
    issectorprinted=True if len(argv)>0 and not argv[0].isdigit() else False
    # make report
    reports=[]
    for id in sector_ids:
        if id < start: continue
        if id > end: break
        sector_log=runscript("lotus-miner sectors status --log %d"%id,isansible=False)
        sector_report=lines2events(sector_log)
        if issectorprinted: printReport(sector_report)
        reports.append(sector_report)
    # analyze report
    analyzeReport(reports)


if __name__ == "__main__":
    sectors=[]
    for f in os.listdir(sectors_log_dir):
        sectors.append(int(f.rstrip(".log")))
    sectors.sort()
    # print(sectors)
    first_id=min(sectors)
    last_id=max(sectors)
    # input start_sector_id, end_sector_id
    reports=makeReport(first_id,last_id)
    print("###################################################")
    analyzeReport(reports)