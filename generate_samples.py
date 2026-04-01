import json
import os
from trae_poster_generator import generate_poster

# 预设的主题颜色，对应生成脚本里的配置
themes = [
    {"name": "Red_Pink", "hex": "#FF6A7A"},
    {"name": "Light_Blue", "hex": "#6A8BFF"},
    {"name": "Light_Green", "hex": "#6AFF8B"},
    {"name": "Light_Yellow", "hex": "#FFD16A"},
    {"name": "Light_Purple", "hex": "#B56AFF"},
    {"name": "Light_Gray", "hex": "#8A95A5"}
]

def main():
    # 创建一个保存示例图的目录
    os.makedirs("docs_assets", exist_ok=True)
    
    # 加载基础数据
    with open("data.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for theme in themes:
        output_path = f"docs_assets/preview_{theme['name']}.png"
        print(f"Generating preview for {theme['name']} theme...")
        generate_poster(
            icon_url=data.get('icon_url', ''),
            brand_text=data.get('brand_text', ''),
            main_text=data.get('main_text', ''),
            cta_url=data.get('cta_url', ''),
            cta_text=data.get('cta_text', ''),
            poster_urls=data.get('poster_urls', []),
            output_path=output_path,
            theme_color=theme['hex']
        )

if __name__ == "__main__":
    main()