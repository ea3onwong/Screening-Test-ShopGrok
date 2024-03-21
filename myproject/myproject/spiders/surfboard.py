import scrapy
import json 

class SurfboardSpider(scrapy.Spider):
    name = "surfboard"
    allowed_domains = ["surfboardempire.com.au"]
    start_urls = ["https://www.surfboardempire.com.au/products.json?page=1"]

    def parse(self, response):
        products = json.loads(response.text)['products']

        for product in products:
            vendor = product['vendor']
            handle = product['handle']
            for variant in product['variants']: 
                yield {
                    'sku_name': variant['sku'], 
                    'product_id': variant['product_id'], 
                    'brand': vendor, 
                    'product_url': response.urljoin(f'/products/{handle}?variant={variant['id']}')
                }

        if products:
            cur_page = response.url.split('page=')[-1]
            next_page = int(cur_page)+1
            next_page_url = f"https://www.surfboardempire.com.au/products.json?page={next_page}"
            yield response.follow(next_page_url, self.parse)
            

    

