import pickle
import json
import numpy as np

def get_estimated_price(giayto, thangmay, gara, viahe, two_mat, three_mat, pccc, qh, benhvien, cho, th, thcs, thpt, dh, sieuthi, benxe, ca, ubnd, baixe, congvien, loaingo, loaiduong, phuong, quan, noithat, area, floors, bedrooms, bathrooms):
    # Khởi tạo mảng đặc trưng với kích thước tương ứng
    x = np.zeros(len(__data_columns))

    # Gán giá trị cho các cột liên quan đến diện tích, số tầng, số phòng ngủ, số toilet
    x[21] = area        # Giả sử cột đầu tiên là diện tích
    x[22] = floors  # Giả sử cột thứ hai là số toilet
    x[23] = bedrooms     # Giả sử cột thứ ba là số phòng ngủ
    x[24] = bathrooms
    # Thiết lập giá trị cho giấy tờ pháp lý
    x[__data_columns.index('giấy tờ pháp lý')] = 1 if giayto else 0
    
    # Thiết lập giá trị cho thang máy
    x[__data_columns.index('thang máy')] = 1 if thangmay else 0
    
    # Thiết lập giá trị cho gara
    x[__data_columns.index('gara để ô tô')] = 1 if gara else 0
    
    # Thiết lập giá trị cho vỉa hè
    x[__data_columns.index('vỉa hè đỗ ô tô')] = 1 if viahe else 0
    
    # Thiết lập giá trị cho các đặc trưng one-hot encoding
    if loaingo in __loaingo:
        x[__loaingo.index(loaingo) + 190] = 1  # Adjusted index for one-hot encoding
    if loaiduong in __loaiduong:
        x[__loaiduong.index(loaiduong) + 197] = 1  # Adjusted index for one-hot encoding
    if phuong in __phuong:
        x[__phuong.index(phuong) + 25] = 1  # Adjusted index for one-hot encoding
    if quan in __quan:
        x[__quan.index(quan) + 201] = 1  # Adjusted index for one-hot encoding


    # Thiết lập giá trị cho các đặc trưng gần kề
    x[__data_columns.index('gần bệnh viện')] = 1 if benhvien else 0
    x[__data_columns.index('gần chợ')] = 1 if cho else 0
    x[__data_columns.index('gần trường tiểu học')] = 1 if th else 0
    x[__data_columns.index('gần trường trung học cơ sở')] = 1 if thcs else 0
    x[__data_columns.index('gần trường trung học phổ thông')] = 1 if thpt else 0
    x[__data_columns.index('gần đại học')] = 1 if dh else 0
    x[__data_columns.index('gần siêu thị trung tâm mua sắm')] = 1 if sieuthi else 0
    x[__data_columns.index('gần bến xe')] = 1 if benxe else 0
    x[__data_columns.index('gần công an phường')] = 1 if ca else 0
    x[__data_columns.index('gần ủy ban nhân dân')] = 1 if ubnd else 0
    x[__data_columns.index('gần bãi đỗ xe')] = 1 if baixe else 0
    x[__data_columns.index('gần công viên')] = 1 if congvien else 0

    # Thiết lập giá trị cho quy hoạch và nội thất đầy đủ
    x[__data_columns.index('pccc')] = 1 if pccc else 0
    x[__data_columns.index('quy hoạch')] = 1 if qh else 0
    x[__data_columns.index('nội thất đầy đủ')] = 1 if noithat else 0


    return round(__model.predict([x])[0],2)

def get_phuong_names():
    return __phuong
def get_quan_names():
    return __quan
def get_loaingo_names():
    return __loaingo
def get_loaiduong_names():
    return __loaiduong

def load_saved_artifacts():
    print("loading saved artifacts...start")
    global  __data_columns
    global __phuong
    global __quan
    global __loaingo
    global __loaiduong

    with open("c:/Users/hieub/HN/server/artifacts/columns.json", "r", encoding='utf-8') as f:
        __data_columns = json.load(f)['data_columns']
        __phuong = __data_columns[25:190]
        __quan = __data_columns[201:]
        __loaingo = __data_columns[190:197]
        __loaiduong = __data_columns[197:201]
    
    global __model
    with open('c:/Users/hieub/HN/server/artifacts/hanoi1_home_prices_model.pickle', 'rb') as f:
        __model = pickle.load(f)
    print("loading saved artifacts...done")

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_phuong_names())
    print(get_estimated_price(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 'ngõ xe ba gác tránh', 'không có thông tin loại đường', 'mỹ đình', 'nam từ liêm', 1, 51, 5, 7, 8))
    print(get_estimated_price(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 'ngõ xe ba gác tránh', 'không có thông tin loại đường', 'hoàng văn thụ', 'hoàng mai', 1, 100, 5, 4, 5))
