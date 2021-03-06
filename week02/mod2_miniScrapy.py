import requests
from lxml import etree
from queue import Queue
import threading
import json


class CrawlThread(threading.Thread):
    '''
    爬虫类
    '''

    def __init__(self, thread_id, queue):
        super().__init__()
        self.thread_id = thread_id
        self.queue = queue
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'referer':'https://www.zhihu.com/question/50160122',
            'cookie' :'_zap=bdb31c07-aa0d-4d78-a776-3a8fb483c128; d_c0="AJDiKy5o7g-PTvE7OO_fhrvHERcr8ipiz0I=|1566477257"; _xsrf=bVh4EowtAKuNswVUpCAHlLoPHuJlQvIv; q_c1=e1fb18e1d3d04551b169bf9b4e47ddfb|1579708032000|1566990013000; _ga=GA1.2.1127958217.1585618878; SESSIONID=es5J9WWADvyLS39JD4TwSyr4yELRVsS6r4jQfdXQcx7; JOID=UFocA0qLPcfxP-dXZ4mOVEM-57Z97kX7ugWwCy_MS7W0bdduJrqqP6w87FVv3LMi8ihBbkmZN2vbZBAs1ggpXRw=; osd=UlkTAUuJPsjzPuVUaIuPVkAx5bd_7Ur5uwezBC3NSba7b9ZsJbWoPq4_41du3rAt8ClDbUabNmnYaxIt1AsmXx0=; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1607263023,1607263093,1609602361,1609602440; capsion_ticket="2|1:0|10:1609602447|14:capsion_ticket|44:OTExNGM5OTA2YzBkNGQ2ZmE2YjhiZGVlMTJhYjg1NTI=|68e096aa4662e911baf5f147d6e9cb6d68952312d36e1b6682c56e755978639f"; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1609643600; KLBRSID=2177cbf908056c6654e972f5ddc96dc2|1609643624|1609643211'
        }

    def run(self):
        # 重写run方法
        print(f'启动线程：{self.thread_id}')
        self.scheduler()
        print(f'结束线程：{self.thread_id}')

    # 模拟任务调度
    def scheduler(self):
        while not self.queue.empty():
            # 队列为空不处理
            page = self.queue.get()
            print(f'下载线程：{self.thread_id}, 下载页面：{page}')
            url = f'https://www.zhihu.com/question/50160122'

            try:
                # downloader 下载器
                print(f'下载线程：{self.thread_id},链接知乎开始')
                response = requests.get(url, headers=self.headers)
                print(f'下载线程：{self.thread_id},获取信息完成')
                dataQueue.put(response.text)
            except Exception as e:
                print('下载出现异常', e)


class ParserThread(threading.Thread):
    '''
    页面内容分析
    '''

    def __init__(self, thread_id, queue, file):
        threading.Thread.__init__(self)      # 上面使用了super()
        self.thread_id = thread_id
        self.queue = queue
        self.file = file

    def run(self):
        print(f'启动线程：{self.thread_id}')
        while flag:                      # 这里有什么优化思路？
            try:
                item = self.queue.get(False)  # 参数为false时队列为空，抛出异常
                if not item:                 
                    continue
                self.parse_data(item)
                self.queue.task_done()  # get之后检测是否会阻塞
            except Exception as e:
                pass
        print(f'结束线程：{self.thread_id}')

    def parse_data(self, item):
        '''
        解析网页内容的函数
        :param item:
        :return:
        '''
        try:
            html = etree.HTML(item)
            books = html.xpath('//div[@class="List-item"]')
            for book in books:
                try:
                    title = book.xpath('./div[@class="ContentItem AnswerItem"]/@data-zop')
                    answer = book.xpath('.//span[@class="RichText ztext CopyrightRichText-richText"]//text()')
                    response = {
                        'title': title,
                        'answer': answer
                    }
                    # 解析方法和scrapy相同，再构造一个json
                    json.dump(response, fp=self.file, ensure_ascii=False)
                except Exception as e:
                    print('book error', e)

        except Exception as e:
            print('page error', e)


if __name__ == '__main__':

    # 定义存放网页的任务队列
    pageQueue = Queue(1)
    for page in range(0, 1):
        pageQueue.put(page)

    # 定义存放解析数据的任务队列
    dataQueue = Queue()



    # 爬虫线程
    crawl_threads = []
    crawl_name_list = ['crawl_1']
    for thread_id in crawl_name_list:
        thread = CrawlThread(thread_id, pageQueue)
        thread.start()
        crawl_threads.append(thread)

    # 将结果保存到一个json文件中
    with open('book.json', 'a', encoding='utf-8') as pipeline_f:

        # 解析线程
        parse_thread = []
        parser_name_list = ['parse_1']
        flag = True
        for thread_id in parser_name_list:
            thread = ParserThread(thread_id, dataQueue, pipeline_f)
            thread.start()
            parse_thread.append(thread)

        # 结束crawl线程
        for t in crawl_threads:
            t.join()

        # 结束parse线程
        flag = False
        for t in parse_thread:
            t.join()

    print('退出主线程')
