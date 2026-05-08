# 📘 Data‑Driven Blog Post: IMDb Movie Analysis

*HackMD Page Link:* **[What Makes a Movie Great](https://hackmd.io/@l6Vo-ZhfQLGdtpdRTjfjBA/SJGemNitWg/)**
---
## Table of Contents
1. [Overview](#overview)
2. [Data](#data)
3. [Repository Structure](#repository-structure)
4. [Requirements](#requirements)
5. [Running Instructions](#running-instructions)
---

## Overview
This project demonstrates an end‑to‑end data workflow:
- **Web scraping** movie metadata from JustWatch using Selenium + BeautifulSoup + Requests
- **Cleaning and structuring** the scraped dataset
- Saving outputs into a dedicated data/ folder
- Exploring sentiment‑style patterns using IMDb ratings
- **Preparing results for a data‑driven blog post**
---

## Data
The datasets (`movies.csv` and `movies_clean.csv`) comes directly from [JustWatch.com's popular tab](https://www.justwatch.com/us/movies?release_year_from=2000). Both are in csv format and is read directly using `pandas`.

The key variables used in this analysis are:

| Variable | Description |
|---|---|
| `Title` | Movie title (string identifying each film). |
| `Year` | Release year of the film (extracted as a four‑digit integer). |
| `IMDb Rating` | Audience rating on IMDb, measured on a 1–10 scale. |
| `Duration` | Runtime of the film in minutes. |
| `Genres` | List of genres assigned to the film (e.g., Drama, Comedy, Thriller). |
| `Cast` | List of actors appearing in the film. |
| `Director` | Director(s) responsible for the film. |
| `Providers` | Streaming platforms where the film is available (e.g., Netflix, Prime Video). |

**⚠️ Data Disclaimer**
Because the JustWatch website relies on lazy‑loading (content loads dynamically as the user scrolls), the number of movies scraped will vary each time scrape.py is run. Factors such as network speed, page rendering timing, and how quickly new tiles load can all influence how many movie entries are captured.

As a result:
- The dataset is not guaranteed to be identical across runs
- Some movies may be missed if they fail to load during scrolling
- Some movies may appear as duplicates due to JustWatch re‑rendering tiles during lazy‑load events
- This variability is an inherent limitation of scraping dynamically loaded websites and should be considered when interpreting the results.
---

## Repository Structure
```
├── README.md                <- Top‑level project overview, instructions, and documentation
│
├── data
│   ├── pre-saved_movies.csv <- Original scraped movie metadata (CSV)             
│   └── movies_clean.csv     <- Final cleaned dataset used for analysis and visualisation
│
├── output
│   ├── figure_1             <- Highest Rated Genres     
│   ├── figure_2             <- IMDb Rating vs Duration    
│   ├── figure_3             <- Average Movie Duration by Genre  
│   ├── figure_4             <- Genre Common with Animation 
│   ├── figure_5             <- Top-Rated Directors 
│   ├── figure_6             <- Top 10 Director-Actor Collaboration  
│   ├── figure_7             <- Top 20 Most Frequent Actors          
│   └── figure_8             <- Top 20 Actors by Movie Rating
│ 
└── src                      <- Source code for the project
    ├── scraper.py           <- Script to scrape movie metadata from JustWatch
    ├── clean.py             <- Script to clean, parse, and structure the dataset
    └── analysis.py          <- Script to run analysis and generate figures   
```
---

## Requirements

Before running the scraper, ensure you have the following:

### System
- Python (tested with version 3.x)

### Python Packages
Install all dependencies via pip: 
```bash
python -m pip install requests==2.33.1 beautifulsoup4==4.14.3 numpy==2.4.4 pandas==3.0.2 selenium==4.43.0 seaborn==0.13.2
```
---

## Running Instructions

1. **Clone the Repository**: Clone the repository from GitHub to your local machine.
   ```bash
   git clone https://github.com/dwy310/data-driven-blog-post.git
   ```

2. **Run scrape.py script**: Run this script to webscrape JustWatch using Python (Make sure you are inside the folder)
   ```bash
   python src/scraper.py
   ```
**NOTE:** If scraping cannot be completed, or if you prefer not to run the scraper at all, you can instead use the pre‑scraped CSV files provided in the data/ folder. Both the pre‑saved dataset and your own partially or fully scraped CSV files can be used directly with clean.py to continue the workflow without interruption.

3. **Run clean.py script**: Run this script to clean raw data file (Make sure you are inside the folder)
   ```bash
   python src/clean.py
   ```
**NOTE:** If you are using the pre‑saved dataset instead of newly scraped data, remember to update the input filename on line 29. Change "movies.csv" to"pre-saved_movies.csv" when loading the dataset. If you are using your own
scraped data, no changes are required.

Both the pre‑saved CSV and your newly scraped CSV contain the same structure, so clean.py will run normally with either file. 

4. **Run analysis.py script**: Run this script to produce figures and conduct analysis (Make sure you are inside the folder)
   ```bash
   python src/analysis.py
   ```
---

