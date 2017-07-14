# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class episodedata(scrapy.Item):
    # Micro
    id = scrapy.Field()             # ID for SQL
    name = scrapy.Field()           # episode name
    start_timestamp = scrapy.Field()# The day(in UNIX timestamp) which this episode first played
    retri_timestamp = scrapy.Field() # The day(in UNIX timestamp) which the data retrieved
    comments = scrapy.Field()       # Number of comments
    fav = scrapy.Field()            # Number of people who "like" it
    thumps_up = scrapy.Field()      # Number of thumpsup
    thumps_down = scrapy.Field()    # Number of thumpsdown
    sex_ratio = scrapy.Field()      # Sex ratio of people who watch this episode, in list form
    age_ratio = scrapy.Field()      # Same as sex ratio
    total_play = scrapy.Field()     # Total play times
    all_play = scrapy.Field()       # A list that contains everyday's play amount of this episode
    # TODO Weibo & Douban
class seriesdata(scrapy.Item):
    # Macro
    pass
