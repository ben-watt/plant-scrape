import scrapy

class FlorAccess(scrapy.Spider):
    name = 'florAccess'
    start_urls = ['https://www.floraccess.com/en/category/35/indoor-plants/']
    next_page = 1
    last_page = 56
    page_param = "?p="

    def parse(self, response):
        for plant in response.css('div#FlorAccess  div > ul > li'):
            plant_page_link = plant.css('a::attr("href")').extract_first()
            plant_page_request = response.follow(plant_page_link, callback=self.parse_plant_page)
            plant_page_request.meta['plant'] = {
                    'name': plant.css('img::attr("alt")').extract_first(),
                    'link': plant_page_link,
                    'img' : plant.css('img::attr("src")').extract_first(),
                    'price' : plant.css('span::text').extract_first(),
                    'potSize': plant.xpath('(.//span[contains(.,"cm")]/text())[1]').extract_first(),
                    'height' : plant.xpath('(.//span[contains(.,"cm")]/text())[4]').extract_first()
                }
            
            yield plant_page_request

        if self.next_page != self.last_page:
            self.next_page += 1
            next_url = '{}{}{}'.format(self.start_urls[0], self.page_param, self.next_page)
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_plant_page(self, response):
        plant = response.meta['plant']
        yield {
            **plant,
            'per_layer' : response.xpath('//div[contains(normalize-space(text()),"Products per layer")]/following::span/div/text()').extract_first(),
            'per_trolley': response.xpath('//div[contains(normalize-space(text()),"Layers per trolley")]/following::span/div/text()').extract_first()
        }