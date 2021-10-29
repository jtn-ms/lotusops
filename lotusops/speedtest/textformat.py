
def analyzeFile(filepath,filters):
    with open(filepath,"r") as f:
        lines=f.readlines()
        for line in lines:
            if any(filter not in line for filter in filters): continue
            # structed=line.strip("\t")
            print(line.rstrip("\n"))
