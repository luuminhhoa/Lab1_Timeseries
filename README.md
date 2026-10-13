<div align="center">

# Lab 1: Khám Phá & Phân Tích Đặc Tính Dữ Liệu Chuỗi Thời Gian
### Phân tích Tự tương quan (ACF/PACF), Kiểm định White Noise, Phân rã Chuỗi (STL), Xử lý Chất lượng Dữ liệu & Trực quan hóa

<p>
  <img src="https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python" alt="Python" />
  <img src="https://img.shields.io/badge/Jupyter-Notebook-orange?style=for-the-badge&logo=jupyter" alt="Jupyter Notebook" />
  <img src="https://img.shields.io/badge/Topic-Time--Series%20Analysis-brightgreen?style=for-the-badge" alt="Time-Series" />
  <img src="https://img.shields.io/badge/Library-Statsmodels%20%7C%20Pandas-purple?style=for-the-badge" alt="Libraries" />
</p>

| Hạng mục | Chi tiết |
|---|---|
| **Notebook chính** | `notebooks/main.ipynb` |
| **Script bổ trợ** | `notebooks/missvl.py` (Mô phỏng missing value 1%) |
| **Dữ liệu** | `data/raw/daily-min-temperatures.csv` (3650 quan sát nhiệt độ tối thiểu tại Melbourne) |
| **Dữ liệu đã xử lý** | `data/processed/daily-min-temperatures-missing.csv` |

</div>

---

## 1. Giới thiệu tổng quan

Dự án thực hiện khám phá, phân tích thống kê và tiền xử lý chuỗi thời gian khí hậu Melbourne giai đoạn 1981–1990 qua 5 bài thực hành:
1. **Phân tích ACF / PACF:** Đo lường độ phụ thuộc quá khứ và nhận diện bậc mô hình tự hồi quy.
2. **Kiểm định White Noise:** So sánh chuỗi thực tế với nhiễu trắng qua dải tin cậy 95%.
3. **Phân rã chuỗi STL:** Tách 3 thành phần Xu hướng (Trend), Mùa vụ (Seasonal) và Phần dư (Residual).
4. **Kiểm tra & Xử lý chất lượng dữ liệu:** Phát hiện ngoại lai (Outliers) và xử lý dữ liệu khuyết thiếu (Missing values).
5. **Trực quan hóa nâng cao:** Khảo sát biến động qua Rolling statistics, Seasonal plot và Heatmap.

---

## 2. Cấu trúc thư mục

```text
Lab1_Timeseries/
├── README.md
├── data/
│   ├── raw/
│   │   └── daily-min-temperatures.csv              # Dữ liệu gốc (3650 dòng)
│   └── processed/
│       └── daily-min-temperatures-missing.csv      # Dữ liệu khuyết thiếu giả lập (1% NaN)
└── notebooks/
    ├── main.ipynb                                  # Notebook thực hành chính (Bài 1 -> Bài 5)
    └── missvl.py                                   # Script tạo missing value ngẫu nhiên
```

---

## 3. Tóm tắt kết quả 5 bài thực hành

### 📌 Bài tập 1: Tính và phân tích ACF / PACF
- **Tự tương quan:** Chuỗi có mức độ tự tương quan rất mạnh và kéo dài. Hệ số ACF tại lag 1 đạt **~0.774**, giảm chậm qua 40 lag và toàn bộ đều nằm ngoài dải tin cậy.
- **Lag quan trọng nhất:** Biểu đồ PACF cắt cụt đột ngột ngay sau lag 1 ($PACF_1 \approx 0.774$, từ lag 2 giảm mạnh về $< 0.19$). Đây là dấu hiệu điển hình của mô hình tự hồi quy **AR(1)**: $y_t$ phụ thuộc trực tiếp chủ yếu vào $y_{t-1}$.
- **Mùa vụ & Xu hướng:** ACF giảm thoai thoải phản ánh quán tính nhiệt độ theo mùa (lặp lại theo chu kỳ 365 ngày); chuỗi dao động quanh mức trung bình năm mà không có xu hướng dốc lên/xuống dài hạn.

---

### 📌 Bài tập 2: Kiểm định White Noise (Nhiễu trắng)
- **Phương pháp kiểm định:** Đánh giá tỷ lệ lag nằm trong dải tin cậy 95% $\left[\pm \frac{1.96}{\sqrt{N}}\right]$.
- **So sánh:**
  - **White Noise (1000 điểm):** ACF giảm ngay về 0 sau lag 0, có **97.5% số lag (39/40)** nằm an toàn trong dải tin cậy `[-0.0620, +0.0620]`. Chỉ 1 lag chạm biên do sai số ngẫu nhiên $(\le 5\%)$ $\rightarrow$ đạt chuẩn nhiễu trắng thuần túy.
  - **Dữ liệu nhiệt độ gốc:** Toàn bộ 40 lag đều vượt xa dải tin cậy $\rightarrow$ **không phải White Noise**, dữ liệu chứa quy luật mạnh mẽ để mô hình hóa dự báo.
  - **Thử nghiệm pha nhiễu (PA2 & PA3):** Ngay cả khi cộng thêm nhiễu hoặc thay thế 1000 điểm bằng nhiễu trắng, 100% các lag vẫn vượt ngưỡng tin cậy, chứng minh tính bền vững (robustness) của chuỗi thời gian thực tế.

---

### 📌 Bài tập 3: Phân rã chuỗi thời gian (STL Decomposition)
Chuyển đổi dữ liệu sang tần suất tháng (Monthly) và bóc tách theo mô hình cộng $Y_t = T_t + S_t + R_t$:
- **Xu hướng (Trend):** Biến động uốn lượn dài hạn: giảm từ ~12.0°C (1981) xuống đáy ~10.6°C (1983–1985), sau đó tăng lên đỉnh ~12.0°C (1988) rồi điều chỉnh nhẹ.
- **Mùa vụ (Seasonal):** Chi phối cực kỳ mạnh mẽ và ổn định qua từng năm. Biên độ dao động đều đặn từ -5.0°C đến +5.0°C (chênh lệch đỉnh - đáy lên tới 10°C).
- **Phần dư (Residual):** Dao động ngẫu nhiên quanh mức 0 (chủ yếu từ -1.5°C đến +1.5°C), tương tự White Noise $\rightarrow$ mô hình STL đã bóc tách triệt để các thành phần có quy luật.

---

### 📌 Bài tập 4: Kiểm tra và xử lý chất lượng dữ liệu

| Vấn đề | Phương pháp phát hiện / Xử lý | Kết quả & Đánh giá |
|---|---|---|
| **Outliers** | Z-score (`\|Z\| > 3`) | Phát hiện **10 điểm dị biệt** (~0.27%). |
| | IQR (`1.5 x IQR`) | Phát hiện **13 điểm dị biệt** (~0.36%, ngưỡng: `[-0.25°C, 22.55°C]`). |
| | *Đánh giá & Khuyến nghị* | Các điểm dị biệt đều ở cực nóng (22.7°C – 26.3°C) vào các tháng mùa hè. Nên dùng **Clipping/Winsorizing** để hạn chế ảnh hưởng của giá trị cực trị mà vẫn giữ nguyên cấu trúc liên tục của chuỗi. |
| **Missing Values** | Tạo giả lập 1% bằng `missvl.py` | Phát hiện **33 giá trị khuyết thiếu** (~0.9%). |
| | Forward-fill (FFill) | Tạo các bậc thang nằm ngang, làm mất biến thiên tự nhiên. |
| | Linear Interpolation | Nối mượt mà giữa các điểm lân cận $\rightarrow$ **Phương pháp tối ưu nhất** cho dữ liệu nhiệt độ liên tục. |

---

### 📌 Bài tập 5: Trực quan hóa dữ liệu chuỗi thời gian
- **Xu hướng chung:** Biểu đồ `Rolling Mean` và `Rolling Std` dao động ổn định quanh các biên độ nhất định, phản ánh chuỗi dừng hoặc dao động tuần hoàn ổn định qua 10 năm.
- **Tính mùa vụ:** Chu kỳ 12 tháng lặp lại rất rõ ràng:
  - Nhiệt độ đạt đỉnh cao nhất vào các tháng đầu năm (tháng 1, 2) và cuối năm (tháng 12).
  - Nhiệt độ chạm đáy sâu vào giữa năm (mùa đông Nam bán cầu - tháng 6, 7).
- **Điểm bất thường:** Năm 1982 ghi nhận nhiệt độ đáy tháng 7 giảm thấp bất thường (xuống gần 4.6°C). Các đỉnh của `Rolling Std` tập trung ở thời điểm giao mùa phản ánh sự chênh lệch nhiệt độ ngắn hạn.

---

## 4. Hướng dẫn chạy dự án

### Cài đặt môi trường
```bash
pip install numpy pandas matplotlib statsmodels seaborn
```

### Chạy Notebook
Khởi chạy notebook và thực thi tuần tự từ Bài 1 đến Bài 5:
```bash
jupyter notebook notebooks/main.ipynb
```

*(Tùy chọn) Chạy script tạo dữ liệu khuyết thiếu:*
```bash
python notebooks/missvl.py
```
File đầu ra sẽ được lưu tại `data/processed/daily-min-temperatures-missing.csv`.
