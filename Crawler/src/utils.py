import urllib.request
import urllib.robotparser

def get_robot_parser(base_url):
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(f"{base_url}/robots.txt")
    try:
        rp.read()
    except:
        pass
    return rp

def can_fetch_url(rp, user_agent, url):
    return rp.can_fetch(user_agent, url) if rp else True

def fetch_html(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'EnsaiBot/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error {url}: {e}")
        return None