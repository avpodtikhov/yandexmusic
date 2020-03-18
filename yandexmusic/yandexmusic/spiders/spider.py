# -*- coding: utf-8 -*-
import scrapy

from py2neo import Graph, Node, Relationship, NodeMatcher

class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['music.yandex.com']
    start_urls = ['https://music.yandex.com/genre/иностранный%20рэп%20и%20хип-хоп/artists?page=0']

    graph = Graph(auth=('neo4j', 'qwerty'))
    def parse(self, response):
        artists = response.xpath("//div[@class='artist']")
        for artist in artists:
            name = artist.xpath(".//div[@class='artist__name deco-typo typo-main']/@title").extract_first()
            genres = artist.xpath(".//a[@class='d-link deco-link d-link_muted deco-link_muted']/@title").getall()
            url = artist.xpath(".//a[@class='d-link deco-link']/@href").extract_first()
            yield scrapy.Request(response.urljoin(url) + '/albums', callback=self.albums, cb_kwargs=dict(name=name, genres=genres))
        url, page = response.url.split('=')
        page = int(page) + 1
        if page <= 10:
            next_page = url + '=' + str(page)
            yield scrapy.Request(next_page, callback=self.parse)

    def albums(self, response, name, genres):
        album_div = response.xpath("//div[@class='page-artist__albums']")[0]
        album_list = album_div.xpath(".//div[@class='album album_selectable']")
        for album in album_list:
            album__type = album.xpath(".//span[@class='album__type']/text()").extract_first()
            if album__type:
                feat_list = album.xpath(".//a[@class='d-link deco-link d-link_muted deco-link_muted']/@title").getall()
                for feat in feat_list:
                    if feat != name:
                        yield {'Artist name': name,
                               'Genres': genres,
                               'Feat': feat
                        }
            else:
                url = album.xpath(".//a[@class='d-link deco-link album__caption']/@href").extract_first()
                yield scrapy.Request(response.urljoin(url), callback=self.tracks, cb_kwargs=dict(name=name, genres=genres))
    
    def tracks(self, response, name, genres):
        feats_list = response.xpath("//span[@class='d-track__artists']")
        tracks_list = []
        for feat in feats_list:
            feats = feat.xpath(".//a[@class='deco-link deco-link_muted']/text()").getall()
            for f in feats:
                f = f.split(' feat. ')
                for f1 in f:
                    if f1 != name:
                        yield {'Artist name': name,
                               'Genres': genres,
                               'Feat': f1
                              }