from searchrunner.scrapers.common import Scraper


class ExpediaScraper(Scraper):

    provider = "Expedia"

    def load_results(self):
        self.load_fake_results(range(1, 1200))
