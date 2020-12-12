import csv
import json
from pathlib import Path

total_keymap_count = 0
total_no_cpp_count = 0
total_error_count = 0
total_keymaps = 0
total_keymaps_without_info_json = 0


def toRow(keyboard):
    global total_keymap_count
    global total_keymap_count
    global total_no_cpp_count
    global total_error_count
    global total_keymaps
    global total_keymaps_without_info_json

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
    total_keymap_count = total_keymap_count+keymap_count
    total_no_cpp_count = total_no_cpp_count+no_cpp_count
    total_error_count = total_error_count+error_count
    total_keymaps = total_keymaps+1
    if keyboard["path"] is None:
        total_keymaps_without_info_json = total_keymaps_without_info_json+1
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
print("total_keymaps: "+str(total_keymaps))
print("total_keymaps_without_info_json: "+str(total_keymaps_without_info_json))
print("total_keymap_count: "+str(total_keymap_count))
print("total_no_cpp_count: "+str(total_no_cpp_count))
print("total_error_count: "+str(total_error_count))
