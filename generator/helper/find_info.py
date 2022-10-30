from pathlib import Path
import qmk.path

def find_info(keyboard):
    """Returns the info.json for this keyboard.
    """
    cur_dir = qmk.path.keyboard(keyboard)
    keyboards_dir = Path('keyboards')
    while not (cur_dir / 'info.json').exists():
        if cur_dir == keyboards_dir:
            return None
        cur_dir = cur_dir.parent

    return str(cur_dir / 'info.json')