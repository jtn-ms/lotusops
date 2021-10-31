entry_points = [
                # log analytics      
                "lotusspeed = lotusops.cli.speedtest:loganalytics",
                # lotusops - rmall, abort, autopledge
                "lotusops = lotusops.cli.lotusops:lotusops",
]

commands = [cmd.strip().replace(" ",'').split('=')[0] for cmd in entry_points]