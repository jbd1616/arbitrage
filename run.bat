@echo off
echo Starting script execution...

REM Run the Python scripts in order
echo Running b365scraper.py
python ./Scrapers/bet365_scraper.py

echo Running b365parser.py
python ./Parsers/bet365_parser.py

echo Running Fscraper.py
python ./Scrapers/Fanduel_scraper.py

echo Running fparser.py
python ./Parsers/fanduel_parser.py

echo Running Combiner.py
python ./Utils/Combiner.py

echo Running Comparator.py
python ./Utils/Comparator.py

echo All scripts executed successfully!
pause

