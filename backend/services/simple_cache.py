import os
import json
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class SimpleCache:
    """简单的文件缓存管理器"""
    
    def __init__(self, cache_dir: str = "cache"):
        """
        初始化缓存管理器
        
        Args:
            cache_dir: 缓存目录路径
        """
        self.cache_dir = cache_dir
        # 确保缓存目录存在
        os.makedirs(cache_dir, exist_ok=True)
        logger.info(f"缓存管理器初始化完成，缓存目录: {cache_dir}")
    
    def _generate_cache_key(self, method_name: str, **params) -> str:
        """
        根据方法名和参数生成缓存键
        
        Args:
            method_name: 方法名
            **params: 参数字典
            
        Returns:
            str: 缓存键
        """
        # 将参数按键排序后拼接
        param_str = "_".join([f"{k}_{v}" for k, v in sorted(params.items())])
        return f"{method_name}_{param_str}"
    
    def get(self, method_name: str, **params) -> Optional[Any]:
        """
        获取缓存数据
        
        Args:
            method_name: 方法名
            **params: 参数字典
            
        Returns:
            缓存的数据，如果不存在返回None
        """
        cache_key = self._generate_cache_key(method_name, **params)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.debug(f"缓存命中: {cache_key}")
                    return data
            except Exception as e:
                # 缓存文件损坏，删除并返回None
                logger.warning(f"缓存文件损坏，已删除: {cache_file}, 错误: {e}")
                try:
                    os.remove(cache_file)
                except:
                    pass
        
        return None
    
    def set(self, method_name: str, data: Any, **params):
        """
        保存缓存数据
        
        Args:
            method_name: 方法名
            data: 要缓存的数据
            **params: 参数字典
        """
        # 只有数据不为空才缓存
        if not data:
            logger.debug(f"数据为空，不缓存: {method_name}")
            return
        
        cache_key = self._generate_cache_key(method_name, **params)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            logger.debug(f"缓存保存成功: {cache_key}")
        except Exception as e:
            logger.error(f"缓存保存失败: {cache_file}, 错误: {e}")
    
    def clear(self, method_name: str = None, **params):
        """
        清理缓存
        
        Args:
            method_name: 方法名，如果为None则清理所有缓存
            **params: 参数字典
        """
        if method_name is None:
            # 清理所有缓存
            try:
                for file in os.listdir(self.cache_dir):
                    if file.endswith('.json'):
                        os.remove(os.path.join(self.cache_dir, file))
                logger.info("所有缓存已清理")
            except Exception as e:
                logger.error(f"清理缓存失败: {e}")
        else:
            # 清理特定缓存
            cache_key = self._generate_cache_key(method_name, **params)
            cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
            try:
                if os.path.exists(cache_file):
                    os.remove(cache_file)
                    logger.info(f"缓存已清理: {cache_key}")
            except Exception as e:
                logger.error(f"清理缓存失败: {cache_file}, 错误: {e}")
    
    def get_cache_info(self) -> dict:
        """
        获取缓存信息
        
        Returns:
            dict: 缓存统计信息
        """
        try:
            files = [f for f in os.listdir(self.cache_dir) if f.endswith('.json')]
            total_size = 0
            for file in files:
                file_path = os.path.join(self.cache_dir, file)
                total_size += os.path.getsize(file_path)
            
            return {
                'cache_dir': self.cache_dir,
                'file_count': len(files),
                'total_size_mb': round(total_size / 1024 / 1024, 2),
                'files': files
            }
        except Exception as e:
            logger.error(f"获取缓存信息失败: {e}")
            return {
                'cache_dir': self.cache_dir,
                'file_count': 0,
                'total_size_mb': 0,
                'files': [],
                'error': str(e)
            }