import google.generativeai as genai

genai.configure(api_key="AIzaSyBcwY5RCaxhzr8jGm4bsLJe2BMdQJTjEEY")

# 使用步骤1中确认可用的模型名称
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash-exp")  # 重点：用实际可用的名称

prompt = "帮我写一篇五百字作文，内容主题围绕秋天，雨，湖"

try:
    response = model.generate_content(prompt)
    print(response.text)
except Exception as e:
    print(f"错误：{e}")