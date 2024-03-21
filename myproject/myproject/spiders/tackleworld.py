import scrapy


class TackleworldSpider(scrapy.Spider):
    name = 'tackleworld'
    allowed_domains = ['tackleworldadelaide.com.au']
    start_urls = ['https://tackleworldadelaide.com.au/']

    def parse(self, response):
        top_menus = response.xpath("//ul[contains(@class, 'navPages-list--categories')]/li[contains(@class, 'navPages-item')]")
        for top_menu in top_menus: 
            top_menu_url = top_menu.xpath(".//a[contains(@class, 'navPages-action')]/@href").get()
            submenu_items = top_menu.xpath(".//ul[contains(@class, 'navPage-subMenu-list')]//li/a")
            if submenu_items: 
                for submenu_item in submenu_items:
                    submenu_url = submenu_item.xpath("./@href").get()
                    yield response.follow(submenu_url, self.parse_category) 
            else: 
                yield response.follow(top_menu_url, self.parse_category)

    def parse_category(self, response): 
        product_tiles = response.xpath("//ul[@class='productGrid']//div[contains(@class, 'card__buttons')]")
        for product in product_tiles: 
            product_url = product.xpath("./a[contains(@class, 'card__button')]/@href").get()
            yield response.follow(product_url, self.parse_product)

        next_page_url = response.xpath("//nav[@class='pagination']//li[contains(@class, 'pagination__item--next')]/a/@href").get()
        if next_page_url: 
            yield response.follow(next_page_url, self.parse_category)

    def parse_product(self, response): 
        product_info = response.xpath("//div[@class='productView__wrapper']")
        yield {
            'sku_name': product_info.xpath(".//dd[@class='productView-info-value']/text()").get(),
            'image_url': product_info.xpath(".//section[@class='productView__images']//a/@href").get(),
            'price_now': product_info.xpath(".//div[@class='productView-price']//span[@class='price']/text()").get(),
            'price_was': product_info.xpath(".//div[@class='productView-price']//span[contains(@class, 'price--rrp')]/text()").get(),
            'product_url': response.url
        }
       

        




                
          




    

    