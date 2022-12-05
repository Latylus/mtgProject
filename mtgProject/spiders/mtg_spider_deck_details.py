import scrapy 
import json

class mtg_deck_details_spider(scrapy.Spider):
    name="mtg_deck_details"

    def start_requests(self):
        if self.given_url :
            yield scrapy.Request(url=self.given_url , callback=self.parse , meta={'archetype_name': ''})
        else:
            with open('deck_links.json','r') as links:
                all_data = json.load(links)
                
                for deck_data in all_data:
                    yield scrapy.Request(url=deck_data['link'], callback=self.parse , meta={'archetype_name': deck_data['archetype_name']})
    
    def parse(self, response):
        main_xpath = "//div[@class='O14'][.='SIDEBOARD']/preceding::div[starts-with(@class,'deck_line')]"
        sideboard_xpath = "//div[@class='O14'][.='SIDEBOARD']/following::div[starts-with(@class,'deck_line')]"
        deck_info_xpath = "//div[@class='event_title'][starts-with(.,'#')]/text()"

        main_card_items = response.xpath(main_xpath)
        sideboard_card_items = response.xpath(sideboard_xpath)

        deck_info = response.xpath(deck_info_xpath).get()

        yield{
            'deck_name' : deck_info.split(' ',1)[1][:-3],
            'archetype_name' : response.meta['archetype_name'],
            'deck_link': response.request.url,
            'deck_rank_at_tournament' : deck_info.split(' ',1)[0][1:],
            'cards' : [ {
                'card_name': item.xpath('./span/text()').get(),
                'count': str(int(item.xpath('./text()').get())),
                'is_sideboard':'False'
            }for item in main_card_items] +
            [ {
                'card_name': item.xpath('./span/text()').get(),
                'count': str(int(item.xpath('./text()').get())),
                'is_sideboard':'True'
            }for item in sideboard_card_items]
        }