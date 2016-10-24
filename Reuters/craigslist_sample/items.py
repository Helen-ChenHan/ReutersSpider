from scrapy.item import Item, Field

class ReutersItem(Item):
    title = Field()
    link = Field()
    article = Field()
    date = Field()
