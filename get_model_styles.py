import argparse
import pandas as pd


STYLES = [
    'unknown', 'colonial', 'neo_classicism', 'modernist', 'ottoman', 'gothic', 'byzantine',
    'venetian', 'baroque', 'russian', 'romanesque', 'renaissance', 'pagoda'
]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--in_txt", type=str, dest="in_txt")
    parser.add_argument("--out_txt", type=str, dest="out_txt")
    parser.add_argument("--buildings_csv", type=str, dest="buildings_csv")
    args = parser.parse_args()

    building_styles_df = pd.read_csv(args.buildings_csv,sep=";", header=None)
    building_styles = {}
    for idx, row in building_styles_df.iterrows():
        style, building = row
        building_styles[building] = style

    with open(args.in_txt, "r") as fin:
        with open(args.out_txt, "w") as fout:
            for line in fin.readlines():
                building, component = line.split("_group")
                if 'unknown' in component.lower():
                    if building in building_styles:
                        style = building_styles[building]
                    else:
                        style = 'unknown'
                else:
                    style = [s for s in STYLES if s in component.lower()]
                    style = style[0]
                fout.write(f"{style}\n")
