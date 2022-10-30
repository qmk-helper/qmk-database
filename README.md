# QMK Database

This repository acts as a storage for all qmk keymaps. It uses a modified version of the firmware to parse the original qmk firmware.

[Current Stats](stats/readme.md)

## Scraping

### Setup

The current master of qmk should be in a subfolder of qmk-database:

- qmk-database (qmk-helper)
  - qmk-firmware (qmk)

### Execution steps

1. Remove previous keyboards.json & keymaps

```bash
rm keyboards.json
rm -r keymaps
```

2. Clone/Pull QMK Firmware https://github.com/qmk/qmk_firmware.git & go into the folder

```bash
git clone https://github.com/qmk/qmk_firmware.git  # Initial download
cd qmk_firmware/ && git pull && cd .. # Refresh
```

3. Run Generator

```bash
python3 generator/main.py run-all
```
