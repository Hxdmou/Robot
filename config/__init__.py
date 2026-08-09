"""
全国综合信息查询系统配置模块
"""
import os

env_vars = {}
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()


class Config:
    """系统配置类"""
    
    AMAP_WEB_KEY = env_vars.get("AMAP_WEB_KEY", "f221c7709ac0a113d85755e15e5a9e79")
    AMAP_JS_KEY = env_vars.get("AMAP_JS_KEY", "377be4220a9eebd6734380fa52c8b11f")
    AMAP_JS_SECURITY_CODE = env_vars.get("AMAP_JS_SECURITY_CODE", "56504076a546bfb490654db68b6d7ce6")
    
    MAP_SDK_TIMEOUT_MS = int(os.getenv("MAP_SDK_TIMEOUT_MS", "8000"))
    
    MAP_ENABLE_3D_BUILDINGS = os.getenv("MAP_ENABLE_3D_BUILDINGS", "True").lower() == "true"
    
    DASHSCOPE_API_KEY = env_vars.get("DASHSCOPE_API_KEY", "sk-8c0c3cae5851420daa15adb305a7a7b9")
    DASHSCOPE_API_KEY_2 = env_vars.get("DASHSCOPE_API_KEY_2", "sk-66e6e41b2a044aa1834a450557127eca")
    DASHSCOPE_API_KEY_3 = env_vars.get("DASHSCOPE_API_KEY_3", "sk-865087a4c68c44d5869302c5f16b620c")
    DASHSCOPE_API_KEY_4 = env_vars.get("DASHSCOPE_API_KEY_4", "sk-513ccdef9168477bb88ca87e3436d3d3")
    
    DASHSCOPE_KEY_POOL = [k for k in [
        DASHSCOPE_API_KEY,
        DASHSCOPE_API_KEY_2,
        DASHSCOPE_API_KEY_3,
        DASHSCOPE_API_KEY_4,
    ] if k]

    # 场景关键词映射（用于RAG系统）
    SCENE_KEYWORDS = {
        "医疗": ["头疼", "发烧", "咳嗽", "医院", "诊所", "药品", "医生", "护士", "挂号", "体检"],
        "法律": ["合同", "借条", "起诉", "律师", "法院", "纠纷", "诉讼", "法律咨询", "知识产权"],
        "政务": ["身份证", "护照", "社保", "公积金", "皖事通", "户口", "驾驶证", "行驶证", "结婚证"],
        "教育": ["课程", "考试", "学校", "大学", "专业", "老师", "学生", "作业", "辅导"],
        "金融": ["汇率", "股票", "基金", "理财", "贷款", "保险", "利率", "投资", "信用卡"],
        "旅游": ["景点", "旅游", "酒店", "民宿", "攻略", "门票", "旅行社", "导游", "自驾游"],
        "农业": ["种植", "养殖", "农药", "化肥", "农机", "作物", "土壤", "灌溉", "农产品"],
        "家居": ["装修", "家电", "家具", "维修", "清洁", "收纳", "灯具", "窗帘", "水电"],
        "体育": ["运动", "健身", "比赛", "足球", "篮球", "跑步", "游泳", "瑜伽", "教练"],
        "育儿": ["婴儿", "幼儿", "早教", "疫苗", "辅食", "奶粉", "尿不湿", "玩具", "幼儿园"],
        "本地服务": ["社区医院", "药店", "缴费", "政务中心", "便民热线", "家政", "快递", "外卖"],
        "6G前沿": ["6G", "太赫兹", "空天地一体化", "卫星通信", "智能超表面", "通感算一体"],
    }
