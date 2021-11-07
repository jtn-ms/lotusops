import os
import sys

msg_help = "\n\
            \n======== lotusspeed =========\
            \n\
            \nDescription: \
            \n            A tool for observing time-consuming in a specific sealing stage,\
            \n            to analyze miner or worker's log single or batch\
            \nUsage: \
            \n       [*miner-log* using output of `lotus-miner sectors status --log <sector-id>`] \
            \n       lotusspeed miner\
            \n       [*worker-log* based on rust loging]   \
            \n       lotusspeed [sealing-stage] [filepath/dirpath] [format(json|txt)]]\
            \nExamples: \
            \n       [worker-log: precommit1]\
            \n       lotusspeed precommit1 p1.log \
            \n       [worker-log: precommit2]\
            \n       lotusspeed precommit2 p2.log \
            \n       [worker-log: commit2]\
            \n       lotusspeed commit2 c2.log"

from .__constants__ import msg_file_or_dir_not_found
from lotusops.speedtest.sectorstatus import AnalyzeSectorLogs
from lotusops.speedtest.jsonformat import analyzeFile
from lotusops.speedtest.textformat import analyzeFile as analyzeTxTFile

def lotusspeed():
    if len(sys.argv) < 2 or \
        any(any(arg.startswith(mark) for mark in ["-h","--h","help"]) for arg in sys.argv): return msg_help
    if "miner" == sys.argv[1]: return AnalyzeSectorLogs([] if len(sys.argv)==2 else sys.argv[2:])
    if not os.path.exists(sys.argv[2]) or not os.path.isfile(sys.argv[2]): return msg_file_or_dir_not_found
    filters = {
        "precommit1": ["seal_pre_commit_phase1"],
        "p1": ["seal_pre_commit_phase1"],
        "pc1": ["seal_pre_commit_phase1"],
        "precommit2": ["seal_pre_commit_phase2","filecoin_proofs"],
        "p2": ["seal_pre_commit_phase2","filecoin_proofs"],
        "pc2": ["seal_pre_commit_phase2","filecoin_proofs"],
        "commit2": ["seal_commit_phase2"],
        "c2": ["seal_commit_phase2"],
        "c": ["seal_commit_phase2"]
    }.get(sys.argv[1], ["seal_commit_phase2"])
    if len(sys.argv) > 3:
        filters.append("SectorId")
        analyzeFile(os.path.abspath(sys.argv[2]),filters)
    else:
        analyzeTxTFile(os.path.abspath(sys.argv[2]),filters)
