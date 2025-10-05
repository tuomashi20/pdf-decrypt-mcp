#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF解密MCP服务安装脚本
"""

from setuptools import setup, find_packages

setup(
    name="pdf-decrypt-mcp",
    version="1.0.0",
    description="PDF解密MCP服务",
    long_description="一个提供PDF文件解密功能的MCP（Model Context Protocol）服务器",
    author="PDF Decrypt Service",
    author_email="decrypt@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "mcp>=1.0.0",
        "PyPDF2>=3.0.0",
        "PyCryptodome>=3.15.0"
    ],
    entry_points={
        "console_scripts": [
            "pdf-decrypt-mcp=pdf_decrypt_mcp.server:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)