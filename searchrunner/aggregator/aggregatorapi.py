import itertools
import logging
import time
from multiprocessing.dummy import Pool as ThreadPool 

import requests
from flask import Flask
from flask import jsonify

import config

app = Flask(__name__)

# In a small API I'd keep the helper functions close for ease of use,
# once it grows you can move them to separate helper files.

############ Helper Functions ############
def scrape(scraper):
    scrape_url = f'http://{config.SCRAPER_HOST}:9000/scrapers/{scraper}'
    app.logger.info(f'Scraping {scrape_url}')
    try:
        resp = requests.get(scrape_url, timeout=10)
        resp.raise_for_status()
        result = resp.json()['results']
    except requests.exceptions.Timeout:
        return f'timeout scraping {scrape_url}'
    except Exception as e:
        return str(e)

    return result

# python sort takes advantage of already sorted subsections
def merge(merge_lists):
    merge_results = []
    for merge_list in merge_lists:
        merge_results = itertools.chain(merge_results, merge_list)
    
    return sorted(merge_results, key=lambda r: r['agony'])

############ API Handlers ############
@app.route('/flights/search')
def aggregate_flights():
    pool = ThreadPool(len(config.SCRAPERS)) 

    # scrape each scraper in its own thread
    start_time = time.time()
    scrape_results = pool.map(scrape, config.SCRAPERS)

    # close the pool and wait for the work to finish 
    pool.close()
    pool.join()
    app.logger.info(f"Took {time.time() - start_time} seconds to scrape all results")

    # handle scraping errors 
    # (currently just log and ignore scrapers that errored, could add retry functionality)
    for idx, scrape_result in enumerate(scrape_results):
        if isinstance(scrape_result, str):
            app.logger.error(scrape_result)
            del scrape_result[idx]

    # merge lists 
    start_time = time.time()
    merge_results = {'results': merge(scrape_results)}
    app.logger.info(f"Took {time.time() - start_time} seconds to merge lists")

    return jsonify(merge_results)


# if running with gunicorn, rather than the debug server
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

