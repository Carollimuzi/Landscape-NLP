import pandas as pd

# 指定文件路径
file_path = '/root/cjr/projects/adaseq/search_result/seed_avg_results_bert.csv'

# 读取CSV文件（处理多层列头）
df = pd.read_csv(file_path, header=[0, 1])

# 显示列名和前几行数据，以便查看列名和数据
print(f"Columns: {df.columns.tolist()}")
print(df.head())

# 查找 'dev_f1' 列，并按照其 'mean' 排序，获取最高的模型
df_sorted = df.sort_values(by=('dev_f1', 'mean'), ascending=False)

# 获取排序后第一行的输出目录
best_model_output_dir = df_sorted.iloc[0]['output_dir']
print(f"The output_dir of the model with the highest dev_f1 is: {best_model_output_dir}")
