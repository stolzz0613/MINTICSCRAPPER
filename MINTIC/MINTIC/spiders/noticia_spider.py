import scrapy

#Titulos = //div[contains(@class, "recuadro")]//div[contains(@class, "titulo")]/a/text()
#Fechas = //div[contains(@class, "recuadro")]//div[contains(@class, "fecha")]/text()
#Link = //div[contains(@class, "recuadro")]//div[contains(@class, "titulo")]/a/href()
#Imagen = //div[contains(@class, "recuadro")]//div[contains(@class, "figure")]/img/@href

class Noticias(scrapy.Spider):
    name = 'news'
    start_urls = [
        'https://mintic.gov.co/portal/715/w3-multipropertyvalues-111101-198259.html'
    ]
    custom_settings = {
        'FEED_URI': 'noticias.json',
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUEST': 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['andres0613@utp.edu.co'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'andresB',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        title= response.xpath('//div[contains(@class, "recuadro")]//div[contains(@class, "titulo")]/a/text()').getall()
        date= response.xpath('//div[contains(@class, "recuadro")]//div[contains(@class, "fecha")]/text()').getall()
        links= response.xpath('//div[contains(@class, "recuadro")]//div[contains(@class, "titulo")]/a/@href').getall()
        images= response.xpath('//div[contains(@class, "recuadro")]//div[contains(@class, "figure")]/img/@src').getall()

        fullLinks= []
        fullImages= []

        for link in links:
            fullLinks.append(response.urljoin(link))
        for image in images:
            fullImages.append(response.urljoin(image))

        res = []
        for e in list(zip(title, fullImages, date, fullLinks)):
            res.append(
                {
                    'title': e[0],
                    'image': e[1],
                    'date': e[2],
                    'link': e[3]
                }
            )
        yield { 'news': res }
