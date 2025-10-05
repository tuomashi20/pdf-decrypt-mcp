#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter

logger = logging.getLogger(__name__)

class PDFDecryptor:
    """PDF解密器类"""
    
    def __init__(self):
        """初始化PDF解密器"""
        self.common_passwords = [
            "",  # 空密码
            "123456",
            "password",
            "123456789",
            "qwerty",
            "abc123",
            "111111",
            "password123",
            "admin",
            "letmein",
            "welcome",
            "monkey",
            "1234567890",
            "password1",
            "123123",
            "000000",
            "iloveyou",
            "赵礼显",
            "赵礼显数学",
            "zhaolixian",
            "zhaolixianmath",
            "math",
            "数学",
            "秋季班",
            "空间向量",
            "空间向量题型拓展",
            "秋季第1讲",
            "aspose",  # 从PDF元数据中看到创建者是Aspose
            "aspose.pdf",
            "pdf",
            "decrypt",
            "unlock",
        ]
    
    def check_pdf_encryption(self, file_path: str) -> Dict[str, Any]:
        """
        检查PDF文件的加密状态
        
        Args:
            file_path: PDF文件路径
            
        Returns:
            包含加密状态信息的字典
        """
        try:
            if not os.path.exists(file_path):
                return {
                    "success": False,
                    "error": f"文件不存在: {file_path}",
                    "is_encrypted": False,
                    "file_info": {}
                }
            
            reader = PdfReader(file_path)
            file_info = {
                "pages": len(reader.pages),
                "title": reader.metadata.title if reader.metadata and reader.metadata.title else "未知",
                "author": reader.metadata.author if reader.metadata and reader.metadata.author else "未知",
                "creator": reader.metadata.creator if reader.metadata and reader.metadata.creator else "未知",
                "producer": reader.metadata.producer if reader.metadata and reader.metadata.producer else "未知",
                "file_size": os.path.getsize(file_path)
            }
            
            if not reader.is_encrypted:
                return {
                    "success": True,
                    "is_encrypted": False,
                    "file_info": file_info
                }
            
            return {
                "success": True,
                "is_encrypted": True,
                "file_info": file_info
            }
            
        except Exception as e:
            logger.error(f"检查PDF加密状态时出错: {e}")
            return {
                "success": False,
                "error": f"检查PDF加密状态时出错: {str(e)}",
                "is_encrypted": False,
                "file_info": {}
            }
    
    def decrypt_pdf(self, input_path: str, output_path: Optional[str] = None, 
                   password: Optional[str] = None) -> Dict[str, Any]:
        """
        解密PDF文件
        
        Args:
            input_path: 输入PDF文件路径
            output_path: 输出PDF文件路径（可选）
            password: 解密密码（可选，如果不提供则尝试常见密码）
            
        Returns:
            包含解密结果的字典
        """
        try:
            if not os.path.exists(input_path):
                return {
                    "success": False,
                    "error": f"输入文件不存在: {input_path}"
                }
            
            reader = PdfReader(input_path)
            
            if not reader.is_encrypted:
                # 如果文件未加密，直接复制
                if not output_path:
                    base_name = os.path.splitext(os.path.basename(input_path))[0]
                    output_path = os.path.join(
                        os.path.dirname(input_path), 
                        f"{base_name}_解密版.pdf"
                    )
                
                with open(input_path, 'rb') as input_file:
                    with open(output_path, 'wb') as output_file:
                        output_file.write(input_file.read())
                
                return {
                    "success": True,
                    "message": "PDF文件未加密，已直接复制",
                    "output_path": output_path,
                    "password_used": ""
                }
            
            # 尝试解密
            passwords_to_try = [password] if password else self.common_passwords
            successful_password = None
            
            for pwd in passwords_to_try:
                if pwd is None:
                    continue
                try:
                    if reader.decrypt(pwd):
                        successful_password = pwd
                        break
                except Exception:
                    continue
            
            if not successful_password:
                return {
                    "success": False,
                    "error": "无法解密PDF文件，所有密码都失败"
                }
            
            # 生成输出路径
            if not output_path:
                base_name = os.path.splitext(os.path.basename(input_path))[0]
                output_path = os.path.join(
                    os.path.dirname(input_path), 
                    f"{base_name}_解密版.pdf"
                )
            
            # 写入解密后的文件
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return {
                "success": True,
                "message": "PDF文件解密成功",
                "output_path": output_path,
                "password_used": successful_password
            }
            
        except Exception as e:
            logger.error(f"解密PDF文件时出错: {e}")
            return {
                "success": False,
                "error": f"解密PDF文件时出错: {str(e)}"
            }
    
    def batch_decrypt_pdfs(self, directory: str, password: Optional[str] = None) -> Dict[str, Any]:
        """
        批量解密目录中的所有PDF文件
        
        Args:
            directory: 目录路径
            password: 解密密码（可选）
            
        Returns:
            包含批量解密结果的字典
        """
        try:
            if not os.path.exists(directory):
                return {
                    "success": False,
                    "error": f"目录不存在: {directory}"
                }
            
            # 获取目录中所有PDF文件
            pdf_files = []
            for file in os.listdir(directory):
                if file.lower().endswith('.pdf') and not file.endswith('_解密版.pdf'):
                    pdf_files.append(file)
            
            results = {
                "success": True,
                "total_files": len(pdf_files),
                "processed_files": 0,
                "encrypted_files": 0,
                "decrypted_files": 0,
                "failed_files": 0,
                "results": []
            }
            
            for pdf_file in pdf_files:
                input_path = os.path.join(directory, pdf_file)
                
                # 检查加密状态
                encryption_status = self.check_pdf_encryption(input_path)
                
                if not encryption_status["success"]:
                    results["failed_files"] += 1
                    results["results"].append({
                        "file": pdf_file,
                        "success": False,
                        "error": encryption_status["error"]
                    })
                    continue
                
                results["processed_files"] += 1
                
                if not encryption_status["is_encrypted"]:
                    results["results"].append({
                        "file": pdf_file,
                        "success": True,
                        "is_encrypted": False,
                        "message": "文件未加密"
                    })
                    continue
                
                results["encrypted_files"] += 1
                
                # 尝试解密
                decrypt_result = self.decrypt_pdf(input_path, password=password)
                
                if decrypt_result["success"]:
                    results["decrypted_files"] += 1
                    results["results"].append({
                        "file": pdf_file,
                        "success": True,
                        "is_encrypted": True,
                        "output_path": decrypt_result["output_path"],
                        "password_used": decrypt_result["password_used"]
                    })
                else:
                    results["failed_files"] += 1
                    results["results"].append({
                        "file": pdf_file,
                        "success": False,
                        "is_encrypted": True,
                        "error": decrypt_result["error"]
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"批量解密PDF文件时出错: {e}")
            return {
                "success": False,
                "error": f"批量解密PDF文件时出错: {str(e)}"
            }