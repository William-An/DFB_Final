import scrapy
import json
import time
from DFB_Series_data_crawler.items import episodedata
from DFB_Series_data_crawler.items import seriesdata

class main_spider(scrapy.Spider):
    name = "main"

    def start_requests(self):
        #with open(self.list) as listFile:
        #    tvseries_list = listFile.readlines()
        #urls = ['http://www.soku.com/search_video/q_'+i.stripe() for i in tvseries_list]
        urls = [
            'http://www.soku.com/search_video/q_欢乐颂'
        ]
        print("[*] Start crawling")
        # Micro and Macro?
        for url in urls:
            yield scrapy.Request(url=url, callback=self.soku_parse)

    def soku_parse(self, response):
        link = response.xpath("/html/body/div[3]/div[3]/div/div/div/div[2]/div[1]/div[4]/div[1]/ul/li[1]/a/@href").extract_first()
        print(link)
        print("[+] Got link at soku site for:", response.xpath("/html/body/div[3]/div[3]/div/div/div/div[2]/div[1]/div[4]/div[1]/ul/li[1]/a/@_log_title").extract_first()," Link:",link)
        yield scrapy.Request(url=link,callback=self.youkulist_parse)
    def youkulist_parse(self, response):
        links = response.xpath("//*[@id='vpofficiallistv5_wrap']/div[1]/div[1]/div[1]/div/a/@href").extract()
        print("[+] Got links for TV series:",response.xpath("/html/head/title/text()").extract_first().split(" ")[0])
        print(links)
        for link in links:
            # Youku index URL
            link = "http://index.youku.com/vr_keyword/id_"+link
            yield scrapy.Request(url=link,callback=self.youkuindex_parse)
    def youkuindex_parse(self,response):
        # Index data: play times, sex ratio,..., etc.
                # 总播放量:12123,12341234
        totalplay, comments, thumpsup, thumpsdown, fav, temp= [eval("".join(i.split(":")[1].split(","))) for  i in response.xpath("//*[@id='youku']/div[1]/div/div[2]/div[1]/div/div[2]/ul/li/text()").extract()]
        raw_data = [str(i) for i in response.css("script").re(r"\[\{.*\}\]")]
        play_data = json.loads(raw_data[0])[0]
        usersratio_data = json.loads(raw_data[1])[0]
        deviceratio_data = json.loads(raw_data[3])[0]

        play_data['vv'][2].reverse()
        name = play_data['name']
        id = eval(name.split(" ")[1][1:])
        start = time.mktime(time.strptime(play_data['vv'][1], "%Y-%m-%d"))
        retri = time.mktime(time.strptime(play_data['vv'][0], "%Y-%m-%d"))
        play_times = play_data['vv'][2]
        sex_ratio = usersratio_data['sex']
        age_ratio = usersratio_data['age']
        dev_ratio = deviceratio_data['device']

        print("[+] Got data on Youku index about",response.xpath("//*[@id='baner']/div[3]/div/span/text()").extract_first())
        # Item for data
        yield episodedata(id=id,name=name,start_timestamp=start,retri_timestamp=retri,\
                          comments=comments,fav=fav,thumps_up=thumpsup,thumps_down=thumpsdown,\
                          sex_ratio=sex_ratio,age_ratio=age_ratio,total_play=totalplay,all_play=play_times)
        # Crawl from search engine, douban, and weibo
    def searchengine_parse(self,response):
        pass
    def douban_parse(self,response):
        pass
    def weibo_parese(self,response):
        pass