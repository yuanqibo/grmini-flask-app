import PIL.Image
import google.generativeai as genai
from io import BytesIO

# 1. 配置API密钥（必须步骤，需先在Google AI Studio获取）
genai.configure(api_key="AIzaSyBcwY5RCaxhzr8jGm4bsLJe2BMdQJTjEEY")  # 替换为你的实际API密钥

# 2. 定义生成图像的prompt
prompt = """
生成一张高档餐厅中的纳米香蕉菜肴图片，整体风格要体现Gemini主题（可融入Gemini的标志元素或科技感设计），
画面需精致、有艺术感，突出"纳米"的小巧精致和餐厅的奢华氛围。
"""

# 3. 调用Gemini模型生成图像（使用支持图像生成的模型）
try:
    # 使用gemini-pro-vision模型（支持图像生成相关任务）
    response = genai.generate_content(
        model="gemini-pro-vision",
        contents=[{"parts": [{"text": prompt}]}]  # 按官方规范构造内容
    )

    # 4. 解析响应中的图像数据并保存
    if response and hasattr(response, 'images') and len(response.images) > 0:
        # 获取图像二进制数据
        image_data = response.images[0]
        # 用PIL打开并保存
        image = PIL.Image.open(BytesIO(image_data))
        image.save("nano_banana_dish.png")
        print("图像生成成功，已保存为 nano_banana_dish.png")
    else:
        print("未生成图像，响应内容：", response.text)

except Exception as e:
    print("生成失败：", str(e))