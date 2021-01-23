#!/bin/bash

# work in a temporary folder
cd $(mktemp /tmp/klaunfish.XXX --directory)

# get and configure bot runner
git clone git@github.com:namin/lichess-bot
git checkout acba34feb7f9d4aa7f76f7c7d1c2ad4c372a0637

# get klaunfish
git clone --depth 1 git@github.com:twiddler/klaunfish
mv klaunfish/oi.py lichess-bot/oi.py
mv klaunfish/paint.py lichess-bot/paint.py
mv klaunfish/rate.py lichess-bot/rate.py
mv klaunfish/strategies.py lichess-bot/strategies.py
mv klaunfish/serve.sh lichess-bot/serve.sh
chmod +x lichess-bot/serve.sh

# merge and install requirements
cat klaunfish/requirements.txt >> lichess-bot/requirements.txt
source lichess-bot/.venv/bin/activate
pip install -r lichess-bot/requirements.txt

# clean up a bit
rm -rf klaunfish

# inform what to do next
echo Go to $(pwd), edit your config.yml and run serve.sh