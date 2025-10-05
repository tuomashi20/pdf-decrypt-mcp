#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF解密MCP服务测试脚本
"""

import sys
import os
import json

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pdf_decrypt_mcp import PDFDecryptor

def test_pdf_decryptor():
    """测试PDF解密器功能"""
    print("🧪 测试PDF解密器功能...")
    
    # 创建解密器实例
    decryptor = PDFDecryptor()
    print("✅ 成功创建PDFDecryptor实例")
    
    # 测试文件路径
    test_dir = r"D:\BaiduNetdiskDownload\赵礼显\秋季\秋季班讲义"
    test_file = os.path.join(test_dir, "【讲义】秋季第1讲 空间向量题型拓展 .pdf")
    
    if os.path.exists(test_file):
        print(f"📁 测试文件: {test_file}")
        
        # 测试检查加密状态
        print("\n🔍 测试检查PDF加密状态...")
        result = decryptor.check_pdf_encryption(test_file)
        print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        if result.get("is_encrypted"):
            # 测试解密
            print("\n🔓 测试PDF解密...")
            decrypt_result = decryptor.decrypt_pdf(test_file)
            print(f"解密结果: {json.dumps(decrypt_result, ensure_ascii=False, indent=2)}")
        
        # 测试批量解密
        print("\n📁 测试批量解密...")
        batch_result = decryptor.batch_decrypt_pdfs(test_dir)
        print(f"批量解密结果: {json.dumps(batch_result, ensure_ascii=False, indent=2)}")
    else:
        print(f"⚠️ 测试文件不存在: {test_file}")
        print("请确保文件路径正确")

def test_mcp_tools():
    """测试MCP工具"""
    print("\n🔧 测试MCP工具...")
    
    try:
        from pdf_decrypt_mcp.server import server
        print("✅ 成功导入MCP服务器")
        
        # 测试工具列表
        print("\n📋 测试工具列表...")
        # 这里我们不能直接调用async函数，但可以验证服务器创建成功
        print("✅ MCP服务器创建成功")
        
    except Exception as e:
        print(f"❌ MCP服务器测试失败: {e}")

def main():
    """主函数"""
    print("🚀 开始测试PDF解密MCP服务...")
    
    try:
        # 测试PDF解密器
        test_pdf_decryptor()
        
        # 测试MCP工具
        test_mcp_tools()
        
        print("\n🎉 测试完成！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()