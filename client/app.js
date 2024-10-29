function onClickedEstimatePrice() {
    console.log("Estimate price button clicked");
    var area = document.getElementById("area").value;
    var floors = document.getElementById("floors").value;
    var bedrooms = document.getElementById("bedrooms").value;
    var bathrooms = document.getElementById("bathrooms").value;
    var giayto = document.getElementById("giayto").checked ? 1 : 0;
    var thangmay = document.getElementById("thangmay").checked ? 1 : 0;
    var gara = document.getElementById("gara").checked ? 1 : 0;
    var viahe = document.getElementById("viahe").checked ? 1 : 0;
    var two_mat = document.getElementById("two_mat").checked ? 1 : 0;
    var three_mat = document.getElementById("three_mat").checked ? 1 : 0;
    var pccc = document.getElementById("pccc").checked ? 1 : 0;
    var qh = document.getElementById("qh").checked ? 1 : 0;
    var benhvien = document.getElementById("benhvien").checked ? 1 : 0;
    var cho = document.getElementById("cho").checked ? 1 : 0;
    var th = document.getElementById("th").checked ? 1 : 0;
    var thcs = document.getElementById("thcs").checked ? 1 : 0;
    var thpt = document.getElementById("thpt").checked ? 1 : 0;
    var dh = document.getElementById("dh").checked ? 1 : 0;
    var sieuthi = document.getElementById("sieuthi").checked ? 1 : 0;
    var benxe = document.getElementById("benxe").checked ? 1 : 0;
    var ca = document.getElementById("ca").checked ? 1 : 0;
    var ubnd = document.getElementById("ubnd").checked ? 1 : 0;
    var baixe = document.getElementById("baixe").checked ? 1 : 0;
    var congvien = document.getElementById("congvien").checked ? 1 : 0;
    var noithat = document.getElementById("noithat").checked ? 1 : 0;
    var loaingo = document.getElementById("loaingo").value;
    var loaiduong = document.getElementById("loaiduong").value;
    var phuong = document.getElementById("phuong").value;
    var quan = document.getElementById("quan").value;

    var url = "http://127.0.0.1:5000/predict_home_price";

    $.post(url, {
        area: parseFloat(area),
        floors: parseInt(floors),
        bedrooms: parseInt(bedrooms),
        bathrooms: parseInt(bathrooms),
        giayto: giayto,
        thangmay: thangmay,
        gara: gara,
        viahe: viahe,
        two_mat: two_mat,
        three_mat: three_mat,
        pccc: pccc,
        qh: qh,
        benhvien: benhvien,
        cho: cho,
        th: th,
        thcs: thcs,
        thpt: thpt,
        dh: dh,
        sieuthi: sieuthi,
        benxe: benxe,
        ca: ca,
        ubnd: ubnd,
        baixe: baixe,
        congvien: congvien,
        noithat: noithat,
        loaingo: loaingo,
        loaiduong: loaiduong,
        phuong: phuong,
        quan: quan
    }, function(data, status) {
        console.log("Response: ", data.estimated_price);
        document.getElementById("uiEstimatedPrice").innerHTML = "<h2>" + data.estimated_price + "tỷ VND</h2>";
    }).fail(function(xhr, status, error) {
        console.error("Có lỗi xảy ra:", error);
        document.getElementById("uiEstimatedPrice").innerHTML = "<h2>Lỗi: Không thể dự đoán giá</h2>";
    });
}


function loadPhuongNames() {
    const url = "http://127.0.0.1:5000/get_phuong_names"; 
    fetch(url)
      .then(response => response.json())
      .then(data => {
        if (data.phuong) {
          const phuongSelect = document.getElementById("phuong");
          phuongSelect.innerHTML = ""; 
          data.phuong.forEach(phuong => {
            const option = document.createElement("option");
            option.value = phuong;
            option.text = phuong;
            phuongSelect.add(option);
          });
        }
      })
      .catch(error => console.error("Có lỗi xảy ra:", error));
  }
  

function loadQuanNames() {
    const url = "http://127.0.0.1:5000/get_quan_names"; 
    fetch(url)
      .then(response => response.json())
      .then(data => {
        if (data.quan) {
          const quanSelect = document.getElementById("quan");
          quanSelect.innerHTML = ""; 
          data.quan.forEach(quan => {
            const option = document.createElement("option");
            option.value = quan;
            option.text = quan;
            quanSelect.add(option);
          });
        }
      })
      .catch(error => console.error("Có lỗi xảy ra:", error));
}

// Hàm lấy danh sách loại ngõ từ API
function loadLoaiNgo() {
    const url = "http://127.0.0.1:5000/get_loaingo_names"; // Đảm bảo URL là chính xác
    fetch(url)
      .then(response => response.json())
      .then(data => {
        if (data.loaingo) {
          const loaingoSelect = document.getElementById("loaingo");
          loaingoSelect.innerHTML = ""; // Xóa các lựa chọn cũ
          data.loaingo.forEach(loaingo => {
            const option = document.createElement("option");
            option.value = loaingo;
            option.text = loaingo;
            loaingoSelect.add(option);
          });
        }
      })
      .catch(error => console.error("Có lỗi xảy ra:", error));
}

// Hàm lấy danh sách loại đường từ API
function loadLoaiDuong() {
    const url = "http://127.0.0.1:5000/get_loaiduong_names"; // Đảm bảo URL là chính xác
    fetch(url)
      .then(response => response.json())
      .then(data => {
        if (data.loaiduong) {
          const loaiduongSelect = document.getElementById("loaiduong");
          loaiduongSelect.innerHTML = ""; // Xóa các lựa chọn cũ
          data.loaiduong.forEach(loaiduong => {
            const option = document.createElement("option");
            option.value = loaiduong;
            option.text = loaiduong;
            loaiduongSelect.add(option);
          });
        }
      })
      .catch(error => console.error("Có lỗi xảy ra:", error));
}


// Gọi tất cả các hàm khi trang được tải
window.onload = () => {
    loadPhuongNames();
    loadQuanNames();
    loadLoaiNgo();
    loadLoaiDuong();
    onClickedEstimatePrice();
    
};
  
