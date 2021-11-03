import os
import sys

msg_help = "\n\
            \n======== lotusops =========\
            \n\
            \nDescription: \
            \n            A lotus-miner assistant tool for mainly processing job-abortion & sector-removal.\
            \n            It's a capsulation tool based on lotus-miner & shell scripts. Make sure lotus-miner is already installed.\
            \nUsage: \
            \n       [job-abortion] - to abort all sealing jobs with a certain keyword,\
            \n       lotusops abort <keyword>\
            \n       [sector-removal] - to remove all sectors with a certain keyword. \
            \n       lotusops remall <keyword>\
            \nExamples: \
            \n       [job-abortion]\
            \n       lotusops abort AP \
            \n       [sector-removal] \
            \n       lotusops rmall AP"

def lotusops():
    if len(sys.argv) < 3 or any(arg.startswith("-h") for arg in sys.argv): return msg_help
    if sys.argv[1] == "abort":
        execute(actioncode="abort",scripts="lotus-miner sealing jobs",filters=sys.argv[2].split("|"),excluded=len(sys.argv)>3)
    elif sys.argv[1] == "rmall":
        execute(actioncode="rmall",scripts="lotus-miner sectors list",filters=sys.argv[2].split("|"),excluded=len(sys.argv)>3)
    else: return msg_help

import string

from lotusops.cli.lotuspledge import runscript

def execute(actioncode="abort",scripts="lotus-miner sealing jobs",filters=["AP"],excluded=False):

    ids=[]
    try:
        if excluded:
            candidates=[line.split()[0] \
                        if not any(filter in line for filter in filters) and \
                            all(c in string.hexdigits for c in line.split(' ')[0]) else '' \
                        for line in runscript(scripts,isansible=False)[1:]]
        else:
            candidates=[line.split()[0] \
                        if all(filter in line for filter in filters)  and \
                           all(c in string.hexdigits for c in line.split(' ')[0]) else '' \
                        for line in runscript(scripts,isansible=False)[1:]]
        candidates=list(filter(None,candidates))
    except: return
    action = "lotus-miner sealing abort" if actioncode == "abort" else "lotus-miner sectors remove --really-do-it"
    for id in candidates:
        script=action+" %s"%id
        print(script)
        output = runscript(script,isansible=False)

