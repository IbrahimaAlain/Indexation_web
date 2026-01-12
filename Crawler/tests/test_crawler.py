import unittest
from unittest.mock import patch
from src.crawler import Crawler

class TestCrawlerStarts(unittest.TestCase):

    @patch('src.crawler.fetch_html')
    @patch('src.crawler.can_fetch_url')
    @patch('src.crawler.get_robot_parser')
    def test_start_from_home(self, mock_rp, mock_can, mock_fetch):
        mock_can.return_value = True
        
        mock_fetch.side_effect = [
            '<a href="/product/1">Voir Produit</a>',
            '<h1>Fiche Produit</h1>'
        ]

        crawler = Crawler("https://web-scraping.dev", max_pages=2)
        crawler.run()

        visited = list(crawler.visited)
        self.assertEqual(visited[0], "https://web-scraping.dev")
        self.assertIn("/product/1", visited[1])

    @patch('src.crawler.fetch_html')
    @patch('src.crawler.can_fetch_url')
    @patch('src.crawler.get_robot_parser')
    def test_start_from_product(self, mock_rp, mock_can, mock_fetch):
        mock_can.return_value = True
        
        mock_fetch.return_value = """
        <html>
            <h1>Super Widget</h1>
            <p class="description">Description du widget</p>
        </html>
        """

        crawler = Crawler("https://web-scraping.dev/product/99", max_pages=1)
        results = crawler.run()

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['url'], "https://web-scraping.dev/product/99")
        self.assertEqual(results[0]['title'], "Super Widget")

if __name__ == '__main__':
    unittest.main()