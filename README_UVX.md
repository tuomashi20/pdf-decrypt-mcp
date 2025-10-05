# PDF解密MCP服务 - UVX部署指南

一个提供PDF文件解密功能的MCP（Model Context Protocol）服务器，支持多种部署方式，特别是uvx部署。

## 🚀 UVX部署（推荐）

UVX是一个现代化的Python应用程序运行器，可以轻松运行和分发Python应用程序，无需手动安装依赖。

### 前置条件

1. 安装Python 3.8+
2. 安装uvx：
   ```bash
   pip install uvx
   # 或者
   pip install pipx && pipx install uvx
   ```

### 方法1: 使用uvx直接运行（推荐）

在Claude Code配置中添加：

```json
{
  "mcpServers": {
    "pdf-decrypt": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/your-username/pdf-decrypt-mcp", "pdf-decrypt-mcp"]
    }
  }
}
```

### 方法2: 使用本地项目路径

如果项目在本地：

```json
{
  "mcpServers": {
    "pdf-decrypt": {
      "command": "uvx",
      "args": ["--from", "/path/to/pdf-decrypt-mcp", "pdf-decrypt-mcp"]
    }
  }
}
```

### 方法3: 使用PyPI包

如果已发布到PyPI：

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

### 方法4: 指定版本

```json
{
  "mcpServers": {
    "pdf-decrypt": {
      "command": "uvx",
      "args": ["--from", "pdf-decrypt-mcp==1.0.0", "pdf-decrypt-mcp"]
    }
  }
}
```

## 📦 其他部署方式

### 传统安装方式

```bash
# 从源码安装
git clone <repository-url>
cd pdf-decrypt-mcp
pip install -e .

# 或者直接安装
pip install pdf-decrypt-mcp
```

然后在Claude Code中配置：

```json
{
  "mcpServers": {
    "pdf-decrypt": {
      "command": "pdf-decrypt-mcp"
    }
  }
}
```

## 🔧 测试部署

### 测试uvx部署

```bash
# 测试本地项目
uvx --from /path/to/pdf-decrypt-mcp pdf-decrypt-mcp --help

# 测试Git仓库
uvx --from git+https://github.com/your-username/pdf-decrypt-mcp pdf-decrypt-mcp --help

# 测试PyPI包
uvx pdf-decrypt-mcp --help
```

### 测试传统安装

```bash
pdf-decrypt-mcp --help
```

## 🛠️ 功能特性

- 🔍 **检查PDF加密状态** - 检查PDF文件是否加密及基本信息
- 🔓 **单个PDF解密** - 解密单个PDF文件
- 📁 **批量PDF解密** - 批量解密目录中的所有PDF文件
- 📋 **列出PDF文件** - 列出目录中的所有PDF文件
- 🔐 **智能密码尝试** - 自动尝试常见密码解密
- 🌏 **中文支持** - 完全支持中文路径和文件名
- 🚀 **零依赖安装** - 使用uvx无需手动管理依赖

## 📋 MCP工具

### 1. check_pdf_encryption
检查PDF文件的加密状态和基本信息。

**参数：**
- `file_path` (必需): PDF文件的完整路径

### 2. decrypt_pdf
解密单个PDF文件。

**参数：**
- `input_path` (必需): 输入PDF文件的完整路径
- `output_path` (可选): 输出PDF文件的完整路径
- `password` (可选): 解密密码

### 3. batch_decrypt_pdfs
批量解密目录中的所有PDF文件。

**参数：**
- `directory` (必需): 包含PDF文件的目录路径
- `password` (可选): 解密密码

### 4. list_pdf_files
列出目录中的所有PDF文件。

**参数：**
- `directory` (必需): 目录路径
- `include_decrypted` (可选): 是否包含已解密的文件

## 💡 使用示例

### 使用Claude Code

```javascript
// 检查PDF加密状态
const result = await mcpCall("check_pdf_encryption", {
  file_path: "/path/to/file.pdf"
});

// 解密单个PDF文件
const result = await mcpCall("decrypt_pdf", {
  input_path: "/path/to/encrypted.pdf"
});

// 批量解密PDF文件
const result = await mcpCall("batch_decrypt_pdfs", {
  directory: "/path/to/pdf/directory"
});
```

### 命令行测试

```bash
# 使用uvx测试
uvx --from /path/to/pdf-decrypt-mcp pdf-decrypt-mcp

# 传统安装测试
pdf-decrypt-mcp
```

## 🔐 常见密码列表

如果不提供密码，系统会自动尝试以下常见密码：

- 空密码（最常见的）
- 数字密码：123456, 111111, 000000等
- 常见单词：password, admin, welcome等
- 中文密码：赵礼显, 赵礼显数学, 数学等
- 技术相关：aspose, pdf, decrypt, unlock等

## ⚠️ 注意事项

1. **文件安全性**：解密过程不会修改原始文件
2. **命名规则**：解密后的文件会在原文件名后添加"_解密版"后缀
3. **权限要求**：确保有足够的文件读写权限
4. **网络连接**：首次使用uvx需要网络连接下载依赖

## 🐛 故障排除

### UVX相关问题

**问题1**: `uvx: command not found`
```bash
# 解决方案
pip install uvx
# 或者
pip install pipx && pipx install uvx
```

**问题2**: 网络连接问题
```bash
# 使用国内镜像
uvx --index-url https://pypi.tuna.tsinghua.edu.cn/simple pdf-decrypt-mcp
```

**问题3**: 权限问题
```bash
# 确保uvx在PATH中
echo $PATH | grep uvx
```

### 功能相关问题

**问题1**: PDF解密失败
- 检查文件路径是否正确
- 确认文件权限
- 尝试提供正确的密码

**问题2**: MCP服务器连接失败
- 检查Claude Code配置格式
- 确认命令路径正确
- 查看错误日志

## 📈 性能优化

1. **批量处理**：对于多个文件，使用批量解密功能
2. **跳过已解密**：自动跳过已解密的文件
3. **缓存机制**：uvx会缓存已下载的包，提高启动速度

## 🔄 更新和维护

### 更新uvx版本
```bash
uvx --from pdf-decrypt-mcp@latest pdf-decrypt-mcp
```

### 清理uvx缓存
```bash
uvx cache clean
```

## 📚 更多资源

- [UVX官方文档](https://github.com/astral-sh/uvx)
- [MCP协议文档](https://modelcontextprotocol.io/)
- [项目源码](https://github.com/your-username/pdf-decrypt-mcp)

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！