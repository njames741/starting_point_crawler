# -*- coding: utf8 -*-
import scrapy
from bs4 import BeautifulSoup
from starting_point.items import StartingPointItem
from opencc import OpenCC

class STCrawler(scrapy.Spider):
    name = 'st'
    # start_urls = ['https://www.qidian.com/finish?action=hidden&orderId=&sign=1&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=2&page=1']
    start_urls = ['https://www.qidian.com/finish?action=hidden&orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=2&page='
                    +str(page) for page in range(1,2457)]

    # https://www.qidian.com/finish?action=hidden&orderId=&sign=1&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=2&page=1
    # https://www.qidian.com/finish?action=hidden&orderId=&sign=1&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=2&page=
    # 所有簽約作品完本共586頁11705本
    # https://www.qidian.com/finish?action=hidden&orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=2&page=
    # 所有完本共2457頁49139本

    

    def parse(self, response):
        res = BeautifulSoup(response.body, 'html.parser')
        for novel in res.select('.book-mid-info'):
            # print(novel.select('h4')[0].text)
            # print(novel.select('a')[0]['href'])
            domain = 'https:'
            yield scrapy.Request(domain + novel.select('a')[0]['href'], self.parse_book)

    def parse_book(self, response):
        res = BeautifulSoup(response.body, 'html.parser')
        stItem = StartingPointItem()
        # print(res.select('.book-intro')[0].text)
        # print(res.select('h1 > em')[0].text)
        # print(res.select('a[class="red-btn J-getJumpUrl "]')[0]['href'])

        # print(res.select('#J-catalogCount')[0].text)
        wordCount = float(res.select('.book-info')[0].select('em')[1].text)
        unit = res.select('.book-info')[0].select('cite')[0].text
        # print(wordCount)
        # print(unit)
        stItem['name'] = res.select('.book-info')[0].select('em')[0].text
        # print(res.select('.book-info')[0].select('em')[0].text)
        stItem['author'] = res.select('.book-info')[0].select('.writer')[0].text
        stItem['novel_type'] = res.select('.tag')[0].select('.red')[0].text
        
        tagList = []
        for temp in res.select('.tag-wrap')[0].select('.tags'):
            tagList.append(temp.text) 
        stItem['novel_tag'] = tagList

        # stItem['count'] = res.select('#J-catalogCount')[0].text
        domain = 'https:'
        if wordCount > 30 and unit == '万字':
            yield scrapy.Request(domain + res.select('a[class="red-btn J-getJumpUrl "]')[0]['href'], self.parse_charter, meta={'item': stItem})
        else:
            pass        

    def parse_charter(self, response):
        res = BeautifulSoup(response.body, 'html.parser')
        stItem = response.meta['item']

        # stItem['name'] = res.select('#j_textWrap > div > div > h1')[0].text
        # stItem['author'] = res.select('#j_textWrap > div > div > h2 > a')[0].text
        # print(res.select('.j_chapterName')[0].text)

        # return stItem

        cname = res.select('.j_chapterName')[0].text
        charterContent = res.select('.read-content')[0].text
        


        content = stItem.get('content')
        if content == None:
            stItem['content'] = [charterContent]
        else:
            content.append(charterContent)
            stItem['content'] = content

        chapterCount = stItem.get('count')
        if chapterCount == None:
            stItem['count'] = 1
        else:
            stItem['count'] = chapterCount+1
        # print(stItem.get('name'))
        nextUrl = 'https:'+res.select('#j_chapterNext')[0]['href']
        if stItem.get('count') == 130:
            yield stItem
        else:
            yield scrapy.Request(nextUrl, self.parse_charter, meta={'item': stItem})

        

        # yield scrapy.Request(nextUrl, self.parse_charter, meta={'item': stItem})
