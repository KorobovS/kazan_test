from PIL import Image
import requests
from io import BytesIO

from bs4 import BeautifulSoup


def get_new_fid():
    # скачиваем файл поставщика и созраняем его в переменную
    url_supplier = 'http://stripmag.ru/datafeed/p5s_full_stock.xml'
    req_supplier = requests.get(url_supplier)
    soup_supplier = BeautifulSoup(req_supplier.content, "lxml-xml")

    # сохраняем описания всех продуктов поставщика
    items_supplier = soup_supplier.find_all('product')

    # скачиваем наш файл и созраняем его в переменную
    url_fid = 'http://alitair.1gb.ru/Intim_Ali_allfids_2.xml'
    req_fid = requests.get(url_fid)
    soup_fid = BeautifulSoup(req_fid.content, "lxml-xml")

    # сохраняем описания всех наших продуктов
    items_fid = soup_fid.find_all('offer')

    # перебираем значения, когда id поставщика совпадает с нашим, перезаписываем цену и наличие
    for item_fid in items_fid:
        prodID = item_fid.get('id')
        for item_supplier in items_supplier:
            if item_supplier.get('prodID') == prodID:

                # перезаписываем значения
                item_fid.find('price')['BaseRetailPrice'] = item_supplier.find('price').get('BaseRetailPrice')
                item_fid.find('price')['BaseWholePrice'] = item_supplier.find('price').get('BaseWholePrice')
                item_fid.find('price')['RetailPrice'] = item_supplier.find('price').get('RetailPrice')
                item_fid.find('price')['WholePrice'] = item_supplier.find('price').get('WholePrice')
                item_fid.find('quantity')[''] = str(item_supplier.find('assort').get('sklad'))


def get_image():
    # открываем картинку, которая будет фоном
    url_die = 'http://alitair.1gb.ru/test_prog_plashki/benefit.png'
    response = requests.get(url_die)
    die = Image.open(BytesIO(response.content))

    # открываем картинку, которая будет накладываться
    url_picture = 'http://alitair.1gb.ru/test_prog_plashki/106044_benefit.jpg'
    response = requests.get(url_picture)
    picture = Image.open(BytesIO(response.content))

    # узнаем ширину и высоту каждой картинки
    width_die, height_die = die.size
    width_picture, height_picture = picture.size

    # опытным путем нахожу ширину надписи (132) и нахожу отступы
    x = 132+(height_die-132-height_picture)//2
    y = (width_die-width_picture)//2

    # накладываю картинку на картинку
    die.paste(picture, (y, x))
    # сохраняю
    die.save('picture.png')

    # закрываю начальные картинки
    die.close()
    picture.close()

if __name__ == '__main__':
    get_new_fid()
    get_image()
