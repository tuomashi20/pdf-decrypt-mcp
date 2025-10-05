# PDF解密MCP服务使用指南

## 概述

PDF解密MCP服务是一个基于Model Context Protocol (MCP)的服务器，提供PDF文件解密功能。该服务可以集成到Claude Code等支持MCP的AI助手中。

## 安装和配置

### 1. 安装服务

```bash
# 进入项目目录
cd pdf-decrypt-mcp

# 安装依赖和服务
pip install -e .
```

### 2. 在Claude Code中配置

在Claude Code的配置文件中添加以下配置：

```json
{
  "mcpServers": {
    "pdf-decrypt": {
      "command": "pdf-decrypt-mcp"
    }
  }
}
```

## 可用工具

### 1. check_pdf_encryption
检查PDF文件的加密状态和基本信息。

**参数：**
- `file_path` (必需): PDF文件的完整路径

**返回示例：**
```json
{
  "success": true,
  "is_encrypted": true,
  "file_info": {
    "pages": 10,
    "title": "未知",
    "author": "未知",
    "creator": "Aspose Ltd.",
    "producer": "Aspose.PDF for .NET 20.5",
    "file_size": 450576
  }
}
```

### 2. decrypt_pdf
解密单个PDF文件。

**参数：**
- `input_path` (必需): 输入PDF文件的完整路径
- `output_path` (可选): 输出PDF文件的完整路径
- `password` (可选): 解密密码

**返回示例：**
```json
{
  "success": true,
  "message": "PDF文件解密成功",
  "output_path": "/path/to/decrypted.pdf",
  "password_used": ""
}
```

### 3. batch_decrypt_pdfs
批量解密目录中的所有PDF文件。

**参数：**
- `directory` (必需): 包含PDF文件的目录路径
- `password` (可选): 解密密码

**返回示例：**
```json
{
  "success": true,
  "total_files": 20,
  "processed_files": 20,
  "encrypted_files": 20,
  "decrypted_files": 20,
  "failed_files": 0,
  "results": [
    {
      "file": "file1.pdf",
      "success": true,
      "is_encrypted": true,
      "output_path": "/path/to/file1_解密版.pdf",
      "password_used": ""
    }
  ]
}
```

### 4. list_pdf_files
列出目录中的所有PDF文件。

**参数：**
- `directory` (必需): 目录路径
- `include_decrypted` (可选): 是否包含已解密的文件

**返回示例：**
```json
{
  "success": true,
  "directory": "/path/to/directory",
  "total_files": 20,
  "files": [
    {
      "name": "file1.pdf",
      "path": "/path/to/file1.pdf",
      "size": 450576,
      "is_decrypted": false
    }
  ]
}
```

## 使用示例

### 示例1：检查单个PDF文件

```javascript
// 使用Claude Code调用
const result = await mcpCall("check_pdf_encryption", {
  file_path: "/path/to/your/file.pdf"
});
```

### 示例2：解密单个PDF文件

```javascript
// 使用Claude Code调用
const result = await mcpCall("decrypt_pdf", {
  input_path: "/path/to/encrypted.pdf",
  output_path: "/path/to/decrypted.pdf"
});
```

### 示例3：批量解密目录中的PDF文件

```javascript
// 使用Claude Code调用
const result = await mcpCall("batch_decrypt_pdfs", {
  directory: "/path/to/pdf/directory"
});
```

### 示例4：列出目录中的PDF文件

```javascript
// 使用Claude Code调用
const result = await mcpCall("list_pdf_files", {
  directory: "/path/to/pdf/directory",
  include_decrypted: false
});
```

## 常见密码列表

如果不提供密码，系统会自动尝试以下常见密码：

- 空密码（最常见的）
- 数字密码：123456, 111111, 000000等
- 常见单词：password, admin, welcome等
- 中文密码：赵礼显, 赵礼显数学, 数学等
- 技术相关：aspose, pdf, decrypt, unlock等

## 注意事项

1. **文件安全性**：解密过程不会修改原始文件，所有解密结果都会保存为新文件
2. **命名规则**：解密后的文件会在原文件名后添加"_解密版"后缀
3. **密码保护**：如果所有常见密码都失败，说明PDF文件使用了强密码保护
4. **磁盘空间**：请确保有足够的磁盘空间存储解密后的文件
5. **路径支持**：完全支持中文路径和文件名

## 错误处理

所有工具调用都会返回包含以下字段的结果：

- `success`: 操作是否成功
- `message`: 操作结果描述
- `error`: 错误信息（如果有）
- 具体操作相关的数据字段

常见错误：
- 文件不存在
- 权限不足
- 磁盘空间不足
- PDF文件损坏
- 密码错误

## 性能优化

1. **批量处理**：对于多个文件，建议使用批量解密功能
2. **跳过已解密**：批量处理时会自动跳过已解密的文件
3. **内存管理**：大文件处理时会自动管理内存使用

## 故障排除

### 问题1：MCP服务器无法启动
- 检查Python版本（需要3.8+）
- 确认所有依赖项已正确安装
- 检查配置文件格式

### 问题2：PDF解密失败
- 确认PDF文件路径正确
- 检查文件权限
- 尝试提供正确的密码

### 问题3：命令行工具不可用
- 重新安装服务：`pip install -e .`
- 检查PATH环境变量

## 技术支持

如遇到问题，请检查：
1. Python和依赖项版本
2. 文件路径和权限
3. 错误日志信息

## 更新日志

- v1.0.0: 初始版本，支持基本的PDF解密功能