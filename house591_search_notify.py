import requests


def lineNotifyMessage(token, msg):
    # HTTP 標頭參數與資料
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code


if __name__ == '__main__':
    pass
