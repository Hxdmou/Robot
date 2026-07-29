
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

import os
import PyPDF2
from datetime import datetime

def verify_pdf_file(file_path):
    """
    Verify PDF file integrity and validity
    """
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Check if PDF is encrypted
            if pdf_reader.is_encrypted:
                return False, "PDF is encrypted"
            
            # Check number of pages
            num_pages = len(pdf_reader.pages)
            if num_pages == 0:
                return False, "PDF has no pages"
            
            # Try to read first page to verify content
            first_page = pdf_reader.pages[0]
            text = first_page.extract_text()
            
            if len(text.strip()) < 10:
                return False, "PDF appears to be empty or corrupted"
            
            # Get file size
            file_size = os.path.getsize(file_path)
            
            return True, {
                "pages": num_pages,
                "size_bytes": file_size,
                "size_mb": file_size / (1024 * 1024),
                "has_content": len(text.strip()) > 50
            }
            
    except Exception as e:
        return False, f"Error reading PDF: {str(e)}"

def main():
    base_dir = OUTPUT_DIR  # was: 智能问答系统PDF资源
    
    print("=" * 80)
    print("PDF文件合法性验证报告")
    print(f"验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    total_files = 0
    valid_files = 0
    invalid_files = 0
    all_results = []
    
    for system_name in os.listdir(base_dir):
        system_path = os.path.join(base_dir, system_name)
        
        if not os.path.isdir(system_path):
            continue
            
        print(f"\n{'=' * 80}")
        print(f"系统: {system_name}")
        print(f"{'=' * 80}")
        
        for filename in os.listdir(system_path):
            if not filename.lower().endswith('.pdf'):
                continue
                
            file_path = os.path.join(system_path, filename)
            total_files += 1
            
            print(f"\n文件: {filename}")
            print(f"路径: {file_path}")
            
            is_valid, result = verify_pdf_file(file_path)
            
            if is_valid:
                valid_files += 1
                print(f"✓ 状态: 有效")
                print(f"  页数: {result['pages']}")
                print(f"  大小: {result['size_mb']:.2f} MB")
                print(f"  内容: {'完整' if result['has_content'] else '较少'}")
                
                all_results.append({
                    "system": system_name,
                    "filename": filename,
                    "status": "有效",
                    "pages": result['pages'],
                    "size_mb": result['size_mb'],
                    "has_content": result['has_content']
                })
            else:
                invalid_files += 1
                print(f"✗ 状态: 无效 - {result}")
                
                all_results.append({
                    "system": system_name,
                    "filename": filename,
                    "status": "无效",
                    "error": result
                })
    
    print(f"\n{'=' * 80}")
    print("验证总结")
    print(f"{'=' * 80}")
    print(f"总文件数: {total_files}")
    print(f"有效文件: {valid_files} ({valid_files/total_files*100:.1f}%)")
    print(f"无效文件: {invalid_files} ({invalid_files/total_files*100:.1f}%)")
    print(f"{'=' * 80}")
    
    # Generate detailed report
    report_path = EXTERNAL_PROJECT_DIR  # was: pdf_verification_report.txt
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("PDF文件合法性验证报告\n")
        f.write(f"验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("验证总结:\n")
        f.write(f"总文件数: {total_files}\n")
        f.write(f"有效文件: {valid_files} ({valid_files/total_files*100:.1f}%)\n")
        f.write(f"无效文件: {invalid_files} ({invalid_files/total_files*100:.1f}%)\n\n")
        
        f.write("=" * 80 + "\n")
        f.write("详细结果:\n")
        f.write("=" * 80 + "\n\n")
        
        for result in all_results:
            f.write(f"系统: {result['system']}\n")
            f.write(f"文件: {result['filename']}\n")
            f.write(f"状态: {result['status']}\n")
            
            if result['status'] == "有效":
                f.write(f"页数: {result['pages']}\n")
                f.write(f"大小: {result['size_mb']:.2f} MB\n")
                f.write(f"内容: {'完整' if result['has_content'] else '较少'}\n")
            else:
                f.write(f"错误: {result['error']}\n")
            
            f.write("-" * 80 + "\n\n")
    
    print(f"\n详细报告已保存至: {report_path}")

if __name__ == "__main__":
    main()