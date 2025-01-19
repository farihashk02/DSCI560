import requests
from bs4 import BeautifulSoup
import csv
from pathlib import Path

def scrape_webpage(url):
    """Scrape the webpage and return its content"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        print(f"Fetching data from {url}...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for successful request

        # Parse the HTML page
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None

def extract_market_data(soup):
    """Extract market data from the markets banner"""
    print("Extracting market data...")
    market_data = []

    # Use the correct class "MarketCard-main" instead of "MarketCard-container"
    market_cards = soup.find_all(class_="MarketCard-main")
    for card in market_cards:
        symbol = card.find(class_="MarketCard-symbol").text.strip()
        position = card.find(class_="MarketCard-stockPosition").text.strip()
        change_pct = card.find(class_="MarketCard-changesPct").text.strip()

        market_data.append({
            'symbol': symbol,
            'position': position,
            'change_percentage': change_pct
        })

    return market_data

def save_to_csv(data, filename, headers):
    """Save data to CSV file"""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        print(f"Successfully created {filename}")
    except IOError as e:
        print(f"Error saving to CSV: {e}")

def main():
    # URL to scrape
    url = "https://www.cnbc.com/world/?region=world"

    # Scrape the webpage
    soup = scrape_webpage(url)

    if soup:
        # Extract market data
        market_data = extract_market_data(soup)
        market_headers = ['symbol', 'position', 'change_percentage']

        # Save the extracted data to CSV
        save_to_csv(market_data, "market_data.csv", market_headers)

if __name__ == "__main__":
    main()
