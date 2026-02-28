#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本转图片工具

该模块提供了一个函数，用于将文本列表转换为居中显示的PNG图片。
功能包括：
- 将列表中的每个元素作为单独的一行文本显示
- 支持自动垂直和水平居中对齐
- 自动选择中文字体（优先使用微软雅黑或黑体）
- 可自定义输出路径、字体大小、背景色、文字颜色和图片尺寸
"""

from PIL import Image, ImageDraw, ImageFont

def list_to_image(lst, output_path="output.png", font_size=20, bg_color=(255, 255, 255), text_color=(0, 0, 0), fixed_width=500, fixed_height=800):
    """
    将列表元素换行写入并生成PNG图片

    参数:
        lst: 要写入的列表
        output_path: 输出图片路径，默认为"output.png"
        font_size: 字体大小，默认为20
        bg_color: 背景颜色，默认为白色
        text_color: 文字颜色，默认为黑色
        fixed_width: 固定图片宽度，默认为800
        fixed_height: 固定图片高度，默认为600
    """
    try:
        # 使用支持中文的字体（如微软雅黑）
        font = ImageFont.truetype("msyh.ttc", font_size)
    except:
        try:
            # 如果找不到微软雅黑，尝试使用黑体
            font = ImageFont.truetype("simhei.ttf", font_size)
        except:
            # 如果都找不到，使用默认字体（可能不支持中文）
            font = ImageFont.load_default()

    # 创建固定尺寸的图片
    img = Image.new("RGB", (fixed_width, fixed_height), bg_color)
    draw = ImageDraw.Draw(img)

    # 计算总文本高度
    total_text_height = len(lst) * (font_size + 5)

    # 计算起始y坐标使文本垂直居中
    y_start = (fixed_height - total_text_height) // 2

    # 写入文本
    y = y_start
    for item in lst:
        text = str(item)
        # 计算文本宽度
        text_width = draw.textlength(text, font=font)
        # 计算x坐标使文本水平居中
        x = (fixed_width - text_width) // 2
        draw.text((x, y), text, fill=text_color, font=font)
        y += font_size + 5  # 行高

    # 保存图片
    img.save(output_path)
    print(f"图片已生成并保存到: {output_path}")


if __name__ == "__main__":
    list_to_image(["苹1果", "香3蕉", "橙子sada2", "西瓜", "葡萄asadq", "芒4果", "菠萝2", "草莓1"], "fruits.png")
