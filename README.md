This is a fork of https://github.com/StrikingLoo/mtgProject .
This project fetches and saves the complete dataset for a given meta from mtgtop8 as the original project was incomplete.
The saved data can also be saved in json format for ease of use.

Although the data is directly available here for the 2018 modern metagame (https://mtgtop8.com/format?f=MO&meta=163&a=), you can also fetch it yourself, or even fetch other metagames with the following process:

- set the metagame link(s) in the `/mtgProject/spiders/mtg_spider_archetypes.py` file
- run the following command in the `/mtgProject` directory : `scrapy crawl mtg_archetypes -O archetypes.json`
- run the following command in the `/mtgProject` directory : `scrapy crawl mtg_decks -O deck_links.json`
- run the following command in the `/mtgProject` directory : `scrapy crawl mtg_deck_details -O all_decks.json`

The `-O` at the end of these commands is a parameter to save the result to the indicated json. You might want to save it to another file but if you do, you will have to update the following spiders to open the right file as inputs.
