#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hexo博客一键发布文章脚本
功能：
1. 创建标准格式的文章模板
2. 自动生成封面图（可选）
3. 自动添加Front-matter
4. 支持多种文章类型
5. 自动部署到GitHub Pages
"""

import os
import sys
import datetime
import argparse
import subprocess
import re
from pathlib import Path

class HexoPublisher:
    def __init__(self, blog_path="."):
        self.blog_path = Path(blog_path)
        self.posts_path = self.blog_path / "source" / "_posts"

    def create_post(self, title, categories=None, tags=None, post_type="article", 
                   cover=None, description=None, top=False):
        """
        创建新文章

        参数:
            title: 文章标题
            categories: 分类列表
            tags: 标签列表
            post_type: 文章类型 (article/tech/life/tutorial)
            cover: 封面图片URL或路径
            description: 文章描述
            top: 是否置顶
        """
        # 生成文件名
        filename = self._generate_filename(title)
        filepath = self.posts_path / filename

        # 检查文件是否已存在
        if filepath.exists():
            print(f"⚠️  文章已存在: {filepath}")
            overwrite = input("是否覆盖? (y/n): ")
            if overwrite.lower() != 'y':
                print("❌ 已取消")
                return

        # 生成Front-matter
        front_matter = self._generate_front_matter(
            title, categories, tags, post_type, cover, description, top
        )

        # 生成文章内容模板
        content = self._generate_content_template(post_type, title)

        # 写入文件
        full_content = front_matter + content
        filepath.write_text(full_content, encoding='utf-8')

        print(f"✅ 文章创建成功: {filepath}")
        print(f"📄 标题: {title}")
        print(f"🏷️  分类: {categories or '未设置'}")
        print(f"🔖 标签: {tags or '未设置'}")

        return filepath

    def _generate_filename(self, title):
        """生成文件名"""
        # 将标题转换为安全的文件名
        safe_title = re.sub(r'[^\w\s-]', '', title).strip()
        safe_title = re.sub(r'[-\s]+', '-', safe_title)
        return f"{safe_title}.md"

    def _generate_front_matter(self, title, categories, tags, post_type, 
                              cover, description, top):
        """生成Front-matter"""
        now = datetime.datetime.now()

        fm = ["---"]
        fm.append(f'title: "{title}"')
        fm.append(f"date: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        fm.append(f"updated: {now.strftime('%Y-%m-%d %H:%M:%S')}")

        # 文章类型
        type_names = {
            "article": "文章",
            "tech": "技术",
            "life": "生活",
            "tutorial": "教程"
        }
        fm.append(f"type: {post_type}")

        # 描述
        if description:
            fm.append(f'description: "{description}"')
        else:
            fm.append(f'description: "{title} - {type_names.get(post_type, "文章")}"')

        # 关键词（从标题和标签生成）
        keywords = [title]
        if tags:
            keywords.extend(tags if isinstance(tags, list) else tags.split(','))
        fm.append(f"keywords: {keywords}")

        # 分类
        if categories:
            if isinstance(categories, list):
                fm.append(f"categories: {categories}")
            else:
                fm.append(f"categories: [{categories}]")

        # 标签
        if tags:
            if isinstance(tags, list):
                fm.append(f"tags: {tags}")
            else:
                fm.append(f"tags: [{tags}]")

        # 封面
        if cover:
            fm.append(f"cover: {cover}")

        # 置顶
        if top:
            fm.append("top: true")
            fm.append("sticky: 100")

        # 其他默认设置
        fm.append("comments: true")
        fm.append("toc: true")  # 显示目录
        fm.append("toc_number: true")  # 目录显示序号
        fm.append("copyright: true")  # 显示版权
        fm.append("mathjax: false")  # 数学公式
        fm.append("katex: false")
        fm.append("aplayer: false")  # 音乐播放器
        fm.append("highlight_shrink: false")  # 代码折叠

        fm.append("---\n")

        return "\n".join(fm)

    def _generate_content_template(self, post_type, title):
        """生成文章内容模板"""
        templates = {
            "article": f"""# {title}

## 引言

在这里写下文章的引言部分...

## 正文

### 第一部分

开始你的文章内容...

### 第二部分

继续展开...

## 总结

总结文章要点...

---

> 💡 **提示**: 记得添加封面图片和优化SEO信息
> 
> 📷 封面建议尺寸: 1200x630 像素
> 
> 🔍 SEO优化: 在description中添加关键词
""",
            "tech": f"""# {title}

## 技术背景

介绍相关技术背景...

## 环境准备

```bash
# 安装依赖
npm install xxx
```

## 实现步骤

### 步骤1: 准备工作

详细说明...

### 步骤2: 核心代码

```javascript
// 示例代码
console.log("Hello World");
```

### 步骤3: 测试验证

测试方法和结果...

## 常见问题

### Q1: xxx问题

**A:** 解决方案...

## 总结

技术要点总结...

---

> 🔧 **技术栈**: 
> 
> 📦 **版本**: 
> 
> 📚 **参考文档**: 
""",
            "life": f"""# {title}

## 前言

记录生活的点滴...

## 正文

分享你的故事...

![图片描述](图片链接)

## 感悟

生活中的感悟...

---

> 🌟 **生活感悟**: 
> 
> 📅 **记录时间**: {datetime.datetime.now().strftime('%Y年%m月%d日')}
""",
            "tutorial": f"""# {title}

## 教程目标

本教程将带你...

## 前置条件

- 基础知识1
- 基础知识2
- 环境要求

## 详细步骤

### 步骤1

```bash
# 命令示例
command example
```

**说明**: 

### 步骤2

操作步骤...

## 效果展示

![效果截图](截图链接)

## 进阶技巧

### 技巧1

高级用法...

## 总结

回顾教程要点...

---

> ⏱️ **预计耗时**: 30分钟
> 
> 📊 **难度**: ⭐⭐⭐
> 
> 🎯 **适合人群**: 初学者/进阶者
"""
        }

        return templates.get(post_type, templates["article"])

    def deploy(self, message="更新文章"):
        """部署到GitHub Pages"""
        print("\n🚀 开始部署...")

        # 生成静态文件
        print("📦 生成静态文件...")
        result = subprocess.run(
            ["hexo", "generate"],
            cwd=self.blog_path,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"❌ 生成失败: {result.stderr}")
            return False

        # 部署
        print("🚀 部署到GitHub Pages...")
        result = subprocess.run(
            ["hexo", "deploy"],
            cwd=self.blog_path,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"❌ 部署失败: {result.stderr}")
            return False

        print("✅ 部署成功!")
        print(f"🌐 访问地址: https://mhd250.github.io/azy-blog/")
        return True

    def list_posts(self):
        """列出所有文章"""
        posts = list(self.posts_path.glob("*.md"))
        print(f"\n📚 共有 {len(posts)} 篇文章:\n")
        for i, post in enumerate(sorted(posts), 1):
            stat = post.stat()
            mtime = datetime.datetime.fromtimestamp(stat.st_mtime)
            print(f"{i}. {post.stem}")
            print(f"   📅 修改时间: {mtime.strftime('%Y-%m-%d %H:%M')}")
            print(f"   📄 大小: {stat.st_size} 字节")
            print()

def main():
    parser = argparse.ArgumentParser(
        description="Hexo博客一键发布工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 创建普通文章
  python publish.py -t "我的文章标题"

  # 创建技术文章
  python publish.py -t "Vue3教程" --type tech -c "技术" --tags "vue,前端"

  # 创建置顶文章
  python publish.py -t "重要公告" --top

  # 创建带封面的文章
  python publish.py -t "精美文章" --cover "https://example.com/cover.jpg"

  # 列出所有文章
  python publish.py --list

  # 创建并立即部署
  python publish.py -t "新文章" --deploy
        """
    )

    parser.add_argument("-t", "--title", help="文章标题")
    parser.add_argument("-c", "--categories", help="文章分类，多个用逗号分隔")
    parser.add_argument("--tags", help="文章标签，多个用逗号分隔")
    parser.add_argument("--type", default="article", 
                       choices=["article", "tech", "life", "tutorial"],
                       help="文章类型 (默认: article)")
    parser.add_argument("--cover", help="封面图片URL或路径")
    parser.add_argument("-d", "--description", help="文章描述")
    parser.add_argument("--top", action="store_true", help="是否置顶")
    parser.add_argument("--list", action="store_true", help="列出所有文章")
    parser.add_argument("--deploy", action="store_true", help="创建后立即部署")
    parser.add_argument("--path", default=".", help="博客根目录路径 (默认: 当前目录)")

    args = parser.parse_args()

    # 初始化发布器
    publisher = HexoPublisher(args.path)

    # 列出文章
    if args.list:
        publisher.list_posts()
        return

    # 检查标题
    if not args.title:
        print("❌ 请提供文章标题，使用 -t 或 --title 参数")
        parser.print_help()
        return

    # 解析分类和标签
    categories = args.categories.split(",") if args.categories else None
    tags = args.tags.split(",") if args.tags else None

    # 创建文章
    print(f"\n📝 正在创建文章: {args.title}\n")
    filepath = publisher.create_post(
        title=args.title,
        categories=categories,
        tags=tags,
        post_type=args.type,
        cover=args.cover,
        description=args.description,
        top=args.top
    )

    # 部署
    if args.deploy and filepath:
        publisher.deploy()

if __name__ == "__main__":
    main()
