
from helper.find_info import find_info
import qmk.keyboard
import json
from milc import cli

def list_keyboards():
    keyboards=qmk.keyboard.list_keyboards()
    return [{"name": keyboard,"path":find_info(keyboard)} for keyboard in keyboards]

@cli.subcommand('Writes a json with all keyboards and their info.jsons')
def store_keyboards(cli):
    keyboards_path = qmk.path.normpath("../keyboards.json")
    keyboards_path.write_text(json.dumps(list_keyboards(), indent=2))