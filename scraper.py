from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# -----------------------------
# SETUP SELENIUM CHROME DRIVER
# -----------------------------
# Setup Chrome Options
chrome_options = Options()
# chrome_options.add_argument("--headless") # Uncomment to run without opening a window

# Initialize the Driver
driver = webdriver.Chrome(options=chrome_options)

# -----------------------------
# LOAD THE MAIN MOVIES PAGE
# -----------------------------

# Open JustWatch movies page
driver.get('https://www.justwatch.com/us/movies')
time.sleep(5)

# -----------------------------
# SCROLL TO LOAD ALL MOVIES
# -----------------------------

# Get initial scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

for _ in range(30):
    # Scroll to bottom of page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    # Small scroll up/down to trigger additional loading
    driver.execute_script("window.scrollBy(0, -100);")
    time.sleep(1)
    driver.execute_script("window.scrollBy(0, 100);")

    # Check if new content loaded
    new_height = driver.execute_script("return document.body.scrollHeight")

    # If height hasn't changed, no more content is loading → stop scrolling
    if new_height != last_height:
        # Content loaded → reset timer
        last_height = new_height
        last_change_time = time.time()
    else:
        # No new content — check if 10 seconds have passed
        if time.time() - last_change_time > 10:
            print("No new content for 10 seconds — stopping scroll.")
            break

    last_height = new_height

# -----------------------------
# COLLECT MOVIE LINKS
# -----------------------------
# Select all movie tiles and extract their <a> links
movies = driver.find_elements(By.CSS_SELECTOR, 'div.title-list-grid__item a')

links = []
for movie in movies:
    link = movie.get_attribute('href')
    if link:
        links.append(link)

links = list(set(links)) # Ensure only unique links

print(f"Total movie links: {len(links)}")

# -----------------------------
# SCRAPE EACH MOVIE PAGE
# -----------------------------
data = []

for i, link in enumerate(links):
    print(f"Scraping movie {i}/{len(links)}") # print which movie its scraping
    try:
    # Open the movie detail page
        driver.get(link)
    except Exception as e:
        print(f"Failed to load {link}: {e}")
        continue  # skip to next movie
    time.sleep(2)

    # Parse page HTML with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract movie title
    try:
        title = soup.find('h1').get_text(strip=True)
    except:
        title = 'N/A'

    # Extract release year
    try:
        year = soup.find("span", class_="release-year").get_text(strip=True)
    except:
        year = 'N/A'

    # Extract IMDB rating
    try:
        imdb = soup.find("span", class_="imdb-score").get_text(strip=True)
    except:
        imdb = "N/A"

    # Extract duration
    try:
        details = soup.find_all("div", class_="title-detail-hero-details__item")
        duration = next((d.text.strip() for d in details if "min" in d.text), "N/A")
    except:
        duration = "N/A"

    # Extract genres
    try:
        for div in soup.find_all("div", class_="poster-detail-infos__value"):
            span = div.find("span")
            if span:
                text = span.get_text(strip=True)

                if "," in text and not any(char.isdigit() for char in text):
                    genres = text
                    break
    except:
        genres = "N/A"

    # Extract cast
    try:
        actors = soup.find_all("div", class_="title-credits__actor")
        cast = ", ".join(actor.find('span', class_='title-credit-name').get_text(strip=True) for actor in actors if actor.find('span', class_='title-credit-name'))
    except:
        cast = "N/A"

    # Extract director
    try:
        directors = soup.find_all("div", class_="poster-detail-infos")
        director = ", ".join(director.find('span', class_='title-credit-name').get_text(strip=True) for director in directors if director.find('span', class_='title-credit-name'))
    except:
        director = "N/A"

    # Extract providers
    try:
        providers = [p.get("alt") for p in soup.select("img.provider-icon")]
        providers = ", ".join(providers)
    except:
        providers = "N/A"

    data.append({
        "Title": title,
        "Year": year,
        "IMDb Rating": imdb,
        "Duration": duration,
        "Genres": genres,
        "Cast": cast,
        "Director": director,
        "Providers": providers
    })

driver.quit()

# -----------------------------
# SAVE RESULTS TO CSV
# -----------------------------
df = pd.DataFrame(data)
df.to_csv("movies.csv", index=False)
print(df.head())