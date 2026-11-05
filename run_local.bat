@echo off
REM Scrape the stores that block cloud servers (Carrefour, Berty Center, Jumia, El Araby) from this PC,
REM then push ONLY the results; GitHub Actions merges them into data.json automatically.
REM First time:  git clone https://github.com/mohamed-bekheet/appliances-compare.git E:\Personal\compare_appliances
REM Needs Git + Python 3 on PATH. Takes ~1 hour (polite: one request every 2 seconds per site).
cd /d "%~dp0"
git pull --rebase -q || goto :err
python -m pip install -q -r tools\scrape\requirements.txt || goto :err
python tools\scrape\run.py --stores carrefour,berty,jumia,elaraby --dry-run --out scraped\local || goto :err
git add scraped\local
git commit -q -m "Local scrape %date%" && (git pull --rebase -q & git push -q)
echo Done. GitHub will merge the results into the site in a few minutes.
pause
exit /b 0
:err
echo Something failed - see the messages above.
pause
exit /b 1
