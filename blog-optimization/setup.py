#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hexo博客一键优化配置脚本
自动应用所有优化配置
"""

import os
import sys
import shutil
import subprocess
import json
from pathlib import Path

class BlogOptimizer:
    def __init__(self, blog_path="."):
        self.blog_path = Path(blog_path)
        self.css_path = self.blog_path / "source" / "css"
        self.js_path = self.blog_path / "source" / "js"
        self.tools_path = self.blog_path / "tools"
        self.img_path = self.blog_path / "source" / "img"
        self.covers_path = self.img_path / "covers"

    def check_prerequisites(self):
        """检查前置条件"""
        print("🔍 检查前置条件...")

        # 检查是否在Hexo目录
        if not (self.blog_path / "_config.yml").exists():
            print("❌ 错误: 当前目录不是Hexo博客根目录")
            print("请切换到博客根目录后运行此脚本")
            return False

        # 检查package.json
        if not (self.blog_path / "package.json").exists():
            print("❌ 错误: 找不到package.json")
            return False

        print("✅ 前置条件检查通过")
        return True

    def install_plugins(self):
        """安装必要的插件"""
        print("\n📦 安装优化插件...")

        plugins = [
            "hexo-generator-search",
            "hexo-generator-feed",
            "hexo-generator-sitemap",
            "hexo-generator-baidu-sitemap",
            "hexo-lazyload-image",
            "hexo-all-minifier",
            "hexo-filter-image-optimization"
        ]

        for plugin in plugins:
            print(f"  安装 {plugin}...")
            result = subprocess.run(
                ["npm", "install", plugin, "--save"],
                cwd=self.blog_path,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(f"  ⚠️  {plugin} 安装失败: {result.stderr}")
            else:
                print(f"  ✅ {plugin} 安装成功")

        print("✅ 插件安装完成")

    def create_directories(self):
        """创建必要的目录"""
        print("\n📁 创建目录结构...")

        directories = [
            self.css_path,
            self.js_path,
            self.tools_path,
            self.covers_path
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ {directory}")

        print("✅ 目录创建完成")

    def update_theme_config(self):
        """更新主题配置"""
        print("\n🎨 更新主题配置...")

        config_file = self.blog_path / "_config.anzhiyu.yml"
        if not config_file.exists():
            print("  ⚠️  主题配置文件不存在，跳过")
            return

        config_content = config_file.read_text(encoding='utf-8')

        # 添加inject配置
        if 'inject:' not in config_content:
            inject_config = """
# 自定义CSS/JS注入
inject:
  head:
    - <link rel="stylesheet" href="/css/apple-style.css">
  bottom:
    - <script src="/js/custom.js"></script>
"""
            config_content += inject_config
            print("  ✅ 添加inject配置")

        # 启用本地搜索
        if 'local_search:' not in config_content:
            search_config = """
# 本地搜索
local_search:
  enable: true
  preload: true
  top_n_per_article: 3
"""
            config_content += search_config
            print("  ✅ 启用本地搜索")

        config_file.write_text(config_content, encoding='utf-8')
        print("✅ 主题配置更新完成")

    def create_publish_script(self):
        """创建一键发布脚本"""
        print("\n📝 创建一键发布脚本...")

        script_content = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import datetime
import argparse
from pathlib import Path

class HexoPublisher:
    def __init__(self, blog_path="."):
        self.blog_path = Path(blog_path)
        self.posts_path = self.blog_path / "source" / "_posts"

    def create_post(self, title, categories=None, tags=None, top=False):
        now = datetime.datetime.now()
        filename = f"{title.replace(' ', '-').replace('/', '-')}.md"
        filepath = self.posts_path / filename

        front_matter = f"""---
title: "{title}"
date: {now.strftime('%Y-%m-%d %H:%M:%S')}
updated: {now.strftime('%Y-%m-%d %H:%M:%S')}
type: article
comments: true
toc: true
toc_number: true
copyright: true
"""

        if categories:
            front_matter += f"categories: [{categories}]\n"
        if tags:
            front_matter += f"tags: [{tags}]\n"
        if top:
            front_matter += "top: true\nsticky: 100\n"

        front_matter += "---\n\n"

        content = f"# {title}\n\n开始撰写你的文章内容...\n"

        filepath.write_text(front_matter + content, encoding='utf-8')
        print(f"✅ 文章创建成功: {filepath}")
        return filepath

    def deploy(self):
        print("🚀 部署到GitHub Pages...")
        os.system("hexo clean && hexo generate && hexo deploy")
        print("✅ 部署完成!")

def main():
    parser = argparse.ArgumentParser(description="Hexo一键发布工具")
    parser.add_argument("-t", "--title", required=True, help="文章标题")
    parser.add_argument("-c", "--categories", help="分类")
    parser.add_argument("--tags", help="标签")
    parser.add_argument("--top", action="store_true", help="置顶")
    parser.add_argument("--deploy", action="store_true", help="立即部署")

    args = parser.parse_args()

    publisher = HexoPublisher()
    publisher.create_post(args.title, args.categories, args.tags, args.top)

    if args.deploy:
        publisher.deploy()

if __name__ == "__main__":
    main()
"""

        script_file = self.tools_path / "publish.py"
        script_file.write_text(script_content, encoding='utf-8')

        # 添加执行权限
        os.chmod(script_file, 0o755)

        print(f"  ✅ 发布脚本创建: {script_file}")
        print("✅ 一键发布脚本创建完成")

    def create_custom_js(self):
        """创建自定义JS"""
        print("\n📜 创建自定义JS...")

        js_content = """
// 自定义JavaScript
console.log('🎉 欢迎来到CoolStar博客!');

// 快捷键支持
document.addEventListener('keydown', (e) => {
  // 按 / 打开搜索
  if (e.key === '/' && e.target.tagName !== 'INPUT') {
    e.preventDefault();
    const searchBtn = document.querySelector('.nav-search-btn');
    if (searchBtn) searchBtn.click();
  }

  // 按 ESC 关闭搜索
  if (e.key === 'Escape') {
    const closeBtn = document.querySelector('.search-close');
    if (closeBtn) closeBtn.click();
  }
});

// 页面加载完成提示
document.addEventListener('DOMContentLoaded', () => {
  console.log('✅ 页面加载完成');
});
"""

        js_file = self.js_path / "custom.js"
        js_file.write_text(js_content, encoding='utf-8')
        print(f"  ✅ JS文件创建: {js_file}")
        print("✅ 自定义JS创建完成")

    def create_robots_txt(self):
        """创建robots.txt"""
        print("\n🤖 创建robots.txt...")

        robots_content = """User-agent: *
Allow: /
Allow: /archives/
Allow: /categories/
Allow: /tags/
Disallow: /js/
Disallow: /css/

Sitemap: https://mhd250.github.io/azy-blog/sitemap.xml
"""

        robots_file = self.blog_path / "source" / "robots.txt"
        robots_file.write_text(robots_content, encoding='utf-8')
        print(f"  ✅ robots.txt创建: {robots_file}")
        print("✅ robots.txt创建完成")

    def generate_site(self):
        """生成静态文件"""
        print("\n🔨 生成静态文件...")

        result = subprocess.run(
            ["hexo", "clean"],
            cwd=self.blog_path,
            capture_output=True,
            text=True
        )

        result = subprocess.run(
            ["hexo", "generate"],
            cwd=self.blog_path,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("✅ 静态文件生成成功")
        else:
            print(f"⚠️  生成警告: {result.stderr}")

    def run_all(self):
        """运行所有优化"""
        print("=" * 50)
        print("🚀 Hexo博客一键优化脚本")
        print("=" * 50)

        if not self.check_prerequisites():
            return False

        try:
            self.install_plugins()
            self.create_directories()
            self.apply_apple_css()
            self.update_hexo_config()
            self.update_theme_config()
            self.create_publish_script()
            self.create_custom_js()
            self.create_robots_txt()
            self.generate_site()

            print("\n" + "=" * 50)
            print("✅ 所有优化配置已完成!")
            print("=" * 50)
            print("\n📋 后续步骤:")
            print("  1. 检查配置文件是否正确")
            print("  2. 运行 'hexo server' 预览效果")
            print("  3. 运行 'hexo deploy' 部署到GitHub Pages")
            print("\n📝 使用一键发布脚本:")
            print("  python tools/publish.py -t '文章标题' --deploy")
            print("\n🎉 享受你的新博客!")

            return True

        except Exception as e:
            print(f"\n❌ 错误: {e}")
            return False

def main():
    optimizer = BlogOptimizer()
    optimizer.run_all()

if __name__ == "__main__":
    main()
