# PDF解密MCP服务 - UVX配置指南

## 方法1: 直接使用uvx命令

在Claude Code配置中添加:
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

## 方法2: 使用本地项目

如果项目在本地:
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

## 方法3: 使用PyPI包

如果已发布到PyPI:
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

## 方法4: 指定版本

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

## 测试命令

测试uvx是否正常工作:
```bash
uvx --from /path/to/pdf-decrypt-mcp pdf-decrypt-mcp --help
```
