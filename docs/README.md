<div align="center">

# Lab 1: Khám Phá & Phân Tích Đặc Tính Dữ Liệu Chuỗi Thời Gian
### Phân tích Tự tương quan (ACF/PACF), Kiểm định White Noise, Phân rã Chuỗi (STL), Tiền Xử Lý & Trực Quan Hóa Dữ Liệu

<p>
  <img src="https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python" alt="Python" />
  <img src="https://img.shields.io/badge/Jupyter-Notebook-orange?style=for-the-badge&logo=jupyter" alt="Jupyter Notebook" />
  <img src="https://img.shields.io/badge/Topic-Time--Series%20Analysis-brightgreen?style=for-the-badge" alt="Time-Series" />
  <img src="https://img.shields.io/badge/Library-Statsmodels%20%7C%20Pandas%20%7C%20Numpy-purple?style=for-the-badge" alt="Libraries" />
</p>

| Thuộc tính | Chi tiết |
|---|---|
| **Notebook chính** | [`scripts/main.ipynb`](../scripts/main.ipynb) |
| **Script sinh dữ liệu khuyết** | [`scripts/missvl.py`](../scripts/missvl.py) (Tạo 1% missing MCAR) |
| **Dữ liệu thô (Raw data)** | [`data/raw/daily-min-temperatures.csv`](../data/raw/daily-min-temperatures.csv) (3650 dòng, Melbourne 1981–1990) |
| **Dữ liệu đã xử lý (Processed)**| [`data/processed/daily-min-temperatures-missing.csv`](../data/processed/daily-min-temperatures-missing.csv) |

</div>

---

## 1. Giới Thiệu Dự Án

Dự án này tập trung vào giai đoạn **EDA (Exploratory Data Analysis) và Tiền xử lý dữ liệu chuỗi thời gian**, khảo sát 10 năm dữ liệu nhiệt độ tối thiểu hàng ngày tại thành phố Melbourne (Úc).

Mục tiêu chính bao gồm:
* Khảo sát cấu trúc tự tương quan (ACF, PACF) để định danh bậc mô hình.
* Thực hiện kiểm định đối chứng với White Noise (Nhiễu trắng).
* Phân rã chuỗi thời gian (STL Loess) thành các thành phần Trend, Seasonal và Residual.
* Phát hiện và xử lý dữ liệu khuyết thiếu (Missing values) và dữ liệu ngoại lai (Outliers).
* Trực quan hóa đặc trưng mùa vụ và phân phối qua biểu đồ đa chiều.

---

## 2. Cấu Trúc Thư Mục

```text
Lab1_Timeseries/
├── data/
│   ├── raw/
│   │   └── daily-min-temperatures.csv              # 3650 quan sát nhiệt độ gốc
│   └── processed/
│       └── daily-min-temperatures-missing.csv      # Dữ liệu khuyết 1% sau tiền xử lý
├── scripts/
│   ├── main.ipynb                                  # Jupyter Notebook thực hành (Bài 1 -> Bài 5)
│   └── missvl.py                                   # Script mô phỏng dữ liệu khuyết
└── docs/
    ├── README.md                                   # Trang chủ tài liệu & chỉ mục (file này)
    ├── 01_data_preprocessing.md                    # Tài liệu kỹ thuật: Missing Value & Outliers
    ├── 02_eda_and_visualization.md                 # Tài liệu trực quan hóa & Phân tích mùa vụ
    ├── 03_statistical_analysis.md                  # Lý thuyết & Kiểm định: ACF/PACF, White Noise, STL
    └── report.md                                   # Báo cáo tổng hợp hoàn chỉnh (Sẵn sàng xuất PDF)
```

---

## 3. Danh Mục Tài Liệu Chi Tiết

Hệ thống tài liệu đã được phân tách thành từng chuyên đề cụ thể:

* 📘 **[01. Tiền Xử Lý Dữ Liệu (Data Preprocessing)](01_data_preprocessing.md)**  
  Chi tiết về phương pháp tạo dữ liệu khuyết 1%, phân tích so sánh Forward-fill vs Linear Interpolation, các thuật toán phát hiện Outliers (Z-score, IQR) và lý do giữ lại các giá trị nhiệt độ cực đoan.

* 📊 **[02. Khám Phá & Trực Quan Hóa (EDA & Visualization)](02_eda_and_visualization.md)**  
  Phân tích đồ thị toàn chuỗi, Rolling Statistics (Mean & Std trượt theo chu kỳ 12), Seasonal line plot theo tháng, Heatmap Seasonality và tích hợp Boxplot đa chiều.

* 📈 **[03. Phân Tích Thống Kê Chuỗi Thời Gian (Statistical Analysis)](03_statistical_analysis.md)**  
  Công thức và thực nghiệm ACF/PACF, cơ sở lựa chọn mô hình tự hồi quy AR(1), kiểm định tiêu chuẩn White Noise trên 3 kịch bản, và phân tích các thành phần Loess trong STL.

* 📑 **[Báo Cáo Tổng Hợp (Dùng để xuất PDF)](report.md)**  
  Văn bản báo cáo học thuật chuẩn hóa tổng kết tất cả phát hiện quan trọng, bảng số liệu và đề xuất định hướng mô hình hóa cho các bước tiếp theo.

---

## 4. Hướng Dẫn Cài Đặt & Thực Thi

### 4.1. Thiết lập môi trường
```bash
pip install numpy pandas matplotlib statsmodels seaborn
```

### 4.2. Khởi chạy thực nghiệm
* Chạy Notebook chính:
  ```bash
  jupyter notebook scripts/main.ipynb
  ```
* (Tùy chọn) Tái tạo dữ liệu khuyết thiếu:
  ```bash
  python scripts/missvl.py
  ```
