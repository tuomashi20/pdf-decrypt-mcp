# 离线部署方案

## 📦 离线安装包创建

由于网络连接问题，您可以创建离线安装包来部署PDF解密MCP服务。

### 方案1: 创建本地PyPI镜像

```bash
# 下载所有依赖包
pip download -r requirements.txt -d offline_packages/

# 创建requirements.txt
echo "mcp>=1.0.0" > requirements.txt
echo "PyPDF2>=3.0.0" >> requirements.txt
echo "PyCryptodome>=3.15.0" >> requirements.txt

# 下载依赖
pip download -r requirements.txt -d offline_packages/
```

### 方案2: 打包完整项目

```bash
# 创建项目包
tar -czf pdf-decrypt-mcp-offline.tar.gz \
    src/ \
    README.md \
    README_UVX.md \
    USAGE_GUIDE.md \
    pyproject.toml \
    setup.py \
    .gitignore

# 或者创建ZIP包
powershell "Compress-Archive -Path * -DestinationPath pdf-decrypt-mcp-offline.zip"
```

## 🚀 离线部署步骤

### 步骤1: 准备离线环境

1. 将项目文件复制到目标机器
2. 确保Python 3.8+已安装
3. 准备离线依赖包

### 步骤2: 本地安装

```bash
# 进入项目目录
cd pdf-decrypt-mcp

# 安装依赖（如果有离线包）
pip install --no-index --find-links=offline_packages/ -r requirements.txt

# 或者直接从PyPI安装
pip install mcp PyPDF2 PyCryptodome

# 安装项目
pip install -e .
```

### 步骤3: 测试安装

```bash
# 测试MCP服务
python -c "from pdf_decrypt_mcp import PDFDecryptor; print('安装成功')"

# 测试命令行工具
pdf-decrypt-mcp --help
```

## 📋 完整离线部署脚本

创建一个离线部署脚本 `offline_install.sh`:

```bash
#!/bin/bash

echo "PDF解密MCP服务 - 离线部署"
echo "============================="

# 检查Python版本
python_version=$(python3 --version 2>&1)
echo "Python版本: $python_version"

# 检查pip
pip_version=$(pip --version 2>&1)
echo "Pip版本: $pip_version"

# 安装依赖
echo "正在安装依赖..."
pip install mcp PyPDF2 PyCryptodome

# 安装项目
echo "正在安装项目..."
pip install -e .

# 测试安装
echo "正在测试安装..."
python3 -c "
try:
    from pdf_decrypt_mcp import PDFDecryptor
    print('✅ 核心模块导入成功')
    
    import pdf_decrypt_mcp
    print('✅ 完整包导入成功')
    
    print('✅ PDF解密MCP服务安装完成!')
except Exception as e:
    print(f'❌ 安装失败: {e}')
"

echo "离线部署完成!"
echo "使用方法: pdf-decrypt-mcp"
```

Windows版本 `offline_install.bat`:

```batch
@echo off
echo PDF解密MCP服务 - 离线部署
echo =============================

REM 检查Python版本
python --version
if %errorlevel% neq 0 (
    echo 错误: Python未安装或不在PATH中
    pause
    exit /b 1
)

REM 检查pip
pip --version
if %errorlevel% neq 0 (
    echo 错误: pip未安装
    pause
    exit /b 1
)

REM 安装依赖
echo 正在安装依赖...
pip install mcp PyPDF2 PyCryptodome
if %errorlevel% neq 0 (
    echo 错误: 依赖安装失败
    pause
    exit /b 1
)

REM 安装项目
echo 正在安装项目...
pip install -e .
if %errorlevel% neq 0 (
    echo 错误: 项目安装失败
    pause
    exit /b 1
)

REM 测试安装
echo 正在测试安装...
python -c "
try:
    from pdf_decrypt_mcp import PDFDecryptor
    print('✅ 核心模块导入成功')
    
    import pdf_decrypt_mcp
    print('✅ 完整包导入成功')
    
    print('✅ PDF解密MCP服务安装完成!')
except Exception as e:
    print(f'❌ 安装失败: {e}')
"

echo 离线部署完成!
echo 使用方法: pdf-decrypt-mcp
pause
```

## 📁 打包分发

### 创建完整安装包

```python
# create_offline_package.py
import os
import shutil
import subprocess
from pathlib import Path

def create_offline_package():
    """创建离线安装包"""
    
    # 创建离线包目录
    offline_dir = Path("pdf-decrypt-mcp-offline")
    if offline_dir.exists():
        shutil.rmtree(offline_dir)
    offline_dir.mkdir()
    
    # 复制项目文件
    files_to_copy = [
        "src",
        "README.md",
        "README_UVX.md", 
        "USAGE_GUIDE.md",
        "pyproject.toml",
        "setup.py",
        ".gitignore"
    ]
    
    for file_name in files_to_copy:
        src_path = Path(file_name)
        if src_path.exists():
            if src_path.is_dir():
                shutil.copytree(src_path, offline_dir / src_path)
            else:
                shutil.copy2(src_path, offline_dir / src_path)
    
    # 创建离线安装脚本
    scripts_dir = offline_dir / "scripts"
    scripts_dir.mkdir()
    
    # 复制安装脚本
    shutil.copy2("offline_install.bat", scripts_dir / "install.bat")
    shutil.copy2("offline_install.sh", scripts_dir / "install.sh")
    
    # 创建requirements.txt
    with open(offline_dir / "requirements.txt", "w") as f:
        f.write("mcp>=1.0.0\n")
        f.write("PyPDF2>=3.0.0\n")
        f.write("PyCryptodome>=3.15.0\n")
    
    # 创建离线包说明
    with open(offline_dir / "OFFLINE_README.txt", "w", encoding="utf-8") as f:
        f.write("PDF解密MCP服务 - 离线安装包\n")
        f.write("=" * 40 + "\n\n")
        f.write("安装步骤:\n")
        f.write("1. 确保Python 3.8+已安装\n")
        f.write("2. 运行 scripts/install.bat (Windows) 或 scripts/install.sh (Linux/Mac)\n")
        f.write("3. 测试: pdf-decrypt-mcp --help\n\n")
        f.write("配置Claude Code:\n")
        f.write('{\n')
        f.write('  "mcpServers": {\n')
        f.write('    "pdf-decrypt": {\n')
        f.write('      "command": "pdf-decrypt-mcp"\n')
        f.write('    }\n')
        f.write('  }\n')
        f.write('}\n')
    
    print(f"离线安装包创建完成: {offline_dir}")
    return offline_dir

if __name__ == "__main__":
    create_offline_package()
```

## 🌐 网络环境适配

### 企业内网部署

1. **内网PyPI仓库**:
```bash
pip install --index-url https://pypi.company.com/simple/ pdf-decrypt-mcp
```

2. **离线文件传输**:
   - 使用U盘或内部网络传输
   - 确保所有依赖包都包含在内

### 受限环境部署

1. **最小依赖安装**:
```bash
pip install --no-deps pdf-decrypt-mcp
# 然后手动安装依赖
```

2. **源码安装**:
```bash
python setup.py install
```

## 📞 技术支持

如果离线部署遇到问题：

1. **检查Python版本**: 确保是3.8+
2. **检查权限**: 确保有安装权限
3. **检查路径**: 确保在正确的目录中
4. **查看日志**: 检查安装过程中的错误信息

## 🎯 推荐方案

基于当前网络状况，推荐：

1. **立即方案**: 使用离线部署
2. **长期方案**: 解决网络问题后使用GitHub
3. **备选方案**: 使用其他Git托管服务

---

**注意**: 离线部署虽然可行，但无法获得自动更新。建议在网络问题解决后切换到在线部署。