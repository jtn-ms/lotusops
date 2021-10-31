import os
import sys

msg_help = "\n\
            \n======== lotusops =========\
            \n\
            \nDescription: \
            \n            A lotus-miner assistant tool for managing sectors & jobs,mainly processing job-abortion, sector-removal, and autopledge.\
            \n            It's a capsulation tool based on lotus-miner & shell scripts. Make sure lotus-miner is already installed.\
            \nUsage: \
            \n       [job-abortion] - to abort all sealing jobs with a certain keyword,\
            \n       lotusops abort <keyword>\
            \n       [sector-removal] - to remove all sectors with a certain keyword. \
            \n       lotusops remall <keyword>\
            \n       [autopledge] - to repeat pledge in a specific interval. \
            \n       lotusops autopledge <time-interval> <worker.ip.lst>\
            \nExamples: \
            \n       [job-abortion]\
            \n       lotusops abort AP \
            \n       [sector-removal] \
            \n       lotusops rmall AP \
            \n       [autopledge]\
            \n       lotusops autopledge 1m 172.26.48.134|172.26.48.135"

def lotusops():
    if len(sys.argv) < 3 or any(argv.startswith("-h") for argv in sys.argv): return msg_help
    if sys.argv[1] == "abort":
        execute(actioncode="abort",scripts="lotus-miner sealing jobs",filters=sys.argv[2].split("|"),excluded=len(sys.argv)>3)
    elif sys.argv[1] == "rmall":
        execute(actioncode="rmall",scripts="lotus-miner sectors list",filters=sys.argv[2].split("|"),excluded=len(sys.argv)>3)
    elif sys.argv[1] == "autopledge":
        autopledge(sys.argv[2],sys.argv[3])
    else: return msg_help

import subprocess
import string

def execute(actioncode="abort",scripts="lotus-miner sealing jobs",filters=["AP"],excluded=False):

    ids=[]
    try:
        if excluded:
            candidates=[line.split(' ')[0] \
                        if not any(filter in line for filter in filters) and \
                            all(c in string.hexdigits for c in line.split(' ')[0]) else '' \
                        for line in subprocess.check_output(scripts.split(" ")).split('\n')][1:]
        else:
            candidates=[line.split(' ')[0] \
                        if all(filter in line for filter in filters)  and \
                           all(c in string.hexdigits for c in line.split(' ')[0]) else '' \
                        for line in subprocess.check_output(scripts.split(" ")).split('\n')][1:]
        candidates=list(filter(None,candidates))
    except: return
    action = "lotus-miner sealing abort" if actioncode == "abort" else "lotus-miner sectors remove --really-do-it"
    for id in candidates:
        slices=action.split(" ")
        slices.append(id)
        output = subprocess.check_output(slices)
        print(output.strip("\n"))

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
        return 60

def autopledge(interval,iplst):
    # load ips
    ips=load_ips(iplst)
    if len(ips) < 1: return msg_workers_needed

    # map(ip,ansible_name)
    ansible_names=getAnsibleNames(ips)
    if len(ansible_names) < 1: return msg_ansible_needs_workers

    ip_process_env_tree={}
    # inquiry
    # {'172.26.48.134':[
    #                   {'11111':
    #                            {LOTUS_WORKER_PATH:/filecoin1/lotusworker5}},
    #                   {'22222':
    #                            {LOTUS_WORKER_PATH:/filecoin1/lotusworker1}
    #                   }
    #                   ]
    # }
    action="ansible workername -m shell -a"
    for ip in ips:
        action = action.replace('workername',ansible_names[ip])
        ip_process_env_tree[ip]=[]
        processes = list(filter(None,[line.split()[1] if 'lotus-worker' in line else '' for line in runscript(action+" 'ps -ef|grep lotus'")]))
        for process in processes:
            # (process,LOTUS_WORKER_PATH)
            envs=list(filter(None,[line\
                 if any(filter in line for filter in ['FIL','LOTUS','CPU','CUDA','TMP','MINER']) else '' \
                 for line in runscript(action+"strings /proc/%s/environ")]))
            envdict={}
            for env in envs:
                k,v=env.split("=")
                envdict[k]=v
            ip_process_env_tree[ip].append({process:envdict})
        
    if len(sys.argv)>4: import json; return json.dumps(ip_process_env_tree, indent=4, sort_keys=True)
    
    sleeptime = interpret(interval)
    while 1:
        pledgeable, ip_process_env_tree = chkavailable(ip_process_env_tree)
        import time
        time.sleep(sleeptime)


def runscript(script):
    if sys.version_info[0]<3:
        import commands
        output = commands.getstatusoutput(script)
    else:
        import subprocess
        output = subprocess.getoutput(script)
    return output.split("\n")

def getAnsibleNames(ips):
    ansible_names={}
    with open('/etc/ansible/hosts','r') as f:
        for line in f.readlines():
            for ip in ips:
                if ip in line: ansible_names[ip]=line.rstrip("\n").split(" ")[0]
    return ansible_names

def chkavailable(ip_process_env_tree):
    storage_per_sector=(32+32+453)
    storage_per_sector_as_kb=storage_per_sector*2**20#KByte
    ansible_names = getAnsibleNames(ip_process_env_tree.keys())
    # current total storage demand
    script='lotus-miner sealing jobs|egrep "AP|PC1|PC2"'
    sectors_cnt = len(runscript(script))
    consumped = sectors_cnt * storage_per_sector
    # calc available storage
    used, useable, total = 0,0,0
    cached_sectors_cnt=0
    for ip,process_env in ip_process_env_tree.items():
        disks=[]
        action = "ansible workername -m shell -a".replace('workername',ansible_names[ip])
        ip_sector_cnt,ip_used_storage,ip_total_storage=0,0,0
        for process,env in process_env.items():
            lotus_worker_path=env['LOTUS_WORKER_PATH']
            if not lotus_worker_path: continue
            storage_root_path=lotus_worker_path.split("/")[1]
            if storage_root_path not in disks: disks.append(storage_root_path)
            # ansible workername -m shell -a 'du $LOTUS_WORKER_PATH/cache -hd1'
            proc_sectors_cnt=len(list(filter(None,[line \
                            if "cache" in line else '' \
                            for line in runscript("%s 'du %s/cache -hd1'".format(action,lotus_worker_path))]))) - 1
            ip_process_env_tree[ip][process]['CACHED_SECTOR_CNT'] = proc_sectors_cnt
            ip_sector_cnt+=proc_sectors_cnt
            # ansible workername -m shell -a 'du $LOTUS_WORKER_PATH -d1'
            proc_used_storage=runscript("%s 'du %s -hd1'".format(action,lotus_worker_path))[-1].split()[0]
            ip_process_env_tree[ip][process]['LOTUS_USED_STORAGE'] = proc_used_storage/2**20
            ip_used_storage+=ip_process_env_tree[ip][process]['LOTUS_USED_STORAGE']
        # ansible workername -m shell -a 'df'
        df_out=list(filter(None,[line
                                 if any(disk in line for disk in disks) else '' \
                                 for line in runscript(action+" 'df'")]))
        ip_total_storage = sum([int(line.split()[1]) for line in df_out])/2**20
        ip_total_used_storage = sum([int(line.split()[2]) for line in df_out])/2**20
        ip_process_env_tree[ip]['TOTAL'] = ip_total_storage
        ip_process_env_tree[ip]['LOTUS_USED'] = ip_used_storage
        ip_process_env_tree[ip]['NON_LOTUS_USED'] = ip_total_used_storage-ip_used_storage
        ip_process_env_tree[ip]['LOTUS_USEABLE'] = ip_total_storage-ip_process_env_tree[ip]['NON_LOTUS_USED']
        ip_process_env_tree[ip]['LOTUS_CACHED'] = ip_sector_cnt*storage_per_sector
        cached_sectors_cnt+=ip_sector_cnt
        useable+=ip_process_env_tree[ip]['LOTUS_USEABLE']
    max_sectors_cnt=max(sectors_cnt,cached_sectors_cnt)
    if useable > (max_sectors_cnt+1)*storage_per_sector: return True,ip_process_env_tree
    return False,ip_process_env_tree





