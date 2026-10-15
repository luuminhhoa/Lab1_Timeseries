# Tiền Xử Lý Dữ Liệu Chuỗi Thời Gian (Data Preprocessing)

Tài liệu này chi tiết hóa quy trình kiểm tra chất lượng dữ liệu, mô phỏng dữ liệu khuyết thiếu, các phương pháp nội suy và xử lý giá trị ngoại lai (outliers) được triển khai trong bài thực hành (Bài tập 4 và script [missvl.py](file:///e:/TimeSeries/Lab1_Timeseries/scripts/missvl.py)).

---

## 1. Mô Phỏng Dữ Liệu Khuyết Thiếu (Synthetic Missing Values)

### 1.1. Mục đích
Dữ liệu nhiệt độ tối thiểu gốc tại Melbourne (`daily-min-temperatures.csv`) gồm **3650 quan sát liên tục** (1981–1990) và không có giá trị khuyết. Để kiểm nghiệm năng lực của các thuật toán xử lý dữ liệu khuyết, một tỷ lệ khuyết thiếu ngẫu nhiên $1\%$ đã được đưa vào chuỗi.

### 1.2. Kỹ thuật sinh dữ liệu khuyết ([missvl.py](file:///e:/TimeSeries/Lab1_Timeseries/scripts/missvl.py))
* **Cơ chế:** Missing Completely At Random (MCAR).
* **Cố định Seed:** `np.random.seed(42)` đảm bảo tính tái lập (reproducibility) của thực nghiệm.
* **Tỷ lệ tạo:** $1\%$ ($\approx 36$ điểm dữ liệu).
* **Kết quả thực tế:** Tạo ra **33 giá trị NaN** (~0.904% tổng số quan sát).
* **File lưu trữ:** `data/processed/daily-min-temperatures-missing.csv`.

```python
import numpy as np
import pandas as pd

# Thiết lập seed tái lập
np.random.seed(42)
mask = np.random.rand(len(df)) < 0.01  # Tỷ lệ 1%
df_missing = df.copy()
df_missing.loc[mask, 'Temp'] = np.nan
```

---

## 2. Chiến Lược Xử Lý Missing Values Trong Chuỗi Thời Gian

Trong chuỗi thời gian, việc xóa dòng (`dropna()`) sẽ **phá vỡ cấu trúc tần suất thời gian liên tục** (gãy tính chu kỳ $D$ hoặc $M$). Do đó, các phương pháp điền/nội suy được ưu tiên:

| Phương pháp | Đặc điểm & Cơ chế | Nhận xét trong bài toán nhiệt độ |
|---|---|---|
| **Forward-fill (FFill)** | Mang giá trị gần nhất phía trước lấp vào vị trí khuyết. | Tạo ra các bậc thang nằm ngang không tự nhiên, làm giảm phương sai ngắn hạn. |
| **Backward-fill (BFill)** | Lấy giá trị tương lai gần nhất lấp ngược về trước. | Gây rò rỉ dữ liệu tương lai (Data Leakage) khi huấn luyện mô hình. |
| **Linear Interpolation** *(Được chọn)* | Nội suy tuyến tính theo khoảng cách thời gian giữa hai đầu điểm mút. | Giữ nguyên độ dốc tự nhiên của nhiệt độ giữa các ngày liền kề. **Tối ưu nhất**. |
| **Time/Polynomial Interpolation** | Nội suy đa thức hoặc nội suy có trọng số khoảng cách thời gian. | Phù hợp khi có các cụm missing dài ngày; với 1% khuyết đơn lẻ thì tuyến tính là đủ mượt. |

---

## 3. Phát Hiện & Xử Lý Outliers (Giá Trị Ngoại Lai)

### 3.1. Phương pháp phát hiện

#### a. Phương pháp Z-Score
$$Z = \frac{x - \mu}{\sigma}$$
* Ngưỡng dị biệt: $|Z| > 3$ (nằm ngoài vùng tin cậy $99.73\%$ theo phân phối chuẩn).
* **Kết quả:** Phát hiện **10 điểm dị biệt** (~0.27%).

#### b. Phương pháp IQR (Interquartile Range)
$$IQR = Q_3 - Q_1$$
* Ngưỡng dưới: $Lower = Q_1 - 1.5 \times IQR$
* Ngưỡng trên: $Upper = Q_3 + 1.5 \times IQR$
* **Kết quả:** Với dữ liệu nhiệt độ Melbourne, dải hợp lệ tính được là `[-0.25°C, 22.55°C]`. Phát hiện **13 điểm dị biệt** (~0.36%).

### 3.2. Bản chất các điểm Outlier phát hiện được
Tất cả các điểm vượt ngưỡng đều rơi vào vùng nhiệt độ cao (**22.7°C – 26.3°C**) vào các tháng mùa hè (tháng 1, tháng 2). 

> **Nhận định chuyên môn:** Đây là các hiện tượng **nhiệt độ cực đoan tự nhiên (Heatwaves)** tại Melbourne chứ không phải do lỗi ghi nhận hay lỗi cảm biến.

### 3.3. Giải pháp đề xuất xử lý Outlier
1. **Không nên xóa điểm (Drop):** Tránh làm mất tính liên tục của chuỗi thời gian.
2. **Winsorization / Clipping:** Kẹp giá trị vào khoảng $[Lower, Upper]$ nếu mô hình dự báo rất nhạy cảm với cực trị (như hồi quy tuyến tính cổ điển).
3. **Giữ nguyên (Retention):** Nếu sử dụng các mô hình học sâu (LSTM, GRU) hoặc mô hình có khả năng học quy luật bất thường.
