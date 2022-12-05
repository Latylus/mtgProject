import json
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings
import sys
sys.path.append('.\\mtgProject\\spiders\\')
import mtg_spider_deck_details as mtg_spiders

# This is a self contained way to fetch a deck without going through a command line

deck_url = "http://www.mtgtop8.com/event?e=27962&d=421767&f=MO"

def getresults(deck_url):
    results = []

    def crawler_results(signal, sender, item, response, spider):
        results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)

    process = CrawlerProcess(get_project_settings())
    process.crawl(mtg_spiders.mtg_deck_details_spider, given_url = deck_url)
    process.start()  # the script will block here until the crawling is finished
    return results

data  = getresults(deck_url)

with open("deck_to_analyse.json", 'w') as f : 
    json.dump(data, f, indent = 4)

