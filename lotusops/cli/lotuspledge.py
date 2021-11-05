import os
import sys

msg_help = "\n\
            \n======== lotuspledge =========\
            \n\
            \nDescription: \
            \n            A lotus auto-pleding assitant tool for implementing auto-pledge more smartly with inspecting workers.\
            \n            It repeats to pledge a sector in a specific interval as long as any worker is affordable for the task. \
            \n            It's a capsulation tool based on lotus-miner & shell scripts. Make sure lotus-miner is already installed.\
            \nUsage: \
            \n       lotuspledge <time-interval> <worker.ip.lst>\
            \nExamples: \
            \n       lotuspledge 1m '172.26.48.134|172.26.48.135'\
            \n       lotuspledge 90 /root/workers.lst\
            \n       lotuspledge inspect '172.26.48.134|172.26.48.135'"


def lotuspledge():
    if  len(sys.argv) < 3 or \
        any(arg.startswith("-h") for arg in sys.argv) or \
        not load_ips(sys.argv[2]): 
            return msg_help
    autopledge(sys.argv[1],sys.argv[2])

import subprocess
import string

msg_workers_needed="The list of precommit workers connected to the miner should be indicated using file or string."
msg_ansible_needed="this action needs anible installed."
msg_ansible_needs_workers="ansible needs workers' ip. It must be added in /etc/ansible/hosts"

def load_ips(iplst):
    ips=[]
    if os.path.isfile(iplst):
        with open(iplst,'r') as f:
            for line in f.readlines():
                ips.append(line.rstrip("\n"))
    else:
        ips=iplst.split("|")
    return ips

def interpret(arg):
    m2s=60
    h2s=m2s*60
    d2s=24*h2s
    try:
        output = {
            'm':m2s*int(arg[:-1]),
            'h':h2s*int(arg[:-1]),
            'd':d2s*int(arg[:-1]),
            's':d2s*int(arg),
        }.get([arg[-1]],int(arg))
    except:
        output = 60
    if output < 60: output=60
    return output

ansible_hosts_path='/etc/ansible/hosts'

def getAnsibleNames(ips):
    ansible_names={}
    with open(ansible_hosts_path,'r') as f:
        for line in f.readlines():
            for ip in ips:
                if ip in line: ansible_names[ip]=line.rstrip("\n").split()[0]
    return ansible_names

def runscript(script,isansible=True):
    
    if sys.version_info[0]<3:
        import commands
        result = commands.getstatusoutput(script).split("\n")
    else:
        import subprocess
        result = subprocess.getoutput(script).split("\n")
    if not isansible: return result
    # just handling one node
    # multiple node mode not implemented yet
    # 'test1 | SUCCESS | rc=0 >>'
    # 'test2 | CHANGED | rc=0 >>'
    non_ansible_start_index=1
    for idx,line in enumerate(result):
        splited=line.split()
        if splited[0] == script.split()[1] and \
            all('|'== splited[i] for i in [1,3]) and\
            splited[4] == "rc=0":
            non_ansible_start_index=idx+1;break
    #
    return  result[non_ansible_start_index:]

PLEDGEING_INTEVERAL=150#s

def autopledge(interval,iplst):
    # load ips
    ips=load_ips(iplst)
    if len(ips) < 1: return msg_workers_needed
    # map(ip,ansible_name)
    ansible_names=getAnsibleNames(ips)
    if len(ansible_names) < 1: return msg_ansible_needs_workers
    ip_process_env_tree={}
    # inquiry
    # {'172.26.48.134':{
    #                   '11111': {LOTUS_WORKER_PATH:/filecoin1/lotusworker5}},
    #                   22222': {LOTUS_WORKER_PATH:/filecoin1/lotusworker1}
    #                   }
    # }
    for ip in ips:
        ip_process_env_tree[ip]={}
        script="ansible workername -m shell -a 'ps -ef|grep lotus'".replace('workername',ansible_names[ip])
        procs = list(filter(None,[line \
                                for line in runscript(script) \
                                if 'lotus-worker' in line]))
        for proc in procs:
            envdict={}
            pid=proc.split()[1]
            # tasks for process
            envdict["TYPE"] = "COMMIT" if "--precommit1=false" in proc else "PRECOMMIT"
            # (process,LOTUS_WORKER_PATH)
            script="ansible {0} -m shell -a 'strings /proc/{1}/environ'".format(ansible_names[ip],pid)
            envs=list(filter(None,[line\
                                 for line in runscript(script) \
                                 if any(filter in line for filter in ['FIL','LOTUS','CPU','CUDA','TMP'])]))
            # environment variables added to tree
            for env in envs:
                k,v=env.split("=")
                envdict[k]=v
            ip_process_env_tree[ip][pid]=envdict
        
    INSPECT_INTERVAL = interpret(interval)
    while 1:
        pledgeable_cnt = chkavailable(ip_process_env_tree)
        if any("inspect" in arg for arg in sys.argv): break
        import time
        while pledgeable_cnt>=0: 
            runscript("lotus-miner sectors pledge",isansible=False)
            pledgeable_cnt-=1
            time.sleep(PLEDGEING_INTEVERAL)
        time.sleep(INSPECT_INTERVAL)

PLEDGE_MARGIN = 1

def chkavailable(ip_process_env_tree):
    storage_per_sector_precommit,storage_per_sector_commit=(32+32+453),(32+32)
    cpus_per_sector = 3
    mem_per_sector = 64
    storage_per_sector_as_kb_for_precommit=storage_per_sector_precommit*2**20#KByte
    ansible_names = getAnsibleNames(ip_process_env_tree.keys())
    # inspect miner
    script='lotus-miner sealing jobs|egrep "AP|PC1|PC2|C1|C2|GET"'
    jobs=list(filter(None,runscript(script,isansible=False)))
    jstats=set([job.split()[4] for job in jobs if not job.split()[4].isdigit()])
    jstats_precommit="AP|PC1|PC2".split("|")
    sectors_cnt_assigned = len([job for job in jobs if any(stat in job.split()[1] for stat in jstats_precommit)])
    workers = {}
    for job in jobs:
        if job.split()[2] not in workers.keys():
            workers[job.split()[2]] = [job.split()[1]]
        else: workers[job.split()[2]].append(job.split()[1])
    script='lotus-miner sectors list|egrep "Packing|PreCommit1|PreCommit2|WaitSeed|CommitWait|Committing|FinalizeSector|Removing|RecoveryTimeout"'
    sectors=runscript(script,isansible=False)
    sstats=set([sector.split()[1] for sector in sectors if not sector.split()[1].isdigit()])
    sstats_precommit="Packing|PreCommit1|PreCommit2".split("|")
    sectors_cnt_queue = len([sector for sector in sectors if any(stat in sector.split()[1] for stat in sstats_precommit)])
    sectors_cnt=max(sectors_cnt_queue,sectors_cnt_assigned)
    print("#######################################################")
    print("MINER REPORT:")
    print("              Queue(%s)"%",".join(["{0}:{1}".format(stat,len([sector for sector in sectors if stat in sector ])) for stat in sstats]))
    print("           Assigned(%s)"%",".join(["{0}:{1}".format(stat,len([job for job in jobs if stat in job ])) for stat in jstats]))

    # inspect workers
    print("#######################################################")
    print("WORKER REPORT: ")
    cached_sectors_cnt=0
    for ip,procs in ip_process_env_tree.items():
        
        action = "ansible %s -m shell -a"%ansible_names[ip]
        
        ip_used_mem,ip_total_mem=0,0
        ip_used_cpus,ip_total_cpus=0,0
        ip_sector_cnt,ip_used_storage,ip_total_storage=0,0,0
        # MEM
        output=runscript("ansible workername -m shell -a 'free'".\
                        replace('workername',ansible_names[ip]))[1].split()
        ip_total_mem = int(float(output[1])/2**20)
        ip_total_used_mem = int(float(output[2])/2**20)
        # CPU
        output=runscript("ansible workername -m shell -a 'nproc --all'".\
                        replace('workername',ansible_names[ip]))[0]
        ip_total_cpus=int(output)
        # USED
        output=runscript("ansible workername -m shell -a 'ps -eo pid,%mem,%cpu,comm --sort=-%cpu'".replace('workername',ansible_names[ip]))[1:]
        ip_proc_usage={line.split()[0]:{"mem":line.split()[1],"cpu":line.split()[2],"pname":line.split()[3]} for line in output}
        ip_total_used_cpus=int(sum(float(value["cpu"]) for value in ip_proc_usage.values())/100)
        ip_total_used_mem=int(max(sum(float(value["mem"]) for value in ip_proc_usage.values())/100*ip_total_mem,ip_used_mem))
        # STORAGE FOR PreCommit
        lotus_disks=[]
        ip_process_env_tree[ip]['STORAGE'] = {
                                                'PATH':{}, \
                                                'PLEDGE_USEABLE(CNT)':0 \
                                            }
        for pid,env in procs.items():
            if any(c not in string.digits for c in pid) or\
               not isinstance(env,dict): continue
            if not env['LOTUS_WORKER_PATH']: continue

            storage_root_path=env['LOTUS_WORKER_PATH'].split("/")[1]
            if storage_root_path not in lotus_disks: 
                lotus_disks.append(storage_root_path)
            # STORAGE, $LOTUS_WORKER_PATH/cache
            # ansible workername -m shell -a 'du $LOTUS_WORKER_PATH/cache -hd1'
            script="%s 'du %s/cache -d1'"%(action,env['LOTUS_WORKER_PATH'])
            sids=list(filter(None,[int(line.split("-")[-1]) \
                            for line in runscript(script) if all(mark in line for mark in ["s-t","cache"])]))
            sids.sort()
            
            ip_process_env_tree[ip][pid]['WORKER'] = {}
            ip_process_env_tree[ip][pid]['WORKER']['CACHED'] = ip_process_env_tree[ip][pid]['WORKER']['RUNNING'] = sids
            ip_process_env_tree[ip][pid]['WORKER']['ID'] = "000000"
            for wid,_sids in workers.items():
                __sids=[int(sid) for sid in _sids];__sids.sort()
                if any(sid in sids for sid in __sids):
                    ip_process_env_tree[ip][pid]['WORKER']['ID'] = wid
                    ip_process_env_tree[ip][pid]['WORKER']['RUNNING'] = __sids
                    break

            ip_process_env_tree[ip][pid]['WORKER']['MISMATCH'] = set(ip_process_env_tree[ip][pid]['WORKER']['CACHED'])^\
                                                                 set(ip_process_env_tree[ip][pid]['WORKER']['RUNNING'])
            
            ip_process_env_tree[ip][pid]['WORKER']['CACHED']=",".join([str(sid) for sid in ip_process_env_tree[ip][pid]['WORKER']['CACHED']])
            ip_process_env_tree[ip][pid]['WORKER']['RUNNING']=",".join([str(sid) for sid in ip_process_env_tree[ip][pid]['WORKER']['RUNNING']])
            ip_process_env_tree[ip][pid]['WORKER']['MISMATCH']=",".join([str(sid) for sid in ip_process_env_tree[ip][pid]['WORKER']['MISMATCH']])
            ip_process_env_tree[ip][pid]['CACHED_SECTOR_CNT'] = len(sids)
            # STORAGE, $LOTUS_WORKER_PATH
            # ansible workername -m shell -a 'du $LOTUS_WORKER_PATH -d1'
            script="%s 'du %s -d1'"%(action,env['LOTUS_WORKER_PATH'])
            proc_used_storage=int(runscript(script)[-1].split()[0])
            ip_process_env_tree[ip][pid]['STORAGE'] = int(proc_used_storage/2**20)
            # CPU, MEM
            proc_mem_usage=int(float(ip_proc_usage[pid]["mem"])/100*ip_total_mem)
            proc_cpu_usage=int(float(ip_proc_usage[pid]["cpu"])/100)
            ip_process_env_tree[ip][pid]['MEM']=proc_mem_usage
            ip_process_env_tree[ip][pid]['CPU']=proc_cpu_usage
            # summing up
            ip_used_mem += ip_process_env_tree[ip][pid]['MEM']
            ip_used_cpus += ip_process_env_tree[ip][pid]['CPU']
            ip_sector_cnt += ip_process_env_tree[ip][pid]['CACHED_SECTOR_CNT']
            ip_used_storage += ip_process_env_tree[ip][pid]['STORAGE']
            
            # excluding c2 for storage

            if storage_root_path not in ip_process_env_tree[ip]['STORAGE']['PATH'].keys():
                ip_process_env_tree[ip]['STORAGE']['PATH'][storage_root_path] = {}
                ip_process_env_tree[ip]['STORAGE']['PATH'][storage_root_path]["TYPE"] = []
                ip_process_env_tree[ip]['STORAGE']['PATH'][storage_root_path]['PRECOMMIT'] = {}
                ip_process_env_tree[ip]['STORAGE']['PATH'][storage_root_path]['PRECOMMIT']['USED'] = 0
                ip_process_env_tree[ip]['STORAGE']['PATH'][storage_root_path]['PRECOMMIT']['CACHED_SECTOR_CNT'] = 0
                ip_process_env_tree[ip]['STORAGE']['PATH'][storage_root_path]['COMMIT'] = {}
                ip_process_env_tree[ip]['STORAGE']['PATH'][storage_root_path]['COMMIT']['USED'] = 0
                ip_process_env_tree[ip]['STORAGE']['PATH'][storage_root_path]['COMMIT']['CACHED_SECTOR_CNT'] = 0

            ip_process_env_tree[ip]['STORAGE']['PATH'][storage_root_path][env["TYPE"]]['USED'] +=  ip_process_env_tree[ip][pid]['STORAGE']
            ip_process_env_tree[ip]['STORAGE']['PATH'][storage_root_path][env["TYPE"]]['CACHED_SECTOR_CNT'] += ip_process_env_tree[ip][pid]['CACHED_SECTOR_CNT']


            ip_process_env_tree[ip]['STORAGE']['PATH'][storage_root_path]["TYPE"].append(env["TYPE"])

        # ansible workername -m shell -a 'df'
        df_out=list(filter(None,[line
                                 for line in runscript(action+" 'df'") \
                                 if any(disk in line for disk in lotus_disks)]))

        for disk in lotus_disks:
            ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['SIZE'] = int([int(line.split()[1]) for line in df_out if disk in line][0]/2**20)
            ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['USED'] = int([int(line.split()[2]) for line in df_out if disk in line][0]/2**20)
            # cached
            ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['PRECOMMIT']['CACHED'] = \
                    ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['PRECOMMIT']['CACHED_SECTOR_CNT'] * storage_per_sector_precommit
            ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['COMMIT']['CACHED'] = \
                    ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['COMMIT']['CACHED_SECTOR_CNT'] * storage_per_sector_commit
            ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['CACHED'] = \
                ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['PRECOMMIT']['CACHED'] +\
                ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['COMMIT']['CACHED']
            # non_lotus usage
            ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['NON_LOTUS_USED'] = \
                    ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['USED']-\
                    ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['PRECOMMIT']['USED']-\
                    ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['COMMIT']['USED']
            ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['NON_LOTUS_USED']=max(0,ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['NON_LOTUS_USED'])
            # lotus usable
            ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['LOTUS_USEABLE'] = \
                    ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['SIZE'] -\
                    ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['NON_LOTUS_USED']
            ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['LOTUS_USEABLE'] = max(0,ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['LOTUS_USEABLE'])
            # pledgeable
            ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['PLEDGE_USEABLE'] = \
                ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['LOTUS_USEABLE'] -\
                max(ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['COMMIT']['CACHED'],\
                    ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['COMMIT']['USED'])\
                if  any(job == "PRECOMMIT" for job in ip_process_env_tree[ip]['STORAGE']['PATH'][disk]["TYPE"]) \
                else 0
            ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['PLEDGE_USEABLE']=max(0,ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['PLEDGE_USEABLE']-PLEDGE_MARGIN)
            ip_process_env_tree[ip]['STORAGE']['PLEDGE_USEABLE(CNT)'] += int(ip_process_env_tree[ip]['STORAGE']['PATH'][disk]['PLEDGE_USEABLE']/storage_per_sector_precommit)
        ip_process_env_tree[ip]['CPU'] = {}
        ip_process_env_tree[ip]['CPU']['TOTAL'] = ip_total_cpus
        ip_process_env_tree[ip]['CPU']['LOTUS_USED'] = ip_used_cpus
        ip_process_env_tree[ip]['CPU']['NON_LOTUS_USED'] = ip_total_used_cpus-ip_used_cpus
        ip_process_env_tree[ip]['CPU']['LOTUS_USEABLE(CNT)'] = int(max(ip_total_cpus-ip_process_env_tree[ip]['CPU']['NON_LOTUS_USED'],0)/cpus_per_sector)
        ip_process_env_tree[ip]['MEM'] = {}
        ip_process_env_tree[ip]['MEM']['TOTAL'] = ip_total_mem
        ip_process_env_tree[ip]['MEM']['LOTUS_USED'] = ip_used_mem
        ip_process_env_tree[ip]['MEM']['NON_LOTUS_USED'] = ip_total_used_mem-ip_used_mem
        ip_process_env_tree[ip]['MEM']['LOTUS_USEABLE(CNT)'] = int(max(ip_total_mem-ip_process_env_tree[ip]['MEM']['NON_LOTUS_USED'],0)/mem_per_sector)
        # affordability check
        cached_sectors_cnt+=min(ip_process_env_tree[ip]['STORAGE']['PLEDGE_USEABLE(CNT)'],\
                                ip_process_env_tree[ip]['CPU']['LOTUS_USEABLE(CNT)'],\
                                ip_process_env_tree[ip]['MEM']['LOTUS_USEABLE(CNT)'])

    import json; print(json.dumps(ip_process_env_tree, indent=4, sort_keys=True))
    return cached_sectors_cnt-sectors_cnt
