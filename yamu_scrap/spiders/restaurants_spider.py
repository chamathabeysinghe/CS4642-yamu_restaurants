import scrapy


class RestaurantsSpider(scrapy.Spider):
    name = "restaurants"

    def start_requests(self):
        with open('urls_final.csv') as f:
            urls = f.readlines()
        urls = [x.strip() for x in urls]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if 'https://www.yamu.lk/place/restaurants?page=' in response.url :
            # listing page
            links = response.xpath('//ul[@class="media-list search-results"]/div[@class="row"]/a/@href').extract()
            for link in links:
                yield scrapy.Request(link, callback=self.parse)
        else:
            # restaurant page
            title = response.xpath('//div[@class="place-title-box"]/h2/text()').extract_first()
            telephone = response.xpath('//ul[@class="place-title-list list-inline"]/li/a/text()').extract_first()
            address = response.xpath('//div[@class="place-title-box"]/p/text()').extract_first()
            summary = response.xpath('//div[@class="place-title-box"]/p[@class="excerpt"]/text()').extract_first()
            author = response.xpath('//div[@class="author-byline"]/div[@class="media"]/div/div/a/span/text()').extract_first()
            cuisine = response.xpath('//p[text()="Cuisine"]/following::p[1]/a/text()').extract()
            price = response.xpath('//p[text()="Price Range"]/following::p[1]/a/text()').extract()
            dish = response.xpath('//p[text()="Dish Types"]/following::p[1]/a/text()').extract()
            overall = response.xpath('//dt/a[text()="Overall Rating"]/following::dd[1]/span/text()').extract_first()
            quality = response.xpath('//dt/a[text()="Quality Rating"]/following::dd[1]/span/text()').extract_first()
            service = response.xpath('//dt/a[text()="Service Rating"]/following::dd[1]/span/text()').extract_first()
            ambience = response.xpath('//dt/a[text()="Ambience Rating"]/following::dd[1]/span/text()').extract_first()
            yield {
                'title': title,
                'telephone':telephone,
                'address':address,
                'summary':summary,
                'author':author,
                'cuisine':cuisine,
                'price':price,
                'dish':dish,
                'overall':overall,
                'quality':quality,
                'service':service,
                'ambience':ambience
            }


