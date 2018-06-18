import scrapy


class RestaurantsSpider(scrapy.Spider):
    name = "restaurants"

    def start_requests(self):
        with open('urls_final.csv') as f:
            urls = f.readlines()
        urls = [x.strip() for x in urls]

        # urls = [
        #     'http://www.observereducation.lk/2017/08/01/enter-the-final-year-bba-awarded-by-ipac-school-of-business-france/',
        #     "http://www.observereducation.lk/2016/11/01/anc-postgraduate-school-opens-applications-for-jan-2017-intake-revamping-cima-mba-for-global-competitiveness/"
        # ]
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

        # title = response.css('h1.entry-title::text').extract_first()
        # content = response.css('div.entry-content')[0].css('p').extract_first()
        # author = response.xpath('//div[@class="entry-meta clearfix"]/span[@class="post-author"]/span/a/text()').extract_first()
        # category = response.xpath('//div[@class="entry-meta clearfix"]/span[@class="cat-links"]/a/text()').extract_first()
        # yield {
        #     'title': title,
        #     'content': content,
        #     'author': author,
        #     'category': category
        # }
        # for quote in response.css('div.quote'):
        #     yield {
        #         'text': quote.css('h1.text::text').extract_first(),
        #         'author': quote.css('small.author::text').extract_first(),
        #         'tags': quote.css('div.tags a.tag::text').extract(),
        #     }
        # for a in response.css('li.next a'):
        #     yield response.follow(a, callback=self.parse)

