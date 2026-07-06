#!/usr/bin/env python3
"""爸爸 PDAC 治疗全程图（仿示例图风格）"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.lines import Line2D
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# 中文字体
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Zen Hei']
plt.rcParams['axes.unicode_minus'] = False

# 颜色
C_BG = '#FAFAFA'
C_TUMOR = '#E74C3C'  # CA19-9 红
C_BIL = '#F39C12'    # 胆红素 橙
C_CHEMO = '#3498DB'  # 化疗蓝
C_EVENT = '#8E44AD'  # 事件紫
C_WBC = '#27AE60'    # 白细胞绿
C_HGB = '#C0392B'    # 血红蛋白暗红
C_GRID = '#DDDDDD'
C_TEXT = '#2C3E50'

fig = plt.figure(figsize=(16, 11), facecolor='white')

# ==== Grid layout ====
# 顶部标题带
# Row1: CA19-9 (left) + TBIL (right)
# Row2: 化疗时间轴 + 关键事件 (整宽)
# Row3: 骨髓抑制 WBC/NEUT (left) + HGB (right)

# ---------- Title ----------
fig.text(0.5, 0.965, '张建来 · 胰腺癌 (PDAC) 治疗全程图',
         ha='center', fontsize=22, fontweight='bold', color=C_TEXT)
fig.text(0.5, 0.938, '2026-03 确诊 → AG 化疗 → Ⅱ 期升 Ⅳ 期 (肝转移) → 胆管炎 → 十二指肠 SEMS · 数据截至 2026-07-03',
         ha='center', fontsize=11, color='#7F8C8D', style='italic')

# ============ Row 1 Left: CA19-9 ============
ax1 = fig.add_axes([0.06, 0.61, 0.42, 0.26])
ca_dates = [datetime(2026,3,30), datetime(2026,5,9)]
ca_vals = [2203, 255]
ax1.plot(ca_dates, ca_vals, marker='o', color=C_TUMOR, linewidth=2.5, markersize=10, zorder=3)
for d, v in zip(ca_dates, ca_vals):
    ax1.annotate(f'{v}', (d, v), textcoords="offset points", xytext=(0,12),
                 ha='center', fontsize=11, fontweight='bold', color=C_TUMOR)
ax1.axhline(y=37, color='green', linestyle='--', alpha=0.5, linewidth=1)
ax1.text(datetime(2026,3,20), 100, '正常上限 37', fontsize=8, color='green')
ax1.set_title('① 肿瘤标志物 CA19-9 (U/mL)', fontsize=13, fontweight='bold', color=C_TEXT, loc='left')
ax1.set_ylabel('CA19-9 (U/mL)', fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_facecolor(C_BG)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
ax1.set_ylim(-100, 2500)
# annotation
ax1.annotate('↓88%\n(ERCP 引流为主)',
             xy=(datetime(2026,4,20), 1200), fontsize=9, color='#555',
             ha='center',
             bbox=dict(boxstyle='round,pad=0.4', fc='#FFF3CD', ec='#FFC107', alpha=0.9))

# ============ Row 1 Right: TBIL ============
ax2 = fig.add_axes([0.55, 0.61, 0.42, 0.26])
bil_dates = [datetime(2026,3,30), datetime(2026,5,9), datetime(2026,5,19), datetime(2026,7,3)]
bil_vals = [162.3, 53.8, 29.9, 7.8]  # 7.8 是 7/3 的
ax2.plot(bil_dates, bil_vals, marker='o', color=C_BIL, linewidth=2.5, markersize=10, zorder=3, label='TBIL 总胆红素')
for d, v in zip(bil_dates, bil_vals):
    ax2.annotate(f'{v}', (d, v), textcoords="offset points", xytext=(0,10),
                 ha='center', fontsize=10, fontweight='bold', color=C_BIL)
ax2.axhline(y=21, color='green', linestyle='--', alpha=0.5, linewidth=1)
ax2.text(datetime(2026,4,1), 12, '正常上限 21', fontsize=8, color='green')
ax2.set_title('② 总胆红素 TBIL (μmol/L)  —  ERCP 支架 + 化疗后完全正常化', fontsize=13, fontweight='bold', color=C_TEXT, loc='left')
ax2.set_ylabel('TBIL (μmol/L)', fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_facecolor(C_BG)
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
ax2.set_ylim(-10, 190)

# ============ Row 2: 时间轴 + 化疗周期 + 事件 ============
# Row2: 时间轴 更高一点容纳三层事件
ax3 = fig.add_axes([0.06, 0.30, 0.91, 0.24])
ax3.set_facecolor(C_BG)

# 时间范围
t_start = datetime(2026,3,20)
t_end = datetime(2026,7,10)
ax3.set_xlim(t_start, t_end)
ax3.set_ylim(0, 11)

# Y 分为三条泳道：
# y=7-8.5 关键事件卡片
# y=4-5.5 化疗周期条
# y=1.5-3  影像检查节点

# ---- 化疗周期条 ----
chemo_cycles = [
    (datetime(2026,5,11), datetime(2026,5,25), 'C1 (14d)'),
    (datetime(2026,5,25), datetime(2026,6,8),  'C2 (14d)'),
    (datetime(2026,6,8),  datetime(2026,6,21), 'C3 (中断)'),
]
for s, e, label in chemo_cycles:
    rect = Rectangle((mdates.date2num(s), 4.2), mdates.date2num(e)-mdates.date2num(s), 1.1,
                     facecolor=C_CHEMO, alpha=0.75, edgecolor='#2874A6', linewidth=1)
    ax3.add_patch(rect)
    mid = mdates.date2num(s) + (mdates.date2num(e)-mdates.date2num(s))/2
    ax3.text(mid, 4.75, label, ha='center', va='center', fontsize=10, color='white', fontweight='bold')

ax3.text(mdates.date2num(datetime(2026,3,22)), 4.75, 'AG 方案\n化疗周期',
         fontsize=9, color=C_CHEMO, fontweight='bold', va='center')

# ---- 关键临床事件 (顶部) ----
# 每个事件: (日期, 文字, 颜色, y层高, x偏移天数用于错位)
from datetime import timedelta
events = [
    (datetime(2026,3,30), '协和急诊\n黄疸+CA19-9 2203', '#E67E22', 8.9, 0),
    (datetime(2026,4,7),  'EUS-FNA\n病理确诊 PDAC', '#C0392B', 7.7, 0),
    (datetime(2026,4,10), 'ERCP 胆道支架\n(北医三院 张铃福)', '#16A085', 9.6, 0),
    (datetime(2026,5,9),  '肿瘤医院\n化疗前基线 CT', '#2980B9', 8.9, 0),
    (datetime(2026,6,14), '[!] MR 确认肝多发转移\nⅡ→Ⅳ 期 mPDAC', '#C0392B', 9.6, -3),
    (datetime(2026,6,21), '[急] 胆管炎急诊\n发热 39.2℃', '#E74C3C', 8.9, 0),
    (datetime(2026,6,22), '三腔营养管\n(北医三院)', '#8E44AD', 7.7, 3),
    (datetime(2026,7,2),  '★ 十二指肠 SEMS\n(北医三院 姚炜)', '#27AE60', 9.2, 0),
]

for d, txt, col, y, x_off_days in events:
    text_x = d + timedelta(days=x_off_days)
    # 事件圆点 (真实日期上)
    ax3.plot(d, 5.9, 'o', color=col, markersize=11, zorder=5, markeredgecolor='white', markeredgewidth=2)
    # 竖线/斜线到卡片
    ax3.plot([d, text_x], [5.9, y-0.05], color=col, linewidth=1.2, alpha=0.6, zorder=2)
    ax3.text(text_x, y, txt, ha='center', va='center', fontsize=8.2, color='white', fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.35', fc=col, ec=col, alpha=0.95))

# ---- 底部：影像/病理节点 ----
imaging = [
    (datetime(2026,4,4),  'CT 增强\n胰头 45mm\nSMV 受压', 1.5),
    (datetime(2026,5,9),  'CT 基线\n胰头 4.2×3.8\n肝疑转移',   1.5),
    (datetime(2026,6,13), 'CT 疗效评估\n病灶稳定',            0.55),
    (datetime(2026,6,14), 'MR 增强\n胰 4.9×3.8\n肝多发转移',   1.5),
]
for d, txt, y in imaging:
    ax3.plot(d, 2.6, 's', color='#5D6D7E', markersize=8, zorder=5)
    ax3.text(d, y, txt, ha='center', va='center', fontsize=7.8, color='#2C3E50',
             bbox=dict(boxstyle='round,pad=0.3', fc='#ECF0F1', ec='#95A5A6', alpha=0.9))

ax3.text(mdates.date2num(datetime(2026,3,22)), 2.6, '影像检查',
         fontsize=9, color='#5D6D7E', fontweight='bold', va='center')
ax3.text(mdates.date2num(datetime(2026,3,22)), 7.95, '关键临床事件',
         fontsize=9, color=C_EVENT, fontweight='bold', va='center')

ax3.set_title('③ 治疗时间轴：诊断 → 化疗 → 病情进展 → 并发症处理', fontsize=13, fontweight='bold', color=C_TEXT, loc='left')
ax3.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
ax3.set_yticks([])
for spine in ['top','right','left']:
    ax3.spines[spine].set_visible(False)
ax3.grid(True, axis='x', alpha=0.25)

# ============ Row 3 Left: WBC / NEUT ============
ax4 = fig.add_axes([0.06, 0.05, 0.42, 0.20])
mye_dates = [datetime(2026,5,9), datetime(2026,5,16), datetime(2026,5,19),
             datetime(2026,5,24), datetime(2026,5,28), datetime(2026,5,31),
             datetime(2026,6,3), datetime(2026,7,3)]
wbc = [5.06, 3.42, 4.48, None, 3.54, 2.63, 3.68, 5.42]
neut = [None, 2.01, 2.21, 1.71, 2.21, 1.18, 1.82, 3.79]

# 过滤 None
wbc_dates = [d for d,v in zip(mye_dates, wbc) if v is not None]
wbc_vals = [v for v in wbc if v is not None]
neut_dates = [d for d,v in zip(mye_dates, neut) if v is not None]
neut_vals = [v for v in neut if v is not None]

ax4.plot(wbc_dates, wbc_vals, marker='o', color=C_WBC, linewidth=2, markersize=8, label='WBC 白细胞')
ax4.plot(neut_dates, neut_vals, marker='s', color='#F39C12', linewidth=2, markersize=7, label='NEUT 中性粒')
ax4.axhline(y=3.5, color=C_WBC, linestyle=':', alpha=0.5, linewidth=1)
ax4.axhline(y=1.5, color='#F39C12', linestyle=':', alpha=0.5, linewidth=1)
ax4.text(datetime(2026,7,4), 3.5, 'WBC 下限', fontsize=7, color=C_WBC, va='center')
ax4.text(datetime(2026,7,4), 1.5, 'NEUT 下限', fontsize=7, color='#F39C12', va='center')

# 标注 II度骨髓抑制
ax4.annotate('II 度骨髓抑制\n(5/31)', xy=(datetime(2026,5,31), 1.18),
             xytext=(datetime(2026,5,31), -0.3),
             fontsize=8, color='red', ha='center',
             arrowprops=dict(arrowstyle='->', color='red'))

ax4.set_title('④ 骨髓抑制监测 WBC / NEUT (10^9/L)', fontsize=13, fontweight='bold', color=C_TEXT, loc='left')
ax4.set_facecolor(C_BG)
ax4.grid(True, alpha=0.3)
ax4.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
ax4.legend(loc='upper right', fontsize=9)
ax4.set_ylim(-0.8, 6.5)

# ============ Row 3 Right: HGB ============
ax5 = fig.add_axes([0.55, 0.05, 0.42, 0.20])
hgb_dates = [datetime(2026,5,9), datetime(2026,5,16), datetime(2026,5,19),
             datetime(2026,5,28), datetime(2026,5,31), datetime(2026,6,3), datetime(2026,7,3)]
hgb_vals = [100, 96, 94, 82, 85, 81, 90]
ax5.plot(hgb_dates, hgb_vals, marker='o', color=C_HGB, linewidth=2.5, markersize=9)
for d, v in zip(hgb_dates, hgb_vals):
    ax5.annotate(f'{v}', (d, v), textcoords="offset points", xytext=(0,10),
                 ha='center', fontsize=9, fontweight='bold', color=C_HGB)
ax5.axhline(y=130, color='green', linestyle='--', alpha=0.4, linewidth=1)
ax5.axhline(y=110, color='#F39C12', linestyle='--', alpha=0.5, linewidth=1)
ax5.axhline(y=90, color='red', linestyle='--', alpha=0.5, linewidth=1)
ax5.text(datetime(2026,7,4), 130, '正常 130', fontsize=7, color='green', va='center')
ax5.text(datetime(2026,7,4), 110, '轻度贫血 110', fontsize=7, color='#F39C12', va='center')
ax5.text(datetime(2026,7,4), 90, '中度 90', fontsize=7, color='red', va='center')

ax5.set_title('⑤ 血红蛋白 HGB (g/L)  —  7/3 回升至 90 (营养支持后)', fontsize=13, fontweight='bold', color=C_TEXT, loc='left')
ax5.set_facecolor(C_BG)
ax5.grid(True, alpha=0.3)
ax5.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
ax5.set_ylim(70, 140)

# ============ 底部标注：分子病理 ============
fig.text(0.5, 0.005,
         '[分子病理] KRAS G12D (26.9%) · TP53 V274D · CDKN2A 缺失 · Smad4 缺失 · CLDN18.2 60% 3+ · MTAP 缺失 · HER2 1+ · MSS/pMMR/TMB 4.1',
         ha='center', fontsize=9.5, color='#5D4037',
         bbox=dict(boxstyle='round,pad=0.5', fc='#FFF8E1', ec='#FFB300', alpha=0.85))

# 保存
out = '/home/ubuntu/.openclaw/workspace-health/charts/journey_v1.png'
plt.savefig(out, dpi=140, bbox_inches='tight', facecolor='white')
print(f'Saved: {out}')
