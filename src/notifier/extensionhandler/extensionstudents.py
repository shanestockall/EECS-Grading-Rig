import pandas as pd


##############################################
################## GLOBALS ###################
##############################################

global extensionCSV
global canvasCSV

##############################################

def load_config():
    with open('config.json') as cfg:
        config = json.load(cfg)
        for key in config.keys():
            if key in globals():
                globals()[key] = config[key]

def main():
    load_config()
    a = pd.read_csv(extensionCSV)
    b = pd.read_csv(canvasCSV)

    merged = a.merge(b, on='netID')
    merged.to_csv("extensionstudents.csv", index=False)

if __name__ == '__main__':
    main()