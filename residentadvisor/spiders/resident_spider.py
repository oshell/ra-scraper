import scrapy
import logging
import sys

from urllib.parse import urljoin

class ResidentSpider(scrapy.Spider):
    name = "resident"

    def start_requests(self):
        urls = [
            'https://www.residentadvisor.net/events/de/berlin/day/2018-11-21'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_event_items)

    def parse_event_items(self, response):
        events = response.css('article.event-item')

        for eventArticle in events:
            event_link = eventArticle.css('h1.event-title > a:first-child')
            event_location_link = eventArticle.css('h1.event-title > span > a:first-child')

            event =	{
              "event_name": "",
              "event_url": "",
              "location_name": "",
              "location_url": "",
              "date": "",
              "venue": "",
              "cost": "",
              "age": ""
            }

            event['event_name'] = event_link.css('::text').extract_first()
            event['event_url'] = event_link.css('::attr(href)').extract_first()
            event['location_name'] = event_location_link.css('::text').extract_first()
            event['location_url'] = event_location_link.css('::attr(href)').extract_first()
            line_up = eventArticle.css('div.event-lineup::text').extract_first()
            follow_url = urljoin(response.url, event['event_url'])
            yield scrapy.Request(follow_url, callback=self.parse_event_item, meta={'event': event})

    def parse_event_item(self, response):
        event = response.request.meta['event']
        detailContainer = response.css('aside#detail')
        event['date']  = detailContainer.css('ul li:first-child::text').extract_first()
        event['venue']  = detailContainer.css('ul li:nth-child(2)::text').extract_first()
        event['cost']  = detailContainer.css('ul li:nth-child(3)::text').extract_first()
        event['age']  = detailContainer.css('ul li:nth-child(4)::text').extract_first()
        yield event
