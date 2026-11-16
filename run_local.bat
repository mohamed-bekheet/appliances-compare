@echo off
setlocal
title Appliances Compare - local scrape
REM Scrapes the stores that block cloud servers (Carrefour, Berty Center, Jumia, El Araby) from this PC,
REM then pushes ONLY the results; GitHub Actions merges them into data.json automatically.
REM First time:  git clone https://github.com/mohamed-bekheet/appliances-compare.git E:\Personal\compare_appliances
REM Needs Git + Python 3 on PATH. Takes ~1 hour (polite: one request every 2 seconds per site).
cd /d "%~dp0"
echo ==== [1/5] Folder: %CD%
where git >nul 2>nul || (echo Git is not installed or not on PATH & goto :err)
set "PY=python"
python --version >nul 2>nul || set "PY=py -3"
%PY% --version || (echo Python 3 is not installed or not on PATH & goto :err)
echo ==== [2/5] git pull
git pull --rebase || goto :err
echo ==== [3/5] installing Python packages
%PY% -m pip install -r tools\scrape\requirements.txt || goto :err
echo ==== [4/5] scraping Carrefour, Berty, Jumia, El Araby - about 1 hour, you will see progress lines below
%PY% -u tools\scrape\run.py --stores carrefour,berty,jumia,elaraby --dry-run --out scraped\local || goto :err
echo ==== [5/5] pushing results
git add scraped\local
git commit -m "Local scrape %date%"
git pull --rebase
git push || goto :err
echo.
echo Done. GitHub will merge the results into the site in a few minutes.
pause
exit /b 0
:err
echo.
echo Something failed - read the messages above.
pause
exit /b 1
