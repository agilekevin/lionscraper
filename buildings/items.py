# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class BuildingsItem(scrapy.Item):
    # allow any values.
	def __setitem__(self, key, value):
	        self._values[key] = value
	        self.fields[key] = {}