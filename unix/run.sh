#!/usr/bin/env bash

filepath=$(dirname "$0")

cd $filepath
cd ../
git fetch https://github.com/alexbrt/ProjectorController.git master > /dev/null 2>&1
if [[ "$(git rev-list HEAD...origin/master --count)" -ne "0" ]]; then
	printf '####################\n'
	printf 'Remote repo has changes.\n'
	printf 'Updating local repo...\n\n'
	git reset --hard FETCH_HEAD
	printf '####################\n\n'
fi
cd ./src
python3 ./main.py
