handi(handy)

A DevOps tool for lotus(filecoin)

Installation

$ pip install -U lotusops


Utilities

1. Handling Sectors/Jobs
- abort all jobs with a certain keyword
```
$ lotusops abort AP 
```
- remove all sectors with a certain keyword
```
$ lotusops rmall Packing
```

2. Speed Testing
- miner
```
$ lotusspeed miner
$ lotusspeed miner 130 260
>>>
*******************************************
min(SectorPacked)---0:01:01
max(SectorPacked)---0:21:34
mean(SectorPacked)---0:05:01.414634
*******************************************
min(SectorPreCommit1)---2:56:53
max(SectorPreCommit1)---6:00:06
mean(SectorPreCommit1)---3:58:34.777778
*******************************************
min(SectorPreCommit2)---0:11:50
max(SectorPreCommit2)---0:56:58
mean(SectorPreCommit2)---0:25:34.888889
*******************************************
min(SectorSeedReady)---1:14:31
max(SectorSeedReady)---1:15:03
mean(SectorSeedReady)---1:14:57.222222
*******************************************
min(SectorCommitted)---0:13:21
max(SectorCommitted)---0:48:32
mean(SectorCommitted)---0:23:52.222222
*******************************************
DURATION: 0.8 days  START: 2021-11-04 19:48:46, FINISH: 2021-11-05 13:51:36
SECTOR SIZE: 32(GiB)
PC1: 0.38T, PC2: 0.38T, C: 0.38T, FIN: 0.38T
```
- worker
```
[precommit1]
$ lotusspeed pc1 worker.log 
>>>
lotusspeed pc1 /filecoin1/worker.log 
SectorId(242)- duration:2:59:38.573000    start:2021-11-04 22:00:33.471000 finish:2021-11-05 01:00:12.044000
SectorId(239)- duration:3:00:14.281000    start:2021-11-04 22:00:42.645000 finish:2021-11-05 01:00:56.926000
SectorId(240)- duration:3:02:18.058000    start:2021-11-04 22:00:39.649000 finish:2021-11-05 01:02:57.707000
SectorId(237)- duration:3:06:00.746000    start:2021-11-04 22:00:30.460000 finish:2021-11-05 01:06:31.206000
SectorId(238)- duration:3:07:11.549000    start:2021-11-04 22:00:30.930000 finish:2021-11-05 01:07:42.479000
SectorId(236)- duration:5:56:47.357000    start:2021-11-04 21:53:19.561000 finish:2021-11-05 03:50:06.918000
*******************************************
MIN:  2:59:38.573000
MAX:  5:56:47.357000
MEAN: 3:32:01.760667
*******************************************

[precommit2]
$ lotusspeed p2 worker.log
>>>
duration:0:13:28.450000    start:2021-11-05 01:00:16.379000 finish:2021-11-05 01:13:44.829000
duration:0:12:36.169000    start:2021-11-05 01:13:44.959000 finish:2021-11-05 01:26:21.128000
duration:0:12:25.859000    start:2021-11-05 01:26:21.280000 finish:2021-11-05 01:38:47.139000
duration:0:12:47.286000    start:2021-11-05 01:38:47.292000 finish:2021-11-05 01:51:34.578000
duration:0:13:05.055000    start:2021-11-05 01:51:35.431000 finish:2021-11-05 02:04:40.486000
duration:0:13:52.662000    start:2021-11-05 03:50:18.829000 finish:2021-11-05 04:04:11.491000
*******************************************
MIN:  0:12:25.859000
MAX:  0:13:52.662000
MEAN: 0:13:02.580167
*******************************************
```

3. Inspect/Autopledge
- Inspect: inspect workers connected to a miner
```
$ lotuspledge inspect "172.26.48.134|172.26.48.135"
>>>

```
- Autopledge: continous pledging with a interval in case of any affordable worker's existance
```
$ lotuspledge 1m "172.26.48.134|172.26.48.135"
>>>
#######################################################
MINER REPORT:
              Queue(Removing:11,PreCommit1:29,Packing:1,FinalizeSector:3,Committing:19)
           Assigned(PC1:29)
#######################################################
WORKER REPORT: 
{
    "172.26.48.134": {
        "236097": {
            "CACHED_SECTOR_CNT": 21,
            "CPU": 2,
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
            "MEM": 648,
            "STORAGE": 6592,
            "TMPDIR": "/filecoin1/lotusworker1/tmp",
            "TYPE": "PRECOMMIT",
            "WORKER": {
                "CACHED": "117,121,123,124,226,227,228,229,230,231,232,233,234,235,247,251,257,262,264,269,270",
                "ID": "4201c3f2",
                "MISMATCH": "226,227,228,229,230,231,232,233,234,235,123,117,121,124",
                "RUNNING": "247,251,257,262,264,269,270"
            }
        },
        "236234": {
            "CACHED_SECTOR_CNT": 8,
            "CPU": 2,
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
            "MEM": 632,
            "STORAGE": 2510,
            "TMPDIR": "/filecoin1/lotusworker5/tmp",
            "TYPE": "PRECOMMIT",
            "WORKER": {
                "CACHED": "235,248,253,255,259,261,268,272",
                "ID": "702477fb",
                "MISMATCH": "235",
                "RUNNING": "248,253,255,259,261,268,272"
            }
        },
        "CPU": {
            "LOTUS_USEABLE(CNT)": 42,
            "LOTUS_USED": 4,
            "NON_LOTUS_USED": 0,
            "TOTAL": 128
        },
        "MEM": {
            "LOTUS_USEABLE(CNT)": 31,
            "LOTUS_USED": 1280,
            "NON_LOTUS_USED": 1,
            "TOTAL": 2003
        },
        "STORAGE": {
            "PATH": {
                "filecoin1": {
                    "CACHED": 14993,
                    "COMMIT": {
                        "CACHED": 0,
                        "CACHED_SECTOR_CNT": 0,
                        "USED": 0
                    },
                    "LOTUS_USEABLE": 20177,
                    "NON_LOTUS_USED": 1282,
                    "PLEDGE_USEABLE": 20177,
                    "PRECOMMIT": {
                        "CACHED": 14993,
                        "CACHED_SECTOR_CNT": 29,
                        "USED": 9102
                    },
                    "SIZE": 21459,
                    "TYPE": [
                        "PRECOMMIT",
                        "PRECOMMIT"
                    ],
                    "USED": 10384
                }
            },
            "PLEDGE_USEABLE(CNT)": 39
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
            "MEM": 70,
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
            "CACHED_SECTOR_CNT": 7,
            "CPU": 9,
            "CUDA_VISIBLE_DEVICES": "0",
            "FIL_PROOFS_MAXIMIZE_CACHING": "1",
            "FIL_PROOFS_PARAMETER_CACHE": "/filecoin1/filecoin-proof-parameters",
            "FIL_PROOFS_SDR_PARENTS_CACHE_SIZE": "1073741824",
            "FIL_PROOFS_USE_GPU_COLUMN_BUILDER": "1",
            "FIL_PROOFS_USE_GPU_TREE_BUILDER": "1",
            "FIL_PROOFS_USE_MULTICORE_SDR": "1",
            "LOTUS_WORKER_PATH": "/filecoin1/lotusworker",
            "MEM": 630,
            "STORAGE": 1856,
            "TMPDIR": "/filecoin1/tmp",
            "TYPE": "PRECOMMIT",
            "WORKER": {
                "CACHED": "245,249,252,256,263,267,273",
                "ID": "d669c220",
                "MISMATCH": "",
                "RUNNING": "245,249,252,256,263,267,273"
            }
        },
        "174342": {
            "CACHED_SECTOR_CNT": 8,
            "CPU": 3,
            "CUDA_VISIBLE_DEVICES": "0",
            "FIL_PROOFS_MAXIMIZE_CACHING": "1",
            "FIL_PROOFS_PARAMETER_CACHE": "/filecoin2/filecoin-proof-parameters",
            "FIL_PROOFS_SDR_PARENTS_CACHE_SIZE": "1073741824",
            "FIL_PROOFS_USE_GPU_COLUMN_BUILDER": "1",
            "FIL_PROOFS_USE_GPU_TREE_BUILDER": "1",
            "FIL_PROOFS_USE_MULTICORE_SDR": "1",
            "LOTUS_WORKER_PATH": "/filecoin2/lotusworker",
            "MEM": 666,
            "STORAGE": 2208,
            "TMPDIR": "/filecoin2/tmp",
            "TYPE": "PRECOMMIT",
            "WORKER": {
                "CACHED": "246,250,254,258,260,265,266,271",
                "ID": "aca0246c",
                "MISMATCH": "",
                "RUNNING": "246,250,254,258,260,265,266,271"
            }
        },
        "CPU": {
            "LOTUS_USEABLE(CNT)": 84,
            "LOTUS_USED": 13,
            "NON_LOTUS_USED": 2,
            "TOTAL": 256
        },
        "MEM": {
            "LOTUS_USEABLE(CNT)": 31,
            "LOTUS_USED": 1366,
            "NON_LOTUS_USED": 2,
            "TOTAL": 2003
        },
        "STORAGE": {
            "PATH": {
                "filecoin1": {
                    "CACHED": 3619,
                    "COMMIT": {
                        "CACHED": 0,
                        "CACHED_SECTOR_CNT": 0,
                        "USED": 0
                    },
                    "LOTUS_USEABLE": 9495,
                    "NON_LOTUS_USED": 1233,
                    "PLEDGE_USEABLE": 9495,
                    "PRECOMMIT": {
                        "CACHED": 3619,
                        "CACHED_SECTOR_CNT": 7,
                        "USED": 1856
                    },
                    "SIZE": 10728,
                    "TYPE": [
                        "PRECOMMIT"
                    ],
                    "USED": 3089
                },
                "filecoin2": {
                    "CACHED": 4136,
                    "COMMIT": {
                        "CACHED": 0,
                        "CACHED_SECTOR_CNT": 0,
                        "USED": 0
                    },
                    "LOTUS_USEABLE": 7256,
                    "NON_LOTUS_USED": -105,
                    "PLEDGE_USEABLE": 7256,
                    "PRECOMMIT": {
                        "CACHED": 4136,
                        "CACHED_SECTOR_CNT": 8,
                        "USED": 2208
                    },
                    "SIZE": 7151,
                    "TYPE": [
                        "PRECOMMIT"
                    ],
                    "USED": 2103
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
            "PLEDGE_USEABLE(CNT)": 32
        }
    }
}

```

License

MIT License <https://choosealicense.com/licenses/mit>