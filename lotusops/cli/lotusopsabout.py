import os
import sys

msg_help = "\n\
            \n======== lotusopsabout =========\
            \n\
            \nDescription: \
            \n             Show avaiable commands & setting for lotus.\
            \nUsage: \
            \n       lotusopsabout settings\
            \n       lotusopsabout commands"

from lotusops.config.setting import showSettings

def lotusopsabout():
        if len(sys.argv) == 1 or any(any(arg.startswith(mark) for mark in ["-h","--h","help"]) for arg in sys.argv): return msg_help
        if sys.argv[1] == "settings": showSettings();return
        if sys.argv[1] == "commands": print("\n".join(["lotusops","lotusspeed","lotuspledge","lotusabout"]));return
        return msg_help

