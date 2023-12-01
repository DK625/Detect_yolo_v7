import mysql.connector
import os
from datetime import datetime
from .data_model import *
from ..config.config import config


class DAO:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

    def close_connection(self):
        self.conn.close()


class Dulieu:
    def __init__(self, name, train_path, test_path):
        self.name = name
        self.train_path = train_path
        self.test_path = test_path


class DulieuDAO(DAO):
    def add_dulieu(self, dulieu):
        query = "INSERT INTO dulieu (name, train_path, test_path) VALUES (%s, %s, %s)"
        values = (dulieu.name, dulieu.train_path, dulieu.test_path)
        self.cursor.execute(query, values)
        self.conn.commit()
        dulieu_id = self.cursor.lastrowid
        dulieu.id = dulieu_id


class Thuattoan:
    def __init__(self, ten, mota):
        self.ten = ten
        self.mota = mota


class ThuattoanDAO(DAO):
    def add_thuattoan(self, thuattoan):
        query = "INSERT INTO thuattoan (ten, mota) VALUES (%s, %s)"
        values = (thuattoan.ten, thuattoan.mota)
        self.cursor.execute(query, values)
        self.conn.commit()
        tt_id = self.cursor.lastrowid
        thuattoan.id = tt_id


class Mohinh:
    def __init__(self, dulieu_id, thuattoan_id, ten, ngayhl, duongdan, mota, soluongmau, acc, pre, re, f1, hoatdong):
        self.dulieu_id = dulieu_id
        self.thuattoan_id = thuattoan_id
        self.ten = ten
        self.ngayhl = ngayhl
        self.duongdan = duongdan
        self.mota = mota
        self.soluongmau = soluongmau
        self.acc = acc
        self.pre = pre
        self.re = re
        self.f1 = f1
        self.hoatdong = hoatdong


class MohinhDAO(DAO):
    def add_mohinh(self, mohinh):
        query = "INSERT INTO mohinh (dulieu_id, thuattoan_id, ten, ngayhl, duongdan, mota, soluongmau, acc, pre, re, f1, hoatdong) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            int(mohinh.dulieu_id), int(mohinh.thuattoan_id),
            mohinh.ten, mohinh.ngayhl, mohinh.duongdan,
            mohinh.mota, int(mohinh.soluongmau),
            float(mohinh.acc), float(mohinh.pre), float(mohinh.re),
            float(mohinh.f1), int(mohinh.hoatdong)
        )

        self.cursor.execute(query, values)
        self.conn.commit()

    def get_all_model(self):
        query = "SELECT * FROM mohinh"
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        models = []
        for row in result:
            model = {
                'id': row[0],
                'dulieu_id': row[1],
                'thuattoan_id': row[2],
                'ten': row[3],
                'ngayhl': row[4],
                'duongdan': row[5],
                'mota': row[6],
                'soluongmau': row[7],
                'acc': row[8],
                'pre': row[9],
                're': row[10],
                'f1': row[11],
                'hoatdong': row[12]
            }
            models.append(model)

        return models

    def delete_model_by_id(self, model_id):
        query = "DELETE FROM mohinh WHERE id = %s"
        value = (model_id,)

        self.cursor.execute(query, value)
        self.conn.commit()


def create_data(model_dict):
    name = "du lieu huan luyen"
    train_path = "C:/Users/Admin/Desktop/Yolov7_Mimi/yolov7_train/train_test/train"
    test_path = "C:/Users/Admin/Desktop/Yolov7_Mimi/yolov7_train/train_test/test"
    new_dulieu = Dulieu(name=name, train_path=train_path, test_path=test_path)

    tentt = "yolov7"
    motatt = "nhan dang doi tuong"
    new_thuattoan = Thuattoan(ten=tentt, mota=motatt)

    ten = "yolov7_model"
    folderPath = "C:\\Users\\Admin\\Desktop\\Yolov7_Mimi\\yolov7_train\\yolov7\\runs\\train"
    exp_dirs = [d for d in os.listdir(folderPath) if
                os.path.isdir(os.path.join(folderPath, d))]
    latest_exp_dir = max(exp_dirs, key=lambda d: int(d[3:]) if d.startswith("exp") and d[3:].isdigit() else 0,
                         default=None)

    modelPath = None
    if latest_exp_dir is not None:
        modelPath = os.path.join(
            folderPath, latest_exp_dir, "weights", "last.pt"
        )
        print(f"Latest experiment directory: {latest_exp_dir}")
        print(f"Model path: {modelPath}")
    else:
        print("No experiment directories found.")

    sampleQuantity = 0
    trainImagesPath = "C:\\Users\\Admin\\Desktop\\Yolov7_Mimi\\yolov7_train\\train_test\\train"
    for file in os.listdir(trainImagesPath):
        if ".jpg" in file:
            sampleQuantity += 1
    testImagesPath = "C:\\Users\\Admin\\Desktop\\Yolov7_Mimi\\yolov7_train\\train_test\\test"
    for file in os.listdir(testImagesPath):
        if ".jpg" in file:
            sampleQuantity += 1

    response_data = {
        "dulieu": {
            "name": new_dulieu.name,
            "train_path": new_dulieu.train_path,
            "test_path": new_dulieu.test_path,
            # Thêm các thuộc tính khác của new_dulieu nếu cần
        },
        "thuattoan": {
            "ten": new_thuattoan.ten,
            "mota": new_thuattoan.mota,
            # Thêm các thuộc tính khác của new_thuattoan nếu cần
        },
        "mohinh": {
            # "dulieu_id": new_mohinh.dulieu_id,
            # "thuattoan_id": new_mohinh.thuattoan_id,
            "ten": ten,
            "ngayhl": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "duongdan": modelPath,
            "mota": model_dict['map_5_value'],
            "soluongmau": sampleQuantity,
            "acc": 0,
            "pre": float(model_dict['p_value']),
            "re": float(model_dict['r_value']),
            "f1": (2 * model_dict['p_value'] * model_dict['r_value'] / (model_dict['p_value'] + model_dict['r_value'])),
            "hoatdong": 0,
        }
    }

    return response_data


def save_data(model_dict):
    # du lieu
    name = "du lieu huan luyen"
    train_path = "C:/Users/Admin/Desktop/Yolov7_Mimi/yolov7_train/train_test/train"
    test_path = "C:/Users/Admin/Desktop/Yolov7_Mimi/yolov7_train/train_test/test"
    new_dulieu = Dulieu(name=name, train_path=train_path, test_path=test_path)

    repos = DulieuDAO(host=config['DB_HOST'], user=config['DB_USER_NAME'], password=config['DB_PASSWORD'],
                      database=config['DB_NAME'])
    repos.add_dulieu(new_dulieu)
    dulieuid = new_dulieu.id
    repos.close_connection()

    # thuat toan

    tentt = "yolov7"
    motatt = "nhan dang doi tuong"
    new_thuattoan = Thuattoan(ten=tentt, mota=motatt)

    repos = ThuattoanDAO(host=config['DB_HOST'], user=config['DB_USER_NAME'], password=config['DB_PASSWORD'],
                         database=config['DB_NAME'])
    repos.add_thuattoan(new_thuattoan)
    thuattoanid = new_thuattoan.id
    repos.close_connection()

    # Kiểm tra xem file "test.cache" tồn tại hay không, nếu có thì xóa
    if os.path.exists("C:/Users/Admin/Desktop/Yolov7_Mimi/yolov7_train/train_test/test.cache"):
        os.remove("C:/Users/Admin/Desktop/Yolov7_Mimi/yolov7_train/train_test/test.cache")

        # Kiểm tra xem file "train.cache"  tồn tại hay không, nếu có thì xóa
    if os.path.exists("C:/Users/Admin/Desktop/Yolov7_Mimi/yolov7_train/train_test/train.cache"):
        os.remove("C:/Users/Admin/Desktop/Yolov7_Mimi/yolov7_train/train_test/train.cache")

    ten = "yolov7_model"
    folderPath = "C:\\Users\\Admin\\Desktop\\Yolov7_Mimi\\yolov7_train\\yolov7\\runs\\train"
    exp_dirs = [d for d in os.listdir(folderPath) if
                os.path.isdir(os.path.join(folderPath, d))]
    latest_exp_dir = max(exp_dirs, key=lambda d: int(d[3:]) if d.startswith("exp") and d[3:].isdigit() else 0,
                         default=None)

    modelPath = None
    if latest_exp_dir is not None:
        modelPath = os.path.join(
            folderPath, latest_exp_dir, "weights", "last.pt"
        )
        print(f"Latest experiment directory: {latest_exp_dir}")
        print(f"Model path: {modelPath}")
    else:
        print("No experiment directories found.")

    sampleQuantity = 0
    trainImagesPath = "C:\\Users\\Admin\\Desktop\\Yolov7_Mimi\\yolov7_train\\train_test\\train"
    for file in os.listdir(trainImagesPath):
        if ".jpg" in file:
            sampleQuantity += 1
    testImagesPath = "C:\\Users\\Admin\\Desktop\\Yolov7_Mimi\\yolov7_train\\train_test\\test"
    for file in os.listdir(testImagesPath):
        if ".jpg" in file:
            sampleQuantity += 1

    new_mohinh = Mohinh(
        dulieu_id=dulieuid,
        thuattoan_id=thuattoanid,
        ten=ten,
        ngayhl=datetime.now().date(),
        duongdan=modelPath,
        mota=model_dict['map_5_value'],
        soluongmau=sampleQuantity,
        acc=0,
        pre=model_dict['p_value'],
        re=model_dict['r_value'],
        # f1=f"{(2 * float(arr[8]) * float(arr[9]) / (float(arr[8]) + float(arr[9]))):.4f}",
        f1=f"{(2 * model_dict['p_value'] * model_dict['r_value'] / (model_dict['p_value'] + model_dict['r_value'])):.4f}",
        hoatdong=0,
    )

    repos = MohinhDAO(host=config['DB_HOST'], user=config['DB_USER_NAME'], password=config['DB_PASSWORD'],
                      database=config['DB_NAME'])
    repos.add_mohinh(new_mohinh)
    repos.close_connection()
    response = {'status': 'saved result'}
    return response


def get_all_mohinh():
    repos = MohinhDAO(host=config['DB_HOST'], user=config['DB_USER_NAME'], password=config['DB_PASSWORD'],
                      database=config['DB_NAME'])
    result = repos.get_all_model()
    return result


def delete_model_by_id(model_id):
    repos = MohinhDAO(host=config['DB_HOST'], user=config['DB_USER_NAME'], password=config['DB_PASSWORD'],
                      database=config['DB_NAME'])
    repos.delete_model_by_id(model_id)
