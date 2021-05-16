# Remove existing keymaps (makes recalculation faster)
rm keyboards.json
rm -r keymaps

# update qmk_firmware (requries clone first)
cd qmk_firmware/ && git pull

# List Keyboards
python3 ../../qmk_firmware/bin/qmk list-keyboards > ../keyboards.json
jq . ../keyboards.json > ../keyboards.formated.json
mv ../keyboards.formated.json ../keyboards.json

# Generate & Copy keymaps
python3 ../../qmk_firmware/bin/qmk create-all-keymaps
mv keymaps/ ..

cd ../stats
python3 stats.py > readme.md