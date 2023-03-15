import requests
import os
from bs4 import BeautifulSoup

from save_website import save_website

if __name__ == '__main__':
    import requests

    s = requests.session()
    cookies = {
        'is_gdpr': '0',
        'is_gdpr_b': 'CN3iTBDcnAEoAg==',
        'yandexuid': '8650096661671817652',
        'yuidss': '8650096661671817652',
        'ymex': '1987177653.yrts.1671817653',
        '_ym_uid': '1671808222292708416',
        '_ym_d': '1671808225',
        'i': '+tmRmwCGAACxAdQ9dNlpXnm55Vv8mRenGSIxV15JGCcs/B/POmnNQRb9mnQVQg7cGAIgqJh1Oq8tEMciFrl/ZBrpeSU=',
        'skid': '9007684931672431819',
        'gdpr': '0',
        'yandex_login': 'pawel.kovinyov',
        'yashr': '8463730321674063298',
        'yp': '1988387207.udn.czoyNTEwMzEwNjp2azrQn9Cw0LLQtdC7INCa0L7QstGL0L3RkdCy#1990199092.pcs.0#1706375092.p_sw.1674839092#1677431093.los.1#1677431093.losc.0#1675443893.mcv.0#1675443893.mcl.1fiubw1#1675443893.szm.1:1920x1080:1920x969',
        'yabs-sid': '1359360311678017345',
        'Session_id': '3:1678038489.5.0.1673027207401:cveeLg:2c.1.2:1|247454205.-1.2.1:25103106|3:10266493.834342.jzsB62W5xNHhbjHhbYePTHbPozE',
        'sessionid2': '3:1678038489.5.0.1673027207401:cveeLg:2c.1.2:1|247454205.-1.2.1:25103106|3:10266493.834342.fakesign0000000000000000000',
        'ys': 'udn.czoyNTEwMzEwNjp2azrQn9Cw0LLQtdC7INCa0L7QstGL0L3RkdCy#c_chck.2572626478',
    }

    headers = {
        'authority': 'mc.yandex.ru',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        # 'cookie': 'is_gdpr=0; is_gdpr_b=CN3iTBDcnAEoAg==; yandexuid=8650096661671817652; yuidss=8650096661671817652; ymex=1987177653.yrts.1671817653; _ym_uid=1671808222292708416; _ym_d=1671808225; i=+tmRmwCGAACxAdQ9dNlpXnm55Vv8mRenGSIxV15JGCcs/B/POmnNQRb9mnQVQg7cGAIgqJh1Oq8tEMciFrl/ZBrpeSU=; skid=9007684931672431819; gdpr=0; yandex_login=pawel.kovinyov; yashr=8463730321674063298; yp=1988387207.udn.czoyNTEwMzEwNjp2azrQn9Cw0LLQtdC7INCa0L7QstGL0L3RkdCy#1990199092.pcs.0#1706375092.p_sw.1674839092#1677431093.los.1#1677431093.losc.0#1675443893.mcv.0#1675443893.mcl.1fiubw1#1675443893.szm.1:1920x1080:1920x969; yabs-sid=1359360311678017345; Session_id=3:1678038489.5.0.1673027207401:cveeLg:2c.1.2:1|247454205.-1.2.1:25103106|3:10266493.834342.jzsB62W5xNHhbjHhbYePTHbPozE; sessionid2=3:1678038489.5.0.1673027207401:cveeLg:2c.1.2:1|247454205.-1.2.1:25103106|3:10266493.834342.fakesign0000000000000000000; ys=udn.czoyNTEwMzEwNjp2azrQn9Cw0LLQtdC7INCa0L7QstGL0L3RkdCy#c_chck.2572626478',
        'origin': 'https://5ka.ru',
        'referer': 'https://5ka.ru/',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }

    response = s.post(
        'https://mc.yandex.ru/watch/49423435?wmode=7&page-url=https%3A%2F%2F5ka.ru%2Fspecial_offers&page-ref=https%3A%2F%2Fwww.google.com%2F&charset=utf-8&browser-info=pv%3A1%3Avf%3Asm0eap24cmhk4ozkpnx0n%3Afp%3A865%3Afu%3A0%3Aen%3Autf-8%3Ala%3Aru-RU%3Av%3A970%3Acn%3A1%3Adp%3A0%3Als%3A1544367248748%3Ahid%3A198589962%3Az%3A180%3Ai%3A20230307174514%3Aet%3A1678200314%3Ac%3A1%3Arn%3A1041141871%3Arqn%3A54%3Au%3A1677363863197118551%3Aw%3A981x969%3As%3A1920x1080x24%3Ask%3A1%3Awv%3A2%3Ads%3A0%2C109%2C605%2C3%2C1%2C0%2C%2C303%2C0%2C%2C%2C%2C1322%3Aco%3A0%3Acpf%3A1%3Ans%3A1678200312746%3Aadb%3A1%3Arqnl%3A1%3Ast%3A1678200314%3At%3A%D0%92%D1%81%D0%B5%20%D0%B0%D0%BA%D1%86%D0%B8%D0%B8&t=gdpr(14)clc(0-0-0)rqnt(1)aw(1)ti(2)',
        cookies=cookies,
        headers=headers,
    )
    response = s.get('https://5ka.ru/special_offers')
    print(response.text)


