def retrain(algorithmId, trainDatasetId):
        newModel = RedLightModel()
        if algorithmId == 1 and trainDatasetId == 1:
            connection = DAO.connectToMySQL()

            algorithm = RedLightAlgorithm()
            SELECT_ALGORITHM = "select * from redlightalgorithm where algorithmId = %s"
            try:
                cursor = connection.cursor()
                cursor.execute(SELECT_ALGORITHM, (str(algorithmId),))
                res = cursor.fetchall()
                if res:
                    for row in res:
                        algorithm = RedLightAlgorithm(
                            algorithmId=algorithmId,
                            name=str(row[1]),
                            description=str(row[2]),
                        )
            except Exception as e:
                print(f"Error: {e}", end="\n")

            trainDataset = RedLightTrainDataset()
            SELECT_TRAINDATASET = (
                "select * from redlighttraindataset where trainDatasetId = %s"
            )
            try:
                cursor = connection.cursor()
                cursor.execute(SELECT_TRAINDATASET, (str(trainDatasetId),))
                res = cursor.fetchall()
                if res:
                    for row in res:
                        trainDataset = RedLightTrainDataset(
                            trainDatasetId=trainDatasetId,
                            name=str(row[1]),
                            path=str(row[2]),
                        )
            except Exception as e:
                print(f"Error: {e}")

            dirList = []
            folderPath = "D:/B20DCCN352/Year_4/Semester_1/PT_HTTM/web/traffic_train/yolov7/runs/train/"
            for folder in os.listdir(folderPath):
                if os.path.isdir(os.path.join(folderPath, folder)):
                    dirList.append(folder)
            if os.path.exists(
                "D:/B20DCCN352/Year_4/Semester_1/PT_HTTM/web/traffic_train/train_data/val.cache"
            ):
                os.remove(
                    "D:/B20DCCN352/Year_4/Semester_1/PT_HTTM/web/traffic_train/train_data/val.cache"
                )
            if os.path.exists(
                "D:/B20DCCN352/Year_4/Semester_1/PT_HTTM/web/traffic_train/train_data/train/labels.cache"
            ):
                os.remove(
                    "D:/B20DCCN352/Year_4/Semester_1/PT_HTTM/web/traffic_train/train_data/train/labels.cache"
                )
            subprocess.check_call(
                "python traffic_train/yolov7/train.py --project traffic_train/yolov7/runs/train --weights traffic_train/yolov7/pretrain/yolov7.pt --data traffic_train/yolov7/data/mydataset.yaml --device cpu --batch-size 1 --epochs 3 --cfg traffic_train/yolov7/cfg/training/yolov7.yaml --hyp traffic_train/yolov7/data/hyp.scratch.p5.yaml",
                shell=True,
                universal_newlines=True,
            )

            newModelDir = []
            while True:
                cnt = len(newModelDir)
                for folder in os.listdir(folderPath):
                    if folder not in dirList and folder not in newModelDir:
                        newModelDir.append(folder)
                if len(newModelDir) == cnt:
                    break

            print(newModelDir)

            for modelDir in newModelDir:
                if os.path.exists(folderPath + modelDir + "/weights/last.pt"):
                    arr = []
                    with open(
                        folderPath + modelDir + "/results.txt", "r"
                    ) as file:
                        for line in file:
                            arr = line.strip().split()

                    modelPath = os.path.join(
                        folderPath + modelDir + "/weights/", "last.pt"
                    )
                    print(modelPath)

                    sampleQuantity = 0
                    trainImagesPath = "D:/B20DCCN352/Year_4/Semester_1/PT_HTTM/web/traffic_train/train_data/train/images/"
                    for file in os.listdir(trainImagesPath):
                        if ".jpg" in file:
                            sampleQuantity += 1
                    print(sampleQuantity)

                    name = "Traffic_yolov7_model_"
                    for i in range(len(modelDir)):
                        if modelDir[i].isdigit():
                            name += modelDir[i]

                    newModel = RedLightModel(
                        trainDataset=trainDataset,
                        algorithm=algorithm,
                        name=name,
                        createDate=datetime.now().date(),
                        path=modelPath,
                        description=f"mAP: {float(arr[10]):.4f}",
                        sampleQuantity=sampleQuantity,
                        acc=0,
                        pre=f"{float(arr[8]):.4f}",
                        rec=f"{float(arr[9]):.4f}",
                        f1=f"{(2*float(arr[8])*float(arr[9])/(float(arr[8])+float(arr[9]))):.4f}",
                        isActive=0,
                    )

        return newModel




# 

# import mysql.connector
# from datetime import date

# try:
#     # Kết nối đến MySQL
#     connection = mysql.connector.connect(
#         host="127.0.0.1",
#         user="root",
#         password="phonglinh520@",
#         database="trainmodel"
#     )

#     # Tạo một con trỏ (cursor) để thực hiện các truy vấn SQL
#     cursor = connection.cursor()

#     # Câu lệnh tạo bảng cho `thuattoan`
#     create_table_thuattoan = """
#     CREATE TABLE IF NOT EXISTS thuattoan (
#         mathuattoan INT AUTO_INCREMENT PRIMARY KEY,
#         ten VARCHAR(255) NOT NULL,
#         mota TEXT
#     )
#     """
#     cursor.execute(create_table_thuattoan)
#     connection.commit()

#     # Câu lệnh tạo bảng cho `dulieu`
#     create_table_dulieu = """
#     CREATE TABLE IF NOT EXISTS dulieu (
#         madulieu INT AUTO_INCREMENT PRIMARY KEY,
#         ten VARCHAR(255) NOT NULL,
#         duongdan VARCHAR(255) NOT NULL
#     )
#     """
#     cursor.execute(create_table_dulieu)
#     connection.commit()

#     # Câu lệnh tạo bảng cho `mohinh`
#     create_table_mohinh = """
#     CREATE TABLE IF NOT EXISTS mohinh (
#         mamohinh INT AUTO_INCREMENT PRIMARY KEY,
#         madulieu INT,
#         mathuattoan INT,
#         ten VARCHAR(255) NOT NULL,
#         ngayhl DATE,
#         path VARCHAR(255) NOT NULL,
#         mota TEXT,
#         soluongmau INT,
#         acc FLOAT,
#         pre FLOAT,
#         re FLOAT,
#         f1 FLOAT,
#         hoatdong INT,
#         FOREIGN KEY (madulieu) REFERENCES dulieu(madulieu),
#         FOREIGN KEY (mathuattoan) REFERENCES thuattoan(mathuattoan)
#     )
#     """
#     cursor.execute(create_table_mohinh)
#     connection.commit()

#     # Câu lệnh tạo bảng cho `ketqua`
#     create_table_ketqua = """
#     CREATE TABLE IF NOT EXISTS ketqua (
#         maketqua INT AUTO_INCREMENT PRIMARY KEY,
#         mamohinh INT,
#         mAP FLOAT,
#         FOREIGN KEY (mamohinh) REFERENCES mohinh(mamohinh)
#     )
#     """
#     cursor.execute(create_table_ketqua)
#     connection.commit()

#     # Thêm dữ liệu vào bảng `thuattoan`
#     add_algorithm_query = "INSERT INTO thuattoan (ten, mota) VALUES (%s, %s)"
#     algorithm_values = ("Algorithm1", "Description1")
#     cursor.execute(add_algorithm_query, algorithm_values)
#     connection.commit()

#     # Thêm dữ liệu vào bảng `dulieu`
#     add_data_query = "INSERT INTO dulieu (ten, duongdan) VALUES (%s, %s)"
#     data_values = ("Data1", "D:\\test_python\\image")
#     cursor.execute(add_data_query, data_values)
#     connection.commit()

#     # Thêm dữ liệu vào bảng `mohinh`
#     add_model_query = """
#     INSERT INTO mohinh (madulieu, mathuattoan, ten, ngayhl, path, mota, soluongmau, acc, pre, re, f1, hoatdong)
#     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#     """
#     model_values = (1, 1, "Model1", date.today(), "/path/to/model1", "Description1", 100, 0.85, 0.75, 0.80, 0.78, 1)
#     cursor.execute(add_model_query, model_values)
#     connection.commit()

#     # Thêm dữ liệu vào bảng `ketqua`
#     add_result_query = "INSERT INTO ketqua (mamohinh, mAP) VALUES (%s, %s)"
#     result_values = (1, 0.90)
#     cursor.execute(add_result_query, result_values)
#     connection.commit()

# except Exception as e:
#     print(f"Error: {e}")

# finally:
#     # Đóng kết nối
#     if connection.is_connected():
#         cursor.close()
#         connection.close()
