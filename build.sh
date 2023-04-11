#!/usr/bin/env sh

set -eu

pipenv requirements > .requirements.txt
rm -rf .vendor
pipenv run pip install --upgrade -r .requirements.txt --target .vendor
rm .requirements.txt
cp -r models .vendor/