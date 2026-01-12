import heapq
import time
from .utils import can_fetch_url, fetch_html, get_robot_parser
from .parser import parse_content

class Crawler:
    def __init__(self, start_url, max_pages=50):
        self.start_url = start_url
        self.max_pages = max_pages
        self.visited = set()
        self.queue = [] 
        heapq.heappush(self.queue, (2, start_url))
        self.rp = get_robot_parser("/".join(start_url.split("/")[:3]))

    def run(self):
        results = []
        while self.queue and len(self.visited) < self.max_pages:
            _, current_url = heapq.heappop(self.queue)

            if current_url in self.visited: continue
            if not can_fetch_url(self.rp, "*", current_url): continue

            print(f"Crawling {len(self.visited)+1}: {current_url}")
            html = fetch_html(current_url)
            
            if html:
                data = parse_content(html, current_url)
                if data:
                    results.append(data)
                    self.visited.add(current_url)
                    for link in data['links']:
                        if link not in self.visited:
                            prio = 1 if '/product/' in link else 2
                            heapq.heappush(self.queue, (prio, link))
            time.sleep(0.5)
        return results