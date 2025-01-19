from bs4 import BeautifulSoup
import csv
from pathlib import Path

def read_html_file(file_path):
    """Read and parse the HTML file"""
    print(f"Reading HTML file from {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return BeautifulSoup(f.read(), 'html.parser')
    except IOError as e:
        print(f"Error reading HTML file: {e}")
        return None

def extract_market_data(soup):
    """Extract market data from the Markets Banner (from the 'main' section)"""
    print("Extracting market data...")
    market_data = []
    
    # Find the MarketsBanner-main section
    main_section = soup.find(class_="MarketsBanner-main")
    
    # Find all the individual market cards inside the main section
    market_cards = main_section.find_all(class_="MarketCard-main")
    
    for card in market_cards:
        # Extract the symbol
        symbol = card.find(class_="MarketCard-symbol").text.strip()
        
        # Extract the position (stock value)
        position = card.find(class_="MarketCard-stockPosition").text.strip()
        
        # Extract the change percentage (check both changePts and changesPct)
        change_pct = None
        change_pct_tag = card.find(class_="MarketCard-changesPct")
        if change_pct_tag:
            change_pct = change_pct_tag.text.strip()
        else:
            change_pct_tag = card.find(class_="MarketCard-changesPts")
            if change_pct_tag:
                change_pct = change_pct_tag.text.strip()

        # Append the data
        market_data.append({
            'symbol': symbol,
            'position': position,
            'change_percentage': change_pct
        })

    return market_data

def extract_news_data(soup):
    """Extract latest news data"""
    print("Extracting latest news data...")
    news_data = []
    
    news_items = soup.find_all(class_="LatestNews-item")
    for item in news_items:
        timestamp = item.find(class_="LatestNews-timestamp").text.strip()
        headline = item.find(class_="LatestNews-headline")
        title = headline.text.strip()
        link = headline['href']
        
        news_data.append({
            'timestamp': timestamp,
            'title': title,
            'link': link
        })
    
    return news_data

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
    # Setup paths
    data_dir = Path("data")
    raw_dir = data_dir / "raw_data"
    processed_dir = data_dir / "processed_data"
    
    # Read HTML file
    html_file = raw_dir / "web_data.html"
    soup = read_html_file(html_file)
    
    if soup:
        # Extract market data
        market_data = extract_market_data(soup)
        market_headers = ['symbol', 'position', 'change_percentage']
        save_to_csv(
            market_data,
            processed_dir / "market_data.csv",
            market_headers
        )
        
        # Extract news data
        news_data = extract_news_data(soup)
        news_headers = ['timestamp', 'title', 'link']
        save_to_csv(
            news_data,
            processed_dir / "news_data.csv",
            news_headers
        )
        
        print("\nData processing completed successfully!")

if __name__ == "__main__":
    main()
