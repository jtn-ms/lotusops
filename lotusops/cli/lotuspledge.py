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
            \n       [autopledge] - \
            \n       lotuspledge <time-interval> <worker.ip.lst>\
            \nExamples: \
            \n       lotuspledge 1m 172.26.48.134|172.26.48.135"

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
    action="ansible workername -m shell -a"
    for ip in ips:
        action = action.replace('workername',ansible_names[ip])
        ip_process_env_tree[ip]={}
        script=action+" 'ps -ef|grep lotus'"
        processes = list(filter(None,[line.split()[1] \
                                      if 'lotus-worker' in line else '' 
                                      for line in runscript(script)]))
        for process in processes:
            # (process,LOTUS_WORKER_PATH)
            script=action+" 'strings /proc/%s/environ'"%process
            envs=list(filter(None,[line\
                 if any(filter in line for filter in ['FIL','LOTUS','CPU','CUDA','TMP','MINER']) else '' \
                 for line in runscript(script)]))

            envdict={}
            for env in envs:
                k,v=env.split("=")
                envdict[k]=v
            ip_process_env_tree[ip][process]=envdict
        
    sleeptime = interpret(interval)
    while 1:
        pledgeable = chkavailable(ip_process_env_tree)
        if pledgeable: print(runscript("lotus-miner sectors pledge",isansible=False)[0])
        import time
        time.sleep(sleeptime)



def chkavailable(ip_process_env_tree):
    storage_per_sector=(32+32+453)
    cpus_per_sector = 3
    mem_per_sector = 64
    storage_per_sector_as_kb=storage_per_sector*2**20#KByte
    ansible_names = getAnsibleNames(ip_process_env_tree.keys())
    # current total storage demand
    script='lotus-miner sealing jobs|egrep "AP|PC1|PC2"'
    sectors_cnt = len(runscript(script,isansible=False))
    # consumped = sectors_cnt * storage_per_sector
    # calc available storage
    useable_cpu, useable_mem, useable_storage = 0,0,0
    cached_sectors_cnt=0
    for ip,procs in ip_process_env_tree.items():
        disks=[]
        action = "ansible %s -m shell -a"%ansible_names[ip]
        ip_sector_cnt,ip_used_storage,ip_total_storage=0,0,0
        ip_used_mem,ip_total_mem=0,0
        ip_used_cpus,ip_total_cpus=0,0
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

        for process,env in procs.items():
            if any(c not in string.digits for c in process) or\
               not isinstance(env,dict): continue
            lotus_worker_path=env['LOTUS_WORKER_PATH']
            if not lotus_worker_path: continue
            storage_root_path=lotus_worker_path.split("/")[1]
            if storage_root_path not in disks: disks.append(storage_root_path)
            # STORAGE, $LOTUS_WORKER_PATH/cache
            # ansible workername -m shell -a 'du $LOTUS_WORKER_PATH/cache -hd1'
            script="%s 'du %s/cache -d1'"%(action,lotus_worker_path)
            proc_sectors_cnt=max(len(list(filter(None,[line \
                            if "cache" in line else '' \
                            for line in runscript(script)]))) - 1,0)
            ip_process_env_tree[ip][process]['CACHED_SECTOR_CNT'] = proc_sectors_cnt
            ip_sector_cnt+=proc_sectors_cnt
            # STORAGE, $LOTUS_WORKER_PATH
            # ansible workername -m shell -a 'du $LOTUS_WORKER_PATH -d1'
            script="%s 'du %s -d1'"%(action,lotus_worker_path)
            proc_used_storage=int(runscript(script)[-1].split()[0])
            ip_process_env_tree[ip][process]['STORAGE'] = int(proc_used_storage/2**20)
            ip_used_storage+=ip_process_env_tree[ip][process]['STORAGE']
            # CPU, MEM
            proc_mem_usage=int(float(ip_proc_usage[process]["mem"])/100*ip_total_mem)
            proc_cpu_usage=int(float(ip_proc_usage[process]["cpu"])/100)
            ip_process_env_tree[ip][process]['MEM']=proc_mem_usage
            ip_process_env_tree[ip][process]['CPU']=proc_cpu_usage
            ip_used_cpus+=ip_process_env_tree[ip][process]['CPU']
            ip_used_mem+=ip_process_env_tree[ip][process]['MEM']
            
        # ansible workername -m shell -a 'df'
        df_out=list(filter(None,[line
                                 if any(disk in line for disk in disks) else '' \
                                 for line in runscript(action+" 'df'")]))
        ip_total_storage = int(sum([int(line.split()[1]) for line in df_out])/2**20)
        ip_total_used_storage = int(sum([int(line.split()[2]) for line in df_out])/2**20)
        ip_process_env_tree[ip]['STORAGE'] = {}
        ip_process_env_tree[ip]['STORAGE']['TOTAL'] = ip_total_storage
        ip_process_env_tree[ip]['STORAGE']['LOTUS_USED'] = ip_used_storage
        ip_process_env_tree[ip]['STORAGE']['NON_LOTUS_USED'] = ip_total_used_storage-ip_used_storage
        ip_process_env_tree[ip]['STORAGE']['LOTUS_USEABLE'] = ip_total_storage-ip_process_env_tree[ip]['STORAGE']['NON_LOTUS_USED']
        ip_process_env_tree[ip]['STORAGE']['LOTUS_CACHED'] = ip_sector_cnt*storage_per_sector
        ip_process_env_tree[ip]['CPU'] = {}
        ip_process_env_tree[ip]['CPU']['TOTAL'] = ip_total_cpus
        ip_process_env_tree[ip]['CPU']['LOTUS_USED'] = ip_used_cpus
        ip_process_env_tree[ip]['CPU']['NON_LOTUS_USED'] = ip_total_used_cpus-ip_used_cpus
        ip_process_env_tree[ip]['CPU']['LOTUS_USEABLE'] = ip_total_cpus-ip_process_env_tree[ip]['CPU']['NON_LOTUS_USED']
        ip_process_env_tree[ip]['CPU']['LOTUS_CACHED'] = ip_sector_cnt*cpus_per_sector
        ip_process_env_tree[ip]['MEM'] = {}
        ip_process_env_tree[ip]['MEM']['TOTAL'] = ip_total_mem
        ip_process_env_tree[ip]['MEM']['LOTUS_USED'] = ip_used_mem
        ip_process_env_tree[ip]['MEM']['NON_LOTUS_USED'] = ip_total_used_mem-ip_used_mem
        ip_process_env_tree[ip]['MEM']['LOTUS_USEABLE'] = ip_total_mem-ip_process_env_tree[ip]['MEM']['NON_LOTUS_USED']
        ip_process_env_tree[ip]['MEM']['LOTUS_CACHED'] = ip_sector_cnt*mem_per_sector
        cached_sectors_cnt+=ip_sector_cnt
        useable_storage+=ip_process_env_tree[ip]['STORAGE']['LOTUS_USEABLE']
        useable_cpu+=ip_process_env_tree[ip]['CPU']['LOTUS_USEABLE']
        useable_mem+=ip_process_env_tree[ip]['MEM']['LOTUS_USEABLE']
    max_sectors_cnt=max(sectors_cnt,cached_sectors_cnt)
    import json; print(json.dumps(ip_process_env_tree, indent=4, sort_keys=True))
    if useable_storage < (max_sectors_cnt+1)*storage_per_sector: return False
    if useable_cpu < (max_sectors_cnt+1)*cpus_per_sector: return False
    if useable_mem < (max_sectors_cnt+1)*mem_per_sector: return False
    return True
