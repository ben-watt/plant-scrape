import scrapy

class Crocus(scrapy.Spider):
    name = 'crocus'
    start_urls = ['https://www.crocus.co.uk/plants/_/house-plants/plcid.20/sort.7/canorder.1/']

    def parse(self, response):
        for plants in response.css('div#results div.grid4-listing'):
            yield {
                    'name': plants.xpath('.//img/@alt').extract_first(),
                    'link': plants.xpath('.//a[2]/@href').extract_first(),
                    'img' : plants.xpath('.//img/@src').extract_first(),
                    'price' : plants.xpath('.//span[@itemprop = "price"]/@content').extract_first(),
                    'potSize': plants.xpath('.//span[@class="variation-size"]/span/text()').extract_first(),
                    'height' : plants.xpath('.//span[@class="variation-size"]/span/text()').extract_first()
                }

        next_page = response.css("a.page.next-page::attr('href')").extract_first()
        yield response.follow(next_page, self.parse)