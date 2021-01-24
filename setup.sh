#!/bin/bash

# work in a temporary folder
TEMPDIR=$(mktemp /tmp/klaunfish.XXX --directory)

# get and configure bot runner
cd $TEMPDIR
git clone git@github.com:namin/lichess-bot .
git checkout acba34feb7f9d4aa7f76f7c7d1c2ad4c372a0637
cd -

# copy necessary scripts
cp oi.py $TEMPDIR/oi.py
cp paint.py $TEMPDIR/paint.py
cp rate.py $TEMPDIR/rate.py
cp strategies.py $TEMPDIR/strategies.py
cp squaresets.py $TEMPDIR/squaresets.py
cp serve.sh $TEMPDIR/serve.sh
chmod +x $TEMPDIR/serve.sh

# merge and install requirements
cat requirements.txt >> $TEMPDIR/requirements.txt
virtualenv $TEMPDIR/.venv
source $TEMPDIR/.venv/bin/activate
pip install -r $TEMPDIR/requirements.txt

# inform what to do next
echo
echo "Edit ${TEMPDIR}/config.yml, then run ${TEMPDIR}/serve.sh"
echo