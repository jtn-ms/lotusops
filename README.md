# lotusops - A DevOps tool for lotus(filecoin)
As a simply & smartly capsulized tool, it helps lotus users to inspect performance of their workers, autopledge cleverly, and abort & remove unnecessary jobs & sectors. This tool uses lotus-miner & ansible commands directly & indirectly. Before using it, please make sure `lotus-miner` & `ansible <workername> -m ping` is affordable on your miner node. The file path for ansible hosts is expected in `/etc/ansible/hosts`
### install
```
[from source]
git clone https://github.com/deep2essence/lotusops
python3 setup.py install

[from package]
pip install -U lotusops
```
### usages
commands|explanation
-----|--------------
***lotusspeed miner \<start-sector-id)\> \<end-sector-id)\>***|analyze a miner log to display time consumped at various sealing steps
ex1: ```lotusspeed miner```| over the whole life time of miner
ex2: ```lotusspeed miner 130 260```| over period between sector id 130 to 260
***lotusspeed \<sealing-type\> \<filepath(worker.log)\>***|analyze a miner log to display time consumped at various sealing steps
ex1: ```lotusspeed p1 worker.log```| inspect p1
ex2: ```lotusspeed p2 worker.log```| inspect p2
ex3: ```lotusspeed c2 worker.log```| inspect c2
***lotusops abort \<keyword\>***|abort all jobs with a certain keyword(AP,PC1,PC2,...)
ex: ```lotusops abort AP```|abort all AP jobs
***lotusops rmall \<keyword\>***|remove all sectors with a certain keyword(Packing, PreCommit1, PreCommit2, ...)
```lotusops rmall Packing```|remove all sectors at stage of Packing
***lotuspledge <interval> \<ip.list\>***|continous pledging with a certain ***interval*** in case of any affordable worker's existance
```lotuspledge inspect "172.26.48.134\|172.26.48.135"```|inspect workers connected to a miner(specifized in params, here 172.26.48.134 & 172.26.48.135)
```lotuspledge 1m 172.26.48.134```|continous pledging with a interval of 1 minute in case of any affordable worker's existance
```lotuspledge 90 ip.lst```| pledging with a certain interval(here, 90s) in case any worker of workers listed in ip.lst is affordable for pledging

### results
```
$ lotusspeed miner 230 270
>>>
*******************************************
MIN(SectorPacked)---0:01:01
MAX(SectorPacked)---0:21:34
MEAN(SectorPacked)---0:05:01
*******************************************
MIN(SectorPreCommit1)---2:56:53
MAX(SectorPreCommit1)---6:00:06
MEAN(SectorPreCommit1)---3:58:34
*******************************************
MIN(SectorPreCommit2)---0:11:50
MAX(SectorPreCommit2)---0:56:58
MEAN(SectorPreCommit2)---0:25:34
*******************************************
MIN(SectorSeedReady)---1:14:31
MAX(SectorSeedReady)---1:15:03
MEAN(SectorSeedReady)---1:14:57
*******************************************
MIN(SectorCommitted)---0:13:21
MAX(SectorCommitted)---0:48:32
MEAN(SectorCommitted)---0:23:52
*******************************************
DURATION: 0.8 days  START: 2021-11-04 19:48:46, FINISH: 2021-11-05 13:51:36
SECTOR SIZE: 32(GiB)
PC1: 0.38T, PC2: 0.38T, C: 0.38T, FIN: 0.38T

$ lotusspeed pc1 worker.log 
>>>
lotusspeed pc1 /filecoin1/worker.log 
SectorId(242)- DURATION:2:59:38    START:2021-11-04 22:00:33 FINISH:2021-11-05 01:00:12
SectorId(239)- DURATION:3:00:14    START:2021-11-04 22:00:42 FINISH:2021-11-05 01:00:56
SectorId(240)- DURATION:3:02:18    START:2021-11-04 22:00:39 FINISH:2021-11-05 01:02:57
SectorId(237)- DURATION:3:06:00    START:2021-11-04 22:00:30 FINISH:2021-11-05 01:06:31
SectorId(238)- DURATION:3:07:11    START:2021-11-04 22:00:30 FINISH:2021-11-05 01:07:42
SectorId(236)- DURATION:5:56:47    START:2021-11-04 21:53:19 FINISH:2021-11-05 03:50:06
*******************************************
MIN:  2:59:38
MAX:  5:56:47
MEAN: 3:32:01
*******************************************

$ lotusspeed p2 worker.log
>>>
DURATION:0:13:28    START:2021-11-05 01:00:16 FINISH:2021-11-05 01:13:44
DURATION:0:12:36    START:2021-11-05 01:13:44 FINISH:2021-11-05 01:26:21
DURATION:0:12:25    START:2021-11-05 01:26:21 FINISH:2021-11-05 01:38:47
DURATION:0:12:47    START:2021-11-05 01:38:47 FINISH:2021-11-05 01:51:34
DURATION:0:13:05    START:2021-11-05 01:51:35 FINISH:2021-11-05 02:04:40
DURATION:0:13:52    START:2021-11-05 03:50:18 FINISH:2021-11-05 04:04:11
*******************************************
MIN:  0:12:25
MAX:  0:13:52
MEAN: 0:13:02
*******************************************

$ lotuspledge inspect "172.26.48.134|172.26.48.135"
>>>
#######################################################
MINER REPORT:
              Queue(Committing:19,Removing:11,Packing:1,FinalizeSector:14)
           Assigned()
#######################################################
WORKER REPORT: 
{
    "172.26.48.134": {
        "557527": {
            "CACHED_SECTOR_CNT": 4,
            "CPU": 3,
            "CUDA_VISIBLE_DEVICES": "0",
            "FIL_PROOFS_MAXIMIZE_CACHING": "1",
            "FIL_PROOFS_PARAMETER_CACHE": "/filecoin1/filecoin-proof-parameters",
            "FIL_PROOFS_SDR_PARENTS_CACHE_SIZE": "1073741824",
            "FIL_PROOFS_USE_GPU_COLUMN_BUILDER": "1",
            "FIL_PROOFS_USE_GPU_TREE_BUILDER": "1",
            "FIL_PROOFS_USE_MULTICORE_SDR": "1",
            "LOTUS_MINER_PATH": "/filecoin1/.lotusminer",
            "LOTUS_PATH": "/filecoin1/.lotus_cali",
            "LOTUS_WORKER_PATH": "/filecoin1/lotusworker1",
            "MEM": 6,
            "STORAGE": 2583,
            "TMPDIR": "/filecoin1/lotusworker1/tmp",
            "TYPE": "PRECOMMIT",
            "WORKER": {
                "CACHED": "2,4,5,7",
                "ID": "000000",
                "MISMATCH": "",
                "RUNNING": "2,4,5,7"
            }
        },
        "557709": {
            "CACHED_SECTOR_CNT": 5,
            "CPU": 3,
            "CUDA_VISIBLE_DEVICES": "0",
            "FIL_PROOFS_MAXIMIZE_CACHING": "1",
            "FIL_PROOFS_PARAMETER_CACHE": "/filecoin1/filecoin-proof-parameters1",
            "FIL_PROOFS_SDR_PARENTS_CACHE_SIZE": "1073741824",
            "FIL_PROOFS_USE_GPU_COLUMN_BUILDER": "1",
            "FIL_PROOFS_USE_GPU_TREE_BUILDER": "1",
            "FIL_PROOFS_USE_MULTICORE_SDR": "1",
            "LOTUS_MINER_PATH": "/filecoin1/.lotusminer",
            "LOTUS_PATH": "/filecoin1/.lotus_cali",
            "LOTUS_WORKER_PATH": "/filecoin1/lotusworker5",
            "MEM": 6,
            "STORAGE": 2583,
            "TMPDIR": "/filecoin1/lotusworker5/tmp",
            "TYPE": "PRECOMMIT",
            "WORKER": {
                "CACHED": "1,3,6,8,9",
                "ID": "000000",
                "MISMATCH": "",
                "RUNNING": "1,3,6,8,9"
            }
        },
        "557905": {
            "CACHED_SECTOR_CNT": 0,
            "CPU": 0,
            "CUDA_VISIBLE_DEVICES": "1",
            "FIL_PROOFS_MAXIMIZE_CACHING": "1",
            "FIL_PROOFS_PARAMETER_CACHE": "/filecoin1/filecoin-proof-parameters",
            "FIL_PROOFS_SDR_PARENTS_CACHE_SIZE": "1073741824",
            "FIL_PROOFS_USE_GPU_COLUMN_BUILDER": "1",
            "FIL_PROOFS_USE_GPU_TREE_BUILDER": "1",
            "FIL_PROOFS_USE_MULTICORE_SDR": "1",
            "LOTUS_MINER_PATH": "/filecoin1/.lotusminer",
            "LOTUS_PATH": "/filecoin1/.lotus_cali",
            "LOTUS_WORKER_PATH": "/filecoin1/lotusworker3",
            "MEM": 18,
            "STORAGE": 0,
            "TMPDIR": "/filecoin1/lotusworker3/tmp",
            "TYPE": "COMMIT",
            "WORKER": {
                "CACHED": "",
                "ID": "000000",
                "MISMATCH": "",
                "RUNNING": ""
            }
        },
        "CPU": {
            "LOTUS_USEABLE(CNT)": 42,
            "LOTUS_USED": 6,
            "NON_LOTUS_USED": 2,
            "TOTAL": 128
        },
        "MEM": {
            "LOTUS_USEABLE(CNT)": 29,
            "LOTUS_USED": 30,
            "NON_LOTUS_USED": 86,
            "TOTAL": 2003
        },
        "STORAGE": {
            "PATH": {
                "filecoin1": {
                    "CACHED": 4653,
                    "COMMIT": {
                        "CACHED": 0,
                        "CACHED_SECTOR_CNT": 0,
                        "USED": 0
                    },
                    "LOTUS_USEABLE": 19696,
                    "NON_LOTUS_USED": 1763,
                    "PLEDGE_USEABLE": 19695,
                    "PRECOMMIT": {
                        "CACHED": 4653,
                        "CACHED_SECTOR_CNT": 9,
                        "USED": 5166
                    },
                    "SIZE": 21459,
                    "TYPE": [
                        "PRECOMMIT",
                        "PRECOMMIT",
                        "COMMIT"
                    ],
                    "USED": 6929
                }
            },
            "PLEDGE_USEABLE(CNT)": 38
        }
    },
    "172.26.48.135": {
        "173917": {
            "CACHED_SECTOR_CNT": 0,
            "CPU": 1,
            "CUDA_VISIBLE_DEVICES": "1",
            "FIL_PROOFS_MAXIMIZE_CACHING": "1",
            "FIL_PROOFS_PARAMETER_CACHE": "/filecoin3/filecoin-proof-parameters",
            "FIL_PROOFS_SDR_PARENTS_CACHE_SIZE": "1073741824",
            "FIL_PROOFS_USE_GPU_COLUMN_BUILDER": "1",
            "FIL_PROOFS_USE_GPU_TREE_BUILDER": "1",
            "FIL_PROOFS_USE_MULTICORE_SDR": "1",
            "LOTUS_WORKER_PATH": "/filecoin3/lotusworker3",
            "MEM": 78,
            "STORAGE": 0,
            "TMPDIR": "/filecoin3/tmp",
            "TYPE": "COMMIT",
            "WORKER": {
                "CACHED": "",
                "ID": "000000",
                "MISMATCH": "",
                "RUNNING": ""
            }
        },
        "174176": {
            "CACHED_SECTOR_CNT": 0,
            "CPU": 5,
            "CUDA_VISIBLE_DEVICES": "0",
            "FIL_PROOFS_MAXIMIZE_CACHING": "1",
            "FIL_PROOFS_PARAMETER_CACHE": "/filecoin1/filecoin-proof-parameters",
            "FIL_PROOFS_SDR_PARENTS_CACHE_SIZE": "1073741824",
            "FIL_PROOFS_USE_GPU_COLUMN_BUILDER": "1",
            "FIL_PROOFS_USE_GPU_TREE_BUILDER": "1",
            "FIL_PROOFS_USE_MULTICORE_SDR": "1",
            "LOTUS_WORKER_PATH": "/filecoin1/lotusworker",
            "MEM": 10,
            "STORAGE": 0,
            "TMPDIR": "/filecoin1/tmp",
            "TYPE": "PRECOMMIT",
            "WORKER": {
                "CACHED": "",
                "ID": "000000",
                "MISMATCH": "",
                "RUNNING": ""
            }
        },
        "174342": {
            "CACHED_SECTOR_CNT": 0,
            "CPU": 3,
            "CUDA_VISIBLE_DEVICES": "0",
            "FIL_PROOFS_MAXIMIZE_CACHING": "1",
            "FIL_PROOFS_PARAMETER_CACHE": "/filecoin2/filecoin-proof-parameters",
            "FIL_PROOFS_SDR_PARENTS_CACHE_SIZE": "1073741824",
            "FIL_PROOFS_USE_GPU_COLUMN_BUILDER": "1",
            "FIL_PROOFS_USE_GPU_TREE_BUILDER": "1",
            "FIL_PROOFS_USE_MULTICORE_SDR": "1",
            "LOTUS_WORKER_PATH": "/filecoin2/lotusworker",
            "MEM": 14,
            "STORAGE": 0,
            "TMPDIR": "/filecoin2/tmp",
            "TYPE": "PRECOMMIT",
            "WORKER": {
                "CACHED": "",
                "ID": "000000",
                "MISMATCH": "",
                "RUNNING": ""
            }
        },
        "CPU": {
            "LOTUS_USEABLE(CNT)": 85,
            "LOTUS_USED": 9,
            "NON_LOTUS_USED": 0,
            "TOTAL": 256
        },
        "MEM": {
            "LOTUS_USEABLE(CNT)": 31,
            "LOTUS_USED": 102,
            "NON_LOTUS_USED": 0,
            "TOTAL": 2003
        },
        "STORAGE": {
            "PATH": {
                "filecoin1": {
                    "CACHED": 0,
                    "COMMIT": {
                        "CACHED": 0,
                        "CACHED_SECTOR_CNT": 0,
                        "USED": 0
                    },
                    "LOTUS_USEABLE": 9227,
                    "NON_LOTUS_USED": 1501,
                    "PLEDGE_USEABLE": 9226,
                    "PRECOMMIT": {
                        "CACHED": 0,
                        "CACHED_SECTOR_CNT": 0,
                        "USED": 0
                    },
                    "SIZE": 10728,
                    "TYPE": [
                        "PRECOMMIT"
                    ],
                    "USED": 1501
                },
                "filecoin2": {
                    "CACHED": 0,
                    "COMMIT": {
                        "CACHED": 0,
                        "CACHED_SECTOR_CNT": 0,
                        "USED": 0
                    },
                    "LOTUS_USEABLE": 7000,
                    "NON_LOTUS_USED": 151,
                    "PLEDGE_USEABLE": 6999,
                    "PRECOMMIT": {
                        "CACHED": 0,
                        "CACHED_SECTOR_CNT": 0,
                        "USED": 0
                    },
                    "SIZE": 7151,
                    "TYPE": [
                        "PRECOMMIT"
                    ],
                    "USED": 151
                },
                "filecoin3": {
                    "CACHED": 0,
                    "COMMIT": {
                        "CACHED": 0,
                        "CACHED_SECTOR_CNT": 0,
                        "USED": 0
                    },
                    "LOTUS_USEABLE": 3449,
                    "NON_LOTUS_USED": 126,
                    "PLEDGE_USEABLE": 0,
                    "PRECOMMIT": {
                        "CACHED": 0,
                        "CACHED_SECTOR_CNT": 0,
                        "USED": 0
                    },
                    "SIZE": 3575,
                    "TYPE": [
                        "COMMIT"
                    ],
                    "USED": 126
                }
            },
            "PLEDGE_USEABLE(CNT)": 30
        }
    }
}
```
