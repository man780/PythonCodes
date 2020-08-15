import logging
import requests
import bs4
import collections
import csv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('wb')

ParseResult = collections.namedtuple(
    'ParseResult',
    (
        'name',
        'price',
        'url',
    )
)

HEADERS = (
    'Имя товара',
    'Цена',
    'Ссылка'
)


class SitesParser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
            'Accept-Language': 'ru',
        }
        self.result = []

    def load_page(self):
        url = 'https://ikarvon.uz/product-category/elektrika-i-svet/rozetki-i-vykljuchateli/'
        res = self.session.get(url=url)
        res.raise_for_status()
        return res.text

    def parse_list_page(self, text: str):
        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.select('li.product')
        for block in container:
            self.parse_block(block=block)

    def parse_block(self, block):
        urlBlock = block.select_one('a')
        if not urlBlock:
            logger.error('Url not found')
            return
        url = urlBlock.get('href')
        if not url:
            logger.error('Url href not found')
            return

        nameBlock = block.select_one('h2 a')
        if not nameBlock:
            logger.error(f'Name block not found on {url}')
        name = nameBlock.text

        price = block.select_one('span.price span.amount').text
        if not price:
            logger.error(f'Price block not found on {url}')
        price = price.replace(' сум', '')
        price = price.replace(',', '')
        price = int(price)

        logger.debug('%s, %s, %s', url, name, price)
        logger.debug('=' * 100)

        self.result.append(ParseResult(
            url=url,
            name=name,
            price=price
        ))

    def save_result(self):
        path = 'export/products.csv'
        with open(path, 'w') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(HEADERS)
            for product in self.result:
                writer.writerow(product)

    def run(self):
        text = self.load_page()
        self.parse_list_page(text=text)
        self.save_result()
        logger.info(f'Получили {len(self.result)} элементов')


if __name__ == '__main__':
    parser = SitesParser()
    parser.run()
