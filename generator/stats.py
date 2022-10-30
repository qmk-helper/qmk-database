import csv
import datetime
import json
from pathlib import Path
from milc import cli

total_keymap_count = 0
total_no_cpp_count = 0
total_error_count = 0
total_keyboards = 0
total_keyboards_without_info_json = 0

def toRow(keyboard):
    global total_keymap_count
    global total_keymap_count
    global total_no_cpp_count
    global total_error_count
    global total_keyboards
    global total_keyboards_without_info_json

    if(not (Path("../keymaps/"+keyboard["name"]+"/keymaps.json").exists())):
        return[]
    keymaps_json = open("../keymaps/"+keyboard["name"]+"/keymaps.json")
    keymaps = json.load(keymaps_json)

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
    total_keyboards = total_keyboards+1
    if keyboard["path"] is None:
        total_keyboards_without_info_json = total_keyboards_without_info_json+1
    return [keyboard["name"], keyboard["path"], keymap_count, no_cpp_count, error_count]

@cli.subcommand('Writes stats about the generation process')
def generate_stats(cli):


    with open('../keyboards.json') as keyboards_json:
        keyboards = json.load(keyboards_json)

    with open('../stats/stats.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["name", "path", "keymap_count",
                            "no_cpp_count", "error_count"])

        for keyboard in keyboards:
            row = toRow(keyboard)
            spamwriter.writerow(row)
    with open('../stats/readme.md', 'w') as stats_readme:
        stats_readme.write("# Statistics of last Build\n\n")
        stats_readme.write("Date: "+str(datetime.datetime.now())+"\n\n")
        stats_readme.write("- Keyboards: "+str(total_keyboards)+"\n")
        stats_readme.write("  - without info.json: " +
            str(total_keyboards_without_info_json)+"\n")
        stats_readme.write("- Keymaps: "+str(total_keymap_count)+"\n")
        stats_readme.write("  - no-cpp: "+str(total_no_cpp_count)+"\n")
        stats_readme.write("  - error: "+str(total_error_count)+"\n")
