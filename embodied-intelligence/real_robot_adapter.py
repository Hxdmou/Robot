"""
真实机械臂适配器（多品牌兼容版 v15.0）
提供统一的机器人控制接口，支持仿真和真实模式切换
兼容品牌：Franka Emika、KUKA、Universal Robots、ABB、Dobot、
          步科、宇树、云深处、Agility Robotics、Apptronik 等全球主流品牌
兼容仿真：PyBullet、MuJoCo、Isaac Sim、ROS2/Gazebo（通过仿真器抽象层）
安全原则：模式隔离、异常保护、状态同步、紧急停止
"""
# ============================================================================
# 免责声明与AI使用规范
# ============================================================================
# 本文件仅供技术研究与学习交流使用，不得用于任何非法用途。
#
# AI使用规范：
#   1. 使用本文件相关内容时须遵守所在地法律法规及伦理准则
#   2. 不得用于侵犯他人合法权益、危害网络安全、破坏公共秩序的活动
#   3. 涉及自动化决策的场景须确保人工复核机制与可解释性
#   4. 处理个人信息时须符合数据保护相关法规要求
#
# 风险提示：
#   本文件内容按"现状"提供，不保证绝对准确无误。
#   使用者须自行评估风险，因使用本文件导致的任何损失由使用者承担。
# ============================================================================



import time
import math
from typing import Dict, Any, Optional, List

from robot_comm import SimRobotComm
from panda_comm import PandaComm
from robot_safety import SafetyController, EmergencyStopMonitor
from robot_arm_db import RobotArmDB, ARM_DATABASE


# ============================================================================
# 全球主流品牌通信映射表（可扩展）
# 覆盖135个产品：协作臂/人形/四足/AMR/医疗/工业/消费级/AI芯片/世界模型/6G通信/XR等
# ============================================================================
BRAND_COMM_MAP = {
    # ==================== Franka Emika ====================
    "franka_panda": "panda_libfranka",
    "franka_research_3": "panda_libfranka",
    # ==================== KUKA ====================
    "kuka_iiwa": "kuka_fri",
    "kuka_lbr_iiwa_14_r820": "kuka_fri",
    "kuka_kr_agilus": "kuka_eki",
    "kuka_kr_quantum": "kuka_eki",
    "kuka_lbr": "kuka_fri",
    # ==================== FANUC ====================
    "fanuc_m2000": "fanuc_tcp",
    # ==================== Universal Robots ====================
    "ur5e": "ur_rtde",
    "ur3e": "ur_rtde",
    "ur10e": "ur_rtde",
    "ur16e": "ur_rtde",
    "ur20": "ur_rtde",
    # ==================== ABB ====================
    "abb_yumi": "abb_egm",
    "abb_irb_14000": "abb_egm",
    "abb_irb_1200": "abb_rapid",
    # ==================== Dobot ====================
    "dobot_magician": "dobot_serial",
    "dobot_cr5": "dobot_tcp",
    "dobot_cr10": "dobot_tcp",
    # ==================== 国产协作臂 ====================
    "airbot_p7": "airbot_tcp",
    "ufactory_cra": "ufactory_tcp",
    "jaka_zu35": "jaka_tcp",
    "jaka_zu12": "jaka_tcp",
    # ==================== 步科Buke ====================
    "buke_collaborative": "buke_modbus",
    "buke_robot_components": "buke_modbus",
    # ==================== 金杯电工Jinbei（供应链） ====================
    "jinbei_flat_wire": "jinbei_tcp",
    # ==================== 宇树Unitree（人形/四足/轮足） ====================
    "unitree_h1": "unitree_udp",
    "unitree_h2": "unitree_udp",
    "unitree_g1": "unitree_udp",
    "unitree_gd01": "unitree_udp",
    "unitree_go2": "unitree_udp",
    "unitree_b2": "unitree_udp",
    "unitree_a2_as2": "unitree_udp",
    # ==================== 云深处DeepRobotics（人形/轮足） ====================
    "deeprobotics_dr02": "deeprobotics_tcp",
    "deeprobotics_shanmao_s10": "deeprobotics_tcp",
    "deeprobotics_shanmao_m20s": "deeprobotics_tcp",
    # ==================== 思灵Agile Robots（Diana/H系列） ====================
    "agile_diana3_g2": "agile_tcp",
    "agile_h20": "agile_tcp",
    "agile_h10w": "agile_tcp",
    # ==================== 具微科技MICBOT（轮足系列） ====================
    "micbot_movenew_p": "micbot_tcp",
    "micbot_curiosity_s01": "micbot_tcp",
    # ==================== 宇泛智能UNIUE（四足系列） ====================
    "uniue_cyberling": "uniue_tcp",
    # ==================== 临界点AgileLink（灵巧手系列） ====================
    "agilink_omnihand3_ultram": "agilink_tcp",
    # ==================== 商汤SenseTime ====================
    "sensetime_sensemart_go": "sensetime_tcp",
    "sensetime_sensenova_u1pro": "sensetime_tcp",
    # ==================== 蚂蚁灵波RobbyAnt ====================
    "robbyant_lingbot_vla2": "robbyant_tcp",
    "robbyant_r2": "robbyant_tcp",
    # ==================== 乐聚Leju ====================
    "leju_industrial_humanoid": "leju_tcp",
    # ==================== 面壁智能ModelBest ====================
    "modelbest_minicpm_robotmanip": "modelbest_tcp",
    "modelbest_minicpm_robottrack": "modelbest_tcp",
    "modelbest_phyai": "modelbest_tcp",
    # ==================== 阶跃星辰StepX ====================
    "stepx_neo": "stepx_tcp",
    "stepx_amoo_assistant": "stepx_tcp",
    # ==================== 阿里千问 ====================
    "ali_qianwen_ai_glasses": "ali_tcp",
    "ali_qianwen_ai_earbuds": "ali_tcp",
    # ==================== 努比亚Nubia ====================
    "nubia_navix_ultra": "nubia_tcp",
    "nubia_imoochi": "nubia_tcp",
    # ==================== 术锐Shurui（医疗机器人） ====================
    "shurui_singport_robot": "shurui_tcp",
    "rebot_b601_dm": "shurui_tcp",
    # ==================== 智元ZhiYuan ====================
    "zhiyuan_a3": "zhiyuan_tcp",
    # ==================== 开普勒Kepler ====================
    "kepler_k2": "kepler_tcp",
    # ==================== 优必选UBTech ====================
    "ubtech_walker": "ubtech_tcp",
    "ubtech_u1": "ubtech_tcp",
    # ==================== 松延动力Sonyond ====================
    "sonyond_xiaoyue": "sonyond_tcp",
    # ==================== 翼菲Yufei ====================
    "yufei_humanoid": "yufei_tcp",
    # ==================== 广电运通GDYT ====================
    "gdyt_g100": "gdyt_tcp",
    # ==================== AMR系列 ====================
    "geek_amr": "amr_tcp",
    "hikrobot_amr": "amr_tcp",
    # ==================== AI眼镜/消费级 ====================
    "moonix_glasses": "consumer_tcp",
    "iflytek_glasses": "consumer_tcp",
    "honor_robot": "consumer_tcp",
    "qingtianzu": "consumer_tcp",
    "aoshark_viatrix": "consumer_tcp",
    "dreame_l5_air": "consumer_tcp",
    # ==================== AI手机 ====================
    # ==================== 中科曙光/算力 ====================
    "shuguang_8000": "hpc_tcp",
    # ==================== 6G/通信网络 ====================
    "bci_glasses_6g": "telecom_tcp",
    "satellite_direct_6g": "telecom_tcp",
    "optical_400g_system": "telecom_tcp",
    "low_altitude_ian": "telecom_tcp",
    "iot_6g_industrial": "telecom_tcp",
    "five_g_a_base_station": "telecom_tcp",
    "ten_gigabit_optical": "telecom_tcp",
    "satellite_internet_test": "telecom_tcp",
    "tesla_doubao": "telecom_tcp",
    # ==================== LLM大模型 ====================
    "kunlun_llm": "llm_tcp",
    "yudian_llm": "llm_tcp",
    "guangming_power_llm": "llm_tcp",
    # ==================== AI世界模型/VLA ====================
    "aiforia_world_model": "world_model_tcp",
    "kunlun_dynamic_engine": "world_model_tcp",
    # ==================== 传感器/电子皮肤 ====================
    "zjutri_e_skin": "sensor_tcp",
    "ai_content_audit": "sensor_tcp",
    # ==================== 晶圆级/AI芯片 ====================
    "cerebras_wse3": "wafer_tcp",
    "tesla_dojo": "wafer_tcp",
    "tsmc_sow_x": "wafer_tcp",
    "tsinghua_wafer": "wafer_tcp",
    "cas_yingtianhu": "wafer_tcp",
    "cas_ouroboros": "wafer_tcp",
    "ziguang_zixuan": "wafer_tcp",
    "qingwei_tx": "wafer_tcp",
    "jingxin_interconnect": "wafer_tcp",
    # ==================== 推理芯片/推理框架 ====================
    "ascend_950": "inference_tcp",
    "aliyun_zhenwu": "inference_tcp",
    "biren_oex": "inference_tcp",
    "muxi_xijing": "inference_tcp",
    "moore_mtt_c256": "inference_tcp",
    "baidu_tianchi": "inference_tcp",
    "deepseek_inference_chip": "inference_tcp",
    "openai_jalapeno": "inference_tcp",
    "sglang": "inference_tcp",
    "vllm": "inference_tcp",
    "radixark": "inference_tcp",
    "miles": "inference_tcp",
    # ==================== 服务机器人/VTLA ====================
    "galbot_g1": "vtla_tcp",
    "galbot_s1": "vtla_tcp",
    "juwei_tech": "vtla_tcp",
    "self_variable_wall_b": "vtla_tcp",
    "toshi_a1": "vtla_tcp",
    "pudu_d9": "vtla_tcp",
    "zhipingfang_alphabot": "vtla_tcp",
    "lexiang_zeroth": "vtla_tcp",
    "qiongche_noematrix": "vtla_tcp",
    "jijia_gigaworld": "vtla_tcp",
    "qianjue_predictive": "vtla_tcp",
    "moxin_moworld": "vtla_tcp",
    "vtla": "vtla_tcp",
    "n0_vtla": "vtla_tcp",
    "omni_vtla": "vtla_tcp",
    # ==================== AI平台/智能体平台 ====================
    "underwater_datacenter": "platform_tcp",
    "space_computing_constellation": "platform_tcp",
    "comi_platform": "platform_tcp",
    "lingxi_app": "platform_tcp",
    "360_agent_factory": "platform_tcp",
    # ==================== XR设备 ====================
    "apple_vision_pro": "xr_tcp",
    "meta_quest_4": "xr_tcp",
    # ==================== 能源/电力机器人 ====================
    "state_grid_inspection": "energy_tcp",
    "energenie_charging": "energy_tcp",
    # ==================== 产业中试/工业场景 ====================
    "hangzhou_embodied_base": "industrial_tcp",
    "qingtong_robot": "industrial_tcp",
    "chuanhua_zhilian": "industrial_tcp",
    "bim_bot_3d_print": "industrial_tcp",
    "brick_laying_robot": "industrial_tcp",
    # ==================== 科研设备/数据集 ====================
    "cmu_noninvasive_bci": "cmu_bci_serial",
    "tsinghua_egoemg": "tsinghua_data_tcp",
    # ==================== 补充: panda别名 + 蚌埠传感谷(6家) + 2家AI芯片 + 1家卫星 ====================
    "panda": "panda_libfranka",
    "中科微感": "sensor_tcp",
    "华鑫智感": "sensor_tcp",
    "希磁科技": "sensor_tcp",
    "海车神驭": "sensor_tcp",
    "至博研": "sensor_tcp",
    "芒果传感": "sensor_tcp",
    "芯动联科": "sensor_tcp",
    "华鑫微纳": "wafer_tcp",
    "紫光展锐V8821": "telecom_tcp",
    "天启星座": "telecom_tcp",
    # ==================== 补充产品 ====================
    "jiunuo_nursing": "shurui_tcp",
    "daai_rehab": "shurui_tcp",
    "senlikang_kangyang": "shurui_tcp",
    "yunji_kangyang": "consumer_tcp",
    "shenzhou_longxin_robot": "industrial_tcp",
    "health_screening_robot": "shurui_tcp",
    "bci_rehab_device": "cmu_bci_serial",
    "lower_limb_exo_rehab": "shurui_tcp",
    "houming_ai_super_employee": "platform_tcp",
    "houming_pengka_nfc": "consumer_tcp",
    "houming_digital_human": "xr_tcp",
    "houming_mars_geo": "platform_tcp",
    "pku_cas_neurodyn_chip": "wafer_tcp",
    # ==================== 补充产品映射 ====================
    "galaxea_g05": "platform_tcp",
    "yuanli_dm05": "platform_tcp",
    "liman_riemann_10": "world_model_tcp",
    "pohu_wam": "world_model_tcp",
    "zhengqi_door_mind": "world_model_tcp",
    "qiyuan_q1": "consumer_tcp",
    "qiyuan_t1": "consumer_tcp",
    "unitree_h2_plus": "unitree_udp",
    "songyan_bumi": "consumer_tcp",
    "efort_wheel_humanoid": "efort_eki",
    "mojia_culture": "consumer_tcp",
    "weijing_laparoscope": "medical_ethercat_p",
    "yuanli_ferrata": "logistics_5g_mqtt",
    "digua_warehouse": "logistics_slam_mqtt",
    "yuanli_apex": "modbus_tcp_ros2",
    "zhengqi_quorra_x5": "consumer_5g_cv2x",
    # ==================== 非运动体兜底（AI芯片/传感器/eVTOL/平台/基建设施/研究基地/通信设备等 → GenericBridgeAdapter） ====================
    "anhui_industrial_net_export": "generic_bridge",
    "beta_creative_tech_hk_ai_infra": "generic_bridge",
    "buerchou_liangchou_no1_atomic_qm_stand": "generic_bridge",
    "cfs_fusion_4b_usd_funding": "generic_bridge",
    "dobot_lumo": "generic_bridge",
    "dognavy_cybergym_global3_opensource1": "generic_bridge",
    "dongfang_gravity_one_ys4_sea": "generic_bridge",
    "dongfang_starlink_05_06": "generic_bridge",
    "eu_7ai_giga_30b_euro": "generic_bridge",
    "fengfei_v5000_evtol": "evtol_map",
    "fudan_qm_flash_27c_science": "generic_bridge",
    "general_fusion_nasdaq": "generic_bridge",
    "hangzhou_wheel_legged_hercules": "generic_bridge",
    "hanwei_force_sensor": "generic_bridge",
    "hongyuan_crossed_roller_bearing": "generic_bridge",
    "lanxiao_lx1_evtol": "evtol_map",
    "leisai_motion_control": "generic_bridge",
    "liupanshui_coke_hydrogen_base": "generic_bridge",
    "longyou_embodied_training_base": "generic_bridge",
    "national_six_nets_shiwuwu_26p9trillion": "generic_bridge",
    "ncku_text2video_embodied_training": "generic_bridge",
    "nokia_ai_ran_6g_platform": "generic_bridge",
    "nvidia_cosmos_physics_ai_alliance": "generic_bridge",
    "pku_bci_alpha_1k_synced": "generic_bridge",
    "shenzhen_collaborative_global_no1": "generic_bridge",
    "ustc_flexible_e_skin": "generic_bridge",
    "yuezhi_anmian_kimi_k3_code_no1": "generic_bridge",
    "yundie_polia_multimodal": "generic_bridge",
    "zhiyuan_central_henan_base": "generic_bridge",
    # ==================== 补充产品映射 ====================
    "zeuth_humanoid": "unitree_udp",
    "hefei_jshen_training_field": "generic_bridge",
    "hefei_jushen_data_company": "generic_bridge",
    "smart_robot_machining_center": "generic_bridge",
    "jiuzhihu_dual_arm_nursing": "shurui_tcp",
    "taibao_home_yanglao_station": "shurui_tcp",
    "baozouzhe_commercial_humanoid": "unitree_udp",
    "zunjie_v800_flagship_mpv": "generic_bridge",
    "shangtang_token_factory": "wafer_tcp",
    "huaweiyun_lingqu_cluster": "wafer_tcp",
    "deepseek_llm_company": "llm_tcp",
    "anthropic_custom_chip_team": "wafer_tcp",
    "discovery_loop_company": "vtla_tcp",
    "spacex_starmind_satellite": "telecom_tcp",
    "yixi_xiaoxiao_ai_agent": "vtla_tcp",
    "caict_token_evaluation": "vtla_tcp",
    "linghang_science_education": "vtla_tcp",
    "yiwu_shangmao_llm": "llm_tcp",
    "honghai_ai_server_oem": "wafer_tcp",
    "shengke_switch_chip": "wafer_tcp",
    "ruijie_ai_switch": "telecom_tcp",
    "ziguang_network_device": "telecom_tcp",
    "zhongxing_ai_network": "telecom_tcp",
    "oulutong_compute_end": "wafer_tcp",
    "huaqin_server_manufacturing": "wafer_tcp",
    "fenghuo_ai_compute_device": "telecom_tcp",
    "cambricon_inference_chip": "wafer_tcp",
    "haiguang_ai_cpu": "wafer_tcp",
    "langchao_ai_server": "wafer_tcp",
    "hongjing_suanli_lease": "wafer_tcp",
    "xiechuang_suanli_data": "wafer_tcp",
    "zhiwei_zhineng_suanli": "wafer_tcp",
    "xingyun_keji_suanli": "wafer_tcp",
    "runjian_suanli_stock": "wafer_tcp",
    "yunsai_zhilian_suanli": "wafer_tcp",
    "litong_dianzi_suanli": "wafer_tcp",
    "chaoxun_tongxin_suanli": "telecom_tcp",
    "zhongbei_tongxin_suanli": "telecom_tcp",
    "hangjin_keji_suanli": "wafer_tcp",
    "honghe_ultrathin_electronic_cloth": "sensor_tcp",
    "fuqiao_electronic_cloth": "sensor_tcp",
    "fenghua_gaoke_mlcc": "sensor_tcp",
    "sanhuan_mlcc": "sensor_tcp",
    "hudian_high_end_pcb": "sensor_tcp",
    "shennan_high_speed_pcb": "sensor_tcp",
    "pengding_ai_pcb": "sensor_tcp",
    "wuxi_aisuanli_pcb": "sensor_tcp",
    "jiantao_copper_clad": "sensor_tcp",
    "changfei_special_fiber": "telecom_tcp",
    "hengtong_special_fiber": "telecom_tcp",
    "zhongtian_special_fiber": "telecom_tcp",
    "yunnan_zheye_inp": "wafer_tcp",
    "sanan_inp_substrate": "wafer_tcp",
    "high_purity_tungsten_target": "sensor_tcp",
    "ultrathin_copper_foil_pcb": "sensor_tcp",
    "changxin_cxmt_dram": "wafer_tcp",
    "google_pixel_tag": "consumer_tcp",
    "huawei_matebook_fold": "consumer_tcp",
    "ai_xunizhubo_compliance": "vtla_tcp",
    "data_ip_registration_trade": "vtla_tcp",
    # ========== 21张截图补充产品映射 ==========
    "national_computing_network_4t_15th": "generic_bridge",
    "chinamobile_4n31x_supercomputing_grid": "telecom_tcp",
    "chinatelecom_xirang_integrated_platform": "telecom_tcp",
    "chinaunicom_ai_computing_integration": "telecom_tcp",
    "aliyun_feitian_heterogeneous_management": "wafer_tcp",
    "tencent_hunyuan_computing_cluster": "wafer_tcp",
    "huawei_ascend_cloudmatrix_ecosystem": "wafer_tcp",
    "baidu_kunlunxin_wenxin_fullstack": "wafer_tcp",
    "shenzhou_kejie_warehouse_ai_agent": "llm_tcp",
    "yunji_hotel_delivery_standard_robot": "consumer_tcp",
    "kunlunwanwei_global_shortform_platform": "consumer_tcp",
    "kunlunwanwei_ai_music_production": "llm_tcp",
    "imt2030_6g_ntn_satellite_terrestrial": "telecom_tcp",
    "nvidia_6g_airan_base_station": "telecom_tcp",
    "haiyou_anlan_16mw_floating_wind": "vtla_tcp",
    "jingwei_hao1_reusable_rocket": "vtla_tcp",
    "cfr1000_1200mw_sodium_fast_reactor": "vtla_tcp",
    "tmsr_2mw_thorium_molten_salt_reactor": "vtla_tcp",
    "300mw_compact_small_pwr": "vtla_tcp",
    "china_full_moon_geological_map_5m": "generic_bridge",
    "chowchow_bank_cross_border_payment_pass": "generic_bridge",
}

# 协议实现映射（协议名 → 适配器类，延迟导入避免依赖缺失）
PROTOCOL_ADAPTERS = {
    # ========== 已有主流品牌协议 ==========
    "panda_libfranka": "panda_comm.PandaComm",
    "kuka_fri": "protocol_adapters.KukaFRIAdapter",
    "kuka_eki": "protocol_adapters.KukaEKIAdapter",
    "ur_rtde": "protocol_adapters.URRTDEAdapter",
    "abb_egm": "protocol_adapters.ABBEGMAdapter",
    "abb_rapid": "protocol_adapters.ABBRapidAdapter",
    "dobot_serial": "protocol_adapters.DobotSerialAdapter",
    "dobot_tcp": "protocol_adapters.DobotTCPAdapter",
    "airbot_tcp": "protocol_adapters.AirbotTCPAdapter",
    "ufactory_tcp": "protocol_adapters.UFactoryTCPAdapter",
    "jaka_tcp": "protocol_adapters.JakaTCPAdapter",
    "buke_modbus": "protocol_adapters.BukeModbusAdapter",
    "unitree_udp": "protocol_adapters.UnitreeUDPAdapter",
    "deeprobotics_tcp": "protocol_adapters.DeepRoboticsTCPAdapter",
    # ========== ***新增品牌通用协议（v15.0补全） ==========
    "fanuc_tcp": "protocol_adapters.GenericTCPAdapter",
    "jinbei_tcp": "protocol_adapters.GenericTCPAdapter",
    "agile_tcp": "protocol_adapters.GenericTCPAdapter",
    "micbot_tcp": "protocol_adapters.GenericTCPAdapter",
    "uniue_tcp": "protocol_adapters.GenericTCPAdapter",
    "agilink_tcp": "protocol_adapters.GenericTCPAdapter",
    "sensetime_tcp": "protocol_adapters.GenericTCPAdapter",
    "robbyant_tcp": "protocol_adapters.GenericTCPAdapter",
    "leju_tcp": "protocol_adapters.GenericTCPAdapter",
    "modelbest_tcp": "protocol_adapters.GenericTCPAdapter",
    "stepx_tcp": "protocol_adapters.GenericTCPAdapter",
    "ali_tcp": "protocol_adapters.GenericTCPAdapter",
    "nubia_tcp": "protocol_adapters.GenericTCPAdapter",
    "shurui_tcp": "protocol_adapters.GenericTCPAdapter",
    "zhiyuan_tcp": "protocol_adapters.GenericTCPAdapter",
    "kepler_tcp": "protocol_adapters.GenericTCPAdapter",
    "ubtech_tcp": "protocol_adapters.GenericTCPAdapter",
    "sonyond_tcp": "protocol_adapters.GenericTCPAdapter",
    "yufei_tcp": "protocol_adapters.GenericTCPAdapter",
    "gdyt_tcp": "protocol_adapters.GenericTCPAdapter",
    "amr_tcp": "protocol_adapters.GenericTCPAdapter",
    "consumer_tcp": "protocol_adapters.GenericTCPAdapter",
    "hpc_tcp": "protocol_adapters.GenericTCPAdapter",
    "telecom_tcp": "protocol_adapters.GenericTCPAdapter",
    "llm_tcp": "protocol_adapters.GenericTCPAdapter",
    "world_model_tcp": "protocol_adapters.GenericTCPAdapter",
    "sensor_tcp": "protocol_adapters.GenericTCPAdapter",
    "wafer_tcp": "protocol_adapters.GenericTCPAdapter",
    "inference_tcp": "protocol_adapters.GenericTCPAdapter",
    "vtla_tcp": "protocol_adapters.GenericTCPAdapter",
    "platform_tcp": "protocol_adapters.GenericTCPAdapter",
    "xr_tcp": "protocol_adapters.GenericTCPAdapter",
    "energy_tcp": "protocol_adapters.GenericTCPAdapter",
    "industrial_tcp": "protocol_adapters.GenericTCPAdapter",
    "cmu_bci_serial": "protocol_adapters.GenericSerialAdapter",
    "tsinghua_data_tcp": "protocol_adapters.GenericTCPAdapter",
    # ========== 补充协议适配器 ==========
    "efort_eki": "protocol_adapters.GenericTCPAdapter",
    "medical_ethercat_p": "protocol_adapters.GenericTCPAdapter",
    "logistics_5g_mqtt": "protocol_adapters.GenericTCPAdapter",
    "logistics_slam_mqtt": "protocol_adapters.GenericTCPAdapter",
    "modbus_tcp_ros2": "protocol_adapters.GenericTCPAdapter",
    "consumer_5g_cv2x": "protocol_adapters.GenericTCPAdapter",
    # ========== 非运动体兜底桥接适配器（AI芯片/传感器/核心板/研究平台/通信/XR 等全类别） ==========
    "generic_bridge": "protocol_adapters.GenericBridgeAdapter",
    # ========== eVTOL 低空飞行器地图适配器（高德/腾讯双路容灾） ==========
    "evtol_map": "protocol_adapters.EVTOLMapAdapter",
}



from deployment_overrides import DEPLOYMENT_OVERRIDES  # 自动生成：真实部署通信/限位默认值
class RobotAdapter:
    """多品牌兼容机器人适配器
    
    设计原则：
      1. 不绑定任何特定品牌或协议 - 通过 robot_arm_db 动态加载配置
      2. 不绑定任何特定仿真器 - 通过 SimulatorBackend 抽象层支持 PyBullet/MuJoCo/Isaac Sim
      3. 安全优先 - 所有运动指令经过安全控制器校验
      4. 可扩展 - 新增品牌只需在 BRAND_COMM_MAP 和 protocol_adapters 中注册
    
    用法：
        # 仿真模式（PyBullet）
        adapter = RobotAdapter(mode="sim", arm_key="franka_panda")
        adapter.initialize()
        
        # 真机模式
        adapter = RobotAdapter(mode="real", arm_key="ur5e", 
                                config={"host": "127.0.0.1"})
        adapter.initialize()
        
        # 统一控制接口（仿真/真机完全一致）
        adapter.move_joints([0, -0.785, 0, -2.356, 0, 1.571, 0.785])
        adapter.move_cartesian(0.5, 0.0, 0.3)
    """

    def __init__(self, mode="sim", arm_key: Optional[str] = None, 
                 config: Optional[Dict[str, Any]] = None,
                 simulator_backend: Optional[str] = "pybullet"):
        """
        Args:
            mode: "sim" 或 "real"
            arm_key: 机器人型号key（如 "franka_panda", "ur5e", "kuka_iiwa"），
                     None 时从 config 中读取或使用默认
            config: 额外配置（host, port, joint_limits 等）
            simulator_backend: 仿真后端（pybullet/mujoco/isaac_sim/ros2），仅 sim 模式有效
        """
        self.mode = mode
        # 原表达式因 Python 运算优先级导致: A or B if C else D → 等价于 (A or B) if C else D
        # → config=None/config={} 时即使传了 arm_key 也会被置 None。修正:加括号显式绑定
        self.arm_key = arm_key or (config.get("arm_key") if config else None)
        self.config = config or {}
        self.simulator_backend = simulator_backend
        self.comm = None
        self.safety = SafetyController()
        self.emergency_stop = None
        self._initialized = False
        self._db = RobotArmDB()

        # 加载机器人配置
        if self.arm_key and self.arm_key in ARM_DATABASE:
            self.arm_config = ARM_DATABASE[self.arm_key]
            # ===== 真实部署默认值（一次性生成，可人工微调）=====
            if self.arm_key in DEPLOYMENT_OVERRIDES:
                _ovr = DEPLOYMENT_OVERRIDES[self.arm_key]
                for _k, _v in _ovr.items():
                    if isinstance(_v, dict) and isinstance(self.arm_config.get(_k), dict):
                        self.arm_config[_k].update(_v)
                    else:
                        self.arm_config[_k] = _v
                _ = None; _ovr = None  # 清理引用
            # ===== 真实部署默认值 · END =====
            self.brand = self.arm_config.get("brand", "Unknown")
            self.model = self.arm_config.get("model", "Unknown")
            self.dofs = self.arm_config.get("degrees_of_freedom", 7)
            self.joint_indices = self.arm_config.get("joint_indices", list(range(self.dofs)))
            self.ee_link = self.arm_config.get("ee_link", "ee_link")
        else:
            self.arm_config = {}
            self.brand = self.config.get("brand", "Custom")
            self.model = self.config.get("model", "Custom")
            self.dofs = self.config.get("dofs", 7)
            self.joint_indices = self.config.get("joint_indices", list(range(self.dofs)))
            self.ee_link = self.config.get("ee_link", "ee_link")

    def _detect_protocol(self) -> str:
        """根据 arm_key 自动检测通信协议"""
        if self.arm_key and self.arm_key in BRAND_COMM_MAP:
            return BRAND_COMM_MAP[self.arm_key]
        return self.arm_config.get("communication", {}).get("protocol", "unknown")

    def _create_comm_real(self):
        """创建真机通信适配器（支持多品牌多协议）"""
        protocol = self._detect_protocol()
        comm_cfg = self.arm_config.get("communication", {})
        host = self.config.get("host") or comm_cfg.get("default_host", "127.0.0.1")
        port = self.config.get("port") or comm_cfg.get("default_port", 8080)

        print(f"[ADAPTER] 目标机器人: {self.brand} {self.model} ({self.arm_key})")
        print(f"[ADAPTER] 通信协议: {protocol} | 地址: {host}:{port}")

        # 优先使用已知适配器
        if protocol == "panda_libfranka":
            return PandaComm(host=host, port=port)
        elif protocol in PROTOCOL_ADAPTERS:
            # 延迟导入，避免缺少依赖时崩溃
            try:
                module_path, class_name = PROTOCOL_ADAPTERS[protocol].rsplit(".", 1)
                module = __import__(module_path, fromlist=[class_name])
                adapter_cls = getattr(module, class_name)
                return adapter_cls(host=host, port=port, config=self.arm_config)
            except (ImportError, AttributeError) as e:
                print(f"[ADAPTER] ⚠️  协议适配器 {protocol} 不可用: {e}")
                print(f"[ADAPTER] 降级为通用TCP适配器，请确保机器人支持标准控制接口")
                from deploy_adapters import MultiProtocolAdapter
                return MultiProtocolAdapter(self.arm_key or "custom")
        else:
            # 未知协议，使用通用适配器
            print(f"[ADAPTER] ⚠️  未知协议: {protocol}，使用通用适配器")
            from deploy_adapters import MultiProtocolAdapter
            return MultiProtocolAdapter(self.arm_key or "custom")

    def _create_comm_sim(self):
        """创建仿真通信适配器（通过仿真器抽象层，不绑定PyBullet）"""
        backend = self.simulator_backend.lower()
        print(f"[ADAPTER] 仿真后端: {backend} | 机器人: {self.brand} {self.model}")

        if backend == "pybullet":
            # 传入关节数量提示，让 SimRobotComm 自动创建匹配尺寸的骨架机器人
            return SimRobotComm(num_joints=max(1, int(getattr(self, "dofs", 6) or 6)))
        elif backend == "mujoco":
            try:
                from sim_backends import MuJoCoBackend
                return MuJoCoBackend(self.arm_config, self.config)
            except ImportError:
                print("[ADAPTER] ⚠️  MuJoCo 不可用，降级为 PyBullet")
                return SimRobotComm(num_joints=max(1, int(getattr(self, "dofs", 6) or 6)))
        elif backend == "isaac_sim":
            try:
                from sim_backends import IsaacSimBackend
                return IsaacSimBackend(self.arm_config, self.config)
            except ImportError:
                print("[ADAPTER] ⚠️  Isaac Sim 不可用，降级为 PyBullet")
                return SimRobotComm(num_joints=max(1, int(getattr(self, "dofs", 6) or 6)))
        elif backend in ("ros2", "gazebo"):
            try:
                from sim_backends import ROS2Backend
                return ROS2Backend(self.arm_config, self.config)
            except ImportError:
                print("[ADAPTER] ⚠️  ROS2 不可用，降级为 PyBullet")
                return SimRobotComm(num_joints=max(1, int(getattr(self, "dofs", 6) or 6)))
        else:
            print(f"[ADAPTER] ⚠️  未知仿真后端: {backend}，使用 PyBullet")
            return SimRobotComm(num_joints=max(1, int(getattr(self, "dofs", 6) or 6)))

    def initialize(self):
        if self.mode == "real":
            self.comm = self._create_comm_real()
        else:
            self.comm = self._create_comm_sim()

        try:
            self.comm.connect()
            self._initialized = True
            print(f"[ADAPTER] 机器人适配器初始化完成 (模式: {self.mode})")

            # 从 arm_config 加载关节限制
            joint_limits = self.config.get("joint_limits") or self.arm_config.get("joint_limits")
            if joint_limits:
                self.safety.set_joint_limits(
                    self.joint_indices,
                    joint_limits.get("lower", []),
                    joint_limits.get("upper", [])
                )

            # 加载工作空间限制
            workspace = self.arm_config.get("workspace")
            if workspace:
                self.safety.set_workspace_limits(workspace)

            if self.mode == "real":
                self.emergency_stop = EmergencyStopMonitor(self.comm)
                self.emergency_stop.start()

            return True
        except Exception as e:
            print(f"[ADAPTER] 初始化失败: {e}")
            if self.comm:
                try:
                    self.comm.disconnect()
                except Exception:
                    pass
            return False

    def shutdown(self):
        if self.emergency_stop:
            self.emergency_stop.stop()

        if self.comm:
            try:
                self.comm.disconnect()
            except Exception:
                pass

        self._initialized = False
        print("[ADAPTER] 机器人适配器已关闭")

    def update_sim_params(self, robot_id, joint_indices, ee_index):
        if self.mode == "sim" and isinstance(self.comm, SimRobotComm):
            self.comm.robot_id = robot_id
            self.comm.joint_indices = joint_indices
            self.comm.ee_index = ee_index

    def list_supported_arms(self) -> List[str]:
        """列出所有支持的机器人型号"""
        return list(ARM_DATABASE.keys())

    def get_arm_info(self) -> Dict[str, Any]:
        """获取当前机器人信息"""
        return {
            "arm_key": self.arm_key,
            "brand": self.brand,
            "model": self.model,
            "dofs": self.dofs,
            "mode": self.mode,
            "simulator_backend": self.simulator_backend if self.mode == "sim" else None,
            "protocol": self._detect_protocol() if self.mode == "real" else None,
            "initialized": self._initialized,
            "connected": self.is_connected(),
        }

    def get_joint_states(self):
        if not self._initialized:
            return []
        return self.comm.get_joint_states()

    def move_joints(self, joint_angles, speed=1.0):
        if not self._initialized:
            raise RuntimeError("适配器未初始化")

        if self.emergency_stop and self.emergency_stop.is_emergency_stop():
            raise RuntimeError("紧急停止中")

        try:
            self.safety.check_joint_limits(joint_angles, self.joint_indices)
            self.comm.move_joints(joint_angles, speed)
            return True
        except Exception as e:
            print(f"[ADAPTER] 移动关节失败: {e}")
            try:
                self.comm.stop()
            except Exception:
                pass
            return False

    def move_cartesian(self, x, y, z, rx=0, ry=0, rz=0, speed=1.0):
        if not self._initialized:
            raise RuntimeError("适配器未初始化")

        if self.emergency_stop and self.emergency_stop.is_emergency_stop():
            raise RuntimeError("紧急停止中")

        try:
            self.safety.check_cartesian_limits(x, y, z)
            self.comm.move_cartesian(x, y, z, rx, ry, rz, speed)
            return True
        except Exception as e:
            print(f"[ADAPTER] 笛卡尔移动失败: {e}")
            try:
                self.comm.stop()
            except Exception:
                pass
            return False

    def get_ee_pose(self):
        if not self._initialized:
            return {"position": [0, 0, 0], "orientation": [0, 0, 0, 1]}
        return self.comm.get_ee_pose()

    def stop(self):
        if self.comm:
            try:
                self.comm.stop()
            except Exception:
                pass

    def converge_to_target(self, target_pos, max_iter=10, threshold=0.001):
        if not self._initialized:
            raise RuntimeError("适配器未初始化")

        for _ in range(max_iter):
            current_pose = self.get_ee_pose()
            current_pos = current_pose["position"]
            error = math.sqrt(
                (current_pos[0] - target_pos[0])**2 +
                (current_pos[1] - target_pos[1])**2 +
                (current_pos[2] - target_pos[2])**2
            )

            if error < threshold:
                return error

            self.move_cartesian(*target_pos, speed=0.5)
            time.sleep(0.1)

        return error

    def is_connected(self):
        return self.comm and getattr(self.comm, "connected", False)

    def set_safety_enabled(self, enabled):
        if enabled:
            self.safety.enable()
        else:
            self.safety.disable()
