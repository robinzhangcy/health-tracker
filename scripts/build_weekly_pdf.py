#!/usr/bin/env python3
"""每周健康趋势记录表 - 通用版"""
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.enums import TA_CENTER
import os

pdfmetrics.registerFont(TTFont('CN', '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'))
pdfmetrics.registerFont(TTFont('CN-B', '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'))

OUT = '/home/ubuntu/.openclaw/workspace-health/output/每周健康趋势表_通用版.pdf'
os.makedirs(os.path.dirname(OUT), exist_ok=True)

# 配色
C_HEADER = colors.HexColor('#2C5F8D')
C_HEADER_BG = colors.HexColor('#E8F0F7')
C_ROW_ALT = colors.HexColor('#F8F9FB')
C_BORDER = colors.HexColor('#C8D0D8')
C_WARN_BG = colors.HexColor('#FDF2F2')
C_WARN = colors.HexColor('#D9534F')
C_SEC_BG = colors.HexColor('#F4EFE7')  # 暖色分类底
C_SEC_TXT = colors.HexColor('#8B5A2B')

S_TITLE = ParagraphStyle('T', fontName='CN-B', fontSize=16, leading=20,
                          textColor=C_HEADER, alignment=TA_CENTER, spaceAfter=2)
S_SUB = ParagraphStyle('S', fontName='CN', fontSize=8.5, leading=11,
                        textColor=colors.HexColor('#666'), alignment=TA_CENTER, spaceAfter=4)
S_NORM = ParagraphStyle('N', fontName='CN', fontSize=9, leading=12)


def header_block():
    title = Paragraph("每周健康趋势记录表", S_TITLE)
    sub = Paragraph("住院 / 居家 · 慢病管理与营养支持通用模板 · 7 日趋势对比", S_SUB)
    info = Table([[
        Paragraph("<b>第__周</b>", S_NORM),
        Paragraph("<b>起止：</b>2026 / __ / __  —  __ / __", S_NORM),
        Paragraph("<b>姓名：</b>______", S_NORM),
        Paragraph("<b>床号/病案号：</b>______", S_NORM),
        Paragraph("<b>治疗阶段：</b>______", S_NORM),
    ]], colWidths=[20*mm, 70*mm, 40*mm, 70*mm, 50*mm])
    info.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'CN'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('BACKGROUND', (0,0), (-1,-1), C_HEADER_BG),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    return [title, sub, info, Spacer(1, 2)]


def weekly_table():
    """每周趋势主表 - 横向 7 天"""
    # 列: 项目 + 7 天 + 趋势
    col_w = [40*mm] + [29*mm]*7 + [20*mm]   # 40 + 29*7 + 20 = 263 mm（横向 A4 = 297 - 20 = 277 mm 边距）

    sections = [
        ("🌡 生命体征", [
            "晨起体重 (kg)",
            "晨起腹围 (cm)",
            "体温·最高 (℃)",
            "体温·最低 (℃)",
            "血压·最高 (mmHg)",
            "血压·最低 (mmHg)",
            "心率·平均 (次/分)",
        ]),
        ("🩸 血糖 (mmol/L)", [
            "空腹",
            "早餐后 2h",
            "午餐后 2h",
            "晚餐后 2h",
            "睡前",
            "夜间最低（如有）",
        ]),
        ("💧 24h 出入量 (ml)", [
            "总入量 (静脉+肠内+肠外+口服)",
            "总出量 (尿+引流+大便+呕吐)",
            "尿量 (ml / 次数)",
            "大便 (次数 / 性状)",
            "净出入 (入−出)",
        ]),
        ("💊 用药 / 化验 / 检查", [
            "今日用药变化",
            "今日检查 / 化验",
            "新发症状",
            "医生交代",
        ]),
        ("📝 整体评估", [
            "精神 (好/一般/差)",
            "食欲 (好/一般/差)",
            "睡眠 (h)",
            "疼痛 (0-10)",
        ]),
    ]

    days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    head = ['项目'] + days + ['趋势/备注']

    data = [head]
    row_styles = []  # (row_idx, type) for styling: 'section' or 'data'
    row_heights = [6.5*mm]

    for sec_name, items in sections:
        # 分类头行
        data.append([sec_name] + [''] * 7 + [''])
        row_styles.append(('section', len(data) - 1))
        row_heights.append(6*mm)
        for it in items:
            data.append([it] + [''] * 7 + [''])
            row_styles.append(('data', len(data) - 1))
            row_heights.append(5*mm)

    t = Table(data, colWidths=col_w, rowHeights=row_heights, repeatRows=1)

    style = [
        ('FONTNAME', (0,0), (-1,-1), 'CN'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        # 表头
        ('FONTNAME', (0,0), (-1,0), 'CN-B'),
        ('FONTSIZE', (0,0), (-1,0), 9.5),
        ('BACKGROUND', (0,0), (-1,0), C_HEADER),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        # 数据
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,1), (0,-1), 'LEFT'),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.4, C_BORDER),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        # 周末列底色
        ('BACKGROUND', (6,0), (6,0), colors.HexColor('#1F4D7A')),  # 周六 head
        ('BACKGROUND', (7,0), (7,0), colors.HexColor('#1F4D7A')),  # 周日 head
    ]

    for typ, ridx in row_styles:
        if typ == 'section':
            style.append(('SPAN', (0, ridx), (-1, ridx)))
            style.append(('BACKGROUND', (0, ridx), (-1, ridx), C_SEC_BG))
            style.append(('FONTNAME', (0, ridx), (-1, ridx), 'CN-B'))
            style.append(('TEXTCOLOR', (0, ridx), (-1, ridx), C_SEC_TXT))
            style.append(('FONTSIZE', (0, ridx), (-1, ridx), 10))
            style.append(('ALIGN', (0, ridx), (-1, ridx), 'LEFT'))
            style.append(('LEFTPADDING', (0, ridx), (-1, ridx), 8))
        else:
            # 数据行隔行底色（在分类块内交替）
            if ridx % 2 == 0:
                style.append(('BACKGROUND', (0, ridx), (-1, ridx), C_ROW_ALT))
            # 周末列淡色背景
            style.append(('BACKGROUND', (6, ridx), (7, ridx), colors.HexColor('#F0F4F8')))

    t.setStyle(TableStyle(style))
    return t


def section_bar(text, emoji=""):
    bar = Table([[Paragraph(f"<b>{emoji}  {text}</b>",
                            ParagraphStyle('ST', fontName='CN-B', fontSize=11, textColor=colors.white))]],
                colWidths=[277*mm])
    bar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_HEADER),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    return bar


def alert_box():
    head1 = "🚨 立即通知医生"
    items1 = [
        "体温 > 38.5℃ 或寒战",
        "血压 > 180/110 或 < 90/60",
        "血糖 < 3.9 或 > 15 mmol/L",
        "24h 尿量 < 500 ml",
        "胃管引流血性 或 > 1000 ml/d",
        "大便黑色 或 鲜血",
        "腹围 1 日 ↑ > 2 cm  /  体重 1 日 ↑ > 1.5 kg",
        "突发胸闷 / 气短 / 下肢肿胀 (VTE 警示)",
    ]
    head2 = "⚠ 趋势异常 24h 内告知医生"
    items2 = [
        "体重连续 3 天下降 > 0.5 kg/d",
        "腹围逐日增加 > 1 cm",
        "净入量连续 ≥ 2 天 > 1000 ml",
        "尿量连续 ≥ 2 天 < 1000 ml",
        "血压连续偏高/偏低 ≥ 3 次",
        "血糖空腹连续 ≥ 3 次 > 10",
        "大便 > 5 次/日 或 > 3 天无大便",
        "精神/食欲明显变差持续 ≥ 2 天",
    ]
    head3 = "📊 每周回顾问题清单"
    items3 = [
        "本周体重 / 腹围 整体趋势？",
        "用药耐受情况？有无新增副作用？",
        "营养摄入是否达标（约 25-30 kcal/kg/d）？",
        "出入量平衡是否合理？",
        "化验指标关键变化？",
        "症状改善 / 加重？",
        "下周复诊 / 复查项目？",
        "需向主治医生沟通的问题？",
    ]

    def col(title_text, color, items):
        body = "<br/>".join(f"• {x}" for x in items)
        return Paragraph(
            f"<font color='{color}'><b>{title_text}</b></font><br/><br/>{body}",
            ParagraphStyle('AC', fontName='CN', fontSize=8.5, leading=12))

    p1 = col(head1, '#D9534F', items1)
    p2 = col(head2, '#E07B00', items2)
    p3 = col(head3, '#2C5F8D', items3)
    t = Table([[p1, p2, p3]], colWidths=[91*mm, 93*mm, 93*mm])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (0,0), C_WARN_BG),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor('#FDF7ED')),
        ('BACKGROUND', (2,0), (2,0), C_HEADER_BG),
        ('BOX', (0,0), (0,0), 1.0, C_WARN),
        ('BOX', (1,0), (1,0), 1.0, colors.HexColor('#E07B00')),
        ('BOX', (2,0), (2,0), 1.0, C_HEADER),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    return t


def summary_box():
    """周末总结 - 自由书写区"""
    body = (
        "<b>本周主要进展（症状/治疗/检查）：</b><br/>"
        "_________________________________________________________________________________________________________________<br/>"
        "_________________________________________________________________________________________________________________<br/><br/>"
        "<b>本周关键化验/检查异常：</b><br/>"
        "_________________________________________________________________________________________________________________<br/>"
        "_________________________________________________________________________________________________________________<br/><br/>"
        "<b>下周计划（复诊/复查/治疗）：</b><br/>"
        "_________________________________________________________________________________________________________________<br/>"
        "_________________________________________________________________________________________________________________"
    )
    p = Paragraph(body, ParagraphStyle('SB', fontName='CN', fontSize=9, leading=18))
    t = Table([[p]], colWidths=[277*mm])
    t.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FBFBFB')),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    return t


# ===== 构建文档（横向 A4）=====
doc = SimpleDocTemplate(OUT, pagesize=landscape(A4),
                        leftMargin=10*mm, rightMargin=10*mm,
                        topMargin=5*mm, bottomMargin=5*mm,
                        title="每周健康趋势记录表")

story = []
story.extend(header_block())
story.append(Spacer(1, 1))
story.append(section_bar("7 日趋势记录 · 每日填写", "📅"))
story.append(Spacer(1, 2))
story.append(weekly_table())

# 第 2 页
story.append(PageBreak())
story.extend(header_block())
story.append(Spacer(1, 1))
story.append(section_bar("危急值速查 + 每周回顾", "🚨"))
story.append(Spacer(1, 4))
story.append(alert_box())
story.append(Spacer(1, 10))
story.append(section_bar("周末总结", "📝"))
story.append(Spacer(1, 4))
story.append(summary_box())

story.append(Spacer(1, 10))
foot = Paragraph(
    "💪 家庭健康管理 · 本表用于日常监测，不替代医疗判断，关键决策务必遵医嘱",
    ParagraphStyle('F', fontName='CN', fontSize=7.5, leading=10,
                   textColor=colors.HexColor('#888'), alignment=TA_CENTER))
story.append(foot)

doc.build(story)
print(f"✅ 已生成: {OUT}")
