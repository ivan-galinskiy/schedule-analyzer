# Scrapy settings for ciencias project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'ciencias'

SPIDER_MODULES = ['ciencias.spiders']
NEWSPIDER_MODULE = 'ciencias.spiders'

ITEM_PIPELINES = [
'ciencias.pipelines.CienciasPipeline',
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ciencias (+http://www.yourdomain.com)'
