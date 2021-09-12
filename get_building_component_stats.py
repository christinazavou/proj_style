import argparse
import pandas as pd
import json


STYLES = [
    'unknown', 'colonial', 'neo_classicism', 'modernist', 'ottoman', 'gothic', 'byzantine',
    'venetian', 'baroque', 'russian', 'romanesque', 'renaissance', 'pagoda'
]

ELEMENTS = [
    'dome', 'door', 'window', 'tower', 'column'
]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--in_txt", type=str, dest="in_txt")
    parser.add_argument("--out_json", type=str, dest="out_json")
    parser.add_argument("--buildings_csv", type=str, dest="buildings_csv")
    args = parser.parse_args()

    building_styles_df = pd.read_csv(args.buildings_csv,sep=";", header=None)
    building_styles = {}
    for idx, row in building_styles_df.iterrows():
        style, building = row
        building_styles[building] = style.lower()

    component_styles = {}
    for c in ELEMENTS:
        component_styles[c] = {s: 0 for s in STYLES}

    with open(args.in_txt, "r") as fin:
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
            c = [c for c in ELEMENTS if c in component.lower()]
            c = c[0]
            component_styles[c][style] += 1
    with open(args.out_json, "w") as fout:
        json.dump(component_styles, fout, indent=2)

