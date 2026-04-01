import json
import os
import random
import urllib.request
import ssl
from io import BytesIO

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from PIL import Image, ImageDraw, ImageFont, ImageOps

# 禁用全局 SSL 验证警告
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_session():
    """创建一个带有重试机制和忽略 SSL 验证的 requests Session"""
    session = requests.Session()
    # 禁用证书验证以避免 SSL 握手错误
    session.verify = False 
    
    # 设置重试策略
    retries = Retry(
        total=3,  # 最大重试次数
        backoff_factor=0.5,  # 重试间隔系数
        status_forcelist=[500, 502, 503, 504, 104]  # 需要重试的 HTTP 状态码 (104 是连接被重置)
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

# 全局复用 session
global_session = get_session()

def download_image(url):
    """从 URL 或本地路径加载图片并返回 PIL Image 对象"""
    if not url:
        return None
        
    # 添加对本地文件的支持
    if os.path.exists(url):
        # 为了支持相对路径，确保如果是本地文件，则将其转换为绝对路径
        # 这里的基准路径采用运行时的当前工作目录
        if not os.path.isabs(url):
            url = os.path.abspath(url)
            
        try:
            return Image.open(url).convert("RGBA")
        except Exception as e:
            print(f"Error opening local file {url}: {e}")
            return Image.new("RGBA", (200, 300), (100, 100, 100, 255))
            
    # 增加重试循环，以防单次请求由于网络波动抛出 EOFError 等底层异常
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # 添加更完整的 User-Agent 伪装成真实浏览器
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive'
            }
            
            # 使用配置好的 session 发送请求，增加超时时间到 30 秒
            response = global_session.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return Image.open(BytesIO(response.content)).convert("RGBA")
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt < max_retries - 1:
                import time
                time.sleep(2)  # 等待后重试
            else:
                print(f"Failed to download {url} after {max_retries} attempts.")
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            break # 非请求错误直接退出
            
    # 如果下载失败，返回一个带灰底的默认空图片
    img = Image.new("RGBA", (200, 300), (100, 100, 100, 255))
    return img

def get_font(size):
    """获取指定大小的字体，如果本地没有则自动下载一个开源无衬线粗体"""
    font_path = "Roboto-Bold.ttf"
    
    # 获取脚本所在的目录，以保证相对路径在不同目录下执行时依然有效
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_abs_path = os.path.join(script_dir, font_path)
    
    if not os.path.exists(font_abs_path):
        print(f"Downloading font to {font_abs_path}...")
        url = "https://github.com/googlefonts/roboto/raw/main/src/hinted/Roboto-Bold.ttf"
        try:
            # 使用 urllib 下载字体文件
            urllib.request.urlretrieve(url, font_abs_path)
        except Exception as e:
            print(f"Failed to download font: {e}")
            # 回退到使用 PIL 默认字体
            return ImageFont.load_default()
            
    try:
        return ImageFont.truetype(font_abs_path, size)
    except Exception as e:
        print(f"Failed to load font from {font_abs_path}: {e}")
        return ImageFont.load_default()

def generate_poster(icon_url, brand_text, main_text, cta_url, cta_text, poster_urls, output_path="output_poster.png", theme_color=None):
    # 图片基础尺寸 (比例 1.91:1)
    width, height = 1200, 630

    # 定义可选的主色调和渐变色组合 (base_color, top_color)
    color_palettes = [
        ("#FF6A7A", "#FFA0A0"), # 默认红/粉
        ("#6A8BFF", "#A0B5FF"), # 浅蓝色
        ("#6AFF8B", "#A0FFA0"), # 浅绿色
        ("#FFD16A", "#FFE1A0"), # 浅黄色
        ("#B56AFF", "#D1A0FF"), # 浅紫色
        ("#8A95A5", "#B0BAC5"), # 浅灰色
    ]

    selected_palette = None
    if theme_color:
        # 如果提供了 theme_color，在预设里查找匹配项
        for palette in color_palettes:
            if theme_color.upper() == palette[0].upper():
                selected_palette = palette
                break
        # 如果找不到匹配的，直接用传入的颜色和稍浅的颜色作为备用
        if not selected_palette:
            selected_palette = (theme_color, theme_color)
            
    if not selected_palette:
        # 每次生成随机选择一个配色方案
        selected_palette = random.choice(color_palettes)
        
    base_color, top_color = selected_palette
    
    # 1. 创建渐变背景
    print(f"Creating background with base color {base_color}...")
    base = Image.new('RGB', (width, height), base_color)
    top = Image.new('RGB', (width, height), top_color)
    mask = Image.new('L', (width, height))
    mask_data = [int(255 * (x / width)) for y in range(height) for x in range(width)]
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    img = base.convert("RGBA")
    draw = ImageDraw.Draw(img)

    # 3. 添加右侧海报集合
    print("Downloading and placing posters...")
    grid_positions = [
        (550, -20), (750, -50), (950, -30), (1100, -10),
        (520, 250), (700, 230), (880, 260), (1050, 210),
        (580, 500), (780, 480), (980, 510)
    ]
    
    # 用户提供的海报数量可能不足 10 张，我们尽量展示
    for i, url in enumerate(poster_urls[:10]):
        if not url.strip():
            continue
        print(f"  -> Processing poster {i+1}...")
        poster = download_image(url.strip())
        
        target_size = (180, 270)
        poster = ImageOps.fit(poster, target_size, method=Image.Resampling.LANCZOS)
        poster = ImageOps.expand(poster, border=6, fill='white')
        
        angle = random.uniform(-15, 15)
        # 旋转时使用透明白作为背景，避免抗锯齿边缘出现黑色底纹，并使用 BICUBIC 提升边缘平滑度
        rotated = poster.rotate(angle, expand=True, fillcolor=(255, 255, 255, 0), resample=Image.Resampling.BICUBIC)
        
        if i < len(grid_positions):
            pos = grid_positions[i]
            final_x = pos[0] + random.randint(-15, 15)
            final_y = pos[1] + random.randint(-15, 15)
            img.paste(rotated, (final_x, final_y), rotated)

    # 4. 添加左上角 Icon 和 品牌文字
    print("Adding icon and brand text...")
    if icon_url:
        icon = download_image(icon_url)
        if icon:
            icon = ImageOps.fit(icon, (40, 40), method=Image.Resampling.LANCZOS)
            img.paste(icon, (50, 40), icon if icon.mode == 'RGBA' else None)
    
    if brand_text:
        font_brand = get_font(22)
        draw.text((105, 48), brand_text, font=font_brand, fill="white")

    # 5. 添加左侧主标题文字 (支持手动换行符 \n，且自动缩放防遮挡)
    print("Adding main text...")
    # 限制最大宽度，防止遮挡右侧海报 (右侧海报约从 x=520 开始)
    max_title_width = 460  
    # 限制最大高度，防止侵占底部 CTA 区域 (从 y=150 开始，CTA 一般在 480，留出 30px 间距)
    max_title_height = 300 
    
    raw_lines = main_text.replace('\\n', '\n').split('\n')
    
    # 动态调整标题字体大小以适应指定区域
    best_font_size = 70
    min_font_size = 20
    final_lines = []
    final_font = None
    final_line_height = 0

    # 预先将每段根据换行符拆分，并在下面进行单词截断计算
    while best_font_size >= min_font_size:
        font_test = get_font(best_font_size)
        test_lines = []
        word_too_long = False
        
        for raw_line in raw_lines:
            words = raw_line.split()
            if not words:
                test_lines.append("")
                continue
            current_line = []
            for word in words:
                current_line.append(word)
                bbox = draw.textbbox((0, 0), " ".join(current_line), font=font_test)
                if bbox[2] > max_title_width:
                    current_line.pop()
                    if current_line:
                        test_lines.append(" ".join(current_line))
                    current_line = [word]
                    
                # 检查单个词是否过长 (防超边界)
                if draw.textbbox((0, 0), word, font=font_test)[2] > max_title_width:
                    word_too_long = True
            if current_line:
                test_lines.append(" ".join(current_line))
                
        # 计算总高度 (预估行高为字体大小的 1.15 倍)
        line_height = best_font_size * 1.15
        total_height = len(test_lines) * line_height
        
        if total_height <= max_title_height and not word_too_long:
            final_lines = test_lines
            final_font = font_test
            final_line_height = line_height
            break
            
        best_font_size -= 2

    # 极端情况的 Fallback
    if not final_lines:
        final_font = get_font(min_font_size)
        final_lines = [main_text]
        final_line_height = min_font_size * 1.15

    y_text = 150
    for line in final_lines:
        if line:
            draw.text((50, int(y_text)), line, font=final_font, fill="white")
        y_text += final_line_height

    # 6. 添加底部 CTA 图片和文字
    print("Adding CTA button and text...")
    # 根据标题实际占用高度计算 CTA 的纵坐标，确保不重叠
    cta_y = max(y_text + 30, 480) 
    if cta_y > 540: # 防止过低超出底部画布
        cta_y = 540
        
    current_x = 50
    
    # 将图标放大 30% (原来是 60，60 * 1.3 ≈ 78)
    icon_target_size = 78
    icon_height = icon_target_size
    
    if cta_url:
        cta = download_image(cta_url)
        if cta:
            # 保持比例缩放播放按钮
            cta.thumbnail((icon_target_size, icon_target_size), Image.Resampling.LANCZOS)
            img.paste(cta, (current_x, int(cta_y)), cta if cta.mode == 'RGBA' else None)
            current_x += cta.width + 20  # 稍微增加图标和文字的间距
            icon_height = cta.height

    if cta_text:
        # 计算文字可用最大宽度，防止遮挡右侧海报
        # 右侧海报约从 x=520 开始，预留 20px 间距，所以最大宽度可到 500
        max_cta_text_width = 500 - current_x 
        
        # 动态调整 CTA 字体大小
        cta_font_size = 47 # 初始设定放大 30% 的字体
        font_cta = get_font(cta_font_size)
        
        while cta_font_size > 16:
            bbox = draw.textbbox((0, 0), cta_text, font=font_cta)
            if bbox[2] <= max_cta_text_width:
                break
            cta_font_size -= 2
            font_cta = get_font(cta_font_size)
            
        # 绝对精准的垂直居中对齐计算：
        # 获取文字包围盒，bbox 的结构为 (left, top, right, bottom)
        bbox = draw.textbbox((0, 0), cta_text, font=font_cta)
        
        # text_height 表示这行文字在 Y 轴上真实的渲染高度
        text_height = bbox[3] - bbox[1]
        
        # 文字在绘制时的锚点默认在左上角 (0, 0)
        # 但是不同字符（带不带下沉比如 'g'/'y'，或者大写）其 bbox 的 top (bbox[1]) 是有偏移的。
        # 真正的居中公式应该是：
        # 图标中心点 Y = cta_y + icon_height / 2
        # 文字中心点 Y = text_y + bbox[1] + text_height / 2
        # 让它们相等：
        # text_y = cta_y + (icon_height / 2) - (text_height / 2) - bbox[1]
        
        text_y = cta_y + (icon_height / 2) - (text_height / 2) - bbox[1]
        
        draw.text((current_x, int(text_y)), cta_text, font=font_cta, fill="white")

    # 解析 output_path，如果是相对路径，则相对于当前工作路径转换
    if not os.path.isabs(output_path):
        output_path = os.path.abspath(output_path)
        
    # 7. 保存最终图片
    img = img.convert("RGB")
    
    # 确保输出目录存在
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    img.save(output_path)
    print(f"Poster generated successfully! Saved to: {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Auto Poster Generator")
    parser.add_argument("--config", type=str, help="Path to JSON config file")
    parser.add_argument("--json", type=str, help="JSON string with config data (for API/external call)")
    args = parser.parse_args()

    data = None
    if args.config and os.path.exists(args.config):
        print(f"Loading config from {args.config}...")
        with open(args.config, 'r', encoding='utf-8') as f:
            data = json.load(f)
    elif args.json:
        print("Loading config from JSON string...")
        data = json.loads(args.json)

    if data:
        generate_poster(
            icon_url=data.get('icon_url', ''),
            brand_text=data.get('brand_text', ''),
            main_text=data.get('main_text', ''),
            cta_url=data.get('cta_url', ''),
            cta_text=data.get('cta_text', ''),
            poster_urls=data.get('poster_urls', []),
            output_path=data.get('output_path', 'output_poster.png'),
            theme_color=data.get('theme_color')
        )
    else:
        print("Please run with a JSON config file or JSON string.")
        print("Usage 1: python manus_poster_generator.py --config data.json")
        print("Usage 2: python manus_poster_generator.py --json '{\"icon_url\":\"...\", ...}'")
