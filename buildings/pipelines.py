# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.contrib.exporter import CsvItemExporter
from scrapy import signals

# define fields and order -- wish there was a way to order some things and have 'the rest' at the end...
fields_to_export = [
    'name',
    'lots',
    'special',
    'soft_wood',
    'hard_wood',
    'soft_iron',
    'hard_iron',
    'scrap_leather',
    'heavy_leather',
    'stone',
    'wool',
    'hemp',
    'meat',
    'vegetables',
    'common_labor',
    'uncommon_labor',
    'uncommon_labor_type',
    'Security',
    'Order',
    'Fear',
    'Finance',
    'Trade',
    'Production',
    'Hope',
    'Faith',
    'Tradition',
    'Subversion',
    'Scorn',
    'Abuse',
    'Spoil',
    'Squalor',
    'Degredation',
    'Cruelty',
    'Tragedy',
    'Atrocity',
    'Gravity',
]

class BuildingsPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('buildings.csv','w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.fields_to_export=fields_to_export
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
