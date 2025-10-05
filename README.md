# PDF解密MCP服务

一个提供PDF文件解密功能的MCP（Model Context Protocol）服务器。

## 功能特性

- 🔍 **检查PDF加密状态** - 检查PDF文件是否加密及基本信息
- 🔓 **单个PDF解密** - 解密单个PDF文件
- 📁 **批量PDF解密** - 批量解密目录中的所有PDF文件
- 📋 **列出PDF文件** - 列出目录中的所有PDF文件
- 🔐 **智能密码尝试** - 自动尝试常见密码解密
- 🌏 **中文支持** - 完全支持中文路径和文件名

## 安装

### 从源码安装

```bash
git clone <repository-url>
cd pdf-decrypt-mcp
pip install -e .
```

### 直接安装

```bash
pip install pdf-decrypt-mcp
```

## 使用方法

### 作为MCP服务器运行

```bash
pdf-decrypt-mcp
```

### 在Claude Code中配置

在Claude Code的配置文件中添加：

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
└── README.md                  # 项目说明
```

### 依赖项

- `mcp>=1.0.0` - MCP协议支持
- `PyPDF2>=3.0.0` - PDF文件处理
- `PyCryptodome>=3.15.0` - 加密算法支持

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