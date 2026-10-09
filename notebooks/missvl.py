import pandas as pd
import numpy as np
import os

# 1. Đọc file dữ liệu gốc
input_file = '../data/raw/daily-min-temperatures.csv'
df = pd.read_csv(input_file, parse_dates=['Date'], index_col='Date')

# 2. Tạo tỷ lệ missing ngẫu nhiên 
np.random.seed(42) # Set seed để lần nào tạo cũng ra cùng vị trí NaN
mask = np.random.rand(len(df)) < 0.01  # Thay đổi thành 1% thay vì 5%

# 3. Tạo dataframe mới và gán giá trị NaN
df_missing = df.copy()
df_missing.loc[mask, 'Temp'] = np.nan

# 4. Lưu ra một file csv mới 
output_dir = '../data/processed'
os.makedirs(output_dir, exist_ok=True)

output_file = f'{output_dir}/daily-min-temperatures-missing.csv'
df_missing.to_csv(output_file)

print(f"Đã lưu file chứa missing value tại: {output_file}")
print("Số lượng giá trị bị thiếu (NaN) đã tạo:")
print(df_missing.isna().sum())
