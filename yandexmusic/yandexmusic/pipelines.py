# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from py2neo import Graph, Node, Relationship, NodeMatcher

class YandexmusicPipeline(object):
    # graph = Graph(auth=('neo4j', 'qwerty'))
    def process_item(self, item, spider):
        matcher = NodeMatcher(spider.graph)
        a = Node("Artist", name=item['Artist name'])
        spider.graph.merge(a,"Artist","name")
        for g in item['Genres']:
            a[g] = 1
        spider.graph.push(a)
        b = Node("Artist", name=item['Feat'])
        b1 = matcher.match("Artist", name=item['Feat']).first()
        if not b1:
            spider.graph.merge(b,"Artist","name")
            spider.graph.push(b)
        else:
            b = b1
        ab = Relationship(a, 'FEAT', b)
        rel = spider.graph.match((a, b), r_type="FEAT").first()
        spider.graph.merge(ab)
        if rel:
            ab['Count'] = rel['Count'] + 1
        else:
            ab['Count'] = 1
        spider.graph.push(ab)
        return item