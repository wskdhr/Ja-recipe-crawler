# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from scpad.items import ScpadItem
class ScpdSpider(scrapy.Spider):
    name = "scpd"
    base_url='https://cookpad.com'
    #allowed_domains = [base_url]
    start_urls = [base_url+'/category/list'
    ]

    def parse(self,response):
        all_node=response.xpath('//div[@class="root_category_title_wrapper"]/h2//@href').extract()
        all_node2=[str(self.base_url)+str(x) for x in all_node]
        for node in all_node2:
            if node in ['https://cookpad.com/category/177',]:
                yield scrapy.Request(node,callback=self.parse_2)
                
        print(all_node2)
        
    def parse_2(self,response):
        #recipename=response.xpath('//div[@class="recipe-preview"]//a[@class="recipe-title font13 "]/text()').extract()

        recipe_node=response.xpath('//a[@class="recipe-title font13 "]/@href').extract()
        recipe_node2=[str(self.base_url)+str(x) for x in recipe_node]
        print(recipe_node2)
        for node in recipe_node2:
            yield scrapy.Request(node,callback=self.parse_3)
        
        nextpage=response.xpath('//a[@class="next_page"]/@href').extract_first()
        nextpage=str(self.base_url)+str(nextpage)
        yield scrapy.Request(nextpage,callback=self.parse_2)
       
        
    def parse_3(self,response):
        item=ScpadItem()
        ingredient=response.xpath('//div[@class="ingredient_name"]//text()').extract()
        reponumber=response.xpath('//li[@id="tsukurepo_tab"]//span[@class="count"]/text()').extract_first()
        title=response.xpath('//h1[@class="recipe-title fn clearfix"]/text()').extract_first()
        item['ingredient']=ingredient
        item['reponumber']=reponumber
        item['recipename']=title
        return item
        
