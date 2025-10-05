# PDF解密MCP服务

一个提供PDF文件解密功能的MCP（Model Context Protocol）服务器，支持多种部署方式，特别是UVX部署。

## 功能特性

- 🔍 **检查PDF加密状态** - 检查PDF文件是否加密及基本信息
- 🔓 **单个PDF解密** - 解密单个PDF文件
- 📁 **批量PDF解密** - 批量解密目录中的所有PDF文件
- 📋 **列出PDF文件** - 列出目录中的所有PDF文件
- 🔐 **智能密码尝试** - 自动尝试常见密码解密
- 🌏 **中文支持** - 完全支持中文路径和文件名
- 🚀 **UVX部署** - 支持现代化uvx部署方式

## 安装与部署

### 🚀 UVX部署（推荐）

UVX是一个现代化的Python应用程序运行器，可以轻松运行和分发Python应用程序，无需手动安装依赖。

#### 前置条件

1. 安装Python 3.8+
2. 安装uvx：
   ```bash
   pip install uvx
   # 或者
   pip install pipx && pipx install uvx
   ```

#### 在Claude Code中配置UVX部署

**方法1: 从GitHub直接运行（推荐）**

```json
{
  "mcpServers": {
    "pdf-decrypt": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/tuomashi20/pdf-decrypt-mcp", "pdf-decrypt-mcp"]
    }
  }
}
```

**方法2: 使用本地项目路径**

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

**方法3: 从PyPI安装**

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

### 传统安装方式

#### 从源码安装

```bash
git clone https://github.com/tuomashi20/pdf-decrypt-mcp.git
cd pdf-decrypt-mcp
pip install -e .
```

#### 直接安装

```bash
pip install pdf-decrypt-mcp
```

## 使用方法

### 作为MCP服务器运行

#### UVX方式
通过Claude Code配置后自动运行，无需手动启动。

#### 传统方式
```bash
pdf-decrypt-mcp
```

### 在Claude Code中配置

#### UVX配置（推荐）

```json
{
  "mcpServers": {
    "pdf-decrypt": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/tuomashi20/pdf-decrypt-mcp", "pdf-decrypt-mcp"]
    }
  }
}
```

#### 传统配置

```json
{
  "mcpServers": {
    "pdf-decrypt": {
      "command": "pdf-decrypt-mcp"
    }
  }
}
```

## 工具说明

### 1. check_pdf_encryption
检查PDF文件的加密状态和基本信息。

**参数：**
- `file_path` (必需): PDF文件的完整路径

**示例：**
```json
{
  "tool": "check_pdf_encryption",
  "arguments": {
    "file_path": "/path/to/your/file.pdf"
  }
}
```

### 2. decrypt_pdf
解密单个PDF文件。

**参数：**
- `input_path` (必需): 输入PDF文件的完整路径
- `output_path` (可选): 输出PDF文件的完整路径
- `password` (可选): 解密密码

**示例：**
```json
{
  "tool": "decrypt_pdf",
  "arguments": {
    "input_path": "/path/to/encrypted.pdf",
    "output_path": "/path/to/decrypted.pdf"
  }
}
```

### 3. batch_decrypt_pdfs
批量解密目录中的所有PDF文件。

**参数：**
- `directory` (必需): 包含PDF文件的目录路径
- `password` (可选): 解密密码

**示例：**
```json
{
  "tool": "batch_decrypt_pdfs",
  "arguments": {
    "directory": "/path/to/pdf/directory"
  }
}
```

### 4. list_pdf_files
列出目录中的所有PDF文件。

**参数：**
- `directory` (必需): 目录路径
- `include_decrypted` (可选): 是否包含已解密的文件

**示例：**
```json
{
  "tool": "list_pdf_files",
  "arguments": {
    "directory": "/path/to/pdf/directory",
    "include_decrypted": false
  }
}
```

## 常见密码列表

如果不提供密码，系统会自动尝试以下常见密码：

- 空密码
- 123456, password, qwerty
- 赵礼显, 赵礼显数学, zhaolixian
- aspose, pdf, decrypt, unlock
- 等等...

## 部署方式对比

| 方式 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **UVX** | 无需安装依赖、自动管理环境、部署简单 | 需要安装uvx | 推荐、生产环境 |
| **源码安装** | 完全控制、可修改源码 | 需要手动管理依赖 | 开发、定制需求 |
| **PyPI安装** | 安装简单 | 需要发布到PyPI | 最终用户 |

## 注意事项

- 解密后的文件会在原文件名后添加"_解密版"后缀
- 解密过程不会修改原始文件
- 请确保有足够的磁盘空间存储解密后的文件
- 某些强加密的PDF文件可能需要特定密码才能解密

## 错误处理

所有工具调用都会返回包含以下字段的结果：

- `success`: 操作是否成功
- `message`: 操作结果描述
- `error`: 错误信息（如果有）
- 具体操作相关的数据字段

## 开发

### 项目结构

```
pdf-decrypt-mcp/
├── src/
│   └── pdf_decrypt_mcp/
│       ├── __init__.py
│       ├── server.py          # MCP服务器主文件
│       └── pdf_decryptor.py   # PDF解密核心功能
├── pyproject.toml             # 项目配置
├── pyproject_uvx.toml         # UVX优化配置
├── README.md                  # 项目说明
└── README_UVX.md              # UVX详细部署指南
```

### 依赖项

- `mcp>=1.0.0` - MCP协议支持
- `PyPDF2>=3.0.0` - PDF文件处理
- `PyCryptodome>=3.15.0` - 加密算法支持

### 开发依赖

- `pytest>=7.0.0` - 测试框架
- `pytest-asyncio>=0.21.0` - 异步测试
- `black>=23.0.0` - 代码格式化
- `isort>=5.12.0` - 导入排序
- `mypy>=1.0.0` - 类型检查

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 更新日志

### v1.0.0
- 初始版本发布
- 支持PDF加密状态检查
- 支持单个和批量PDF解密
- 支持中文路径和文件名
- 智能密码尝试功能
- 新增UVX部署支持

## 相关链接

- **GitHub:** https://github.com/tuomashi20/pdf-decrypt-mcp
- **详细UVX部署指南:** [README_UVX.md](https://github.com/tuomashi20/pdf-decrypt-mcp/blob/main/README_UVX.md)