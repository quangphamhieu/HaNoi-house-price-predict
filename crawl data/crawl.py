import time
import pandas as pd
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import google.generativeai as genai

# Thiết lập API key
API_KEY = ''  # Your API key 
genai.configure(api_key=API_KEY)

# Tạo mô hình sử dụng gemini-1.5-flash
model = genai.GenerativeModel("gemini-1.5-flash")

def clean_response_text(response_text):
    # Bỏ dòng chứa tiêu đề không cần thiết
    cleaned_lines = []
    for line in response_text.split('\n'):
        line = line.replace("*", "").replace("/", "").replace('"', "").replace("+", "").replace("-", "").replace(",", "").strip()
        
        if ":" in line:
            # Kiểm tra nếu là một cặp key:value thì giữ lại
            cleaned_lines.append(line)
    
    # Ghép các dòng đã xử lý lại thành đoạn text
    return "\n".join(cleaned_lines)

def get_description_dict(description1, description2):
    # Tạo prompt mới nếu cần thiết
    prompt = f'''Tôi có thông tin mô tả của 1 căn nhà. Bạn hãy đọc và trả về dưới dạng key:value các thông tin sau (cố gắng tự hiểu, tự tìm ra và đưa ra hợp lý nhé, nhiều thông tin viết tắt lắm nên cố hiểu nhé). Đây là các key mà bạn sẽ trả về :
                -'thang máy'(trả lời câu hỏi 'căn nhà có thang máy không'):value là 'có' hoặc 'không' (có thể sẽ không xuất hiện thông tin giống hệt nên chỉ cần xuất hiện từ 'thang máy' hay 'TM' thì xác định value là có luôn)
                -'gara để ô tô'(trả lời câu hỏi 'nhà có để ô tô được không'):value là 'có' hoặc 'không' (có thể sẽ không xuất hiện thông tin giống hệt nên chỉ cần xuất hiện từ 'hầm để xe' hay 'gara đỗ ô tô' hay 'nhà để ô tô' hay 'ô tô đỗ trong nhà' nói chung là liên quan đến việc để ô tô trong nhà thì xác định value là có luôn)
                -'vỉa hè đỗ ô tô'(trả lời câu hỏi 'trước nhà có vỉa hè hay nơi đỗ ô tô không'):value là 'có' hoặc 'không' (có thể sẽ không xuất hiện thông tin giống hệt nên chỉ cần xuất hiện từ 'vỉa hè' hay 'đỗ ô tô trước cửa' nói chung là thông tin liên quan đến việc để ô tô trước cửa nhà thì xác định value là có luôn)
                -'nhà 2 mặt tiền'(trả lời câu hỏi 'nhà có mấy mặt tiền'):value là 'có' hoặc 'không' (có thể sẽ không xuất hiện thông tin giống hệt nên chỉ cần xuất hiện từ '2 mặt tiền' hay '2 mặt' thì xác định value là có luôn)
                -'nhà 3 mặt tiền'(trả lời câu hỏi 'trước nhà có vỉa hè hay nơi đỗ ô tô không'):value là 'có' hoặc 'không' (có thể sẽ không xuất hiện thông tin giống hệt nên chỉ cần xuất hiện từ '3 mặt tiền' hay '3 mặt' thì xác định value là có luôn)
                -'nội thất'(trả lời câu hỏi 'nhà có đủ nội thất không'):value là 'có' hoặc 'không' (có thể sẽ không xuất hiện thông tin giống hệt nên chỉ cần xuất hiện từ 'nội thất' hay 'nội thất đầy đủ' thì xác định value là có luôn)
                -'PCCC'(trả lời câu hỏi 'nhà có hệ thống phòng cháy chữa cháy không'):value là 'có' hoặc 'không' (có thể sẽ không xuất hiện thông tin giống hệt nên chỉ cần xuất hiện từ 'PCCC' hay 'hệ thống báo cháy' nói chung là thông tin liên quan đến hệ thống phòng cháy chữa thì xác định value là có luôn)
                -'Quy hoạch'(trả lời câu hỏi 'nhà có quy hoạch không'):value là 'có' hoặc 'không' (có thể sẽ không xuất hiện thông tin giống hệt nên chỉ cần xuất hiện từ 'quy hoạch' hay 'QH' thì xác định value là có luôn, tất nhiên là cũng phải xem trước đó có xuất hiện từ 'không' không giả sử có cụm 'không nằm trong quy hoạch' thì value sẽ là 'không')
                -'gần bệnh viện'(trả lời câu hỏi 'nhà có gần bệnh viện không'):value là 'có' hoặc 'không' (có thể sẽ không xuất hiện thông tin giống hệt nên chỉ cần xuất hiện từ 'bệnh viện' hay 'BV' thì xác định value là có luôn)
                -'gần chợ'(trả lời câu hỏi 'nhà có chợ không'):value là 'có' hoặc 'không' (có thể sẽ không xuất hiện thông tin giống hệt nên chỉ cần xuất hiện từ 'chợ' thì xác định value là có luôn)
                -'gần trường tiểu học'(trả lời câu hỏi 'nhà có gần trường tiểu học không'):value là 'có' hoặc 'không' (có thể sẽ không xuất hiện thông tin giống hệt nên chỉ cần xuất hiện từ 'tiểu học' hay 'TH' thì xác định value là có luôn)
                -'gần trường trung học cơ sở'(trả lời câu hỏi 'nhà có gần trường trung học cơ sở không'):value là 'có' hoặc 'không' (có thể sẽ không xuất hiện thông tin giống hệt nên chỉ cần xuất hiện từ 'trung học cơ sở' hay 'THCS' thì xác định value là có luôn)
                -'gần trường trung học phổ thông'(trả lời câu hỏi 'nhà có gần trung học phổ thông không'):value là 'có' hoặc 'không' (có thể sẽ không xuất hiện thông tin giống hệt nên chỉ cần xuất hiện từ 'trung học phổ thông' hay 'THPT' thì xác định value là có luôn)
                -'gần đại học'(trả lời câu hỏi 'nhà có gần đại học không'):value là 'có' hoặc 'không' (có thể sẽ không xuất hiện thông tin giống hệt nên chỉ cần xuất hiện từ 'đại học' hay 'ĐH' thì xác định value là có luôn)
                -'gần siêu thị, trung tâm mua sắm'(trả lời câu hỏi 'nhà có gần trung tâm thương mai không'):value là 'có' hoặc 'không' (có thể sẽ không xuất hiện thông tin giống hệt nên chỉ cần xuất hiện từ 'siêu thị' hay 'tttm' hay 'mall' hay 'vincome' hay 'aeon' hay 'big c' thì xác định value là có luôn)
                -'gần bến xe'(trả lời câu hỏi 'nhà có gần bến xe không'):value là 'có' hoặc 'không' (có thể sẽ không xuất hiện thông tin giống hệt nên chỉ cần xuất hiện từ 'bến xe' thì xác định value là có luôn)
                -'gần công an phường'(trả lời câu hỏi 'nhà có gần công an phường không'):value là 'có' hoặc 'không' (có thể sẽ không xuất hiện thông tin giống hệt nên chỉ cần xuất hiện từ 'công an phường' hay 'CA phường' thì xác định value là có luôn)
                -'gần ủy ban nhân dân'(trả lời câu hỏi 'nhà có gần ủy ban nhân dân phường không'):value là 'có' hoặc 'không' (có thể sẽ không xuất hiện thông tin giống hệt nên chỉ cần xuất hiện từ 'ủy ban nhân dân' hay 'UBND' thì xác định value là có luôn)
                -'gần bãi đỗ xe'(trả lời câu hỏi 'gần nhà có bãi đỗ xe ô tô nào không'): value là 'có' hoặc 'không' (có thể sẽ không xuất hiện thông tin giống hệt nên chỉ cần xuất hiện từ 'bãi xe' hay 'bãi đỗ xe' thì xác định value là có luôn)
                -'gần công viên'(trả lời câu hỏi 'nhà có gần công viên không'):value là 'có' hoặc 'không' (có thể sẽ không xuất hiện thông tin giống hệt nên chỉ cần xuất hiện từ 'công viên' hay 'cv' thì xác định value là có luôn)
                -'loại ngõ'(trả lời câu hỏi 'nhà nằm trong ngõ thuộc loại nào'):value là 1 trong những cái sau:'ngõ thông tứ tung'(loại ngõ nối liền nhiều đường nhiều ngõ khác nhau, thông sang các nơi khác), 'ngõ cụt, nông'(loại ngõ không đi được sang ngõ khác, đi đến cuối không đi được tiếp ) 'ngõ hẹp'(chỉ đủ 1 xe máy hay rộng dưới 1m), 'ngõ 2 xe máy tránh nhau' (loại ngõ đủ để 2 xe đi tránh nhau hay ngõ rộng từ 1m đến 2m), 'ngõ xe ba gác tránh' (rộng hơn ngõ 2 xe máy tránh nhau 1 tí), 'ngõ ô tô tránh' (loại ngõ đủ cho 1 ô tô đi vào, rộng khoảng 2m đến 3m), ngõ 2 ô tô tránh nhau (loại ngõ đủ rộng để cho 2 ô tô đi ngược chiều cùng đi vào, rộng khoảng 5m giống như phố) (có thể sẽ xuất hiện nhiều thông tin không trùng khớp như 'ngõ ô tô tải tránh' thì bạn phải tự xem xét nó phù hợp với cái nào rồi cho vào loại ngõ phù hợp nhé và nếu không có thông tin nào về loại ngõ thì value sẽ là 'không')
                -'loại đường'(trả lời câu hỏi 'nhà nằm trên đường như thế nào'):value là 1 trong những cái sau:'đường hẹp'(loại đường chỉ đủ để 2 3 xe máy cùng đi, hay chỉ đủ 1 ô tô và 1 xe máy, rộng khoảng 4m trở xuống), 'đường 2 ô tô tránh nhau' (loại đường đủ 2 ô tô đi ngược chiều nhau, rộng khoảng 4m đến 8m), đường rộng (loại đường đủ từ 4 ô tô trở lên, rộng khoảng 10m trở lên) (có thể xuất hiện thông tin không trùng khớp như 'đường ô tô tải tránh' thì bạn tự xem xét cho vào loại đường phù hợp nhé và nếu không có thông tin nào vè loại đường thì value sẽ là 'không' )
    Nhớ đấy chỉ trả về các key này thôi, đúng định dạng chữ tôi đã viết vì nếu khác ( 'thang máy' và 'Thang máy' là 2 key khác nhau) thì sẽ sai và đừng sinh thêm key linh tinh nào ngoài những cái tôi đã liệt kê ở trên. Và value trả về đúng dạng tôi đã nêu: 'có' hoặc 'không' (trừ key 'loại ngõ' và 'loại đường' có nhiều value khác những nhớ vẫn đúng những gì tôi đã nêu và nếu không có thông tin về loại ngõ hay loại đường thì value là 'không' nhé) 
    Dưới đây là mô tả căn nhà:
    \n{description1}\n{description2}'''
    
    try:
        # Gọi API Gemini
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        cleaned_text = clean_response_text(response_text)
        description_dict = {}
        for line in cleaned_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                description_dict[key.strip()] = value.strip()
        return description_dict
    except Exception as e:
        print(f"Lỗi khi gọi API: {e}")
        return None

# Khởi tạo trình duyệt với undetected_chromedriver
browser = uc.Chrome()

# Danh sách chứa tất cả các URL của căn hộ
all_urls = []

# Đặt số trang bạn muốn quét
num_pages = 50  # Số lượng trang cần quét

# Duyệt qua từng trang để lấy các liên kết
for page in range(1, num_pages + 1):
    if page == 1:
        url = 'https://batdongsan.com.vn/ban-nha-rieng-thanh-xuan'
    else:
        url = f'https://batdongsan.com.vn/ban-nha-rieng-thanh-xuan/p{page}'

    browser.get(url)
    time.sleep(5)  # Đợi trang tải hoàn toàn
    
    house_links = browser.find_elements(By.XPATH, '//a[@class="js__product-link-for-product-id"]')
    urls = [link.get_attribute('href') for link in house_links]
    all_urls.extend(urls)

# Tạo danh sách để chứa các kết quả
results = []

# Duyệt qua từng URL để lấy thông tin chi tiết
test_urls = all_urls[:10]  # Thay đổi số lượng URL ở đây để quét nhiều hơn

for url in all_urls:
    browser.get(url)
    time.sleep(4)  # Đợi trang tải hoàn toàn
    try:
        head = browser.find_element(By.XPATH, '//h1[@class="re__pr-title pr-title js__pr-title"]').text
    except:
        print(f"Head not found for URL: {url}")
        continue
    
    try:
        fronth = browser.find_element(By.XPATH, '//span[contains(text(),"Mặt tiền")]/following-sibling::span').text
    except:
        fronth = "Not found"
    
    try:
        sugar = browser.find_element(By.XPATH, '//span[contains(text(),"Đường vào")]/following-sibling::span').text
    except:
        sugar = "Not found"
    
    try:
        home = browser.find_element(By.XPATH, '//span[contains(text(),"Hướng nhà")]/following-sibling::span').text
    except:
        home = "Not found"
    
    try:
        balcony = browser.find_element(By.XPATH, '//span[contains(text(),"Hướng ban công")]/following-sibling::span').text
    except:
        balcony = "Not found"
        
    try:
        toilet = browser.find_element(By.XPATH, '//span[contains(text(),"Số toilet")]/following-sibling::span').text
    except:
        toilet = "Not found"
    try:
        furniture = browser.find_element(By.XPATH, '//span[contains(text(),"Nội thất")]/following-sibling::span').text
    except:
        furniture = "Not found"
    try:
        date = browser.find_element(By.XPATH, '//div[@class="re__pr-short-info-item js__pr-config-item"]//span[@class="title" and contains(text(),"Ngày đăng")]/following-sibling::span[@class="value"]').text
    except:
        date = "Not found"

    try:
        address = browser.find_element(By.XPATH, '//span[@class="re__pr-short-description js__pr-address"]').text
    except:
        address = "Not found"

    try:
        area = browser.find_element(By.XPATH, '//span[@class="re__pr-specs-content-item-value"]').text
    except:
        area = "Not found"

    try:
        price = browser.find_element(By.XPATH, '//span[contains(text(),"Mức giá")]/following-sibling::span').text
    except:
        price = "Not found"

    try:
        legal_documents = browser.find_element(By.XPATH, '//span[contains(text(),"Pháp lý")]/following-sibling::span').text
    except:
        legal_documents = "Not found"

    try:
        floor = browser.find_element(By.XPATH, '//span[contains(text(),"Số tầng")]/following-sibling::span').text
    except:
        floor = "Not found"

    try:
        bedroom = browser.find_element(By.XPATH, '//span[contains(text(),"Số phòng ngủ")]/following-sibling::span').text
    except:
        bedroom = "Not found"

    try:
        div_content = browser.find_element(By.CLASS_NAME, 're__section-body')
        content = div_content.text
    except:
        content = "Not found"

    try:
        iframes = browser.find_elements(By.TAG_NAME, 'iframe')
        iframe_src = None
        
        for iframe in iframes:
            src = iframe.get_attribute('data-src') or iframe.get_attribute('src')
            if src and "google.com/maps/embed/v1/place" in src:
                iframe_src = src
                break
        
        if iframe_src and "q=" in iframe_src:
            coordinates = iframe_src.split("q=")[-1].split("&")[0]
        else:
            coordinates = "Not found"
    except:
        coordinates = "Not found"

    # Gọi API Gemini để chuyển đổi mô tả thành JSON
    descriptions_json = get_description_dict(head, content)
    # In ra JSON để kiểm tra
    # Thêm kết quả vào danh sách, và bổ sung các cột từ JSON
    result = {
        'Ngày đăng': date,
        'Tiêu đề': head,
        'Địa chỉ': address,
        'Diện tích': area,
        'Giá tiền': price,
        'Giấy tờ pháp lý': legal_documents,
        'Số tầng': floor,
        'Số phòng ngủ': bedroom,
        'Số toilet': toilet,
        'Vị trí': coordinates,
        'Mô tả': content,
        'Mặt tiền': fronth,
        'Đường vào': sugar,
        'Hướng nhà': home,
        'Hướng ban công': balcony,
        'Nội thất': furniture,
    }
    
    # Nếu có dữ liệu JSON hợp lệ, thêm các cột mới từ JSON
    if descriptions_json:
        for key, value in descriptions_json.items():
            result[key] = value  # Thêm từng cột vào kết quả

    results.append(result)

# Đóng trình duyệt khi hoàn tất
browser.quit()

# Chuyển kết quả thành DataFrame
df = pd.DataFrame(results)

# Xuất kết quả ra file Excel
df.to_excel('ThanhXuanNhaRieng.xlsx', index=False)
