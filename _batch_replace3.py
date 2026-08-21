# -*- coding: utf-8 -*-
'''第三批补齐：PART 08江淮制造 / PART 13智慧农业 / PART 15教育AI
每个模块补入08-20/21最新搜索内容（替换无日期的旧条目，保持条目数不变）
'''
import sys, io
sys.stdout.reconfigure(encoding='utf-8')

FILE = r'F:\个人作品\具身智能\generate_business_ppt.py'
t = io.open(FILE, encoding='utf-8').read()

# ============ 精确匹配旧内容 → 新内容 ============
REPLACEMENTS = [
    # PART 08 江淮制造：替换"最新行情"区第一条（无日期旧数据）
    (
        "'【安徽汽车产业规模数据】安徽是全国新能源汽车产业重镇，2026年全省新能源汽车产量预计超过250万辆，同比增长40%，产量占全国比重超过15%，集聚蔚来汽车、比亚迪、大众安徽、奇瑞汽车、江淮汽车五大整车企业，以及国轩高科、中创新航等动力电池企业，形成完整新能源汽车产业链，是全国新能源汽车出口重要基地",
        "'【江淮制造·2026年8月21日】光明日报\"活力中国调研行\"：安徽上半年高技术制造业增加值增长44.6%对规上工业增长贡献率55.9%，新能源汽车/新型显示/机器人等优势产业稳居全国第一方阵；奇瑞智造二工厂成国内首个通过国家智能制造能力成熟度四级认证的新能源乘用车工厂1-7月累计销售新能源车60.4万辆同比+42.3%连续23年中国品牌乘用车出口第一；蔚来新桥二工厂车身车间941台机器人火热作业+\"天探\"AI全身自检系统3分钟完成超1000项功能自测效率是人工10倍；奇瑞智界超级工厂10台机器人\"千手观音\"工位毫秒级协同关键工序100%自动化；安徽已集聚7家整车企业3000余家零部件企业\"芯屏汽合\"产业闭环企业不出安徽就能造一辆智能电动汽车"
    ),
    # PART 13 智慧农业：替换right区最后一条"未来趋势"（无日期）
    (
        "'【未来趋势】2030年农业机器人普及率达50%，基本实现农业生产智能化'",
        "'【农业无人机·2026年8月21日】贵州六盘水20多万亩红心猕猴桃进入采摘季引入吊运无人机空中转运鲜果采收效率大幅提升；中国农林植保无人机保有量从2018年约3万架增至2025年约30万架，农用无人机年作业面积突破4.6亿亩相比人工效率提升超30倍农药用量减少30%以上综合成本下降50%，当前渗透率约20%预计2030年升至50%以上；大疆农业无人机已应用100多个国家和地区全球累计销量突破60万台国内单年作业台数超32万台单年作业量突破33亿亩次实现650万吨物资吊运；杭州乔戈里科技智能采摘机器人搭载激光雷达/机器视觉多传感器融合+AI大模型自主识别成熟果实软爪轻抓技术正复制到番茄/草莓/黄瓜/彩椒；2026年中央一号文件首次提出拓展无人机/物联网/机器人应用场景农作物耕种收综合机械化率达76.7%农业科技进步贡献率超64%'"
    ),
    # PART 15 教育AI：替换right区第一条"T30"（无日期）
    (
        "'【科大讯飞AI学习机T30】旗舰学习机，星火大模型加持，个性化精准学，AI错题本/AI作文批改/AI口语陪练",
        "'【讯飞半年报·2026年8月20日】科大讯飞发布2026年半年度报告：营业收入116.23亿元同比+6.52%，研发投入超30亿元同比增超6亿元占营收比重超25%；星火智能批阅机签约销售量同比增长14倍累计服务学校超5000所，2026春季学期系统日均作业批改量突破360万份智能批改调用量较上学期增长5倍，小学阶段应用学校数量增长1.5倍语文学科批改量增长10倍；讯飞AI学习机推出T90旗舰系列与S90进阶系列完成从入门到高端全价格带布局，618期间再度位居京东/天猫两大平台学习机品类销售额首位；智慧教育产品已在全国33个省级行政区域落地应用并拓展至日本/新加坡等海外市场；8月18-20日2026全球智慧教育大会上讯飞星光AI超级智能体亮相，专为教师打造低门槛AI应用创作能力让一线教师成为AI应用开发主力军'"
    ),
]

count = 0
for old, new in REPLACEMENTS:
    if old in t:
        t = t.replace(old, new, 1)
        count += 1
        print(f'[OK] 替换成功: {old[:40]}...')
    else:
        print(f'[FAIL] 未找到: {old[:40]}...')

io.open(FILE, 'w', encoding='utf-8').write(t)
print(f'第三批补齐完成：{count}/3 条')

# 验证：22模块全部有新鲜内容
import re
lines = t.split('\n')
FRESH = re.compile(r'2026年8月2[01]日')
# PART01-12
parts = {}
for i, l in enumerate(lines):
    m = re.match(r"all_modules\.append\(\('PART (\d+)'", l)
    if m and int(m.group(1)) <= 12:
        parts[int(m.group(1))] = i
sorted_p = sorted(parts.keys())
all_ok = True
for idx, p in enumerate(sorted_p):
    start = parts[p]
    end = parts[sorted_p[idx+1]] if idx+1 < len(sorted_p) else 1380
    seg = '\n'.join(lines[start:end])
    n = len(FRESH.findall(seg))
    if n == 0:
        all_ok = False
        print(f'  [缺失] PART {p:02d}')
# PART13-22
cat_start = next(i for i, l in enumerate(lines) if 'def make_detail_module' in l)
module_starts = [i for i in range(cat_start, len(lines))
                 if re.match(r"\s+# (智慧农业|医疗健康|教育AI|能源电力|自动驾驶|人形运动会|真机部署|物流仓储|灵巧手|安防应急)", lines[i])]
for idx, s in enumerate(module_starts):
    e = module_starts[idx+1] if idx+1 < len(module_starts) else len(lines)
    seg = '\n'.join(lines[s:e])
    n = len(FRESH.findall(seg))
    if n == 0:
        all_ok = False
        print(f'  [缺失] PART {13+idx:02d}')
print(f'22模块核对: {"全部通过，无遗漏" if all_ok else "仍有缺失!"}')
