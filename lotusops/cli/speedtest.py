import os
import sys

msg_help = "\n\
            \n======== loganalytics =========\
            \n\
            \nDescription: \
            \n            A tool for observing time-consuming in a specific sealing stage,\
            \n            to analyze miner or worker's log single or batch\
            \nUsage: \
            \n       [*worker-log* based on rust loging]   \
            \n       loganalytics [sealing-stage] [filepath/dirpath] \
            \n       [*miner-log* using output of `lotus-miner sectors status --log <sector-id>`] \
            \n       loganalytics miner\
            \nExamples: \
            \n       [worker-log: precommit1]\
            \n       loganalytics precommit1 p1.log \
            \n       [worker-log: precommit2]\
            \n       loganalytics precommit2 p2.log \
            \n       [worker-log: commit2]\
            \n       loganalytics commit2 c2.log"

from .__constants__ import msg_file_or_dir_not_found
from lotusops.speedtest.sealingspeed import AnalyzeSectorLogs

def loganalytics():
    if len(sys.argv) < 2 or any(argv.startswith("-h") for argv in sys.argv): return msg_help
    if "miner" == sys.argv[1]: return AnalyzeSectorLogs()
    if not os.path.exists(sys.argv[2]) or not os.path.isfile(sys.argv[2]): return msg_file_or_dir_not_found
