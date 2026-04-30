# 📘 Data‑Driven Blog Post: IMDb Movie Analysis

This project demonstrates an end‑to‑end data workflow:
- **Web scraping** movie metadata from IMDb using Selenium + BeautifulSoup
- **Cleaning and structuring** the scraped dataset
- Saving reproducible outputs into a dedicated data/ folder
- Exploring sentiment‑style patterns using IMDb ratings
- Applying modelling techniques to understand what drives movie ratings
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

## Prerequisites

Before running the scraper, ensure you have the following:

- Python (tested with version 3.x)
- Selenium WebDriver (Tested using the Chrome driver)
- BeautifulSoup
- Requests
- Pandas
- Seasborn

You can install the necessary libraries using pip:
```bash
python -m pip install requests beautifulsoup4 pandas selenium Seaborn

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
