"""Generate a keymap.json from a keymap.c file.
"""
import json
import multiprocessing
import time
from milc import cli
import qmk.keymap
import qmk.keyboard
import qmk.path



@cli.subcommand('Generates all keymap json for all keyboards')
def create_all_keymaps(cli):
    print("Collecting keyboards")
    start = time.time()
    keyboards = qmk.keyboard.list_keyboards()
    end_keyboards = time.time()
    print("Collected keyboards in " + str(end_keyboards - start))
    print("Converting keymaps")

    # multithreaded
    if(keyboards):
        pool = multiprocessing.Pool()
        pool.map(create_keymaps, keyboards)
        pool.close() 
    # singlethreaded
    # if(keyboards):
    #     for keyboard in keyboards:
    #         create_keymaps(keyboard)

    end = time.time()
    print(end - start)
    print("Converted keymaps in " + str(end - end_keyboards))
    print("Total time: " + str(end - start))


def create_keymaps(keyboard):
    cli.log.info(keyboard)
    keymaps = [{"name": keymap.name,"path":str(keymap)} for keymap in qmk.keymap.list_keymaps(keyboard,fullpath=True)] 
    if(keymaps):
        for keymap in keymaps:
            
            keymap_path = qmk.path.normpath(keymap["path"] + "/keymap.c")
            keymap_name=keymap['name']
            
           
            if not keymap_path.exists():
                # cli.log.error(keyboard + " | " + keymap["name"] + ': C file does not exist')
                keymap["error"] = "No C file"
                continue

            try:
                keymap_json = qmk.keymap.c2json(keyboard, keymap_name, keymap_path, use_cpp=True)
            except UnicodeDecodeError:
                # cli.log.error(keyboard + " | " + keymap["name"] + ': Unable to decode unicode')
                keymap["error"] = "Unicode Decode Error"
                continue
            except:
                cli.log.error(keyboard + " | " + keymap_name + ': Unknown Error')
                keymap["error"] = "Unknown"
                continue

            try:
                keymap_json = qmk.keymap.generate_json(  keymap_json['keymap'], keymap_json['keyboard'], keymap_json['layout'], keymap_json['layers'])
            except KeyError:
                # cli.log.warning(keyboard + " | " + keymap["name"] + ': Something went wrong. Retrying with --no-cpp')
                keymap["no-cpp"] = True
                try:
                    try:
                        keymap_json = qmk.keymap.c2json(keyboard, keymap_name, keymap_path, use_cpp=False)
                    except UnicodeDecodeError:
                        # cli.log.error(keyboard + " | " + keymap["name"] + ': Unable to decode unicode')
                        keymap["error"] = "Unicode Decode Error"
                        continue

                    keymap_json = qmk.keymap.generate_json( keymap_json['keymap'],keymap_json['keyboard'], keymap_json['layout'], keymap_json['layers'])
                except KeyError:
                    # cli.log.error(keyboard + " | " + keymap["name"] + ': Something went wrong. Failed on keymap')
                    keymap["error"] = "Unknown Error"
                    continue
            output_path = qmk.path.normpath("../keymaps/" + keyboard + "/" + keymap_name + ".keymap.json")
            if output_path:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(json.dumps(keymap_json))
                # cli.log.info(keyboard + " | " + keymap["name"] + ': Wrote to %s.', output_path)
        summary_path = qmk.path.normpath("../keymaps/" + keyboard + "/" + "keymaps.json")
        if summary_path:
            summary_path.parent.mkdir(parents=True, exist_ok=True)
            summary_path.write_text(json.dumps(keymaps))