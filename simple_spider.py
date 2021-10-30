
import requests
from helpers.Timer import Timer
import time
from config import Spider


class SimpleSpider:

    config = {}
    base_url = ""
    login_data = {}
    token = ''

    def __init__(self, config):
        self.config = config
        self.login_data = self.config['login_data']
        self.base_url = self.config['base_url']

    def __login(self):
        response = requests.post(self.base_url + "/api/member/checkLogin", self.login_data)
        data = response.json()['data']
        print(data)
        self.token = data['token']
        print(self.token)

    def check_login(self, response, func):
        res_json = response.json()
        print(res_json)
        if res_json['code'] != 200 and 'msg' in res_json.keys() and res_json['msg'].count("token") > 0:
            self.__login()
            return func(self.token)
        if res_json['code'] != 200:
            if 'msg' in res_json.keys():
                print(res_json['msg'])
            if 'message' in res_json.keys():
                print(res_json['message'])
        return response

    def get_3000_zuan_info(self, token):
        post_data = {'token': token}
        response = requests.post(self.base_url + "/api/oneps/index", post_data)
        return self.check_login(response, self.get_3000_zuan_info)

    def join_3000_zuan_lottery(self, token):
        if not self.in_time_range("11:59:50", "12:00:55"):
            print("不在抽奖活动时间范围内11:59:50～12:00:55，跳过......")
            return False
        info = self.get_3000_zuan_info(token).json()
        psid = info['data']['list'][0]['id']
        post_data = {'token': token, 'id': psid}
        url = self.base_url + "/api/oneps/join"
        response = requests.post(url, post_data)
        self.check_login(response, self.join_3000_zuan_lottery)

    def make_order(self, token):
        if not self.in_time_range("11:29:50", "11:31:55"):
            print("不在抢单时间范围内11:29:50～11:31:55，跳过......")
            return False
        headers = {"from": "ios", "versionName": "1.3.0"}
        order_data = {"num": 1, "goods_id": 10, "token": token}
        response = requests.post(self.base_url + "/api/Mallorder/makeOrder", order_data, headers=headers)
        self.check_login(response, self.make_order)

    @staticmethod
    def in_time_range(start_at, end_at):
        today_str = time.strftime("%Y-%m-%d ")

        current_timestamp = time.time()
        tuple_time_start = time.strptime(today_str+start_at, "%Y-%m-%d %H:%M:%S")

        start_timestamp = time.mktime(tuple_time_start)
        tuple_time_end = time.strptime(today_str+end_at, "%Y-%m-%d %H:%M:%S")

        end_timestamp = time.mktime(tuple_time_end)

        # if (current_timestamp > start_timestamp) and (current_timestamp < end_timestamp):
        if start_timestamp < current_timestamp < end_timestamp:
            return True
        return False

    def make_requests(self):
        if self.token == '':
            self.__login()
        self.join_3000_zuan_lottery(self.token)
        self.make_order(self.token)

    def run_spider(self):
        # 时间戳默认为当前
        start_time = time.time()
        # 设置时间元组默认值
        tuple_time = time.localtime()
        # 设置程序开始运行的时间默认值
        datetime = time.strftime("%Y-%m-%d ", tuple_time)
        # len(self.config["start_at"])!=8 不判断字符串长度 改为判断字符串冒号:出现的次数
        if "start_at" in self.config.keys():
            start_at = self.config['start_at']
            # 时间字符拼接 用于转化为时间元组
            datetime = datetime + start_at
            # 时间字符串冒号:的个数
            count_t = start_at.count(":")
            if count_t == 2:
                tuple_time = time.strptime(datetime, "%Y-%m-%d %H:%M:%S")
            if count_t == 1:
                tuple_time = time.strptime(datetime, "%Y-%m-%d %H:%M")
            # 时间元组转为时间戳
            start_time = time.mktime(tuple_time)
        last_seconds = 60
        if 'last_seconds' in self.config.keys():
            last_seconds = self.config['last_seconds']
        speed_ttl = 1
        if 'speed_ttl' in self.config.keys():
            speed_ttl = self.config['speed_ttl']
        print("准备就绪    程序启动时间: " + datetime + " 持续秒数： " + str(last_seconds) + " 请求频率[间隔秒数]： " + str(speed_ttl))

        timer = Timer(self.make_requests, start_time, start_time + last_seconds)
        timer.ttl = speed_ttl
        timer.run()


if __name__ == "__main__":
    sgq = SimpleSpider(Spider().get_config())
    sgq.run_spider()

