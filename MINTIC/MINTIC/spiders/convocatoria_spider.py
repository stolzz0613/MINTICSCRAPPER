import scrapy

#Titulos = //div[contains(@class, "recuadro")]//div[contains(@class, "titulo")]/a/text()
#Fechas = //div[contains(@class, "recuadro")]//div[contains(@class, "fecha")]/text()
#Link = //div[contains(@class, "recuadro")]//div[contains(@class, "titulo")]/a/href()
#Imagen = //div[contains(@class, "recuadro")]//div[contains(@class, "figure")]/img/@href

class Convocatorias(scrapy.Spider):
    name = 'convocatorias'
    start_urls = [
        'https://mintic.gov.co/portal/715/w3-multipropertyvalues-111099-198259.html'
    ]
    custom_settings = {
        'FEED_URI': 'convocatorias.json',
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUEST': 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['andres0613@utp.edu.co'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'andresB',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def getImage(self, response, **kwargs):
        title= kwargs['title']
        date= kwargs['date']
        link= kwargs['link']
        image= response.xpath('//div[contains(@class, "recuadro")]//div[contains(@class, "figure")]/img/@src').get()
        imageLink= response.urljoin(image)

        yield {
            'title': title,
            'date': date,
            'link': link,
            'image': imageLink
        }
        
    def parse(self, response):
        title= response.xpath('//div[contains(@class, "recuadro")]//div[contains(@class, "titulo")]/a/text()').getall()
        date= response.xpath('//div[contains(@class, "recuadro")]//div[contains(@class, "fecha")]/text()').getall()
        links= response.xpath('//div[contains(@class, "recuadro")]//div[contains(@class, "titulo")]/a/@href').getall()

        fullLinks= []

        for link in links:
            fullLinks.append(response.urljoin(link))

        for e in list(zip(title, date, fullLinks)):
            yield response.follow(e[2], callback=self.getImage, cb_kwargs= { 'title': e[0], 'date': e[1], 'link': e[2] })

        