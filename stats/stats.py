import csv
import json
from pathlib import Path


def toRow(keyboard):
    if(not (Path("../keymaps/"+keyboard["name"]+"/keymaps.json").exists())):
        return[]
    keymaps_json = open("../keymaps/"+keyboard["name"]+"/keymaps.json")
    keymaps = json.load(keymaps_json)
    print(keyboard["name"])
    keymap_count = 0
    no_cpp_count = 0
    error_count = 0
    for keymap in keymaps:
        keymap_count = keymap_count+1
        if("no-cpp" in keymap):
            no_cpp_count = no_cpp_count+1
        if("error" in keymap):
            error_count = error_count+1

    return [keyboard["name"], keyboard["path"], keymap_count, no_cpp_count, error_count]


with open('../keyboards.json') as keyboards_json:
    keyboards = json.load(keyboards_json)
    # print(keyboards)

# print(toRow({"name": "zlant", "path": ""}))

with open('stats.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(["name", "path", "keymap_count",
                         "no_cpp_count", "error_count"])

    for keyboard in keyboards:
        row = toRow(keyboard)
        spamwriter.writerow(row)
