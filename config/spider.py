from config.baseconfig import BaseConfig
import os


class Spider(BaseConfig):
    name = 'spider'

    DEFAULT_CONFIG = {}

    SAMPLE_CONFIG = {
        "base_url": "http://test.yoursite.com",
        "last_seconds": 3600,
        "speed_ttl": 1,
        "start_at": "11:25",
        "login_data": {
            "phone": "15988888888",
            "vcode": "123456",
            "sgq": "",
            "sgq2": "",
            "phonemodel": "MI 9 Transparent Edition",
            "phoneversion": 10,
            "deviceToken": "",
            "platform": "android",
            "version": "130"
        }
    }


if __name__ == '__main__':
    spider = Spider()
    print(spider.get_config())
