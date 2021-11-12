import toml

lotusops_setting_filepath = "/etc/lotusops/config/setting.toml"

def showSettings():
    print("The configuration file is located in %s.\nThe modification of it's content will affect this tool's operations.\n"%lotusops_setting_filepath)
    with open(lotusops_setting_filepath,"r") as f:
        config = toml.loads(f.read())
        config_string = toml.dumps(config)
        print(config_string)

def loadSetting():
    config={}
    with open(lotusops_setting_filepath,"r") as f:
        config = toml.loads(f.read())
    return config

def saveSettings(new_config):
    config_string = toml.dumps(new_config)
    with open(lotusops_setting_filepath,"w") as f:
        f.write(config_string)

def changeSetting(k,sk,v):
    with open(lotusops_setting_filepath,"rw") as f:
        config = toml.loads(f.read())
        if k not in config.keys(): config[k] = {}
        config[k][sk] = v
        f.write(config)