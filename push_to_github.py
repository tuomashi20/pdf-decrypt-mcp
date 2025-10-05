#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF解密MCP服务 - GitHub部署脚本
"""

import subprocess
import sys
import os

def run_command(command, description):
    """运行命令并处理错误"""
    print(f"[正在] {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"[成功] {description} 完成")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"[失败] {description} 失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False, e.stderr

def check_git_status():
    """检查Git状态"""
    print("[检查] 检查Git状态...")
    
    success, status = run_command("git status", "获取Git状态")
    if success:
        print("[信息] Git状态正常")
        return True
    else:
        print("[错误] Git状态异常")
        return False

def configure_git():
    """配置Git用户信息（如果需要）"""
    print("[配置] 检查Git配置...")
    
    try:
        # 检查是否有用户名和邮箱配置
        success, _ = run_command("git config user.name", "检查用户名")
        if not success:
            run_command("git config user.name \"PDF Decrypt Service\"", "设置用户名")
            run_command("git config user.email \"pdf-decrypt-service@example.com\"", "设置邮箱")
        
        print("[成功] Git配置完成")
        return True
    except Exception as e:
        print(f"[错误] Git配置失败: {e}")
        return False

def add_commit_changes():
    """添加并提交所有更改"""
    print("[提交] 添加并提交更改...")
    
    # 添加所有文件
    success, _ = run_command("git add .", "添加文件到暂存区")
    if not success:
        return False
    
    # 检查是否有更改需要提交
    success, status = run_command("git status --porcelain", "检查更改状态")
    if not success:
        return False
    
    if not status.strip():
        print("[信息] 没有新的更改需要提交")
        return True
    
    # 提交更改
    commit_message = """Update GitHub deployment files

- Add GitHub deployment guide
- Add automated deployment script
- Update project documentation
- Prepare for GitHub release

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"""
    
    success, _ = run_command(f'git commit -m "{commit_message}"', "提交更改")
    return success

def create_github_repo_instructions():
    """创建GitHub仓库的说明"""
    print("\n" + "="*60)
    print("📋 GitHub仓库创建指南")
    print("="*60)
    
    print("\n🔧 手动创建GitHub仓库:")
    print("1. 访问 https://github.com")
    print("2. 点击右上角的 '+' 按钮，选择 'New repository'")
    print("3. 填写仓库信息:")
    print("   - Repository name: pdf-decrypt-mcp")
    print("   - Description: PDF解密MCP服务 - 支持UVX部署的PDF文件解密工具")
    print("   - 选择 Public 或 Private")
    print("   - 不要勾选任何初始化选项")
    print("4. 点击 'Create repository'")
    
    print("\n🔗 连接到GitHub仓库:")
    print("创建仓库后，运行以下命令:")
    
    # 获取当前目录
    current_dir = os.getcwd()
    print(f"cd \"{current_dir}\"")
    print("git remote add origin https://github.com/YOUR_USERNAME/pdf-decrypt-mcp.git")
    print("git branch -M main")
    print("git push -u origin main")
    
    print("\n💡 重要提醒:")
    print("- 将 YOUR_USERNAME 替换为您的GitHub用户名")
    print("- 确保您有仓库的写入权限")
    print("- 如果使用SSH，请将URL改为git@github.com:YOUR_USERNAME/pdf-decrypt-mcp.git")
    
    print("\n🚀 UVX部署命令:")
    print("仓库创建后，用户可以直接使用:")
    print("uvx --from git+https://github.com/YOUR_USERNAME/pdf-decrypt-mcp pdf-decrypt-mcp")

def main():
    """主函数"""
    print("🚀 PDF解密MCP服务 - GitHub部署")
    print("="*50)
    
    # 检查是否在Git仓库中
    if not os.path.exists(".git"):
        print("[错误] 当前目录不是Git仓库")
        return
    
    # 配置Git
    if not configure_git():
        print("[错误] Git配置失败")
        return
    
    # 检查Git状态
    if not check_git_status():
        print("[错误] Git状态检查失败")
        return
    
    # 添加并提交更改
    if add_commit_changes():
        print("[成功] 代码提交完成")
    else:
        print("[警告] 代码提交失败或没有新更改")
    
    # 显示GitHub创建指南
    create_github_repo_instructions()
    
    print("\n" + "="*50)
    print("[完成] GitHub部署准备完成！")
    print("="*50)
    
    print("\n📁 下一步操作:")
    print("1. 按照上述指南在GitHub上创建仓库")
    print("2. 运行git命令连接到远程仓库")
    print("3. 推送代码到GitHub")
    print("4. 验证部署是否成功")

if __name__ == "__main__":
    main()