import scrapy
from buildings.items import BuildingsItem
import html2text
import string

converter = html2text.HTML2Text()

class BuildingSpider(scrapy.Spider):
	name='building'
	allowed_domains=['www.thelionage.com']
	start_urls=['http://www.thelionage.com/buildings/']

	def parse(rself, response):
	    for sel in response.xpath('//div[contains(@class, "slide-meta")]'):
	    	item = BuildingsItem()
	    	item['name'] = ''
	    	item['lots'] = ''
	    	name_and_lots=sel.xpath('p[contains(@class, "title")]/text()').re(r'(.*) *\-.*Lots: ?(.*)')
	    	if not name_and_lots:
	    		print sel.xpath('p[contains(@class, "title")]/text()').extract()
	    	if len(name_and_lots) > 1:
	    		item['name'] = name_and_lots[0]
	    		item['lots'] = name_and_lots[1]

	    	desc = sel.xpath('div[contains(@class, "description")]/p')
	    	item['soft_wood'] = desc.re(r'([0-9]*) soft wood')
	    	item['hard_wood'] = desc.re(r'([0-9]*) hard wood')
	    	item['soft_iron'] = desc.re(r'([0-9]*) soft iron')
	    	item['hard_iron'] = desc.re(r'([0-9]*) hard iron')
	    	item['scrap_leather'] =desc.re(r'([0-9]*) scrap leather')
	    	item['heavy_leather'] = desc.re(r'([0-9]*) heavy leather')
	    	item['hemp'] = desc.re(r'([0-9]*) hemp')
	    	item['stone'] = desc.re(r'([0-9]*) stone')
	    	item['vegetables'] = desc.re(r'([0-9]*) vegetables')
	    	item['meat'] = desc.re(r'([0-9]*) meat')
	    	item['wool'] = desc.re(r'([0-9]*) wool')
	    	item['common_labor'] = desc.re(r'([0-9]*) common')
	    	item['uncommon_labor'] = desc.re(r'([0-9]*) uncommon')
	    	item['uncommon_labor_type'] = desc.re(r'uncommon *\((.*)\)')
	    	item['special'] = filter(lambda x: x in string.printable, converter.handle(desc.re(r'Special:(.*)')[0]))

	        deltas = ['Security','Order','Fear','Finance','Trade','Production','Hope','Faith',
	        			'Tradition','Subversion','Scorn','Abuse','Spoil','Squalor','Degredation',
	        			'Cruelty','Tragedy','Atrocity','Gravity']

	    	for vvs in deltas: # vvs = virtues and vices
	    		item[vvs] = get_first(desc.re(vvs+r' *((\-|\+)[0-9])')) 
	    	yield item

	    	#print name, lots, delta_dict
def get_first(list):
	if len(list) >0:
		return list[0]
	else: 
		return ''