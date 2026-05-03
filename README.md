# 📘 Data‑Driven Blog Post: IMDb Movie Analysis

This project demonstrates an end‑to‑end data workflow:
- **Web scraping** movie metadata from IMDb using Selenium + BeautifulSoup
- **Cleaning and structuring** the scraped dataset
- Saving reproducible outputs into a dedicated data/ folder
- Exploring sentiment‑style patterns using IMDb ratings
- **Preparing results for a data‑driven blog post**

The dataset includes:
- Title
- Year
- IMDb Rating
- Duration
- Genres
- Cast
- Director
- Providers (streaming availability)

# ⚠️ Data Disclaimer
The dataset used in this project is scraped directly from JustWatch. Because the JustWatch website relies on lazy‑loading (content loads dynamically as the user scrolls), the number of movies scraped will vary each time scrape.py is run. Factors such as network speed, page rendering timing, and how quickly new tiles load can all influence how many movie entries are captured.

As a result:
- The dataset is not guaranteed to be identical across runs
- Some movies may be missed if they fail to load during scrolling
- Some movies may appear as duplicates due to JustWatch re‑rendering tiles during lazy‑load events
- This variability is an inherent limitation of scraping dynamically loaded websites and should be considered when interpreting the results.

## Prerequisites

Before running the scraper, ensure you have the following:

- Python (tested with version 3.x)
- Selenium WebDriver (Tested using the Chrome driver)
- BeautifulSoup
- Requests
- Pandas
- Seaborn

You can install the necessary libraries using pip:
```bash
python -m pip install requests beautifulsoup4 pandas selenium seaborn

```

## Usage

1. **Clone the Repository**: Clone the repository from GitHub to your local machine.
   ```bash
   git clone https://github.com/dwy310/data-driven-blog-post.git
   ```


2. **Run scrape.py script**: Run this script to webscrape JustWatch using Python (Make sure you are inside the folder)
   ```bash
   python scrape.py
   ```

3. **Run clean.py script**: Run this script to clean raw data file (Make sure you are inside the folder)
   ```bash
   python clean.py
   ```


4. **Run analysis.py script**: Run this script to produce figures and conduct analysis (Make sure you are inside the folder)
   ```bash
   python analysis.py
   ```

## Project Directory
```
├── README.md               <- Top‑level project overview, instructions, and documentation
│
├── data
│   ├── movies.csv          <- Original scraped movie metadata (CSV)             
│   └── movies_clean.csv  <- Final cleaned dataset used for analysis and visualisation
│
├── output
│   ├── figure_1          <- Highest Rated Genres     
│   ├── figure_2          <- IMDb Rating vs Duration    
│   ├── figure_3          <- Average Movie Duration by Genre  
│   ├── figure_4          <- Genre Common with Animation 
│   ├── figure_5          <- Top-Rated Directors 
│   ├── figure_6          <- Top 10 Director-Actor Collaboration  
│   ├── figure_7          <- Top 20 Most Frequent Actors          
│   └── figure_8          <- Top 20 Actors by Movie Rating
│ 
└── src                     <- Source code for the project
    ├── scrape.py           <- Script to scrape movie metadata from JustWatch
    ├── clean.py            <- Script to clean, parse, and structure the dataset
    └── analysis.py         <- Script to run analysis and generate figures   
```
