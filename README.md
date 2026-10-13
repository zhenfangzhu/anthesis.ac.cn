# Anthesis

**当我们与人工智能共同成长，我们会成为什么？**  
**As we grow alongside AI, what will we become?**

我是朱振方（Zhenfang Zhu），Anthesis 是我的个人研究网站。我关注 AI Agent、人的自主权，以及人与 AI 在长期交互中的共同成长。

[访问网站](https://anthesis.ac.cn/) · [English](https://anthesis.ac.cn/en/) · [关于我](https://anthesis.ac.cn/about.html)

## 内容与方向

- **研究笔记**：我在这里记录研究问题、阅读与思考，从[为什么是 Anthesis](https://anthesis.ac.cn/why-anthesis.html)开始。
- **模型与评测**：我整理关于模型行为、诚实、学习与自主权的公开研究。目前我还没有发布独立测评与排名。
- **研究方向**：我希望围绕长期交互的 Agent、基础模型与训练方法，以及评测与对照实验展开研究。

我在本仓库维护网站源码与页面内容。你可以从[研究笔记](https://anthesis.ac.cn/notes.html)和[模型与评测](https://anthesis.ac.cn/models.html)开始阅读。

## English

I am **Zhenfang Zhu (朱振方)**, a graduate of the University of Science and Technology of China and a co-founder of Redding AI. Anthesis is my personal research website. I study AI agents, human agency, and how people and AI grow together over time.

I share my research notes, literature summaries, and research directions here. On the model evaluation page, I currently summarize published work; I have not yet released independent evaluations or rankings. I maintain the website source and page content in this repository.

[Research notes](https://anthesis.ac.cn/en/notes.html) · [Models and evaluations](https://anthesis.ac.cn/en/models.html) · [About](https://anthesis.ac.cn/en/about.html)

## 本地预览 / Local preview

静态 HTML、CSS 和 JavaScript 网站，无需安装前端依赖。使用 Python 3，在仓库根目录运行：

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

打开 <http://127.0.0.1:8000/>。这是本地静态预览；发布由 GitHub Pages 完成。

This is a static HTML, CSS, and JavaScript website. No frontend dependency installation is required. Run the command above with Python 3 from the repository root, then open the local URL.

## 目录与维护 / Structure and maintenance

| 路径 / Path | 用途 / Purpose |
| --- | --- |
| 根目录 `*.html` | 中文页面 / Chinese pages |
| `en/` | 生成的英文页面 / Generated English pages |
| `assets/` | 图片与英文翻译映射 / Images and English translation map |
| `style.css`、`language.js` | 共享样式与语言切换 / Shared styles and language navigation |
| `scripts/build-locales.py` | 生成英文页面并更新页面资源版本、语言链接与站点地图 / Locale and metadata generation |
| `scripts/notify_indexnow.py` | 部署后提交变更网址 / Notify IndexNow after deployment |

修改中文页面及 `assets/translations-en.json` 后，运行以下命令，并一并检查生成的中英文页面：

```sh
python3 scripts/build-locales.py
```

Update the Chinese source pages and translation map before running the generator. Review the generated changes and preview both languages before publishing.

## 反馈与联系 / Feedback and contact

如果你发现失效链接、页面问题或需要更正的引用，欢迎通过 [Issues](https://github.com/zhenfangzhu/anthesis.ac.cn/issues)告诉我，并提供页面地址与具体问题。

If you find a broken link, a website issue, or a reference that needs correction, please let me know by opening an issue with the page URL and a description.

[个人网站 / Personal website](https://zhuzhenfang.com/) · [GitHub](https://github.com/zhenfangzhu) · [Email](mailto:zhuzhenfang@ustc.edu)
