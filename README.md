# 爬取起點中文網已完本小說所有類別的書名，並統計數量

用以練習scrapy爬蟲框架

+ items.py：定義要爬取目標的數據結構
+ middlewares.py：暫時沒用到
+ pipelines.py：對爬完的資料進行後續處理，簡單過濾、調整格式、存檔路徑等
+ settings.py：設定爬蟲的全局設置，如CONCURRENT_REQUESTS同時發送request的數量
+ spiders：目錄下有爬蟲主體的python檔案

## 執行

	scrapy crawl st #st為crawler.py裡面設置的名稱