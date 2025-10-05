#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF解密MCP服务安装脚本
"""

import subprocess
import sys
import os

def run_command(command, description):
    """运行命令并处理错误"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} 完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def install_dependencies():
    """安装依赖项"""
    print("🔧 开始安装依赖项...")
    
    dependencies = [
        "mcp>=1.0.0",
        "PyPDF2>=3.0.0", 
        "PyCryptodome>=3.15.0"
    ]
    
    for dep in dependencies:
        if not run_command(f'pip install "{dep}"', f"安装 {dep}"):
            return False
    
    return True

def create_package():
    """创建并安装包"""
    print("📦 创建并安装包...")
    
    # 切换到项目目录
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    # 安装包
    if not run_command("pip install -e .", "安装PDF解密MCP服务包"):
        return False
    
    return True

def test_installation():
    """测试安装"""
    print("🧪 测试安装...")
    
    try:
        # 测试导入
        import pdf_decrypt_mcp
        print("✅ 成功导入pdf_decrypt_mcp模块")
        
        # 测试PDF解密器
        from pdf_decrypt_mcp import PDFDecryptor
        decryptor = PDFDecryptor()
        print("✅ 成功创建PDFDecryptor实例")
        
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def print_usage_info():
    """打印使用信息"""
    print("\n" + "="*50)
    print("🎉 PDF解密MCP服务安装完成！")
    print("="*50)
    
    print("\n📖 使用方法:")
    print("1. 直接运行服务器:")
    print("   pdf-decrypt-mcp")
    
    print("\n2. 在Claude Code中配置:")
    print("   在配置文件中添加:")
    print("   {")
    print('     "mcpServers": {')
    print('       "pdf-decrypt": {')
    print('         "command": "pdf-decrypt-mcp"')
    print("       }")
    print("     }")
    print("   }")
    
    print("\n🔧 可用工具:")
    print("- check_pdf_encryption: 检查PDF加密状态")
    print("- decrypt_pdf: 解密单个PDF文件")
    print("- batch_decrypt_pdfs: 批量解密PDF文件")
    print("- list_pdf_files: 列出PDF文件")
    
    print("\n📚 获取帮助:")
    print("   使用 get_prompt 工具获取详细指南")
    
    print("\n" + "="*50)

def main():
    """主函数"""
    print("🚀 开始安装PDF解密MCP服务...")
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ 需要Python 3.8或更高版本")
        sys.exit(1)
    
    print(f"✅ Python版本: {sys.version}")
    
    # 安装步骤
    steps = [
        ("安装依赖项", install_dependencies),
        ("创建包", create_package),
        ("测试安装", test_installation)
    ]
    
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        if not step_func():
            print(f"❌ {step_name}失败，安装中止")
            sys.exit(1)
    
    # 打印使用信息
    print_usage_info()

if __name__ == "__main__":
    main()