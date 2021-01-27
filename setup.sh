#!/bin/bash

# work in a temporary folder
TEMPDIR=$(mktemp /tmp/klaunfish.XXX --directory)

# get and configure bot runner
cd $TEMPDIR
git clone git@github.com:namin/lichess-bot .
git checkout acba34feb7f9d4aa7f76f7c7d1c2ad4c372a0637
cd -

# copy scripts and config
ln -s "$(pwd)/oi.py" $TEMPDIR/
ln -s "$(pwd)/paint.py" $TEMPDIR/
ln -s "$(pwd)/rate.py" $TEMPDIR/
ln -s "$(pwd)/search.py" $TEMPDIR/
rm $TEMPDIR/strategies.py
ln -s "$(pwd)/strategies.py" $TEMPDIR/
ln -s "$(pwd)/graph.py" $TEMPDIR/
ln -s "$(pwd)/config.yml" $TEMPDIR/
cp serve.sh $TEMPDIR/
chmod +x $TEMPDIR/serve.sh

# merge and install requirements
cat requirements.txt >> $TEMPDIR/requirements.txt
virtualenv $TEMPDIR/.venv
source $TEMPDIR/.venv/bin/activate
pip install -r $TEMPDIR/requirements.txt

# inform what to do next
echo
echo "Setup complete. Run ${TEMPDIR}/serve.sh!"
echo