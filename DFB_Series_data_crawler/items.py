# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class episodedata(scrapy.Item):
    # Micro
    id = scrapy.Field()                 # ID for SQL
    name = scrapy.Field()               # episode name
    start_timestamp = scrapy.Field()    # The day(in UNIX timestamp) which this episode first played
    retri_timestamp = scrapy.Field()    # The day(in UNIX timestamp) which the data retrieved
    comments = scrapy.Field()           # Number of comments
    fav = scrapy.Field()                # Number of people who "like" it
    thumps_up = scrapy.Field()          # Number of thumpsup
    thumps_down = scrapy.Field()        # Number of thumpsdown
    sex_ratio = scrapy.Field()          # Sex ratio of people who watch this episode, in list form
    age_ratio = scrapy.Field()          # Same as sex ratio
    dev_ratio = scrapy.Field()
    total_play = scrapy.Field()         # Total play times
    all_play = scrapy.Field()           # A list that contains everyday's play amount of this episode
    douban_topics = scrapy.Field()      # The number of topics of this episode
    douban_responses = scrapy.Field()   # The number of responses under all topics of this episode
    # TODO Weibo & Douban
class seriesdata(scrapy.Item):
    # Macro
    douban_rate = scrapy.Field()
    douban_rateamount = scrapy.Field()
    douban_rateratio = scrapy.Field()
    douban_collections = scrapy.Field()
    douban_wishes = scrapy.Field()
    douban_doing = scrapy.Field()
    name = scrapy.Field()               # episode name
    start_timestamp = scrapy.Field()    # The day(in UNIX timestamp) which this episode first played
    retri_timestamp = scrapy.Field()    # The day(in UNIX timestamp) which the data retrieved
    sex_ratio = scrapy.Field()          # Sex ratio of people who watch this episode, in list form
    age_ratio = scrapy.Field()          # Same as sex ratio
    dev_ratio = scrapy.Field()
    all_play = scrapy.Field()           # A list that contains everyday's play amount of this episode
    baidu_search = scrapy.Field()
    # TODO more macro vars
    pass
