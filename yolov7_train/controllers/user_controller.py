import json
from datetime import datetime, timedelta

import jwt
from flask import Flask, current_app, jsonify, request
import pandas as pd
from datetime import date

from ..config.connect_db import db
# from ..config.marsh_mallow import user_schema
# from ..controllers.verify_and_authorization import Middleware
# from ..models.model import Users
# from ..services import user_service
from flask_restful import Resource, reqparse
import subprocess
from ..models.dao import *
from ..config.config import config


# users_schema = user_schema(many=True)


# def sign_up():
#     data = json.loads(request.data)
#     if data and ("name" in data) and ("email" in data) \
#             and ("password" in data) and ("comfirm_password" in data) \
#             and ("role_id" in data) and ("mobile_number" in data) \
#             and ("admission_id" in data) and ("gender" in data) \
#             and ("dob" in data) and ("address" in data):
#         user_data = user_service.handle_user_sign_up(data)
#         response = jsonify(
#             {
#                 "user": user_data,
#             }
#         )
#         response.status_code = 200
#         return response
#     response = jsonify(
#         {
#             "err_code": "1",
#             "message": "Missing inputs parameter!",
#         }
#     )
#     response.status_code = 404
#     return response
#
#
# def handle_loging():
#     data = json.loads(request.data)
#     if data and ("email" in data) and ("password" in data):
#         email = data["email"]
#         password = data["password"]
#         user_data = user_service.handle_user_login(email, password)
#         if user_data['err_code'] != 0:
#             response = jsonify(user_data)
#             response.status_code = 401
#             return response
#         role = "member"
#         print()
#         print(user_data)
#         if user_data['role_id'] == 1:
#             role = "admin"
#         # pip install PyJWT
#
#         if user_data["err_code"] == 0:
#             token = jwt.encode(
#                 {
#                     "role_id": role,
#                     "id": user_data['id'],
#                     "exp": datetime.utcnow() + timedelta(minutes=3000),
#                 },
#                 current_app.config["SECRET_KEY"],
#             )
#             response = jsonify(
#                 {
#                     "id": user_data['id'],
#                     "token": token,
#                     "isAdmin": True if user_data['role_id'] == 1 else False,
#                     "err_code": user_data["err_code"],
#                     "err_message": user_data["err_message"],
#                 }
#             )
#             response.status_code = 200
#             return response
#         response = jsonify(
#             {
#                 "err_code": user_data["err_code"],
#                 "message": user_data["err_message"],
#             }
#         )
#         response.status_code = 200
#         return response
#     response = jsonify({"err_code": "1", "message": "Missing inputs parameter!"})
#     response.status_code = 404
#     return response
#
#
# def create_new_category():
#     data = json.loads(request.data)
#     try:
#         current_user = Middleware()
#         user_data = user_service.create_new_list(data, current_user["email"])
#         return jsonify(
#             {
#                 "message": user_data,
#             }
#         )
#     except:
#         return jsonify(
#             {
#                 "err_message": "not logged in yet",
#             }
#         )
#
#
# def handle_get_all_member():
#     type_member = request.args.get('type')
#     data = Middleware()
#     if data and ("id" in data) and ("role_id" in data):
#         user_data = user_service.get_all_users(data, type_member)
#         return jsonify({"users": user_data})


# except Exception as e:
#     response = jsonify({"error": str(e)})
#     response.status_code = 400
#     return response


# def handle_edit_users():
#     try:
#         current_user = Middleware()
#         data = json.loads(request.data)
#         if (data and ("first_name" in data) and ("last_name" in data) and ("address" in data)) and ("id" in data):
#             message = user_service.update_user_data(data, current_user)
#             response = jsonify({"message": message})
#             response.status_code = 202
#             return response
#         return jsonify({"err_code": "1", "err_message": "Missing inputs parameter!"})
#     except:
#         return jsonify({"err_message": "not logged in yet"})
#
#
# def handle_delete_users():
#     try:
#         current_user = Middleware()
#         data = json.loads(request.data)
#         if data and ("role_id" in current_user) and "id" in data:
#             message = user_service.delete_user(data["id"], current_user)
#             response = jsonify({"message": message})
#             response.status_code = 202
#             return response
#         return jsonify({"err_code": "1", "err_message": "Missing inputs parameter!"})
#     except:
#         return jsonify({"err_message": "not logged in yet"})
#
#
# def handle_get_all_category():
#     try:
#         category_data = user_service.get_all_category()
#         return jsonify({"err_code": 0, "err_message": "OK", "category_detail": category_data})
#     except Exception as e:
#         return jsonify({"error": str(e)})
#
#
# def handle_get_all_book():
#     try:
#         book_data = user_service.get_all_books_with_category()
#         return jsonify({"err_code": 0, "err_message": "OK", "book_detail": book_data})
#     except Exception as e:
#         return jsonify({"error": str(e)})
#
#
# def handle_create_book():
#     try:
#         data = json.loads(request.data)
#         book_data = user_service.handle_create_book(data)
#         if 'error' in book_data:
#             response = jsonify({"error": book_data['error']})
#             response.status_code = 400
#             return response
#         else:
#             response = jsonify({"data": book_data})
#             response.status_code = 201
#             return response
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#
#
# def update_book():
#     try:
#         data = json.loads(request.data)
#         current_user = Middleware()
#         book_data = user_service.update_book(data, current_user)
#         if 'error' in book_data:
#             response = jsonify({"error": book_data['error']})
#             response.status_code = 400
#             return response
#         else:
#             response = jsonify({"data": book_data})
#             response.status_code = 200
#             return response
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# def get_recent_transactions():
#     user_id = request.args.get('user_id')
#     book_data = user_service.get_recent_transactions(user_id)
#     if 'error' in book_data:
#         response = jsonify({"error": book_data['error']})
#         response.status_code = 400
#         return response
#     else:
#         response = jsonify({"data": book_data})
#         response.status_code = 201
#         return response
#
#
# def create_transactions():
#     data = json.loads(request.data)
#     current_user = Middleware()
#     transaction = user_service.create_transactions(data, current_user)
#     if 'error' in transaction:
#         response = jsonify({"error": transaction['error']})
#         response.status_code = 400
#         return response
#     else:
#         response = jsonify({"data": transaction})
#         response.status_code = 201
#         return response
#
#
def delete_model():
    model_id = request.args.get('model_id')
    delete_model_by_id(model_id)
    return jsonify({"message": "Deleted model"})


def get_model():
    models = get_all_mohinh()
    return jsonify({"models": models})


def train_model():
    try:
        subprocess.check_call(
            "python yolov7_train/yolov7/train.py --project yolov7_train/yolov7/runs/train --weights yolov7_train/yolov7/pretrain/yolov7.pt --data yolov7_train/yolov7/data/mydataset.yaml --device cpu --batch-size 1 --epochs 1 --cfg yolov7_train/yolov7/cfg/training/yolov7.yaml --hyp yolov7_train/yolov7/data/hyp.scratch.p5.yaml",
            shell=True,
            universal_newlines=True
        )

        # Đọc kết quả từ tệp result.txt và in ra màn hình
        results_file_from_train = 'C:/Users/Admin/Desktop/Yolov7_Mimi/yolov7_train/yolov7/results.txt'
        #
        # Đọc dữ liệu vào DataFrame
        df = pd.read_csv(results_file_from_train, sep='\s+', header=None)

        # Lấy giá trị từ cột cần trích xuất (Epoch cuối - 1/1)
        model_dict = {}
        if not df.empty:
            model_dict = {
                "images_value": df.iloc[-1][6],
                "p_value": df.iloc[-1][11],
                "r_value": df.iloc[-1][12],
                "map_5_value": df.iloc[-1][13]
            }

            # In giá trị
        else:
            print("DataFrame is empty.")

        data = create_data(model_dict)
        response = data
        return response

        # Xoá nội dung của tệp result.txt
        with open(results_file_from_train, 'w') as result_file:
            result_file.write('')

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def save_result():
    try:
        results_file_from_train = 'C:/Users/Admin/Desktop/Yolov7_Mimi/yolov7_train/yolov7/results.txt'
        #
        # Đọc dữ liệu vào DataFrame
        df = pd.read_csv(results_file_from_train, sep='\s+', header=None)
        model_dict = {}
        if not df.empty:
            # Lấy giá trị từ cột cần trích xuất (Epoch cuối - 1/1)
            model_dict = {
                "images_value": df.iloc[-1][6],
                "p_value": df.iloc[-1][11],
                "r_value": df.iloc[-1][12],
                "map_5_value": df.iloc[-1][13]
            }

        else:
            print("DataFrame is empty.")
        data = save_data(model_dict)
        response = data
        return response
    except Exception as e:
        print(f"Error: {e}")
