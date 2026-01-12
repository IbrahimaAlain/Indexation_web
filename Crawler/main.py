import json
from src.crawler import Crawler

START_URL = "https://web-scraping.dev/products"
OUTPUT_FILE = "resultats.json"

if __name__ == "__main__":
    crawler = Crawler(START_URL, max_pages=50)
    data = crawler.run()

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for entry in data:
            json.dump(entry, f, ensure_ascii=False)
            f.write('\n')
            
    print(f"Terminé. {len(data)} lignes écrites.")