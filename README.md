# lotusops
A DevOps tool for lotus(filecoin)
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

$ lotuspledge inspect "172.26.48.134|172.26.48.135"
>>>

```
