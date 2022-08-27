import math
import time
import random
import requests
from bs4 import BeautifulSoup


class House591Spider():
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68',
        }

    def search(self, filter_params=None, sort_params=None):
        """ 搜尋房屋

        :param filter_params: 篩選參數
        :param sort_params: 排序參數
        :param want_page: 想要抓幾頁
        :return total_count: requests 房屋總數
        :return house_list: requests 搜尋結果房屋資料
        """
        house_list = []
        page = 1

        # 紀錄 Cookie 取得 X-CSRF-TOKEN
        s = requests.Session()
        url = 'https://rent.591.com.tw/'
        r = s.get(url, headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        token_item = soup.select_one('meta[name="csrf-token"]')

        headers = self.headers.copy()
        headers['X-CSRF-TOKEN'] = token_item.get('content')

        # 搜尋房屋
        url = 'https://rent.591.com.tw/home/search/rsList'
        params = 'is_format_data=1&is_new_list=1&type=1'
        if filter_params:
            # 加上篩選參數，要先轉換為 URL 參數字串格式
            params += ''.join([f'&{key}={value}' for key, value, in filter_params.items()])
        else:
            params += '&region=1&kind=0'
        # 在 cookie 設定地區縣市，避免某些條件無法取得資料
        s.cookies.set('urlJumpIp', filter_params.get('region', '1') if filter_params else '1', domain='.591.com.tw')

        # 排序參數
        if sort_params:
            params += ''.join([f'&{key}={value}' for key, value, in sort_params.items()])

        # 開始request
        r = s.get(url, params=params, headers=headers)
        if r.status_code != requests.codes.ok:
            print('請求失敗', r.status_code)
        data = r.json()
        total_records = data['records']
        total_records = int(total_records.replace(',', ''))
        want_page = math.ceil(total_records / 30)
        house_list.extend(data['data']['data'])
        print('搜尋結果房屋總數：', total_records)

        time.sleep(5)

        while page < want_page:
            params += f'&firstRow={page*30}'
            r = s.get(url, params=params, headers=headers)
            if r.status_code != requests.codes.ok:
                print('分頁請求失敗', r.status_code)
                break
            page += 1
            data = r.json()
            total_records = int(data['records'])
            house_list.extend(data['data']['data'])
            # 隨機 delay 一段時間
            time.sleep(random.uniform(2, 5))

        return total_records, house_list


if __name__ == "__main__":
    post_id_container = []
    house591_spider = House591Spider()

    # 篩選條件
    filter_params = {
        'region': '1',  # (地區) 台北
        'section': '11',  # 南港區
        'kind': '2',  # (類型) 獨立套房
        'multiPrice': '10000_20000',
        # 'other': 'newPost',  # (特色)

    }
    # 排序依據
    sort_params = {
        # 以最新時間排序
        'order': 'posttime',  # 發布時間
        'orderType': 'desc'  # 由近到遠 # asc
    }
    total_count, houses = house591_spider.search(filter_params, sort_params)

    for count in range(0, total_count):
        # 儲存現有的物件id
        post_id_container.append(houses[count]['post_id'])
        print(houses[count]['post_id'])
