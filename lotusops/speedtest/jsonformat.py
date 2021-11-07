# {"level":"info","ts":"2021-07-26T15:10:04.756+0800","logger":"filcrypto::proofs::api","caller":"src/proofs/api.rs:374","msg":"seal_commit_phase2: start"}
# {"level":"info","ts":"2021-07-26T15:10:04.836+0800","logger":"filecoin_proofs::api::seal","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/filecoin-proofs-8.0.2/src/api/seal.rs:459","msg":"seal_commit_phase2:start: SectorId(81)"}
# {"level":"info","ts":"2021-07-26T15:10:04.836+0800","logger":"filecoin_proofs::caches","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/filecoin-proofs-8.0.2/src/caches.rs:49","msg":"trying parameters memory cache for: STACKED[34359738368]"}
# cat /filecoin/worker.log|grep seal_commit_phase2
# {"level":"info","ts":"2021-07-26T15:10:04.836+0800","logger":"filecoin_proofs::caches","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/filecoin-proofs-8.0.2/src/caches.rs:54","msg":"found params in memory cache for STACKED[34359738368]"}
# {"level":"info","ts":"2021-07-26T15:10:04.836+0800","logger":"filecoin_proofs::api::seal","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/filecoin-proofs-8.0.2/src/api/seal.rs:488","msg":"got groth params (34359738368) while sealing"}
# {"level":"info","ts":"2021-07-26T15:10:04.836+0800","logger":"filecoin_proofs::api::seal","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/filecoin-proofs-8.0.2/src/api/seal.rs:509","msg":"snark_proof:start"}
################# 2.5min{ 
# {"level":"info","ts":"2021-07-26T15:10:04.848+0800","logger":"bellperson::groth16::prover","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/bellperson-0.14.2/src/groth16/prover.rs:276","msg":"Bellperson 0.14.2 is being used!"}
# {"level":"info","ts":"2021-07-26T15:12:34.490+0800","logger":"bellperson::groth16::prover","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/bellperson-0.14.2/src/groth16/prover.rs:561","msg":"starting proof timer"}
################# } GPU is available for FFT!
# {"level":"info","ts":"2021-07-26T15:12:36.907+0800","logger":"bellperson::gpu::locks","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/bellperson-0.14.2/src/gpu/locks.rs:157","msg":"GPU is available for FFT!"}
# {"level":"debug","ts":"2021-07-26T15:12:36.907+0800","logger":"bellperson::gpu::locks","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/bellperson-0.14.2/src/gpu/locks.rs:20","msg":"Acquiring GPU lock at "/tmp/bellman.gpu.lock" ..."}
# {"level":"debug","ts":"2021-07-26T15:12:36.907+0800","logger":"bellperson::gpu::locks","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/bellperson-0.14.2/src/gpu/locks.rs:24","msg":"GPU lock acquired!"}
# {"level":"info","ts":"2021-07-26T15:12:37.018+0800","logger":"bellperson::gpu::fft","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/bellperson-0.14.2/src/gpu/fft.rs:47","msg":"FFT: 1 working device(s) selected."}
# {"level":"info","ts":"2021-07-26T15:12:37.018+0800","logger":"bellperson::gpu::fft","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/bellperson-0.14.2/src/gpu/fft.rs:48","msg":"FFT: Device 0: GeForce RTX 2080 Ti"}
################ 3.5min{ GPU FFT kernel instantiated!
# {"level":"info","ts":"2021-07-26T15:12:37.018+0800","logger":"bellperson::domain","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/bellperson-0.14.2/src/domain.rs:568","msg":"GPU FFT kernel instantiated!"}
# {"level":"debug","ts":"2021-07-26T15:16:15.906+0800","logger":"bellperson::gpu::locks","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/bellperson-0.14.2/src/gpu/locks.rs:31","msg":"GPU lock released!"}
################ } GPU is available for Multiexp!
# {"level":"info","ts":"2021-07-26T15:16:20.413+0800","logger":"bellperson::gpu::locks","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/bellperson-0.14.2/src/gpu/locks.rs:158","msg":"GPU is available for Multiexp!"}
# {"level":"debug","ts":"2021-07-26T15:16:20.413+0800","logger":"bellperson::gpu::locks","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/bellperson-0.14.2/src/gpu/locks.rs:20","msg":"Acquiring GPU lock at "/tmp/bellman.gpu.lock" ..."}
# {"level":"debug","ts":"2021-07-26T15:16:20.413+0800","logger":"bellperson::gpu::locks","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/bellperson-0.14.2/src/gpu/locks.rs:24","msg":"GPU lock acquired!"}
# {"level":"info","ts":"2021-07-26T15:16:20.624+0800","logger":"bellperson::gpu::multiexp","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/bellperson-0.14.2/src/gpu/multiexp.rs:246","msg":"Multiexp: 2 working device(s) selected. (CPU utilization: 0)"}
# {"level":"info","ts":"2021-07-26T15:16:20.624+0800","logger":"bellperson::gpu::multiexp","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/bellperson-0.14.2/src/gpu/multiexp.rs:252","msg":"Multiexp: Device 0: GeForce RTX 2080 Ti (Chunk-size: 7488999)"}
# {"level":"info","ts":"2021-07-26T15:16:20.624+0800","logger":"bellperson::gpu::multiexp","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/bellperson-0.14.2/src/gpu/multiexp.rs:252","msg":"Multiexp: Device 1: GeForce RTX 2080 Ti (Chunk-size: 7488999)"}
################ 13min{ GPU Multiexp kernel instantiated!
# {"level":"info","ts":"2021-07-26T15:16:20.624+0800","logger":"bellperson::multiexp","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/bellperson-0.14.2/src/multiexp.rs:402","msg":"GPU Multiexp kernel instantiated!"}
# {"level":"debug","ts":"2021-07-26T15:29:18.412+0800","logger":"bellperson::gpu::locks","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/bellperson-0.14.2/src/gpu/locks.rs:31","msg":"GPU lock released!"}
################ }
# {"level":"info","ts":"2021-07-26T15:29:18.436+0800","logger":"bellperson::groth16::prover","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/bellperson-0.14.2/src/groth16/prover.rs:522","msg":"prover time: 1003.945903624s"}
# {"level":"info","ts":"2021-07-26T15:29:21.069+0800","logger":"filecoin_proofs::api::seal","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/filecoin-proofs-8.0.2/src/api/seal.rs:517","msg":"snark_proof:finish"}
# {"level":"info","ts":"2021-07-26T15:29:21.069+0800","logger":"filecoin_proofs::api::seal","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/filecoin-proofs-8.0.2/src/api/seal.rs:927","msg":"verify_seal:start: SectorId(81)"}
# {"level":"info","ts":"2021-07-26T15:29:21.069+0800","logger":"filecoin_proofs::caches","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/filecoin-proofs-8.0.2/src/caches.rs:49","msg":"trying parameters memory cache for: STACKED[34359738368]-verifying-key"}
# {"level":"info","ts":"2021-07-26T15:29:21.069+0800","logger":"filecoin_proofs::caches","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/filecoin-proofs-8.0.2/src/caches.rs:54","msg":"found params in memory cache for STACKED[34359738368]-verifying-key"}
# {"level":"info","ts":"2021-07-26T15:29:21.069+0800","logger":"filecoin_proofs::api::seal","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/filecoin-proofs-8.0.2/src/api/seal.rs:970","msg":"got verifying key (34359738368) while verifying seal"}
# {"level":"info","ts":"2021-07-26T15:29:21.083+0800","logger":"filecoin_proofs::api::seal","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/filecoin-proofs-8.0.2/src/api/seal.rs:995","msg":"verify_seal:finish: SectorId(81)"}
# {"level":"info","ts":"2021-07-26T15:29:21.083+0800","logger":"filecoin_proofs::api::seal","caller":"/root/.cargo/registry/src/github.com-1ecc6299db9ec823/filecoin-proofs-8.0.2/src/api/seal.rs:543","msg":"seal_commit_phase2:finish: SectorId(81)"}
# {"level":"info","ts":"2021-07-26T15:29:21.083+0800","logger":"filcrypto::proofs::api","caller":"src/proofs/api.rs:400","msg":"seal_commit_phase2: finish"}

import os
import json

worker_log=os.path.abspath(".\\Calibnet\\worker.commit.log")
if (os.name != 'nt'): 
    sectors_log_dir=os.path.abspath("./worker.commit.log")
    
def msg2sectorId(msg):
    s = msg.find("(")
    e = msg.find(")")
    import string
    if s < 0 or e < 0 or e < s or \
       any(c not in string.digits for c in msg[s+1:e]): return -1
    return int(msg[s+1:e])

# in:  2021-06-21 23:52:25+0800
#      2021-06-21 23:52:25.442
#      2021-06-21 23:52:25 +0800 CST:
# out: datetime.datetime(2021, 6, 21, 23, 52, 25)
import datetime
def string2datetime(st):
    if " +0800 CST:"in st: return datetime.datetime.strptime(st, "%Y-%m-%d %H:%M:%S +0800 CST:")
    if "+800" in st: return datetime.datetime.strptime(st, "%Y-%m-%dT%H:%M:%S.%f+0800")
    return datetime.datetime.strptime(st, "%Y-%m-%dT%H:%M:%S.%f")

def makeReport(logfile,filters=["seal_commit_phase2","SectorId"]):
    sectors={}
    with open(logfile,'r') as f:
        lines=f.readlines()
        lastfinish=-1
        for line in lines:
            log=line.rstrip("\n")
            try: jslog=json.loads(log)
            except: continue
            if "msg" not in jslog.keys() or \
               any(filstr not in jslog["msg"] for filstr in  filters): continue
            
            id=msg2sectorId(jslog["msg"])
            ts=string2datetime(jslog["ts"])
            if id not in sectors.keys(): sectors[id]={}
            if "start" in jslog["msg"]: 
                sectors[id]["start"] = ts
                sectors[id]["interval"]=sectors[id]["start"] - lastfinish if lastfinish != -1 and sectors[id]["start"] > lastfinish else datetime.timedelta(0)
                sectors[id]["duration"] = datetime.timedelta(0)
                sectors[id]["finish"] = ts
            if "finish" in jslog["msg"]: 
                sectors[id]["finish"] = ts
                sectors[id]["duration"] = sectors[id]["finish"] - sectors[id]["start"] if sectors[id]["finish"] > sectors[id]["start"] else datetime.timedelta(0)
                lastfinish = ts
    return sectors

from lotusops.speedtest.sectorstatus import strfdelta

def analyzeReports(reports,stages=["duration","interval"]):
    print("*******************************************")
    for stage in stages:
        mean_=datetime.timedelta(0)
        max_=datetime.timedelta(0)
        min_=datetime.timedelta(days=10)
        mean_=datetime.timedelta(0)
        ## initialize
        sum=datetime.timedelta(0)
        cnt=0
        for id in reports.keys():
            report=reports[id]
            if stage not in report.keys(): continue
            if report[stage] == datetime.timedelta(0): continue
            if report[stage] > max_: max_=report[stage]
            if report[stage] < min_: min_=report[stage]
            sum+= report[stage]
            cnt+=1
        if cnt == 0: break
        mean_=sum/cnt
        print("MIN({0}) ---{1}".format(stage,strfdelta(min_)))
        print("MAX({0}) ---{1}".format(stage,strfdelta(max_)))
        print("MEAN({0})---{1}".format(stage,strfdelta(mean_)))
        print("*******************************************")
               
def printReports(reports):
    for id in reports.keys():
        print("SectorId({0})-{1}-({2})-({3})".format(id,strfdelta(reports[id]["duration"]),reports[id]["start"].strftime("%Y-%m-%d %H:%M:%S"),reports[id]["finish"].strftime("%Y-%m-%d %H:%M:%S")))
    print("#################################")
    for id in reports.keys():
        print("SectorId({0})-{1}".format(id,reports[id]["interval"]))

def analyzeFile(filepath,filters,isdetailed=False):
    reports = makeReport(filepath,filters=["seal_commit_phase2","SectorId"])
    if isdetailed: printReports(reports)
    print("#################################")
    analyzeReports(reports)    

if __name__ == "__main__":
    analyzeFile(worker_log)
    
# 2021-07-24T22:19:31.744 INFO filcrypto::proofs::api > seal_commit_phase2: start
# 2021-07-24T22:19:31.858 INFO filecoin_proofs::api::seal > seal_commit_phase2:start: SectorId(4)
# 2021-07-24T22:19:31.859 INFO filecoin_proofs::caches > trying parameters memory cache for: STACKED[34359738368]
# 2021-07-24T22:19:31.859 INFO filecoin_proofs::caches > found params in memory cache for STACKED[34359738368]
# 2021-07-24T22:19:31.859 INFO filecoin_proofs::api::seal > got groth params (34359738368) while sealing
# 2021-07-24T22:19:31.859 INFO filecoin_proofs::api::seal > snark_proof:start
####################### 3min{ bellperson::groth16
# 2021-07-24T22:19:31.879 INFO bellperson::groth16::prover > Bellperson 0.14.2 is being used!
# 2021-07-24T22:22:29.014 INFO bellperson::groth16::prover > starting proof timer
####################### } GPU is available for FFT!
# 2021-07-24T22:22:38.887 INFO bellperson::gpu::locks > GPU is available for FFT!
# 2021-07-24T22:22:38.887 DEBUG bellperson::gpu::locks > Acquiring GPU lock at "/filecoin/lotustmp/bellman.gpu.lock" ...
# 2021-07-24T22:22:38.887 DEBUG bellperson::gpu::locks > GPU lock acquired!
# 2021-07-24T22:22:39.042 INFO bellperson::gpu::fft > FFT: 1 working device(s) selected.
# 2021-07-24T22:22:39.042 INFO bellperson::gpu::fft > FFT: Device 0: GeForce RTX 2080 Ti
######################  5.5min{ GPU FFT kernel instantiated!
# 2021-07-24T22:22:39.042 INFO bellperson::domain > GPU FFT kernel instantiated!
# 2021-07-24T22:28:04.580 DEBUG bellperson::gpu::locks > GPU lock released!
###################### } GPU is available for Multiexp!
# 2021-07-24T22:28:14.442 INFO bellperson::gpu::locks > GPU is available for Multiexp!
# 2021-07-24T22:28:14.442 DEBUG bellperson::gpu::locks > Acquiring GPU lock at "/filecoin/lotustmp/bellman.gpu.lock" ...
# 2021-07-24T22:28:14.442 DEBUG bellperson::gpu::locks > GPU lock acquired!
# 2021-07-24T22:28:15.395 INFO bellperson::gpu::multiexp > Multiexp: 6 working device(s) selected. (CPU utilization: 0)
# 2021-07-24T22:28:15.395 INFO bellperson::gpu::multiexp > Multiexp: Device 0: GeForce RTX 2080 Ti (Chunk-size: 7488999)
# 2021-07-24T22:28:15.395 INFO bellperson::gpu::multiexp > Multiexp: Device 1: GeForce RTX 2080 Ti (Chunk-size: 7488999)
# 2021-07-24T22:28:15.395 INFO bellperson::gpu::multiexp > Multiexp: Device 2: GeForce RTX 2080 Ti (Chunk-size: 7488999)
# 2021-07-24T22:28:15.395 INFO bellperson::gpu::multiexp > Multiexp: Device 3: GeForce RTX 2080 Ti (Chunk-size: 7488999)
# 2021-07-24T22:28:15.395 INFO bellperson::gpu::multiexp > Multiexp: Device 4: GeForce RTX 2080 Ti (Chunk-size: 7488999)
# 2021-07-24T22:28:15.395 INFO bellperson::gpu::multiexp > Multiexp: Device 5: GeForce RTX 2080 Ti (Chunk-size: 7488999)
######################## 5.5min{  GPU Multiexp kernel instantiated!
# 2021-07-24T22:28:15.395 INFO bellperson::multiexp > GPU Multiexp kernel instantiated!
# 2021-07-24T22:36:41.818 WARN bellperson::gpu::locks > GPU acquired by a high priority process! Freeing up Multiexp kernels...
######################## }
# 2021-07-24T22:36:42.089 DEBUG bellperson::gpu::locks > GPU lock released!
# 2021-07-24T22:36:42.089 INFO bellperson::gpu::locks > GPU is available for Multiexp!
# 2021-07-24T22:36:42.089 DEBUG bellperson::gpu::locks > Acquiring GPU lock at "/filecoin/lotustmp/bellman.gpu.lock" ...
# 2021-07-24T22:36:42.089 DEBUG bellperson::gpu::locks > GPU lock acquired!
# 2021-07-24T22:36:42.835 INFO bellperson::gpu::multiexp > Multiexp: 6 working device(s) selected. (CPU utilization: 0)
# 2021-07-24T22:36:42.835 INFO bellperson::gpu::multiexp > Multiexp: Device 0: GeForce RTX 2080 Ti (Chunk-size: 7488999)
# 2021-07-24T22:36:42.835 INFO bellperson::gpu::multiexp > Multiexp: Device 1: GeForce RTX 2080 Ti (Chunk-size: 7488999)
# 2021-07-24T22:36:42.835 INFO bellperson::gpu::multiexp > Multiexp: Device 2: GeForce RTX 2080 Ti (Chunk-size: 7488999)
# 2021-07-24T22:36:42.835 INFO bellperson::gpu::multiexp > Multiexp: Device 3: GeForce RTX 2080 Ti (Chunk-size: 7488999)
# 2021-07-24T22:36:42.835 INFO bellperson::gpu::multiexp > Multiexp: Device 4: GeForce RTX 2080 Ti (Chunk-size: 7488999)
# 2021-07-24T22:36:42.835 INFO bellperson::gpu::multiexp > Multiexp: Device 5: GeForce RTX 2080 Ti (Chunk-size: 7488999)
######################## 6.5min{ GPU Multiexp kernel instantiated!
# 2021-07-24T22:36:42.835 INFO bellperson::multiexp > GPU Multiexp kernel instantiated!
# 2021-07-24T22:43:07.124 DEBUG bellperson::gpu::locks > GPU lock released!
######################## }
# 2021-07-24T22:43:07.147 INFO bellperson::groth16::prover > prover time: 1238.133344429s
# 2021-07-24T22:43:09.454 INFO filecoin_proofs::api::seal > snark_proof:finish
# 2021-07-24T22:43:09.455 INFO filecoin_proofs::api::seal > verify_seal:start: SectorId(4)
# 2021-07-24T22:43:09.455 INFO filecoin_proofs::caches > trying parameters memory cache for: STACKED[34359738368]-verifying-key
# 2021-07-24T22:43:09.455 INFO filecoin_proofs::caches > found params in memory cache for STACKED[34359738368]-verifying-key
# 2021-07-24T22:43:09.455 INFO filecoin_proofs::api::seal > got verifying key (34359738368) while verifying seal
# 2021-07-24T22:43:09.471 INFO filecoin_proofs::api::seal > verify_seal:finish: SectorId(4)
# 2021-07-24T22:43:09.471 INFO filecoin_proofs::api::seal > seal_commit_phase2:finish: SectorId(4)
# 2021-07-24T22:43:09.471 INFO filcrypto::proofs::api > seal_commit_phase2: finish

