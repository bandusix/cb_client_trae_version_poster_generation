# 卡皮AI搜索 Trae Auto Poster Generator (自动海报生成脚本)

这是一个用于快速生成包含图片网格、品牌 Icon、自适应排版主标题和 CTA（Call To Action）按钮的海报生成脚本。该脚本专门为了接口调用、批处理以及跨语言接入设计。

## 🌟 核心特性
- **高度自适应文字**：不论标题多长、语言为何种，代码会自动调整文字大小以适应画布，绝不超边或被截断。
- **智能居中对齐**：通过精确的字符度量（Ascent / Descent）实现文字与图标的水平视觉居中。
- **自动主题配色**：若不指定，脚本会在6种极具质感的浅色渐变背景（如浅蓝、浅粉、浅绿等）中随机抽选；也支持自定义指定主题色。
- **稳健的下载机制**：自带网络超时重试和异常捕获逻辑，防止因某张图片下载失败导致生成中断。
- **灵活的接口接入**：支持本地调用、命令行文件传参以及直接通过 JSON 字符串传参。

---

## 🛠️ 参数说明

无论你通过哪种方式调用，底层的数据结构（JSON/Dict）都需要包含以下参数：

| 参数名 | 类型 | 必填 | 说明 | 示例 |
| :--- | :--- | :--- | :--- | :--- |
| `icon_url` | String | 否 | 左上角品牌 Icon，支持网络 URL 或是本地绝对路径 | `"https://capybaba.io/favicon.png"` |
| `brand_text` | String | 否 | 紧跟在品牌 Icon 后的品牌名称 | `"capybaba.io"` |
| `main_text` | String | 是 | 左侧的主标题。支持使用 `\n` 进行换行 | `"Top 10\nComedy\nMovies & TV\nShows"` |
| `cta_url` | String | 否 | 左下角的播放/行动按钮图标，支持网络 URL 或本地绝对路径/相对路径 | `"assets/play_icon.png"` |
| `cta_text` | String | 否 | 紧跟在 CTA 图标后的行动呼吁文字 | `"Watch Now"` |
| `poster_urls` | Array | 是 | 右侧要展示的海报图片集合，推荐传入 9~10 张网络图片 | `["https://xxx/1.jpg", "https://xxx/2.jpg"]` |
| `output_path` | String | 否 | 生成海报后的保存路径及名称 | `"trae图片优化v9版本.png"` |
| `theme_color` | String | 否 | 【可选】自定义渐变背景色（Hex格式）。若不填，则从内置的浅色主题中随机抽取 | `"#FF6A7A"` |

---

## 🚀 接入方式示例

为满足不同技术栈后端的调用需求，脚本支持三种调用方式：

### 方式一：通过 JSON 配置文件调用（批处理推荐）
将以上参数保存为一个 `.json` 文件（例如 `data.json`），然后在终端中执行：

```bash
# 假设你已经准备好了 data.json 文件
python3 trae_poster_generator.py --config data.json
```

### 方式二：通过 JSON 字符串直接传参（跨语言后端调用推荐）
如果你使用 Node.js、Go、PHP、Java 等语言，可以直接通过执行系统命令（`exec`）并将序列化后的 JSON 字符串传入，免去了读写临时文件的 IO 开销：

```bash
python3 trae_poster_generator.py --json '{
    "icon_url": "https://capybaba.io/favicon-128x128.png",
    "brand_text": "capybaba.io",
    "main_text": "Top 10\nComedy\nMovies & TV\nShows",
    "cta_url": "assets/play_icon.png",
    "cta_text": "Watch Now",
    "poster_urls": [
        "https://media.themoviedb.org/t/p/w220_and_h330_face/7wIBfBl2gejt6xHxNSK0reVIm7E.jpg",
        "https://media.themoviedb.org/t/p/w220_and_h330_face/bRBeSHfGHwkEpImlhxPmOcUsaeg.jpg"
    ],
    "output_path": "trae图片优化v9版本.png"
}'
```

### 方式三：作为 Python 模块直接调用（Python 后端推荐）
如果你本身使用的是 Django、FastAPI 等 Python 框架，可直接 `import` 并传入字典：

```python
from trae_poster_generator import generate_poster

# 组装你的数据 (可能来源于数据库或前端请求)
payload = {
    "icon_url": "https://capybaba.io/favicon-128x128.png",
    "brand_text": "capybaba.io",
    "main_text": "Top 10\nComedy\nMovies & TV\nShows",
    "cta_url": "assets/play_icon.png",
    "cta_text": "Watch Now",
    "poster_urls": [
        "https://media.themoviedb.org/t/p/w220_and_h330_face/7wIBfBl2gejt6xHxNSK0reVIm7E.jpg",
        "https://media.themoviedb.org/t/p/w220_and_h330_face/bRBeSHfGHwkEpImlhxPmOcUsaeg.jpg"
    ],
    "output_path": "trae图片优化v9版本.png"
}

# 直接调用生成
generate_poster(**payload)
```

---

## 完整实例素材 (现有 Demo 演示)
这里是一份目前我们可以完美运行并生成海报的 `data.json` 实例：

```json
{
    "icon_url": "https://capybaba.io/favicon-128x128.png",
    "brand_text": "capybaba.io",
    "main_text": "Top 10\nComedy\nMovies & TV\nShows",
    "cta_url": "assets/play_icon.png",
    "cta_text": "Watch Now",
    "poster_urls": [
        "https://media.themoviedb.org/t/p/w220_and_h330_face/7wIBfBl2gejt6xHxNSK0reVIm7E.jpg",
        "https://media.themoviedb.org/t/p/w220_and_h330_face/bRBeSHfGHwkEpImlhxPmOcUsaeg.jpg",
        "https://media.themoviedb.org/t/p/w220_and_h330_face/7F0jc75HrSkLVcvOXR2FXAIwuEv.jpg",
        "https://media.themoviedb.org/t/p/w220_and_h330_face/znTPnXCK3lEQJgqXCvP7e5FUz6f.jpg",
        "https://media.themoviedb.org/t/p/w220_and_h330_face/wfuqMlaExcoYiUEvKfVpUTt1v4u.jpg",
        "https://media.themoviedb.org/t/p/w220_and_h330_face/buPFnHZ3xQy6vZEHxbHgL1Pc6CR.jpg",
        "https://media.themoviedb.org/t/p/w220_and_h330_face/yihdXomYb5kTeSivtFndMy5iDmf.jpg",
        "https://media.themoviedb.org/t/p/w220_and_h330_face/jjyuk0edLiW8vOSnlfwWCCLpbh5.jpg",
        "https://media.themoviedb.org/t/p/w220_and_h330_face/mjkS2iAgWj3ik1DTjvI15nHZ7yl.jpg"
    ],
    "output_path": "trae图片优化v9版本.png"
}
```