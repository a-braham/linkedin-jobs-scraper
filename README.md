# Linkedin Job scraper

A scprit to extract jobs from linkedin jobs.

## Features
- Login
- Profile
- Search By Title
- Search By Location
- Export To CSV

## How To Run
- Create python virtual environment
``` $ virtualenv -p python3 env```

- Install Requirements
``` $ pip install -r requirements.txt```

- Create a .env file in the root folder and set variables as in the .env-example
- Source the .env file
``` $ source .env```
- Run scraper
```python scraper.py```

## Todo
1. Configure docker to run scraper
2. Deploy to GCP Jobs



