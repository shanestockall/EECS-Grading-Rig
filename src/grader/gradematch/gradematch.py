import pandas as pd


##############################################
################## GLOBALS ###################
##############################################

global gradebookCSV
global gradesCSV

##############################################

def load_config():
    with open('config.json') as cfg:
        config = json.load(cfg)
        for key in config.keys():
            if key in globals():
                globals()[key] = config[key]

def main():
    load_config()
    a = pd.read_csv(gradebookCSV)
    b = pd.read_csv(bradesCSV)

    merged = a.merge(b, on='ID')
    merged.to_csv("export.csv", index=False)

if __name__ == '__main__':
    main()
