import itertools
import logging

import requests
from flask import Flask
from flask import jsonify

from searchrunner.aggregator import config

app = Flask(__name__)

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

def scrape(scraper):
    scrape_url = f'http://{config.SCRAPER_HOST}:9000/scrapers/{scraper}'
    app.logger.info(f'Scraping {scrape_url}')
    try:
        resp = requests.get(scrape_url, timeout=10)
        resp.raise_for_status()
        app.logger.info(resp.json().keys())
        result = resp.json()['results']
    except requests.exceptions.Timeout:
        return f'timeout scraping {scrape_url}'
    except Exception as e:
        return str(e)

    return result

@app.route('/flights/search')
def aggregate_flights():
    app.logger.info('asld;kfjasd')
    scrape_results = []
    for scraper in config.SCRAPERS:
        app.logger.info('testing')
        scrape_contents = scrape(scraper)
        if isinstance(scrape_contents, str):
            app.logger.info(scrape_contents)
        else:
            scrape_results.append(scrape_contents)

    # merge lists
    scrape_merge = []
    for scrape_result in scrape_results:
        scrape_merge = itertools.chain(scrape_merge, scrape_result)
    
    return jsonify({'results': sorted(scrape_merge, key=lambda r: r['agony'])})

