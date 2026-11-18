@echo off
cd /d "%~dp0"
echo Probing candidate stores from this computer (home connection)...
python tools\scrape\probe.py --out scraped\probe_local.md
echo.
echo Done. Result: scraped\probe_local.md
pause
