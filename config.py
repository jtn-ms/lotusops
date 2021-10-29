entry_points = [
                # log analytics      
                "lotusspeed = lotusops.cli.speedtest:loganalytics",
]

commands = [cmd.strip().replace(" ",'').split('=')[0] for cmd in entry_points]