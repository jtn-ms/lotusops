# lotusops
A DevOps tool for lotus(filecoin)
### install
```
[from source]
git clone https://github.com/deep2essence/lotusops
python setup.py install

[from package]
pip install -U lotusops
```
### usages
commands|explanation|result
-----|--------------|-------
```lotusspeed miner```|analyze a miner log to display<br> time consumped at various <br>sealing steps|#############################<br>min(SectorPacked)---0:01:05<br>max(SectorPacked)---21:15:02<br>mean(SectorPacked)---1:12:40<br>#############################<br>min(SectorPreCommit1)---2:55:38<br>max(SectorPreCommit1)---12:33:49<br>mean(SectorPreCommit1)---3:57:55<br>#############################<br>min(SectorPreCommit2)---0:08:27<br>max(SectorPreCommit2)---3:21:59<br>mean(SectorPreCommit2)---1:09:05<br>#############################<br>min(SectorSeedReady)---1:14:59<br>max(SectorSeedReady)---1:15:01<br>mean(SectorSeedReady)---1:14:59<br>#############################<br>min(SectorCommitted)---0:15:34<br>max(SectorCommitted)---12:49:31<br>mean(SectorCommitted)---1:36:41<br>#############################
```lotusspeed precommit1 worker.log```| analyze a worker log to display time consumped at a specific sealing stage|  ...<br>2021-10-30T13:00:18.441 INFO filcrypto::proofs::api > seal_pre_commit_phase1: start
<br>2021-10-30T13:00:18.441 INFO filecoin_proofs::api::seal > seal_pre_commit_phase1:start: SectorId(129)
<br>2021-10-30T19:00:16.879 INFO filecoin_proofs::api::seal > seal_pre_commit_phase1:finish: SectorId(129)
<br>2021-10-30T19:00:16.879 INFO filcrypto::proofs::api > seal_pre_commit_phase1: finish
<br>...
```lotusops abort <keyword>```|abort all jobs<br> with a certain keyword|
```lotusops rmall <keyword>```|remove all sectors<br> with a certain keyword|
```lotusops autopledge <interval> <>```|continous pledge<br> in a certain interval|

