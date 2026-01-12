from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_metadata(soup):
    title_tag = soup.select_one('h1') or soup.select_one('title')
    title = title_tag.get_text(strip=True) if title_tag else ""
    
    desc_tag = soup.select_one('.description, [itemprop="description"]')
    if desc_tag:
        description = desc_tag.get_text(strip=True)
    else:
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc['content'] if meta_desc else ""
    
    return title, description

def extract_links(soup, current_url):
    links = []
    for a in soup.find_all('a', href=True):
        full = urljoin(current_url, a['href'])
        if full.startswith("https://web-scraping.dev"): 
            links.append(full)
    return links

def parse_content(html, current_url):
    if not html: return None
    soup = BeautifulSoup(html, 'html.parser')

    title, description = extract_metadata(soup)
    links = extract_links(soup, current_url)

    return {
        "url": current_url,
        "title": title,
        "description": description,
        "links": links
    }