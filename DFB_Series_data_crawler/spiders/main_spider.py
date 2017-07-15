import scrapy
import json
import time
from DFB_Series_data_crawler.items import episodedata
from DFB_Series_data_crawler.items import seriesdata
from bs4 import BeautifulSoup
class micro_spider(scrapy.Spider):
    name = "micro"

    def start_requests(self):
        with open(self.list) as listFile:
            tvseries_list = listFile.readlines()
        urls = ['http://www.soku.com/search_video/q_'+i.strip() for i in tvseries_list]
        #urls = [
        #    'http://www.soku.com/search_video/q_欢乐颂'
        #]
        self.logger.info("[*] Start crawling")
        # Micro and Macro?
        for url in urls:
            yield scrapy.Request(url=url, callback=self.soku_parse)

    def soku_parse(self, response):
        link = response.xpath("/html/body/div[3]/div[3]/div/div/div/div[2]/div[1]/div[4]/div[1]/ul/li[1]/a/@href").extract_first()
        # print(link)
        self.logger.info("[+] Got link at soku site for: "+response.xpath("/html/body/div[3]/div[3]/div/div/div/div[2]/div[1]/div[4]/div[1]/ul/li[1]/a/@_log_title").extract_first()+" Link: "+link)
        yield scrapy.Request(url=link,callback=self.youkulist_parse)
    def youkulist_parse(self, response):
        links = response.xpath("//*[@id='vpofficiallistv5_wrap']/div[1]/div[1]/div[1]/div/a/@href").extract()
        self.logger.info("[+] Got links for TV series: "+response.xpath("/html/head/title/text()").extract_first().split(" ")[0])
        # print(links)
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
        id = int(name.split(" ")[1])
        start = time.mktime(time.strptime(play_data['vv'][1], "%Y-%m-%d"))
        retri = time.mktime(time.strptime(play_data['vv'][0], "%Y-%m-%d"))
        play_times = play_data['vv'][2]
        sex_ratio = usersratio_data['sex']
        age_ratio = usersratio_data['age']
        dev_ratio = deviceratio_data['device']

        self.logger.info("[+] Got data on Youku index about "+response.xpath("//*[@id='baner']/div[3]/div/span/text()").extract_first())
        # Item for data
        youkudata = episodedata(id=id,name=name,start_timestamp=start,retri_timestamp=retri,\
                          comments=comments,fav=fav,thumps_up=thumpsup,thumps_down=thumpsdown,\
                          sex_ratio=sex_ratio,age_ratio=age_ratio,total_play=totalplay,all_play=play_times)
        # douban.com/search?q=欢乐颂
        request = scrapy.Request(url="http://douban.com/search?q="+youkudata['name'].split(" ")[0],callback=self.douban_finder, dont_filter=True)   # Dont_filter allow scrapy to crawl same page for different epsiodes
        request.meta['data'] = youkudata
        self.logger.info("[*] Switching to Douban, "+youkudata['name'])
        yield request
        # Crawl from search engine, douban, and weibo
    def douban_finder(self,response):
        data = response.meta['data']
        link = response.xpath("//*[@id='content']/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/h3/a/@href").extract_first()
        request = scrapy.Request(url=link,callback=self.doubancomment_finder, dont_filter=True)
        request.meta['data'] = data
        self.logger.info("[*] Crawling link for "+data['name'])
        yield request
        # weibo_cookies = util.cookies2dict(self.weibo_cookies)
    def doubancomment_finder(self,response):
        data = response.meta['data']
        self.logger.info("[*] Crawling comments links for"+data['name'])
        link = "https://movie.douban.com/j/discussion/episode_discussions?ep_id="+response.xpath("//*[@id='content']/div[2]/div[1]/div[7]/div[2]/div[1]/a[@data-num="+str(data['id'])+"]/@data-epid").extract_first()
        request = scrapy.Request(url=link, callback=self.douban_parser)
        request.meta['data'] = data
        yield request
    def douban_parser(self,response):
        data = response.meta['data']
        self.logger.info("[*] Crawling topics and responses for "+data['name']+str(data['id']))
        comments = json.loads(response.body_as_unicode())
        data['douban_topics'] = comments['count']
        reply = sum([int(i.string) for i in BeautifulSoup(comments['html']).find_all('td',class_='reply-num') if i.string is not None])
        data['douban_responses'] = reply
        yield data
    def weibo_parese(self,response):

        pass
    def searchengine_parse(self,response):

        pass


class macro_spider(scrapy.Spider):
    pass
class util():
    @staticmethod
    def cookies2dict(self,cookies):
        cookies = cookies.split(";")
        cookies = [i.strip() for i in cookies]
        cookies = [tuple(i.split("=")) for  i in cookies]
        return dict(cookies)
