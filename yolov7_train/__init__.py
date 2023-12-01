from flask import Flask, render_template
from flask_cors import CORS
from flask_restful import Api
from yolov7_train.config.config import config

from .route.web import *

from .views import render_train_page, render_main_page
from .config.connect_db import db
from yolov7_train.models.data_model import *


def create_app():
    app = Flask(__name__)
    api = Api(app)
    app.config.from_mapping(config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    CORS(app, supports_credentials=True)

    api.add_resource(Train, "/api/train")
    api.add_resource(Result, "/api/save_result")
    api.add_resource(Model, "/api/model")
    # api.add_resource(Category, "/api/allcategories")
    # api.add_resource(Book, "/api/books")
    # api.add_resource(User, "/api/get_all_member")
    # api.add_resource(Transaction, "/api/transactions")
    # api.add_resource(Recharge, "/api/recharge")
    # api.add_resource(Point, "/api/update_point")

    # app.config['TEMPLATES_AUTO_RELOAD'] = True

    # app.template_folder = 'views/templates' (bỏ '/' trước views)

    # Thêm route để render main.templates khi gọi vào path '/'
    @app.route('/', methods=['GET'])
    def render_main():
        return render_main_page()

    @app.route('/train', methods=['GET'])
    def render_train():
        return render_template('train.html')

    return app

# python yolov7_train/yolov7/train.py --batch 8 --cfg  yolov7_train/yolov7/cfg/training/yolov7.yaml --epochs 1 --data yolov7_train/yolov7/data/mydataset.yaml --weights 'yolov7_train/yolov7/pretrain/yolov7.pt'

# --project yolov7_train/yolov7/runs/train --weights yolov7_train/yolov7/pretrain/yolov7.pt --data yolov7_train/yolov7/data/mydataset.yaml --device cpu --batch-size 1 --epochs 3 --cfg yolov7_train/yolov7/cfg/training/yolov7.yaml --hyp yolov7_train/yolov7/data/hyp.scratch.p5.yaml