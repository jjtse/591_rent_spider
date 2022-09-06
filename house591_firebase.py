import firebase_admin
from firebase_admin import db
from firebase_admin import credentials


def access_db():
    # 取得資料庫存取權
    cred = credentials.Certificate("key/serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://rent591-spider-default-rtdb.asia-southeast1.firebasedatabase.app"
    })
    ref = db.reference("/")
    # 拉下來的資料型態為字典
    data_dict = ref.get()

    return data_dict


def push_data(new_post_list):
    ref = db.reference("/")

    for i in range(0, len(new_post_list)):
        post_id = new_post_list[i]
        print(post_id)

        ref.push().set({
            post_id: 'null'
        })


if __name__ == '__main__':
    pass
