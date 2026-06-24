#!/usr/bin/env python3
"""每日健康记录 A4 PDF — 张建来病情管理"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

# 中文字体
pdfmetrics.registerFont(TTFont('CN', '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'))
pdfmetrics.registerFont(TTFont('CN-B', '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'))

OUT = '/home/ubuntu/.openclaw/workspace-health/output/每日健康记录表_通用版.pdf'
os.makedirs(os.path.dirname(OUT), exist_ok=True)

# 颜色
C_HEADER = colors.HexColor('#2C5F8D')     # 深蓝
C_HEADER_BG = colors.HexColor('#E8F0F7')  # 浅蓝
C_ROW_ALT = colors.HexColor('#F8F9FB')    # 灰白
C_WARN = colors.HexColor('#D9534F')       # 红
C_WARN_BG = colors.HexColor('#FDF2F2')    # 浅红
C_OK_BG = colors.HexColor('#F0F7F0')      # 浅绿
C_BORDER = colors.HexColor('#C8D0D8')     # 浅灰边

styles = getSampleStyleSheet()
S_TITLE = ParagraphStyle('T', fontName='CN-B', fontSize=18, leading=22,
                          textColor=C_HEADER, alignment=TA_CENTER, spaceAfter=4)
S_SUB = ParagraphStyle('S', fontName='CN', fontSize=9, leading=12,
                        textColor=colors.HexColor('#666'), alignment=TA_CENTER, spaceAfter=10)
S_H2 = ParagraphStyle('H2', fontName='CN-B', fontSize=12, leading=16,
                       textColor=C_HEADER, spaceBefore=8, spaceAfter=4)
S_NORM = ParagraphStyle('N', fontName='CN', fontSize=9, leading=12)
S_SMALL = ParagraphStyle('SM', fontName='CN', fontSize=8, leading=10, textColor=colors.HexColor('#444'))


def header_block():
    title = Paragraph("每日健康记录表", S_TITLE)
    sub = Paragraph("住院 / 居家 · 慢病管理与营养支持通用模板", S_SUB)
    info = Table([[
        Paragraph("<b>日期：</b>2026 / __ / __ （星期__）", S_NORM),
        Paragraph("<b>住院第__天</b>", S_NORM),
        Paragraph("<b>治疗阶段：</b>______", S_NORM),
        Paragraph("<b>床号 / 病案号：</b>______", S_NORM),
    ]], colWidths=[60*mm, 35*mm, 35*mm, 40*mm])
    info.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'CN'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('BACKGROUND', (0,0), (-1,-1), C_HEADER_BG),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    return [title, sub, info, Spacer(1, 6)]


def vital_table():
    """生命体征 — 7 时段"""
    head = ['时段','时间','体温℃','血压','心率','血糖','体重(晨)','腹围(晨)','备注/症状']
    rows = [
        ['晨起',   '06:00', '', '   /   ', '', '空腹', '___ kg', '___ cm', ''],
        ['早餐后', '09:00', '', '   /   ', '', '餐后2h', '—', '—', ''],
        ['午前',   '11:30', '', '   /   ', '', '餐前', '—', '—', ''],
        ['午餐后', '14:00', '', '   /   ', '', '餐后2h', '—', '—', ''],
        ['下午',   '17:00', '', '   /   ', '', '餐前', '—', '—', ''],
        ['晚餐后', '20:00', '', '   /   ', '', '餐后2h', '—', '—', ''],
        ['睡前',   '22:00', '', '   /   ', '', '睡前', '—', '—', ''],
        ['夜间',   '__:__', '', '   /   ', '', '', '—', '—', ''],
    ]
    data = [head] + rows
    col_w = [14*mm, 14*mm, 14*mm, 22*mm, 14*mm, 22*mm, 22*mm, 22*mm, 36*mm]
    t = Table(data, colWidths=col_w, rowHeights=[7*mm]+[8*mm]*len(rows))
    style = [
        ('FONTNAME', (0,0), (-1,-1), 'CN'),
        ('FONTNAME', (0,0), (-1,0), 'CN-B'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('FONTSIZE', (0,1), (-1,-1), 9),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BACKGROUND', (0,0), (-1,0), C_HEADER),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.4, C_BORDER),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]
    # 隔行底色
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(('BACKGROUND', (0,i), (-1,i), C_ROW_ALT))
    # 时段列加粗
    style.append(('FONTNAME', (0,1), (0,-1), 'CN-B'))
    style.append(('TEXTCOLOR', (0,1), (0,-1), C_HEADER))
    t.setStyle(TableStyle(style))
    return t


def intake_table():
    """入量"""
    head = ['时间', '类别', '项目', '量 (ml)', '速度', '备注']
    blank = ['', '', '', '', '', '']
    rows = [blank for _ in range(6)]
    data = [head] + rows
    col_w = [18*mm, 20*mm, 50*mm, 20*mm, 20*mm, 52*mm]
    t = Table(data, colWidths=col_w, rowHeights=[7*mm]+[7*mm]*len(rows))
    style = [
        ('FONTNAME', (0,0), (-1,-1), 'CN'),
        ('FONTNAME', (0,0), (-1,0), 'CN-B'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BACKGROUND', (0,0), (-1,0), C_HEADER),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.4, C_BORDER),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(('BACKGROUND', (0,i), (-1,i), C_ROW_ALT))
    t.setStyle(TableStyle(style))
    return t


def output_table():
    head = ['时间', '类别', '量 (ml) / 次数', '颜色 / 性状', '备注']
    blank = ['', '', '', '', '']
    rows = [blank for _ in range(5)]
    data = [head] + rows
    col_w = [18*mm, 30*mm, 35*mm, 40*mm, 57*mm]
    t = Table(data, colWidths=col_w, rowHeights=[7*mm]+[7*mm]*len(rows))
    style = [
        ('FONTNAME', (0,0), (-1,-1), 'CN'),
        ('FONTNAME', (0,0), (-1,0), 'CN-B'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BACKGROUND', (0,0), (-1,0), C_HEADER),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.4, C_BORDER),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(('BACKGROUND', (0,i), (-1,i), C_ROW_ALT))
    t.setStyle(TableStyle(style))
    return t


def summary_table():
    """24h 汇总"""
    data = [
        ['📥 入量汇总', '', '', '📤 出量汇总', '', ''],
        ['静脉补液', '____ ml', '', '尿量', '____ ml', '(___ 次)'],
        ['肠内营养 TPF', '____ ml', '', '胃管引流', '____ ml', '颜色 ____'],
        ['肠外营养 PN', '____ ml', '', '大便', '___ 次', '性状 ____'],
        ['口服水/汤', '____ ml', '', '呕吐', '____ ml', ''],
        ['总入量', '____ ml', '', '总出量', '____ ml', ''],
        ['净出入', '入 − 出 = ____ ml', '', '评估', '☐ 平衡  ☐ 净入↑⚠  ☐ 净出↑⚠', ''],
    ]
    col_w = [28*mm, 30*mm, 4*mm, 28*mm, 30*mm, 36*mm]
    t = Table(data, colWidths=col_w, rowHeights=[7*mm]+[7.5*mm]*6)
    style = [
        ('FONTNAME', (0,0), (-1,-1), 'CN'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('FONTNAME', (0,0), (1,0), 'CN-B'),
        ('FONTNAME', (3,0), (5,0), 'CN-B'),
        ('FONTNAME', (0,-1), (0,-1), 'CN-B'),
        ('FONTNAME', (3,-1), (3,-1), 'CN-B'),
        ('FONTNAME', (0,-2), (0,-2), 'CN-B'),
        ('FONTNAME', (3,-2), (3,-2), 'CN-B'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BACKGROUND', (0,0), (1,0), C_HEADER_BG),
        ('BACKGROUND', (3,0), (5,0), C_HEADER_BG),
        ('TEXTCOLOR', (0,0), (1,0), C_HEADER),
        ('TEXTCOLOR', (3,0), (5,0), C_HEADER),
        ('GRID', (0,0), (1,-1), 0.4, C_BORDER),
        ('GRID', (3,0), (5,-1), 0.4, C_BORDER),
        ('LINEBELOW', (0,-2), (1,-2), 1.2, C_HEADER),
        ('LINEBELOW', (3,-2), (5,-2), 1.2, C_HEADER),
        ('BACKGROUND', (0,-1), (1,-1), C_HEADER_BG),
        ('BACKGROUND', (3,-1), (5,-1), C_HEADER_BG),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]
    t.setStyle(TableStyle(style))
    return t


def alert_box():
    """关键阈值速查 — 红色警示框"""
    head1 = "🚨 立即通知医生"
    items1 = [
        "体温 > 38.5℃ 或寒战",
        "血压 > 180/110 或 < 90/60",
        "血糖 < 3.9 或 > 15 mmol/L",
        "24h 尿量 < 500 ml",
        "胃管引流为血性 或 > 1000 ml/d",
        "大便黑色 或 鲜血",
        "腹围 1 日内增加 > 2 cm",
        "体重 1 日内增加 > 1.5 kg",
        "突发胸闷 / 气短 / 下肢肿胀 (VTE)",
    ]
    head2 = "⚠ 24h 内告知医生"
    items2 = [
        "体温 37.5–38.5℃",
        "血压 160–180 / 100–110",
        "血糖 10–15 或 4.0–5.0",
        "净入量持续 > 1000 ml × 2 天",
        "大便 > 5 次/日 或 > 3 天无大便",
        "三腔管耐受问题（腹胀/反流）",
        "精神状态明显变差",
        "新发疼痛 / 黄疸加深",
        "ALB、PA、K、P 等急剧波动",
    ]
    left_lines = "<br/>".join(f"• {x}" for x in items1)
    right_lines = "<br/>".join(f"• {x}" for x in items2)
    p_left = Paragraph(f"<font color='#D9534F'><b>{head1}</b></font><br/><br/>{left_lines}",
                       ParagraphStyle('AL', fontName='CN', fontSize=8.5, leading=12))
    p_right = Paragraph(f"<font color='#E07B00'><b>{head2}</b></font><br/><br/>{right_lines}",
                        ParagraphStyle('AR', fontName='CN', fontSize=8.5, leading=12))
    t = Table([[p_left, p_right]], colWidths=[90*mm, 90*mm])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (0,0), C_WARN_BG),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor('#FDF7ED')),
        ('BOX', (0,0), (0,0), 1.0, C_WARN),
        ('BOX', (1,0), (1,0), 1.0, colors.HexColor('#E07B00')),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    return t


def medication_box():
    """当前用药备忘 — 顶部参考"""
    items = [
        ['类别', '药物', '剂量频次', '注意'],
        ['抗感染', '头孢他啶', '2g ivgtt qd', '+ 美洛西林 + 左奥硝唑'],
        ['保肝',   '谷胱甘肽 1.2g', 'ivgtt qd', '硫普罗宁 0.1g qd'],
        ['肠内营养', 'TPF (能全力类)', '60 ml/h 鼻饲泵入', '500 ml/d 起步，渐加量'],
        ['肠外营养', '糖+脂+氨基酸+电解质', 'PN 每日 1 组', '含 14AA-SF 肝病配方'],
        ['止吐',    '昂丹司琼', '8 mg 按需', 'q8-12h, ≤16 mg/d'],
        ['补血',    '生血宝合剂', '15 ml tid', '口服 / 鼻饲'],
        ['化疗',   '白蛋白紫杉醇 + 吉西他滨', 'C__ 暂缓', '待营养/感染稳定'],
    ]
    col_w = [18*mm, 45*mm, 50*mm, 65*mm]
    t = Table(items, colWidths=col_w, rowHeights=[7*mm]+[7*mm]*(len(items)-1))
    style = [
        ('FONTNAME', (0,0), (-1,-1), 'CN'),
        ('FONTNAME', (0,0), (-1,0), 'CN-B'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BACKGROUND', (0,0), (-1,0), C_HEADER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.4, C_BORDER),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
    ]
    for i in range(1, len(items)):
        if i % 2 == 0:
            style.append(('BACKGROUND', (0,i), (-1,i), C_ROW_ALT))
    t.setStyle(TableStyle(style))
    return t


def section_title(text, emoji=""):
    bar = Table([[Paragraph(f"<b>{emoji}  {text}</b>",
                            ParagraphStyle('ST', fontName='CN-B', fontSize=11, textColor=colors.white))]],
                colWidths=[180*mm])
    bar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_HEADER),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    return bar


def notes_box():
    p = Paragraph(
        "<b>今日重点观察：</b>______________________________________________________"
        "____________________________________________________________________"
        "<br/><br/>"
        "<b>医生交代：</b>____________________________________________________________"
        "____________________________________________________________________"
        "<br/><br/>"
        "<b>明日待办：</b>____________________________________________________________"
        "____________________________________________________________________",
        ParagraphStyle('NB', fontName='CN', fontSize=9, leading=18))
    t = Table([[p]], colWidths=[180*mm])
    t.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FBFBFB')),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    return t


# ===== 构建文档 =====
doc = SimpleDocTemplate(OUT, pagesize=A4,
                        leftMargin=12*mm, rightMargin=12*mm,
                        topMargin=8*mm, bottomMargin=8*mm,
                        title="每日健康记录表 - 通用版")

story = []
# 第 1 页：生命体征 + 出入量
story.extend(header_block())
story.append(Spacer(1,1))
story.append(section_title("生命体征 · 每日 7+1 时段", "🩺"))
story.append(Spacer(1, 2))
story.append(vital_table())
story.append(Spacer(1, 3))

story.append(section_title("入量记录 · 每次填一条", "💧"))
story.append(Spacer(1, 2))
story.append(intake_table())
story.append(Spacer(1, 3))

story.append(section_title("出量记录 · 每次填一条", "🚽"))
story.append(Spacer(1, 2))
story.append(output_table())
story.append(Spacer(1, 3))

story.append(section_title("24h 汇总", "📊"))
story.append(Spacer(1, 2))
story.append(summary_table())

# 第 2 页：用药 + 警示 + 记事
story.append(PageBreak())
story.extend(header_block())

story.append(section_title("危急值速查 · 一目了然", "🚨"))
story.append(Spacer(1, 4))
story.append(alert_box())
story.append(Spacer(1, 8))

story.append(section_title("每日总结", "📝"))
story.append(Spacer(1, 4))
story.append(notes_box())

story.append(Spacer(1, 8))
foot = Paragraph(
    "💪 家庭健康管理 · 本表用于日常监测，不替代医疗判断，关键决策务必遵医嘱",
    ParagraphStyle('F', fontName='CN', fontSize=7.5, leading=10,
                   textColor=colors.HexColor('#888'), alignment=TA_CENTER))
story.append(foot)

doc.build(story)
print(f"✅ 已生成: {OUT}")
