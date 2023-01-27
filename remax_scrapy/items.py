# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RemaxScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    first_name = scrapy.Field()
    middle_name = scrapy.Field()
    last_name = scrapy.Field()
    office_name = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zipcode = scrapy.Field()
    image_url = scrapy.Field()
    country = scrapy.Field()
    title = scrapy.Field()
    email = scrapy.Field()
    profile_url = scrapy.Field()
    website = scrapy.Field()
    office_phone_numbers = scrapy.Field()
    agent_phone_numbers = scrapy.Field()
    social = scrapy.Field()
    description = scrapy.Field()
    languages = scrapy.Field()
