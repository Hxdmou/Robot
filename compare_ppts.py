
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

from pptx import Presentation

def compare_ppts():
    ppt1_path = EXTERNAL_PROJECT_DIR  # was: A2A_PROTOCOL_AI_AGENT_V14_完整填充版.pptx
    ppt2_path = EXTERNAL_PROJECT_DIR  # was: A2A_PROTOCOL_AI_AGENT_V14_终极完整版.pptx
    
    print("=" * 120)
    print("📊 两个PPT文件对比")
    print("=" * 120)
    
    prs1 = Presentation(ppt1_path)
    prs2 = Presentation(ppt2_path)
    
    print(f"\n文件1: {ppt1_path}")
    print(f"  幻灯片数: {len(prs1.slides)}")
    
    print(f"\n文件2: {ppt2_path}")
    print(f"  幻灯片数: {len(prs2.slides)}")
    
    # 检查项目3
    print("\n" + "=" * 120)
    print("📌 项目3对比")
    print("=" * 120)
    
    if len(prs1.slides) > 2:
        slide1 = prs1.slides[2]
        for shape in slide1.shapes:
            if shape.has_table:
                table1 = shape.table
                print(f"\n文件1项目3: {len(table1.rows)}行 × {len(table1.columns)}列")
                
                # 检查层级
                layers1 = []
                for i in range(1, min(12, len(table1.rows))):
                    layer_id = table1.cell(i, 0).text.strip()
                    layers1.append(layer_id)
                print(f"  层级: {', '.join(layers1)}")
                break
    
    if len(prs2.slides) > 2:
        slide2 = prs2.slides[2]
        for shape in slide2.shapes:
            if shape.has_table:
                table2 = shape.table
                print(f"\n文件2项目3: {len(table2.rows)}行 × {len(table2.columns)}列")
                
                # 检查层级
                layers2 = []
                for i in range(1, min(12, len(table2.rows))):
                    layer_id = table2.cell(i, 0).text.strip()
                    layers2.append(layer_id)
                print(f"  层级: {', '.join(layers2)}")
                break
    
    print("\n" + "=" * 120)
    print("💡 重要提示")
    print("=" * 120)
    print("请确保您打开的是: A2A_PROTOCOL_AI_AGENT_V14_终极完整版.pptx")
    print("而不是: A2A_PROTOCOL_AI_AGENT_V14_完整填充版.pptx")

if __name__ == "__main__":
    compare_ppts()