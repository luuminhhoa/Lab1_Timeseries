# Trực Quan Hóa Dữ Liệu Chuỗi Thời Gian (EDA & Visualization)

Tài liệu này tổng hợp toàn bộ các kỹ thuật trực quan hóa được triển khai trong Bài tập 5 nhằm khai thác sâu các đặc trưng biến động, tính dừng sơ bộ và chu kỳ mùa vụ của chuỗi nhiệt độ Melbourne.

---

## 1. Biểu Đồ Chuỗi Thời Gian Toàn Phần (Full Time Series Plot)

* **Loại biểu đồ:** Line chart toàn chuỗi 10 năm (1981–1990).
* **Mục tiêu:** Quan sát tổng quan hình thái dữ liệu, mật độ dao động và độ biến thiên theo thời gian.
* **Nhận xét trực quan:**
  * Chuỗi mang tính dao động điều hòa rất rõ rệt và đều đặn theo chu kỳ 1 năm.
  * Không xuất hiện hiện tượng vỡ cấu trúc (structural break) hoặc trôi dạt (drift) quá lớn.

---

## 2. Phân Tích Thống Kê Trượt (Rolling Statistics)

Khảo sát tính dừng (Stationarity) sơ bộ bằng kỹ thuật cửa sổ trượt:

$$\mu_{t, w} = \frac{1}{w}\sum_{i=0}^{w-1} y_{t-i}, \quad \sigma_{t, w} = \sqrt{\frac{1}{w-1}\sum_{i=0}^{w-1} (y_{t-i} - \mu_{t, w})^2}$$

* **Cửa sổ khảo sát:** $w = 12$ ngày (hoặc tháng khi resample).
* **Đường Rolling Mean (Trung bình trượt):** Uốn lượn tuần hoàn theo nhịp mùa, khẳng định chuỗi chưa dừng ở trung bình (non-stationary in mean do mùa vụ).
* **Đường Rolling Std (Độ lệch chuẩn trượt):**
  * Dao động tương đối ổn định trong khoảng hẹp.
  * Xuất hiện các đỉnh nhọn cục bộ vào các giai đoạn giao mùa (tháng 3–4 và tháng 10–11), phản ánh thời tiết diễn biến thất thường hơn ở thời điểm chuyển mùa.

---

## 3. Phân Tích Mùa Vụ Nâng Cao (Seasonality Analysis)

### 3.1. Seasonal Plot Theo Tháng (Multi-line Plot)
* **Quy cách:** Trục hoành là 12 tháng (T1 $\rightarrow$ T12), mỗi năm biểu diễn bằng một đường riêng biệt.
* **Quan sát:**
  * Tất cả 10 đường đồ thị đều đồng quy theo một hình mẫu duy nhất dạng chữ U:
    * **Đỉnh:** Tháng 1 và Tháng 2 (Mùa hè - dao động trung bình từ 13°C đến 16°C).
    * **Đáy:** Tháng 7 (Mùa đông - hạ sâu xuống quanh mức 6°C - 8°C).
    * **Tăng trở lại:** Từ tháng 8 đến tháng 12.
  * Năm 1982 có điểm rơi nhiệt độ tháng 7 thấp bất thường so với 9 năm còn lại.

### 3.2. Heatmap Ma Trận Mùa Vụ (Month × Year)
* **Cấu trúc:** Ma trận $12 \times 10$ với dải màu `YlOrRd`.
* **Ưu điểm:** Cho phép so sánh đồng thời cả hai chiều: biến đổi theo từng tháng trong năm và biến động của cùng một tháng qua các năm.
* **Đặc điểm nổi bật:** Vùng trung tâm (tháng 6, 7, 8) luôn có tông màu vàng nhạt (nhiệt độ thấp), trong khi hai đầu bảng (tháng 1, 2, 12) ngả sang tông đỏ cam đậm.

---

## 4. Phân Tích Phân Phối Bằng Boxplot (Đề xuất tích hợp)

Boxplot là công cụ bổ trợ đắc lực để kiểm tra độ đối xứng, dải phân vị IQR và điểm ngoại lai cục bộ:

```python
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Boxplot theo Tháng: Đo lường độ biến thiên nội bộ từng tháng
sns.boxplot(data=df_handled, x=df_handled.index.month, y='Temp', palette='coolwarm')

# 2. Boxplot theo Năm: Khảo sát xu thế nóng lên toàn cầu qua 10 năm
sns.boxplot(data=df_handled, x=df_handled.index.year, y='Temp', palette='Set2')
```

* **Boxplot theo Tháng:** Thể hiện rõ các tháng mùa hè có dải IQR rộng hơn (thời tiết biến động lớn giữa các ngày), trong khi tháng mùa đông dải IQR hẹp và tập trung hơn.
* **Boxplot theo Năm:** Vị trí đường Median giữa các năm hầu như đi ngang ổn định quanh mức 11°C – 12°C, cho thấy khí hậu Melbourne trong thập niên 80 duy trì cân bằng nhiệt dài hạn.
