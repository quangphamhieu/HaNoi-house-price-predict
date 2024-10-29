from flask import Flask, request, jsonify
import util

app = Flask(__name__)
@app.route('/get_phuong_names', methods=['GET'])
def get_phuong_names():
    response = jsonify({
        'phuong': util.get_phuong_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
@app.route('/get_quan_names', methods=['GET'])
def get_quan_names():
    response = jsonify({
        'quan': util.get_quan_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
@app.route('/get_loaingo_names', methods=['GET'])
def get_loaingo_names():
    response = jsonify({
        'loaingo': util.get_loaingo_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
@app.route('/get_loaiduong_names', methods=['GET'])
def get_loaiduong_names():
    response = jsonify({
        'loaiduong': util.get_loaiduong_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    area = float(request.form['area'])
    floors = int(request.form['floors'])
    bedrooms = int(request.form['bedrooms'])
    bathrooms = int(request.form['bathrooms'])
    giayto = int(request.form.get('giayto', '0'))
    thangmay = int(request.form.get('thangmay', '0'))
    gara = int(request.form.get('gara', '0'))
    viahe = int(request.form.get('viahe', '0'))
    two_mat = int(request.form.get('two_mat', '0'))
    three_mat = int(request.form.get('three_mat', '0'))
    pccc = int(request.form.get('pccc', '0'))
    qh = int(request.form.get('qh', '0'))
    benhvien = int(request.form.get('benhvien', '0'))
    cho = int(request.form.get('cho', '0'))
    th = int(request.form.get('th', '0'))
    thcs = int(request.form.get('thcs', '0'))
    thpt = int(request.form.get('thpt', '0'))
    dh = int(request.form.get('dh', '0'))
    sieuthi = int(request.form.get('sieuthi', '0'))
    benxe = int(request.form.get('benxe', '0'))
    ca = int(request.form.get('ca', '0'))
    ubnd = int(request.form.get('ubnd', '0'))
    baixe = int(request.form.get('baixe', '0'))
    congvien = int(request.form.get('congvien', '0')) 
    noithat = int(request.form.get('noithat', '0'))


    loaingo = request.form.get('loaingo')
    loaiduong = request.form.get('loaiduong')
    phuong = request.form.get('phuong')
    quan = request.form.get('quan')
    
    
    
    response = jsonify({
        'estimated_price': util.get_estimated_price(giayto, thangmay, gara, viahe, two_mat, three_mat, pccc, qh, benhvien, cho, th, thcs, thpt, dh, sieuthi, benxe, ca, ubnd, baixe, congvien, loaingo, loaiduong, phuong, quan, noithat, area, floors, bedrooms, bathrooms)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run()
    