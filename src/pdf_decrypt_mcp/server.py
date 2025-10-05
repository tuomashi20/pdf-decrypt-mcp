#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import json
import logging
import sys
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    GetPromptRequest,
    GetPromptResult,
    ListPromptsRequest,
    ListPromptsResult,
    ListResourcesRequest,
    ListResourcesResult,
    ListToolsRequest,
    ListToolsResult,
    Prompt,
    PromptArgument,
    Resource,
    TextContent,
    Tool,
    ToolInfo,
)

from .pdf_decryptor import PDFDecryptor

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建MCP服务器
server = Server("pdf-decrypt-mcp")

# 创建PDF解密器实例
pdf_decryptor = PDFDecryptor()

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """列出所有可用的工具"""
    return [
        Tool(
            name="check_pdf_encryption",
            description="检查PDF文件的加密状态和基本信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "PDF文件的完整路径"
                    }
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="decrypt_pdf",
            description="解密单个PDF文件",
            inputSchema={
                "type": "object",
                "properties": {
                    "input_path": {
                        "type": "string",
                        "description": "输入PDF文件的完整路径"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "输出PDF文件的完整路径（可选，默认在原文件同目录添加'_解密版'）"
                    },
                    "password": {
                        "type": "string",
                        "description": "解密密码（可选，如果不提供则尝试常见密码）"
                    }
                },
                "required": ["input_path"]
            }
        ),
        Tool(
            name="batch_decrypt_pdfs",
            description="批量解密目录中的所有PDF文件",
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "包含PDF文件的目录路径"
                    },
                    "password": {
                        "type": "string",
                        "description": "解密密码（可选，如果不提供则尝试常见密码）"
                    }
                },
                "required": ["directory"]
            }
        ),
        Tool(
            name="list_pdf_files",
            description="列出目录中的所有PDF文件",
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "目录路径"
                    },
                    "include_decrypted": {
                        "type": "boolean",
                        "description": "是否包含已解密的文件（默认为false）",
                        "default": False
                    }
                },
                "required": ["directory"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """处理工具调用"""
    try:
        if name == "check_pdf_encryption":
            file_path = arguments.get("file_path")
            if not file_path:
                return CallToolResult(
                    content=[TextContent(type="text", text="错误: file_path 参数是必需的")]
                )
            
            result = pdf_decryptor.check_pdf_encryption(file_path)
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
            )
        
        elif name == "decrypt_pdf":
            input_path = arguments.get("input_path")
            if not input_path:
                return CallToolResult(
                    content=[TextContent(type="text", text="错误: input_path 参数是必需的")]
                )
            
            output_path = arguments.get("output_path")
            password = arguments.get("password")
            
            result = pdf_decryptor.decrypt_pdf(input_path, output_path, password)
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
            )
        
        elif name == "batch_decrypt_pdfs":
            directory = arguments.get("directory")
            if not directory:
                return CallToolResult(
                    content=[TextContent(type="text", text="错误: directory 参数是必需的")]
                )
            
            password = arguments.get("password")
            
            result = pdf_decryptor.batch_decrypt_pdfs(directory, password)
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
            )
        
        elif name == "list_pdf_files":
            directory = arguments.get("directory")
            if not directory:
                return CallToolResult(
                    content=[TextContent(type="text", text="错误: directory 参数是必需的")]
                )
            
            include_decrypted = arguments.get("include_decrypted", False)
            
            try:
                import os
                if not os.path.exists(directory):
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"错误: 目录不存在: {directory}")]
                    )
                
                pdf_files = []
                for file in os.listdir(directory):
                    if file.lower().endswith('.pdf'):
                        if include_decrypted or not file.endswith('_解密版.pdf'):
                            file_path = os.path.join(directory, file)
                            file_size = os.path.getsize(file_path)
                            pdf_files.append({
                                "name": file,
                                "path": file_path,
                                "size": file_size,
                                "is_decrypted": file.endswith('_解密版.pdf')
                            })
                
                result = {
                    "success": True,
                    "directory": directory,
                    "total_files": len(pdf_files),
                    "files": pdf_files
                }
                
                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
                )
                
            except Exception as e:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"列出PDF文件时出错: {str(e)}")]
                )
        
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"错误: 未知工具 '{name}'")]
            )
    
    except Exception as e:
        logger.error(f"处理工具调用时出错: {e}")
        return CallToolResult(
            content=[TextContent(type="text", text=f"处理工具调用时出错: {str(e)}")]
        )

@server.list_resources()
async def handle_list_resources() -> List[Resource]:
    """列出所有可用的资源"""
    return []

@server.list_prompts()
async def handle_list_prompts() -> List[Prompt]:
    """列出所有可用的提示"""
    return [
        Prompt(
            name="decrypt_pdf_guide",
            description="PDF解密操作指南",
            arguments=[
                PromptArgument(
                    name="operation",
                    description="操作类型: single, batch, check",
                    required=False
                )
            ]
        )
    ]

@server.get_prompt()
async def handle_get_prompt(name: str, arguments: Dict[str, str]) -> GetPromptResult:
    """获取提示内容"""
    if name == "decrypt_pdf_guide":
        operation = arguments.get("operation", "general")
        
        if operation == "single":
            content = """# 单个PDF文件解密指南

## 使用步骤

1. 使用 `check_pdf_encryption` 工具检查PDF文件是否加密
2. 如果文件已加密，使用 `decrypt_pdf` 工具进行解密

## 工具参数

### check_pdf_encryption
- `file_path`: PDF文件的完整路径

### decrypt_pdf  
- `input_path`: 输入PDF文件的完整路径
- `output_path`: 输出PDF文件的完整路径（可选）
- `password`: 解密密码（可选）

## 示例

```json
{
  "tool": "check_pdf_encryption",
  "arguments": {
    "file_path": "/path/to/encrypted.pdf"
  }
}
```

```json
{
  "tool": "decrypt_pdf",
  "arguments": {
    "input_path": "/path/to/encrypted.pdf",
    "output_path": "/path/to/decrypted.pdf"
  }
}
```
"""
        elif operation == "batch":
            content = """# 批量PDF文件解密指南

## 使用步骤

1. 使用 `list_pdf_files` 工具查看目录中的PDF文件
2. 使用 `batch_decrypt_pdfs` 工具批量解密目录中的所有PDF文件

## 工具参数

### list_pdf_files
- `directory`: 目录路径
- `include_decrypted`: 是否包含已解密的文件（可选）

### batch_decrypt_pdfs
- `directory`: 包含PDF文件的目录路径
- `password`: 解密密码（可选）

## 示例

```json
{
  "tool": "list_pdf_files",
  "arguments": {
    "directory": "/path/to/pdfs"
  }
}
```

```json
{
  "tool": "batch_decrypt_pdfs",
  "arguments": {
    "directory": "/path/to/pdfs"
  }
}
```
"""
        else:
            content = """# PDF解密MCP服务指南

## 功能概述

本MCP服务提供以下PDF解密功能：

1. **检查PDF加密状态** - 检查PDF文件是否加密及基本信息
2. **单个PDF解密** - 解密单个PDF文件
3. **批量PDF解密** - 批量解密目录中的所有PDF文件
4. **列出PDF文件** - 列出目录中的所有PDF文件

## 工具列表

- `check_pdf_encryption` - 检查PDF加密状态
- `decrypt_pdf` - 解密单个PDF文件
- `batch_decrypt_pdfs` - 批量解密PDF文件
- `list_pdf_files` - 列出PDF文件

## 使用提示

- 如果不提供密码，系统会自动尝试常见密码
- 解密后的文件会在原文件名后添加"_解密版"后缀
- 支持中文路径和文件名

## 注意事项

- 请确保有足够的磁盘空间存储解密后的文件
- 解密过程不会修改原始文件
- 某些强加密的PDF文件可能需要特定密码才能解密
"""
        
        return GetPromptResult(
            description=f"PDF解密指南 - {operation}",
            messages=[
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": content
                    }
                }
            ]
        )
    
    return GetPromptResult(
        description="未知提示",
        messages=[
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": "未找到指定的提示"
                }
            }
        ]
    )

async def main():
    """主函数"""
    try:
        # 使用stdio服务器运行MCP服务
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="pdf-decrypt-mcp",
                    server_version="1.0.0",
                    capabilities=server.get_capabilities(
                        notification_options=None,
                        experimental_capabilities=None
                    )
                )
            )
    except Exception as e:
        logger.error(f"启动MCP服务器时出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())