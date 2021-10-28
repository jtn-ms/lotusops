
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
from .constant import event

def file2events(logfile):
    sector_report={}
    with open(logfile,"r") as f:
        lines=f.readlines()
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
    if "SectorPacked" in report.keys():  print("SectorPacked:     {0}".format(report["SectorPacked"]["period"]))
    if "SectorPreCommit1" in report.keys(): print("SectorPreCommit1: {0}".format(report["SectorPreCommit1"]["period"]))
    if "SectorPreCommit2" in report.keys(): print("SectorPreCommit2: {0}".format(report["SectorPreCommit2"]["period"]))
    # if "SectorSeedReady" in report.keys(): print("SectorSeedReady:  {0}".format(report["SectorSeedReady"]["period"])
    if "SectorCommitted" in report.keys(): print("SectorCommitted:  {0}".format(report["SectorCommitted"]["period"]))
    if "SectorFinalized" in report.keys(): print("SectorFinalized:  {0}".format(report["SectorFinalized"]["time"]))

#################
#  dir analysis #
#################



def makeReport(start_id,end_id):
    reports=[]
    for idx in range(start_id,end_id):
        logfile=os.path.join(sectors_log_dir,"%d.log"%idx)
        print(logfile)
        if not os.path.exists(logfile): continue
        sector_report=file2events(logfile)
        printReport(sector_report)
        reports.append(sector_report)
        
    return reports

def analyzeReport(reports):
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
        mean_=sum/cnt
        print("min({0})---{1}".format(stage,min_))
        print("max({0})---{1}".format(stage,max_))
        print("mean({0})---{1}".format(stage,mean_))
        print("*******************************************")

    ## calc
    # for report in reports:
        


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