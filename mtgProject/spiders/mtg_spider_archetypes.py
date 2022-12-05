import scrapy 

target_urls = ['http://mtgtop8.com/format?f=MO&meta=163']

class mtg_archetypes_spider(scrapy.Spider):
    name="mtg_archetypes"
    
    def start_requests(self):
        urls = target_urls
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        xpath = "//a[starts-with(@href,'archetype')]"
        item = response.xpath(xpath)
        for arch in item.getall():
            yield{
                'link' : 'http://mtgtop8.com/' + arch.split("\"")[1].replace("&amp;", "&"),
                'name' : arch.split("\"")[2][1:-4],
            }
