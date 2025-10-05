# GitHub部署指南

## 步骤1: 创建GitHub仓库

1. 登录 [GitHub](https://github.com)
2. 点击右上角的 "+" 按钮，选择 "New repository"
3. 填写仓库信息：
   - Repository name: `pdf-decrypt-mcp`
   - Description: `PDF解密MCP服务 - 支持UVX部署的PDF文件解密工具`
   - 选择 Public 或 Private（根据需要）
   - 不要勾选 "Add a README file"（我们已经有了）
   - 不要勾选 "Add .gitignore"（我们已经有了）
   - 不要勾选 "Choose a license"（我们已经在代码中包含）
4. 点击 "Create repository"

## 步骤2: 连接本地仓库到GitHub

创建仓库后，GitHub会显示快速设置页面。选择 "...or push an existing repository from the command line" 部分，运行以下命令：

```bash
cd "D:\BaiduNetdiskDownload\赵礼显\秋季\秋季班讲义\pdf-decrypt-mcp"
git remote add origin https://github.com/YOUR_USERNAME/pdf-decrypt-mcp.git
git branch -M main
git push -u origin main
```

**注意**: 将 `YOUR_USERNAME` 替换为您的GitHub用户名。

## 步骤3: 验证部署

推送完成后，您可以：

1. 访问您的GitHub仓库页面
2. 检查所有文件是否已正确上传
3. 验证README.md是否正确显示

## 步骤4: 使用UVX部署（推荐）

现在您可以直接使用UVX从GitHub部署：

```json
{
  "mcpServers": {
    "pdf-decrypt": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/YOUR_USERNAME/pdf-decrypt-mcp", "pdf-decrypt-mcp"]
    }
  }
}
```

## 步骤5: 可选 - 发布到PyPI

如果您想发布到PyPI，可以：

1. 注册PyPI账户
2. 安装发布工具：`pip install build twine`
3. 构建包：`python -m build`
4. 发布：`python -m twine upload dist/*`

发布后，用户可以直接使用：
```json
{
  "mcpServers": {
    "pdf-decrypt": {
      "command": "uvx",
      "args": ["pdf-decrypt-mcp"]
    }
  }
}
```

## 常见问题

### Q: 推送时出现权限错误
A: 确保您有仓库的写入权限，或者使用SSH密钥而不是HTTPS。

### Q: UVX部署失败
A: 检查您的项目结构是否符合Python包的要求，特别是pyproject.toml文件。

### Q: 如何更新代码
A: 修改代码后，运行：
```bash
git add .
git commit -m "Your commit message"
git push
```

## 项目结构说明

```
pdf-decrypt-mcp/
├── src/pdf_decrypt_mcp/          # 主要源代码
│   ├── __init__.py               # 包初始化
│   ├── server_fixed.py           # MCP服务器
│   └── pdf_decryptor.py          # PDF解密核心
├── README.md                     # 项目说明
├── README_UVX.md                 # UVX部署指南
├── USAGE_GUIDE.md                # 使用指南
├── pyproject.toml                # 项目配置
├── pyproject_uvx.toml            # UVX配置
├── setup.py                      # 安装脚本
└── .gitignore                    # Git忽略文件
```

## 维护说明

1. 定期更新依赖项
2. 测试新版本的兼容性
3. 更新文档
4. 处理用户反馈和Issue

## 许可证

本项目使用MIT许可证，详情请参见代码中的许可证信息。