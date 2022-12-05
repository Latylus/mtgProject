import scrapy 
import json

class mtg_decks_spider(scrapy.Spider):
    name="mtg_decks"
    def start_requests(self):
        
        with open('archetypes.json','r') as links:
            all_data = json.load(links)
            urls = [x["link"] for x in all_data]
            # urls = links.read().split('\n')[:self.n]
            # urls = ['http://mtgtop8.com/'+deck for deck in urls]
        for url in urls:
            yield scrapy.Request(url=url, callback = self.parse, meta={'page_number': 1})

    def parse(self, response):
        current_url = response.request.url
        page_number = response.meta['page_number']
        # Get data on current page
        # xpath is different from what the web inspector gives us
        archetype_name = response.xpath("//table[@class='Stable'][1]/descendant::div[@class='w_title'][@align='center']/text()").get()
        xpath = "//table[@class='Stable'][1]/tr[@class='hover_tr']"
        
        for element in response.xpath(xpath):
            yield {
                'link' : 'http://mtgtop8.com/' + element.xpath('(./td/a[@href])[1]/@href').get(),
                'archetype_name' : archetype_name,
                'name' : element.xpath('(./td/a[@href])[1]/text()').get(),
                'rank' : element.xpath('(./td[count(*)=0])[1]/text()').get()
            }
        # Check if there is a next page
        xpath_next_button = "//div[@class = 'Nav_PN'][contains(.,'Next')]"
        # if this can't be found it means either the next is greyed out (we're already at the last page), or there is only one page
        next_button = response.xpath(xpath_next_button)
        # Go get data on next page if there is one
        if next_button:
            yield scrapy.FormRequest(url = current_url, formdata = {'current_page' : str(page_number+1)}, callback = self.parse(response), meta={'page_number': page_number+1})

          
        
