import matplotlib.pyplot as plt
import matplotlib

# 优先使用系统中已安装的中文字体（按实际情况选择）
# Windows 推荐：SimHei（黑体）、Microsoft YaHei（微软雅黑）
# macOS 推荐：Heiti TC（黑体）、PingFang SC（苹方）
# Linux 推荐：WenQuanYi Micro Hei（文泉驿微米黑）
matplotlib.rcParams["font.family"] = ["Heiti TC", "SimHei", "WenQuanYi Micro Hei", "Arial Unicode MS"]
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示异常

# 测试代码
plt.plot([1, 2, 3], [4, 5, 1])
plt.title("中文标题测试")  # 包含警告中的"试"字
plt.xlabel("横轴标签")
plt.ylabel("纵轴标签")
plt.show()