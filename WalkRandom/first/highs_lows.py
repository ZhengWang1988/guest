import csv
from matplotlib import pyplot as plt


filename = "sitka_weather_07-2014.csv"
with open(filename) as f:
	reader = csv.reader(f)
	header_row = next(reader)
	# print(header_row)
	# for index,column_header in enumerate(header_row):
	# 	print(index,column_header)

	highs = []
	for row in reader:
		highs.append(int(row[1]))
	print(highs)

	# 根据数据绘制图形
	fig = plt.figure(dpi=128,figsize=(10,6))
	plt.plot(highs,c='red')

	# 设置图形格式
	plt.title("Daily high temperatures,July 2014",)