

import os
import sys

from pathlib import Path
import milc



# simulate qmk cli environment
qmk_firmware= Path(os.path.dirname(os.path.abspath(__file__)), '../qmk_firmware').expanduser().resolve()
os.chdir(str(qmk_firmware))
sys.path.append(str(qmk_firmware / 'lib/python'))
os.environ['ORIG_CWD'] = os.getcwd()

# Subcommands
import list_keyboards
import generate_all_keymaps
import stats



@milc.cli.entrypoint('CLI wrapper for running QMK commands.')
def qmk_main(cli):
    cli.print_help()

@milc.cli.subcommand('Performs all generator steps')
def run_all(cli):
    list_keyboards.store_keyboards(cli)
    generate_all_keymaps.create_all_keymaps(cli)
    stats.generate_stats(cli)

milc.cli()

# python3 ./generator/main.py store-keyboards