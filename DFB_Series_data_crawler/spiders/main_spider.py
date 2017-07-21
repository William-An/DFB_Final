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
                          sex_ratio=sex_ratio,age_ratio=age_ratio,dev_ratio=dev_ratio,total_play=totalplay,all_play=play_times)
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
        link = "https://movie.douban.com/j/discussion/episode_discussions?ep_id="+response.xpath('//div[@class="mod"]/div[@class="bd"]/div[1]/a[@data-num='+str(data['id'])+']/@data-epid').extract_first()
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
    name = "macro"
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
        link = "http://index.youku.com/vr_keyword/id_"+link # Get link to youku index
        self.logger.info("[+] Got link at soku site for: "+response.xpath("/html/body/div[3]/div[3]/div/div/div/div[2]/div[1]/div[4]/div[1]/ul/li[1]/a/@_log_title").extract_first()+" Link: "+link)
        yield scrapy.Request(url=link,callback=self.youkuindex_referer)
    def youkuindex_referer(self, response): # Refer to TV Series page instead of just episode page
        link = response.xpath("//*[@id=\"baner\"]/div[3]/div/div/a[3]/@href").extract_first()
        self.logger.info("[+] Got links for TV series: "+response.xpath('//*[@id="baner"]/div[3]/div/span/text()').extract_first().split(" ")[0])
        yield scrapy.Request(url=link,callback=self.youkuindex_parse)
    def youkuindex_parse(self,response):
        raw_data = [str(i) for i in response.css("script").re(r"\[\{.*\}\]")]
        play_data = json.loads(raw_data[1])[0]
        usersratio_data = json.loads(raw_data[2])[0]
        deviceratio_data = json.loads(raw_data[4])[0]

        play_data['vv'][2].reverse()
        name = play_data['name'].split(" ")[0]
        start = time.mktime(time.strptime(play_data['vv'][1], "%Y-%m-%d"))
        retri = time.mktime(time.strptime(play_data['vv'][0], "%Y-%m-%d"))
        play_times = play_data['vv'][2]
        sex_ratio = usersratio_data['sex']
        age_ratio = usersratio_data['age']
        dev_ratio = deviceratio_data['device']

        self.logger.info("[+] Got data on Youku index about "+response.xpath('//*[@id="add_shows_name"]/text()').extract_first())
        # Item for data
        youkudata = seriesdata(name=name,start_timestamp=start,retri_timestamp=retri,\
                                sex_ratio=sex_ratio,age_ratio=age_ratio,dev_ratio=dev_ratio,\
                                all_play=play_times)
        # douban.com/search?q=欢乐颂
        request = scrapy.Request(url="http://douban.com/search?q="+youkudata['name'],callback=self.douban_finder, dont_filter=True)   # Dont_filter allow scrapy to crawl same page for different epsiodes
        request.meta['data'] = youkudata
        self.logger.info("[*] Switching to Douban, "+youkudata['name'])
        yield request
        # Crawl from search engine, douban, and weibo
    def douban_finder(self,response):
        data = response.meta['data']
        link = response.xpath("//div[@class='content'][1]/div/h3/a/@href").extract_first()
        try:
            request = scrapy.Request(url=link,callback=self.douban_rateparser, dont_filter=True)
        except TypeError as err:
            self.logger.error("Error at "+data['name'])
            self.logger.error(str(err))
            self.logger.error(str(data))
        request.meta['data'] = data
        self.logger.info("[*] Crawling link for "+data['name'])
        yield request
        # weibo_cookies = util.cookies2dict(self.weibo_cookies)
    def douban_rateparser(self,response):
        data = response.meta['data']
        self.logger.info("[*] Crawling data from Douban for "+data['name'])
        data['douban_rateratio'] = response.xpath('//*[@id="interest_sectl"]/div/div[3]/div/span[@class="rating_per"]/text()').extract()
        data['douban_rate'] = response.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()').extract_first()
        data['douban_rateamount'] = response.xpath('//*[@id="interest_sectl"]/div/div[2]/div/div[2]/a/span/text()').extract_first()
        request = scrapy.Request(url=response.url+"collections",callback=self.douban_collectionparser)
        request.meta['data'] = data
        yield request
    def douban_collectionparser(self,response):
        data = response.meta['data']
        self.logger.info("[*] Crawling the amount of collections, wishes, and doing of "+data['name'])
        data['douban_collections'] = response.xpath('//*[@id="collections_bar"]/span/text()').extract_first()
        data['douban_wishes'] = response.xpath('//*[@id="wishes_bar"]/span/a/text()').extract_first()
        data['douban_doing'] = response.xpath('//*[@id="doings_bar"]/span/a/text()').extract_first()
        #data['baidu_search'] = [0 for i in range(((data['retri_timestamp'])-(data['start_timestamp']))/86400+1)]  #[0...0]

        request = scrapy.Request(url="https://www.baidu.com/s?wd="+data['name']+"&gpc=stf="+str(data['start_timestamp'])+","+str(data['start_timestamp'])+"|stftype=2",callback=self.baidu_engine)
        request.meta['data'] = data
        request.meta['next_stamp'] = data['start_timestamp']+86400
        yield request
        print("special tag")
    def baidu_engine(self,response):
        data = response.meta['data']
        next = response.meta['next_stamp']
        if abs(data['retri_timestamp']-next) < 100:
            # Reach the end
            self.logger.info("[+] Crawled baidu search result for "+data['name'])
            yield data
        data['baidu_search'].append(util.filterChinese(response.xpath('//div[@class="nums"]/text()').extract_first()))
        request = scrapy.Request(url="https://www.baidu.com/s?wd="+data['name']+"&gpc=stf="+str(next)+","+str(next)+"|stftype=2",callback=self.baidu_engine)
        request.meta['data'] = data
        request.meta['next_stamp'] = next+86400
        yield request

class util():
    @staticmethod
    def cookies2dict(self,cookies):
        cookies = cookies.split(";")
        cookies = [i.strip() for i in cookies]
        cookies = [tuple(i.split("=")) for  i in cookies]
        return dict(cookies)
    @staticmethod
    def filterChinese(string):
        result = ""
        for i in string:
            if i.isdecimal():
                result+=i
        if result is not "":
            return eval(result)
        else:
            return 0
