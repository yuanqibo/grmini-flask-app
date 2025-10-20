import google.generativeai as genai

# 配置你的API密钥
genai.configure(api_key="AIzaSyBcwY5RCaxhzr8jGm4bsLJe2BMdQJTjEEY")

# 列出所有可用模型
models = genai.list_models()
for model in models:
    # 筛选支持generateContent的模型（可生成内容的模型）
    if "generateContent" in model.supported_generation_methods:
        print(f"可用模型名称: {model.name}")
        print(f"支持的方法: {model.supported_generation_methods}\n")