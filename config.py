entry_points = [
                # log analytics      
                "lotusspeed = lotusops.cli.speedtest:lotusspeed",
                # lotusops - rmall, abort,
                "lotusops = lotusops.cli.lotusops:lotusops",
                #  autopledge
                "lotuspledge = lotusops.cli.lotuspledge:lotuspledge",
                #  show configuration & commands
                "lotusopsabout = lotusops.cli.lotusopsabout:lotusopsabout",                
]

commands = [cmd.strip().replace(" ",'').split('=')[0] for cmd in entry_points]