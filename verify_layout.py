# -*- coding: utf-8 -*-
"""
精确估算内容高度，验证是否溢出
"""
import re

# ========== 字体参数（严格按用户要求） ==========
FONT_SIZE_PT = 10  # 字号10pt
LINE_SPACING = 1.1  # 行距1.1
PT_PER_INCH = 72  # 1英寸=72磅
LINE_HEIGHT_INCH = FONT_SIZE_PT * LINE_SPACING / PT_PER_INCH  # 每行高度≈0.1528英寸
TITLE_HEIGHT_INCH = 11 * 1.1 / PT_PER_INCH  # 标题11pt≈0.168英寸
PROCESS_TITLE_HEIGHT_INCH = 10 * 1.1 / PT_PER_INCH  # 过程标题10pt≈0.153英寸

print(f'字体参数：')
print(f'  字号: {FONT_SIZE_PT}pt')
print(f'  行距: {LINE_SPACING}')
print(f'  每行高度: {LINE_HEIGHT_INCH:.4f}英寸')
print()

# ========== 文本框宽度（测试脚本v3参数） ==========
# 细节页无卡片，从x=0.25开始到x=13.333-0.2=13.18，宽度=12.88英寸
DETAIL_BOX_WIDTH_INCH = 13.333 - 2*0.15 - 0.1 - 0.05  # 12.88英寸
# 内容页左右栏卡片：col_w=(13.333-2*0.12-0.15)/2≈6.47英寸，文本框宽度=6.47-0.14=6.33英寸
CONTENT_BOX_WIDTH_INCH = (13.333 - 2*0.12 - 0.15)/2 - 0.14  # ≈6.33英寸
# 内容页下部通栏宽度=13.333-2*0.12-0.16=12.93英寸
CONTENT_LOWER_BOX_WIDTH_INCH = 13.333 - 2*0.12 - 0.16  # ≈12.93英寸

# 平均每英寸能放多少中文字符：10pt中文字≈0.14英寸宽 → 约7字符/英寸
CHARS_PER_INCH = 7
DETAIL_CHARS_PER_LINE = int(DETAIL_BOX_WIDTH_INCH * CHARS_PER_INCH)
CONTENT_CHARS_PER_LINE = int(CONTENT_BOX_WIDTH_INCH * CHARS_PER_INCH)
CONTENT_LOWER_CHARS_PER_LINE = int(CONTENT_LOWER_BOX_WIDTH_INCH * CHARS_PER_INCH)

print(f'文本框宽度：')
print(f'  细节页通栏: {DETAIL_BOX_WIDTH_INCH:.2f}英寸 → 约{DETAIL_CHARS_PER_LINE}字符/行')
print(f'  内容页左右栏: {CONTENT_BOX_WIDTH_INCH:.2f}英寸 → 约{CONTENT_CHARS_PER_LINE}字符/行')
print(f'  内容页下部通栏: {CONTENT_LOWER_BOX_WIDTH_INCH:.2f}英寸 → 约{CONTENT_LOWER_CHARS_PER_LINE}字符/行')
print()

def calc_lines(text, chars_per_line):
    """估算文本折行数"""
    # 去掉【】标签，按中文实际字符数计算
    clean_text = re.sub(r'【[^】]+】', '', text)
    char_count = len(clean_text)
    # 英文/数字宽度约为中文一半，简单估算
    lines = max(1, -(-char_count // chars_per_line))  # 向上取整
    return lines

def estimate_height(items, chars_per_line, has_title=False, title_lines=1, space_after_pt=0):
    """估算总高度"""
    total_lines = title_lines if has_title else 0
    total_lines += sum(calc_lines(item, chars_per_line) for item in items)
    space_after_total = len(items) * space_after_pt / PT_PER_INCH
    total_height = total_lines * LINE_HEIGHT_INCH + space_after_total
    return total_lines, total_height

# ========== 测试最长内容（消费电子细节页20条） ==========
detail_items_long = [
'【华为Mate 80 Pro】麒麟9020（7nm），8核CPU+12核GPU+24核NPU（120TOPS）；6.8英寸2K OLED 1-120Hz LTPO，3000nit亮度；后置5000万超光变主摄+4000万超广角+800万潜望长焦；5000mAh硅碳负极电池，100W有线+80W无线快充；鸿蒙OS 5.0支持天通卫星通话+北斗卫星消息；IP68防水；存储：8+256G 6499/12+256G 6999/12+512G 7999/16+1T 8999元',
'【华为Pura 80 Ultra】麒麟9020；6.9英寸2K LTPO OLED；一英寸超感光主摄（f/1.2-f/4.0可变光圈）+4000万超广角+2亿像素潜望长焦（200倍数码变焦）+TOF；5500mAh电池100W有线+80W无线；XMAGE影像系统+AI大模型计算摄影；IP68；纳米微晶陶瓷机身；存储：12+256G 8999/16+512G 9999/16+1T 11999元；2026年7月发布',
'【华为MateBook X Pro 2026】英特尔酷睿Ultra 9 288V + 昇腾310B独立NPU（128TOPS AI算力）；32GB LPDDR5X内存+2TB PCIe 4.0 SSD；14.2英寸3.1K柔性OLED原色屏，120Hz刷新率，100% DCI-P3色域；70Wh电池140W快充；1.15kg重量；鸿蒙OS for PC支持多屏协同/AI摘要/AI修图/AI会议纪要；存储：16+512G 9999/32+1T 12999/32+2T 15999元',
'【苹果iPhone 18 Pro Max】A19 Pro芯片（3nm第二代），8核CPU+8核GPU+16核NPU（150TOPS）；6.9英寸Super Retina XDR OLED，1-120Hz ProMotion，3500nit峰值亮度；后置4800万主摄（传感器位移防抖）+4800万超广角+1200万5倍潜望长焦；4800mAh电池45W有线+25W MagSafe无线；iOS 20全功能支持Apple Intelligence；钛金属中框IP69防水；存储：256G 9999/512G 11499/1T 13499元；2026年9月发布',
'【苹果MacBook Pro 16 M5】Apple M5 Max芯片：16核CPU（12性能+4能效）+40核GPU+32核NPU（180TOPS）；最高192GB统一内存+最高8TB SSD；16.2英寸Liquid Retina XDR显示屏，3456×2234分辨率，120Hz ProMotion，1600nit HDR峰值亮度；100Wh电池21小时视频播放；140W MagSafe快充；macOS Sequoia深度整合Apple Intelligence；重量2.1kg；存储：36+512G 19999/64+1T 24999/96+2T 29999/192+8T 45999元',
'【苹果Vision Pro 2】M5芯片+R2芯片；Micro-OLED双眼4K分辨率（单眼2300万像素），120Hz刷新率，120度视场角；重量450g（比一代减轻30%）；眼动追踪+手势追踪+空间音频；visionOS 3支持空间视频拍摄/沉浸式办公/空间游戏；外接电池续航4小时；存储：256G 14999元；2026年6月WWDC发布',
'【小米16 Ultra】高通骁龙8 Gen4（3nm）+澎湃P2快充芯片+澎湃G2电池管理芯片；6.9英寸2K LTPO AMOLED华星C9屏，1-144Hz自适应刷新率，4000nit峰值亮度，1920Hz PWM调光；后置徕卡四摄：一英寸LYT-900主摄（f/1.4-f/4.0可变光圈）+4000万超广角+2亿像素5倍潜望长焦+5000万像素10倍超长焦；6000mAh硅碳负极电池120W有线+50W无线；澎湃OS 3.0支持双向卫星通信；IP68防水陶瓷机身；存储：12+256G 5999/16+512G 6499/16+1T 7499/24+2T 8499元',
'【小米16 Pro】骁龙8 Gen4；6.7英寸2K 144Hz LTPO AMOLED；后置5000万LYT-800主摄+5000万超广角+5000万3倍潜望长焦；5500mAh电池120W有线+50W无线快充；澎湃OS 3.0；IP68防水金属中框玻璃后盖；存储：12+256G 4999/12+512G 5499/16+1T 6299元',
'【小米RedmiBook Pro 16 2026】英特尔酷睿Ultra 7 268V + 小米自研NPU（80TOPS AI算力）；32GB LPDDR5X内存+1TB PCIe 4.0 SSD（可扩展）；16英寸3.2K 120Hz IPS屏，100% sRGB色域，500nit亮度；80Wh电池100W快充；1.8kg重量；澎湃OS for Windows支持AI字幕/AI会议/AI画图/AI写作；存储：16+512G 4999/32+1T 5999元；2026年3月发布',
'【小米SU7 Ultra】三电机四驱系统：前220kW+后350kW+后350kW，系统总功率960kW（1306马力），系统总扭矩1680N·m；0-100km/h加速1.98秒，0-200km/h加速5.8秒，最高车速350km/h；宁德时代麒麟II电池130kWh，CLTC续航800km，800V高压平台10分钟补能400km；小米全栈自研智驾系统双Orin-X芯片（508TOPS）+激光雷达+11摄像头+12超声波+5毫米波雷达；21英寸轮毂碳陶瓷刹车；空气悬架+CDC电磁减振；售价52.99万元；2026年3月发布已交付',
'【AI功能共性】三大品牌旗舰全部支持：自然语言语音助手（连续对话/复杂指令/多轮交互）、AI拍照修图（AI消除/AI扩图/AI增强/AI夜景）、AI会议（实时录音转写/智能摘要/待办提取/多语种翻译）、AI写作（文案/邮件/报告/代码生成）、AI搜索（自然语言搜索/信息整合总结）、AI安全（隐私计算/端侧处理不上云）',
'【端侧大模型】华为盘古大模型端侧版（13B参数）、苹果Apple Intelligence（云端30B参数+端侧3B混合推理）、小米MiLM大模型端侧版（7B/13B），推理延迟<1秒，隐私敏感数据全程端侧处理不上传',
'【生态互联】华为鸿蒙分布式软总线支持手机/PC/平板/手表/车机/智能家居无缝流转接续；苹果Continuity支持iPhone/Mac/iPad/Watch/Vision Pro全生态设备无缝协同接力；小米澎湃OS HyperConnect支持全生态AIoT设备互联互通智能联动',
'【通信技术】华为独家支持天通一号卫星通话+北斗卫星消息+星闪NearLink；苹果支持卫星SOS紧急求助+卫星消息共享；小米支持双向卫星通信（天通+北斗）+5.5G NTN；三家旗舰均标配Wi-Fi 7/蓝牙5.4/NFC/红外遥控',
'【材料工艺】华为采用昆仑玻璃2代+玄武架构+纳米微晶陶瓷；苹果采用Grade 5钛金属中框+超瓷晶面板；小米采用龙晶玻璃+航空铝中框+陶瓷后盖；抗跌落抗刮擦耐用性较上一代提升2-3倍',
'【市场份额】2026年H1中国智能手机市场：华为28%份额重回第一，苹果18%第二，小米15%第三，三家合计占据61%市场份额；AI PC市场联想/华为/苹果/小米位列前四',
'【技术趋势1】端侧NPU算力快速提升：2026年旗舰手机NPU算力达100-150TOPS，AI PC NPU算力达80-180TOPS，可本地运行7B-13B参数大模型',
'【技术趋势2】多模态AI成为消费电子标配：支持文字/图像/视频/语音/3D空间等多模态信息理解、生成、编辑能力',
'【技术趋势3】AI代理（Agent）深度整合系统：手机/PC上的AI助理能够自主理解指令并完成订票/订餐/安排日程/处理邮件等复杂任务',
'【未来方向】2027-2030年AI终端形态向AR智能眼镜/脑机接口/智能家居服务机器人延伸，全场景个人AI助理成为现实'
]

print('===== 细节页（双数页）估算 =====')
detail_lines, detail_height = estimate_height(detail_items_long, DETAIL_CHARS_PER_LINE, has_title=True, title_lines=1, space_after_pt=0)
detail_box_height = 6.97 - 0.05  # 文本框高度≈6.92英寸
print(f'  总折行数：{detail_lines}行')
print(f'  估算内容高度：{detail_height:.2f}英寸')
print(f'  文本框可用高度：{detail_box_height:.2f}英寸')
print(f'  剩余空间：{detail_box_height - detail_height:.2f}英寸')
print(f'  是否溢出：{"❌ 溢出" if detail_height > detail_box_height else "✅ 不溢出"}')
print()

# ========== 内容页左右栏10条（人形机器人内容） ==========
content_left = [
'【市场规模】2026年全球人形机器人市场规模突破1200亿元人民币，中国市场占比超40%达480亿元，同比增长128%；全球出货量预计达18万台，其中中国市场出货8万台，占比44%',
'【产业定位】人形机器人是继智能手机、新能源汽车之后下一代通用智能终端，被国家列为未来产业重点培育方向，纳入十四五、十五五规划战略性新兴产业',
'【量产里程碑】2026年是人形机器人量产元年：特斯拉Optimus Gen3年产能目标10万台，优必选Walker X2年产能5万台，波士顿动力Atlas年产能1万台',
'【成本下降】人形机器人整机成本从2022年200万元/台快速下降到2026年20-30万元/台，预计2028年降至10-15万元，2030年进一步降至5-8万元',
'【核心技术突破】关节减速器国产化率从2023年15%提升到2026年65%；伺服电机国产化率达70%；六维力传感器国产化率突破50%',
'【政策支持】工信部发布《人形机器人创新发展指导意见》提出2025年实现技术突破、2027年形成完整产业生态',
'【产业链完善】已形成从核心零部件→本体制造→系统集成→场景应用完整产业链，四大产业集群快速成型',
'【资本热度】2026年H1人形机器人领域融资额超380亿元，单笔融资额平均超5亿元，多家企业估值超百亿元',
'【应用场景拓展】已从工业制造→商业服务→家庭服务→特种作业多场景落地',
'【安徽布局】安徽将人形机器人列为十大新兴产业重点方向，芜湖埃夫特、合肥欣奕华、蚌埠传感器形成配套'
]
print('===== 内容页左右栏估算 =====')
left_lines, left_height = estimate_height(content_left, CONTENT_CHARS_PER_LINE, has_title=True, title_lines=1, space_after_pt=0)
left_box_height = 2.9 - 0.1  # 文本框高度≈2.8英寸
print(f'  总折行数：{left_lines}行')
print(f'  估算内容高度：{left_height:.2f}英寸')
print(f'  文本框可用高度：{left_box_height:.2f}英寸')
print(f'  剩余空间：{left_box_height - left_height:.2f}英寸')
print(f'  是否溢出：{"❌ 溢出" if left_height > left_box_height else "✅ 不溢出"}')
print()

# ========== 内容页下部5条 ==========
content_process = [
'【研发阶段（2022-2025）】技术验证期：波士顿动力Atlas实现后空翻但液压驱动成本高昂；特斯拉Optimus Gen1亮相仅能简单行走；国内企业完成原型机验证，单台成本超百万元',
'【量产元年（2026年）】规模化落地期：特斯拉/优必选等头部企业实现万台级量产交付，核心零部件国产化率超80%，成本快速下降至15-25万元区间，工业场景率先规模化部署',
'【规模爆发（2027-2028）】成本下探至10-15万元，应用场景从工业向商业服务/家庭陪护渗透，年销量突破20万台，产业生态逐步成熟',
'【普及阶段（2029-2030）】成本进一步降至5-8万元接近家用轿车价格，具身智能大模型成熟，年销量突破100万台，中国成为全球最大生产应用市场',
'【产业价值】带动核心零部件/AI算法/系统集成/场景应用全产业链发展，预计2030年带动相关产业规模超万亿元，创造百万级就业岗位'
]
print('===== 内容页下部通栏估算 =====')
lower_lines, lower_height = estimate_height(content_process, CONTENT_LOWER_CHARS_PER_LINE, has_title=True, title_lines=1, space_after_pt=2)
lower_box_height = 2.79 - 0.1  # 文本框高度≈2.69英寸
print(f'  总折行数：{lower_lines}行')
print(f'  估算内容高度：{lower_height:.2f}英寸')
print(f'  文本框可用高度：{lower_box_height:.2f}英寸')
print(f'  剩余空间：{lower_box_height - lower_height:.2f}英寸')
print(f'  是否溢出：{"❌ 溢出" if lower_height > lower_box_height else "✅ 不溢出"}')
