# QMK Database

This repository acts as a storage for all qmk keymaps. It uses a modified version of the firmware to parse the original qmk firmware.

[Current Stats](stats/readme.md)

## Scraping

### Setup

The tooling is in the qmk-helper fork of the qmk-firmwware, this repo should be in the same root folder as the qmk-database. the current master of qmk should be in a subfolder of qmk-database:

- qmk-firmware (qmk-helper)
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
git clone https://github.com/qmk/qmk_firmware.git # Initial download
cd qmk_firmware/ && git pull # Refresh
```

4. List Keyboards

```bash
python3 ../../qmk_firmware/bin/qmk list-keyboards > ../keyboards.json
```

5. Convert Keymaps

```bash
python3 ../../qmk_firmware/bin/qmk create-all-keymaps
mv keymaps/ ..

```

6. Generate Stats

```bash
cd ../stats
python3 stats.py > readme.md
```
