# AI Guide 导航网站

> 一个为 **AI Guide（鱼皮的 AI 知识库）** 打造的高颜值导航与宣传站点，帮助用户快速理解项目价值、学习路径与核心内容版块。

<p align="center">
  <a href="https://ai.codefather.cn" target="_blank" rel="noopener noreferrer"><img alt="在线阅读" src="https://img.shields.io/badge/在线阅读-ai.codefather.cn-6366f1?style=for-the-badge"></a>
  <a href="https://ai.codefather.cn/vibe" target="_blank" rel="noopener noreferrer"><img alt="Vibe Coding 教程" src="https://img.shields.io/badge/Vibe%20Coding-零基础教程-f472b6?style=for-the-badge"></a>
  <a href="https://github.com/liyupi/ai-guide" target="_blank" rel="noopener noreferrer"><img alt="GitHub" src="https://img.shields.io/badge/GitHub-liyupi%2Fai--guide-111827?style=for-the-badge"></a>
</p>

![AI Guide 导航站封面](assets/readme/ai-guide-cover.jpg)

## 项目简介

AI Guide 是一个**完全免费、持续更新、面向大众的 AI 知识共享平台**。本目录下的 `index.html` 提供了一个静态导航网站，用来集中展示 AI Guide 的核心卖点：

- 为什么它适合 AI 初学者快速入门
- 它覆盖了哪些热门模型、工具和实战方向
- 用户可以如何从学习一路走到项目实战、产品变现与社区共建

如果你想给第一次接触 AI 的用户一个**低门槛、强视觉、易传播**的入口页，这个站点就是为此设计的。

## 这个网站解决了什么问题

面对 AI 领域内容爆炸、概念分散、工具变化快的问题，很多用户往往会陷入：

- 不知道从哪里开始学
- 看了很多内容，但没有形成完整路径
- 知道工具名字，却不知道该怎么真正用起来
- 学会一点后，又不知道如何做项目、做产品、做传播

AI Guide 导航网站把这些问题重新组织成了一个清晰的浏览体验：

- **一眼看懂项目定位**：免费开源、面向实战、持续更新
- **快速定位想学内容**：Vibe Coding、AI 模型、AI 编程工具、MCP、变现等
- **直接建立学习顺序**：从基础认知到工具使用，再到项目与商业化
- **帮助传播项目价值**：适合 README、社媒分享、落地页宣传与 GitHub 展示

## 核心亮点

### 1. 聚焦 AI 初学者友好的导航体验

首页 Hero 区直接说明项目价值，并提供：

- 在线阅读入口
- Vibe Coding 专题入口
- GitHub Star 入口
- 关键词搜索与热门主题跳转

这使网站既可以作为宣传页，也可以作为内容导航入口。

### 2. 用内容矩阵说明 AI Guide 的覆盖范围

网站将内容整理为 6 个高频板块：

- **Vibe Coding 零基础教程**
- **AI 模型大全**
- **AI 编程工具**
- **项目实战教程**
- **产品变现指南**
- **知识百科与资源**

![AI Guide 内容矩阵](assets/readme/ai-guide-sections.jpg)

这些板块覆盖了从“认识 AI”到“用 AI 做项目”，再到“把项目做成产品”的完整链路。

### 3. 用路线图降低学习门槛

网站内置学习路线图，将用户旅程拆分为 5 个阶段：

1. AI 基础入门
2. Vibe Coding 入门
3. 项目实战与进阶
4. 产品变现与推广
5. 社区共建与国际化

![AI 学习路线图](assets/readme/ai-guide-roadmap.jpg)

这让用户不只是“看到很多内容”，而是知道**下一步该学什么**。

### 4. 视觉风格适合宣传与传播

站点采用高对比深色界面与玻璃拟态卡片风格，结合：

- 渐变主色与高亮按钮
- 动态背景与柔和发光效果
- 明确的分区层级
- 响应式布局
- 键盘可访问性与 reduced-motion 支持

适合用作：

- GitHub 项目展示页
- 活动宣传页
- 社区分享入口
- AI 教程导航站

## 网站内容结构

当前站点主要由以下部分组成：

- **Hero 首屏**：项目定位、核心入口、站内搜索
- **数据统计区**：Star、Fork、文章规模、语言版本等信息
- **精选内容板块**：6 大核心栏目
- **Vibe Coding 聚焦区**：零基础入门教程强调
- **学习路线图**：从入门到进阶再到变现
- **最近更新**：突出内容持续迭代
- **Star 增长趋势**：增强项目信任感
- **社区入口**：作者信息与共建引导
- **CTA 区块**：鼓励用户立即开始 AI 学习之旅

## 在线地址

- 项目主页：<https://ai.codefather.cn>
- Vibe Coding 教程：<https://ai.codefather.cn/vibe>
- AI Guide GitHub：<https://github.com/liyupi/ai-guide>

## 本地预览

这是一个纯静态网站，不依赖额外构建流程。

```bash
cd site
python3 -m http.server 8000
```

然后访问：<http://localhost:8000>

## 目录结构

```text
site/
├── README.md                  # 网站项目介绍文档
├── index.html                 # ai-guide 导航网站主页面（单文件静态站）
└── assets/
    └── readme/                # README 配套宣传图片
```

## 部署方式

仓库已配置 GitHub Pages 工作流：

- 推送 `site/**` 相关变更到 `main` 分支时自动触发
- 将 `site/` 目录作为 Pages 制品上传
- 自动部署为静态站点

对应配置文件：

- `../.github/workflows/deploy-pages.yml`

## README 配图说明

本 README 中使用的插图保存在以下目录：

- `assets/readme/ai-guide-cover.jpg`
- `assets/readme/ai-guide-roadmap.jpg`
- `assets/readme/ai-guide-sections.jpg`

这些图片用于帮助读者快速理解网站定位、内容矩阵与学习路径，也适合在 GitHub 项目页中直接用于展示和传播。

## 致谢

- 内容项目：**AI Guide / 鱼皮的 AI 知识库**
- 网站主题方向：围绕免费开源 AI 学习资源、Vibe Coding 与项目实战展开
- 本仓库站点形式：静态导航宣传页，便于展示、部署与迭代
