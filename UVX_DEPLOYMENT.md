# UVX快速部署指南

## 🚀 一键部署（推荐）

在Claude Code配置中添加以下配置：

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

## 📋 前置条件

1. **安装Python 3.8+**
   ```bash
   # 检查Python版本
   python --version
   ```

2. **安装uvx**
   ```bash
   # 方法1: 直接安装uvx
   pip install uvx
   
   # 方法2: 通过pipx安装（推荐）
   pip install pipx
   pipx install uvx
   
   # 方法3: 使用uv（如果已安装）
   uv tool install uvx
   ```

## 🔧 UVX部署的优势

| 特性 | UVX部署 | 传统安装 |
|------|---------|----------|
| **依赖管理** | ✅ 自动管理虚拟环境 | ❌ 手动安装依赖 |
| **版本隔离** | ✅ 避免冲突 | ❌ 可能冲突 |
| **部署速度** | ✅ 一键部署 | ❌ 多步骤安装 |
| **更新便捷** | ✅ 自动更新 | ❌ 手动重新安装 |
| **系统清洁** | ✅ 独立环境 | ❌ 污染系统Python |

## 🛠️ 多种部署方式

### 方式1: 从GitHub直接部署（推荐）

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

### 方式2: 本地项目部署

```json
{
  "mcpServers": {
    "pdf-decrypt": {
      "command": "uvx",
      "args": ["--from", "/本地路径/pdf-decrypt-mcp", "pdf-decrypt-mcp"]
    }
  }
}
```

### 方式3: 使用特定分支或版本

```json
{
  "mcpServers": {
    "pdf-decrypt": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/tuomashi20/pdf-decrypt-mcp@main", "pdf-decrypt-mcp"]
    }
  }
}
```

### 方式4: 开发模式部署

```json
{
  "mcpServers": {
    "pdf-decrypt": {
      "command": "uvx",
      "args": ["--editable", "/本地路径/pdf-decrypt-mcp", "pdf-decrypt-mcp"]
    }
  }
}
```

## ⚙️ 高级配置选项

### 指定Python版本

```json
{
  "mcpServers": {
    "pdf-decrypt": {
      "command": "uvx",
      "args": [
        "--python", "python3.9",
        "--from", "git+https://github.com/tuomashi20/pdf-decrypt-mcp",
        "pdf-decrypt-mcp"
      ]
    }
  }
}
```

### 添加额外依赖

```json
{
  "mcpServers": {
    "pdf-decrypt": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/tuomashi20/pdf-decrypt-mcp",
        "--with", "requests,beautifulsoup4",
        "pdf-decrypt-mcp"
      ]
    }
  }
}
```

### 环境变量配置

```json
{
  "mcpServers": {
    "pdf-decrypt": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/tuomashi20/pdf-decrypt-mcp",
        "pdf-decrypt-mcp"
      ],
      "env": {
        "PDF_DECRYPT_LOG_LEVEL": "INFO",
        "PDF_DECRYPT_CACHE_DIR": "/path/to/cache"
      }
    }
  }
}
```

## 🐛 故障排除

### 常见问题

1. **uvx命令未找到**
   ```bash
   # 确认uvx已安装
   which uvx
   # 或
   where uvx
   ```

2. **Python版本不兼容**
   ```bash
   # 检查Python版本
   uvx --python python3.8 --help
   ```

3. **网络连接问题**
   ```bash
   # 使用镜像源
   uvx --index-url https://pypi.tuna.tsinghua.edu.cn/simple/ --from git+https://github.com/tuomashi20/pdf-decrypt-mcp pdf-decrypt-mcp
   ```

4. **权限问题**
   ```bash
   # 确保有写入权限
   uvx --verbose --from git+https://github.com/tuomashi20/pdf-decrypt-mcp pdf-decrypt-mcp
   ```

### 调试命令

```bash
# 查看详细日志
uvx --verbose --from git+https://github.com/tuomashi20/pdf-decrypt-mcp pdf-decrypt-mcp

# 查看缓存信息
uvx --cache-dir --from git+https://github.com/tuomashi20/pdf-decrypt-mcp pdf-decrypt-mcp

# 强制重新安装
uvx --force --from git+https://github.com/tuomashi20/pdf-decrypt-mcp pdf-decrypt-mcp
```

## 📝 配置示例

### 完整的Claude Code配置文件

```json
{
  "mcpServers": {
    "pdf-decrypt": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/tuomashi20/pdf-decrypt-mcp",
        "pdf-decrypt-mcp"
      ],
      "env": {
        "PDF_DECRYPT_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Windows系统配置

```json
{
  "mcpServers": {
    "pdf-decrypt": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/tuomashi20/pdf-decrypt-mcp",
        "pdf-decrypt-mcp"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

## 🔄 更新和维护

### 更新到最新版本

```json
{
  "mcpServers": {
    "pdf-decrypt": {
      "command": "uvx",
      "args": [
        "--force",
        "--from", "git+https://github.com/tuomashi20/pdf-decrypt-mcp",
        "pdf-decrypt-mcp"
      ]
    }
  }
}
```

### 清理缓存

```bash
# 清理uvx缓存
uvx --clear-cache

# 或手动删除缓存目录
rm -rf ~/.local/share/uvx/cache/
```

## 📚 参考资源

- [UVX官方文档](https://github.com/astral-sh/uvx)
- [项目GitHub仓库](https://github.com/tuomashi20/pdf-decrypt-mcp)
- [MCP协议文档](https://modelcontextprotocol.io/)
- [Claude Code配置指南](https://docs.anthropic.com/claude/docs/claude-code)