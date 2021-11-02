entry_points = [
                # log analytics      
                "lotusspeed = lotusops.cli.speedtest:lotusspeed",
                # lotusops - rmall, abort,
                "lotusops = lotusops.cli.lotusops:lotusops",
                #  autopledge
                "lotuspledge = lotusops.cli.lotuspledge:lotuspledge",
]

commands = [cmd.strip().replace(" ",'').split('=')[0] for cmd in entry_points]