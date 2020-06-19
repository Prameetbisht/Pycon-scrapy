import scrapy
from scrapy.http import Request


class QuotesSpider(scrapy.Spider):
    name = 'pycon'
    start_urls = [
        'https://in.pycon.org/cfp/2016/proposals/']
    proj_name1 = []

    def parse(self, response):
        data = []
        text = response.css('span[class=align-middle]').extract()
        title = response.xpath('//div[@class="col-sm-11 col-xs-12"]/h3[@class="proposal--title"]//@href').extract()
        # links = response.xpath('h3.proposal--title::text a::attr(href)').getall()
        # 'tags': quote.css('div.tags a.tag::text').getall()
        for i in title:
            data.append(str('https://in.pycon.org') + i)

        # print(data)
        # return data
        for links in data:
            yield Request(url=links, callback=self.proj)

    def proj(self, response):
        title = response.xpath('//h1[@class="proposal-title"]//text()').extract()[0].strip()
        author = response.xpath('/html/body/div[2]/div/div/div/div/div[1]/div/p/small/b[1]/text()').extract()[0].strip()
        date = response.xpath('/html/body/div[2]/div/div/div/div/div[1]/div/p/small/b[2]/time/text()').extract()[
            0].strip()
        section = response.xpath('/html/body/div[2]/div/div/div/div/div[2]/section[2]/table//text()').extract()[4]
        types = response.xpath('/html/body/div[2]/div/div/div/div/div[2]/section[2]/table//text()').extract()[10]
        target = response.xpath('/html/body/div[2]/div/div/div/div/div[2]/section[2]/table//text()').extract()[
            16].replace("\n", "").replace(" ", "")
        last_u = response.xpath('/html/body/div[2]/div/div/div/div/div[2]/section[2]/table//text()').extract()[23]
        votes = response.xpath('/html/body/div[2]/div/div/div/div/div[2]/div/div/h1//text()').extract()[0].replace("\n",
                                                                                                                   "").replace(
            " ", "")
        if votes is not None:

            des = response.xpath('/html/body/div[2]/div/div/div/div/div[2]/section[1]/div[1]//text()').extract()[3::]
            des2 = [sub.replace("\n","").replace("'',", "") for sub in des]
            pre = response.xpath('/html/body/div[2]/div/div/div/div/div[2]/section[1]/div[2]//text()').extract()[3::]
            pre2 = [sub.replace("\n", "").replace("'',", "") for sub in pre]
            d_url = response.xpath('/html/body/div[2]/div/div/div/div/div[2]/section[1]/div[3]//text()').extract()[2::]
            d_url2 = [sub.replace("\n", "").replace("'',", "") for sub in d_url]
            sp_info = response.xpath('/html/body/div[2]/div/div/div/div/div[2]/section[1]/div[4]//text()').extract()[3::]
            sp_info2 = [sub.replace("\n", "").replace("''", "") for sub in sp_info]
            sp_links = response.xpath('/html/body/div[2]/div/div/div/div/div[2]/section[1]/div[5]//text()').extract()[3::]
            sp_links2 = [sub.replace("\n", "").replace("'',", "") for sub in sp_links]

            if des and pre and d_url is not None:
                yield {
                    'Title': title,
                    'Author': author,
                    'Publish Date': date,
                    'url': response.url,
                    'Target Audience': target,
                    'Types': types,
                    'Section': section,
                    'Last Updated': last_u,
                    'Vote Count': votes,
                    'Description': des2,
                    'Prerequsite': pre2,
                    'URL': d_url2,
                    'Speaker Info': sp_info2,
                    'Speakers Links': sp_links2

                }
            else:
                print("NA")
        else:
            print("NA")
