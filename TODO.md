Soku: www.soku.com/search_video/q_XXX
每一部的第一集的XPATH: /html/body/div[3]/div[3]/div/div/div/div[2]/div[1]/div[4]/div[1]/ul/li[1]/a
/html/body/div[3]/div[3]/div/div/div/div[2]/div[1]/div[4]/div[1]/ul/li[1]/a/@href
点击去每一集的XPATH: //*[@id='vpofficiallistv5_wrap']/div[1]/div[1]/div[1]/div/a/@href


Youku index的JS中有所有的数据:
    var youkuData = eval('('+'[{"vv":["2017-07-09","2017-06-14",["898510","944523","924139","935174","942226","988633","730631","1193103","1255796","1265448","1289824","1299355","1381871","1374666","1677538","1819157","1921469","2020209","2228680","2577146","2906672","3984297","5538911","8886569","22523406","151258"]],"name":"楚乔传 13"}]'+')');
    data2 = eval('('+'[{"sex":["39.7","60.3"],"age":["2.7","65.9","22.2","9.2"],"occupation":["10.8","45.2","22.0","22.1"],"edu":["7.6","64.6","21.8","4.7","1.2"],"name":"楚乔传 13"}]'+')');
用re甄别:
fetch("http://index.youku.com/vr_keyword/id_http://v.youku.com/v_show/id_XMTUzOTM5MjAxNg==.html",response)
data=[str(i) for i in response.css("script").re(r"\[\{.*\}\]")]
直接JSON输出
jsobj=json.loads(data[0])[0]
jsb = json.loads(data[1])[0]

异步传输Search engine and weibo, douban， Item pipeline

WEIBO
用cookies绕过验证
