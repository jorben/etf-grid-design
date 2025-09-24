"""
文件操作工具函数
"""

import os
import json
import pickle
from pathlib import Path
from typing import Any, Optional, Dict
import logging

logger = logging.getLogger(__name__)

def ensure_dir_exists(dir_path: str) -> bool:
    """
    确保目录存在
    
    Args:
        dir_path: 目录路径
        
    Returns:
        是否成功创建或已存在
    """
    try:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"创建目录失败: {dir_path}, 错误: {e}")
        return False

def safe_file_operation(operation: str, file_path: str, data: Any = None) -> Any:
    """
    安全的文件操作
    
    Args:
        operation: 操作类型 ('read', 'write', 'delete', 'exists')
        file_path: 文件路径
        data: 写入数据（仅写入操作需要）
        
    Returns:
        操作结果
    """
    try:
        path = Path(file_path)
        
        if operation == 'exists':
            return path.exists()
        
        elif operation == 'read':
            if not path.exists():
                return None
            
            if file_path.endswith('.json'):
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            elif file_path.endswith('.pkl'):
                with open(path, 'rb') as f:
                    return pickle.load(f)
            else:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()
        
        elif operation == 'write':
            # 确保父目录存在
            ensure_dir_exists(str(path.parent))
            
            if file_path.endswith('.json'):
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            elif file_path.endswith('.pkl'):
                with open(path, 'wb') as f:
                    pickle.dump(data, f)
            else:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(str(data))
            return True
        
        elif operation == 'delete':
            if path.exists():
                path.unlink()
            return True
        
        else:
            raise ValueError(f"不支持的操作类型: {operation}")
    
    except Exception as e:
        logger.error(f"文件操作失败: {operation} {file_path}, 错误: {e}")
        return None if operation == 'read' else False

def get_file_info(file_path: str) -> Optional[Dict[str, Any]]:
    """
    获取文件信息
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件信息字典
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return None
        
        stat = path.stat()
        return {
            'name': path.name,
            'size': stat.st_size,
            'created': stat.st_ctime,
            'modified': stat.st_mtime,
            'is_file': path.is_file(),
            'is_dir': path.is_dir(),
            'extension': path.suffix
        }
    except Exception as e:
        logger.error(f"获取文件信息失败: {file_path}, 错误: {e}")
        return None

def get_dir_size(dir_path: str) -> int:
    """
    获取目录大小
    
    Args:
        dir_path: 目录路径
        
    Returns:
        目录大小（字节）
    """
    try:
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(dir_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                if os.path.exists(file_path):
                    total_size += os.path.getsize(file_path)
        return total_size
    except Exception as e:
        logger.error(f"获取目录大小失败: {dir_path}, 错误: {e}")
        return 0

def clean_old_files(dir_path: str, days: int = 30) -> int:
    """
    清理旧文件
    
    Args:
        dir_path: 目录路径
        days: 保留天数
        
    Returns:
        删除的文件数量
    """
    try:
        import time
        current_time = time.time()
        cutoff_time = current_time - (days * 24 * 60 * 60)
        deleted_count = 0
        
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.getmtime(file_path) < cutoff_time:
                    os.remove(file_path)
                    deleted_count += 1
        
        return deleted_count
    except Exception as e:
        logger.error(f"清理旧文件失败: {dir_path}, 错误: {e}")
        return 0

def backup_file(file_path: str, backup_suffix: str = '.bak') -> bool:
    """
    备份文件
    
    Args:
        file_path: 原文件路径
        backup_suffix: 备份文件后缀
        
    Returns:
        是否备份成功
    """
    try:
        import shutil
        backup_path = file_path + backup_suffix
        shutil.copy2(file_path, backup_path)
        return True
    except Exception as e:
        logger.error(f"备份文件失败: {file_path}, 错误: {e}")
        return False

def compress_file(file_path: str, output_path: str = None) -> bool:
    """
    压缩文件
    
    Args:
        file_path: 原文件路径
        output_path: 输出路径（可选）
        
    Returns:
        是否压缩成功
    """
    try:
        import gzip
        import shutil
        
        if output_path is None:
            output_path = file_path + '.gz'
        
        with open(file_path, 'rb') as f_in:
            with gzip.open(output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        return True
    except Exception as e:
        logger.error(f"压缩文件失败: {file_path}, 错误: {e}")
        return False