# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
from opencc import OpenCC
import os

class StartingPointPipeline(object):

    def process_item(self, item, spider):
        openCCs2twp = OpenCC('s2twp')
        openCCs2tw = OpenCC('s2tw')
        self.file = codecs.open('/home/nj/graduation/crawl2/starting_point/temp/'+openCCs2tw.convert(item.get('name'))+'.txt', 'w', encoding='utf-8')
        self.file.write(openCCs2tw.convert(item.get("author"))+ "\n")
        self.file.write(item.get("novel_type")+ "\n")
        # self.file.write(openCC.convert(item.get("count"))+ "\n")
        for a in item.get("content"):
            self.file.write(openCCs2twp.convert(a)+ "\n")
        return item

    # def process_item(self, item, spider):
    #     openCCs2twp = OpenCC('s2twp')
    #     openCCs2tw = OpenCC('s2tw')

    #     novel = {   
    #                 "書名" : openCCs2tw.convert(item.get('name')),
    #                 "作者" : openCCs2tw.convert(item.get("author")),
    #                 "類別" : openCCs2twp.convert(item.get("novel_type")),
    #                 "內容" : openCCs2twp.convert(item.get("count"))
    #             }

    def spider_closed(self, spider):
        self.file.close()



class JsonPipeline(object):
    def process_item(self, item, spider):
        openCCs2twp = OpenCC('s2twp')
        openCCs2tw = OpenCC('s2tw')

        base_dir = '/home/nj/graduation/crawl2/starting_point/temp/' + openCCs2tw.convert(item.get("novel_type")) + '/'  
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)

        filename = base_dir + openCCs2tw.convert(item.get('name'))+ '.json'
        # 打開json文件，以dumps的方式存入數據
        # 注意需要有一個參數ensure_ascii=False ，不然數據會直接為utf編碼的方式存入比如
        # :“/xe15”
        content = item.get("content")
        contentTW = []
        for temp in content:
            if len(temp) < 1000:
                continue
            else:
                contentTW.append(openCCs2twp.convert(temp.replace("　","").replace(" ","").replace("\n","")))

        tag = item.get("novel_tag")
        tagList =[]
        for temp in tag:
            tagList.append(openCCs2twp.convert(temp))

        novel = {   
                    "書名" : openCCs2tw.convert(item.get('name')),
                    "作者" : openCCs2tw.convert(item.get("author")),
                    "類別" : openCCs2twp.convert(item.get("novel_type")),
                    "內容" : contentTW,
                    "標籤" : tagList
                }

        with open(filename,'w') as load_f:
            json.dump(novel, load_f, ensure_ascii=False)

        return item