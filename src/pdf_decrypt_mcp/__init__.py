#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF解密MCP服务

提供PDF文件解密功能的MCP服务器，支持：
- 检查PDF加密状态
- 单个PDF文件解密
- 批量PDF文件解密
- 列出PDF文件
"""

__version__ = "1.0.0"
__author__ = "PDF Decrypt Service"
__email__ = "decrypt@example.com"

from .pdf_decryptor import PDFDecryptor

# 延迟导入server以避免导入问题
def main():
    """主函数入口点"""
    from .server_fixed import main as server_main
    return server_main()

__all__ = ["PDFDecryptor", "main"]