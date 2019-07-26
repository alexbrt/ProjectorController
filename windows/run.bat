@echo off
set filepath=%~dp0
cd %filepath%
cd ../
git fetch
for /F "tokens=*" %%g in ('git rev-list HEAD...origin/master --count') do (set commitsaway=%%g)
if %commitsaway% neq 0 (
	echo ####################
	echo Remote repo has changes.
	echo.
	echo Updating local repo...
	echo.
	git reset --hard FETCH_HEAD
	echo ####################
	echo.
)
python ./src/main.py
