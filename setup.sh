#!/bin/bash

# work in a temporary folder
TEMPDIR=$(mktemp /tmp/klaunfish.XXX --directory)

# get and configure bot runner
cd $TEMPDIR
git clone git@github.com:namin/lichess-bot .
git checkout acba34feb7f9d4aa7f76f7c7d1c2ad4c372a0637
cd -

# copy necessary scripts
cp oi.py $TEMPDIR/
cp paint.py $TEMPDIR/
cp rate.py $TEMPDIR/
cp search.py $TEMPDIR/
cp strategies.py $TEMPDIR/
cp serve.sh $TEMPDIR/
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