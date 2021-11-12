import os
import sys

msg_help = "\n\
            \n======== lotusops =========\
            \n\
            \nDescription: \
            \n            A lotus-miner assistant tool for mainly processing job-abortion, sector-removal, pledging.\
            \n            It's a capsulation tool based on lotus-miner & shell scripts. Make sure lotus-miner is already installed.\
            \nUsage: \
            \n       [job-abortion] - to abort all sealing jobs with a certain keyword,\
            \n       lotusops abort <keyword>\
            \n       [sector-removal] - to remove all sectors with a certain keyword. \
            \n       lotusops remall <keyword>\
            \n       [multi-pledge] - to keep pledging with a certain interval until reaching to the indicated number in param. \
            \n       lotusops pledge <interval> <pledging-cnt>\
            \nExamples: \
            \n       [job-abortion]\
            \n       lotusops abort AP \
            \n       [sector-removal] \
            \n       lotusops rmall AP\
            \n       [multipledge] \
            \n       lotusops pledge 1m 28"

def lotusops():
    if len(sys.argv) < 3 or any(any(arg.startswith(mark) for mark in ["-h","--h","help"]) for arg in sys.argv): return msg_help
    if sys.argv[1] == "abort":
        execute(actioncode="abort",scripts="lotus-miner sealing jobs",filters=sys.argv[2].split("|"),excluded=len(sys.argv)>3)
    elif sys.argv[1] == "rmall":
        execute(actioncode="rmall",scripts="lotus-miner sectors list",filters=sys.argv[2].split("|"),excluded=len(sys.argv)>3)
    elif sys.argv[1] == "pledge" and len(sys.argv) > 3 and sys.argv[3].isdigit():
        execute(actioncode="pledge",scripts="lotus-miner sectors pledge",filters=sys.argv[2],excluded=sys.argv[3])
    else: return msg_help

import string

from lotusops.cli.lotuspledge import runscript
from lotusops.cli.lotuspledge import interpret

def execute(actioncode="abort",scripts="lotus-miner sealing jobs",filters=["AP"],excluded=False):
    # if pledge
    # pledge, lotus-miner sectors pledge, 1m, 28
    # for id in {1..28}; do lotus-miner sectors pledge; sleep 2m;done
    if actioncode == "pledge":
        interval=interpret(filters)
        try:
            cnt = int(excluded)
        except: cnt=1
        import time
        while cnt>0:
            print(runscript(scripts,isansible=False))
            cnt-=1
            time.sleep(interval)
        return
    # elif abort/rmall
    ids=[]
    try:
        if excluded:
            candidates=[line.split()[0] \
                        for line in runscript(scripts,isansible=False)[1:] \
                            if not any(filter in line for filter in filters) and \
                            all(c in string.hexdigits for c in line.split()[0])]
        else:
            candidates=[line.split()[0] \
                        for line in runscript(scripts,isansible=False)[1:]\
                            if all(filter in line for filter in filters)  and \
                                all(c in string.hexdigits for c in line.split()[0])]
        candidates=list(filter(None,candidates))
    except: return
    action = "lotus-miner sealing abort" if actioncode == "abort" else "lotus-miner sectors remove --really-do-it"
    for id in candidates:
        script=action+" %s"%id
        print(script)
        output = runscript(script,isansible=False)

