#!/usr/bin/env python3
"""
版本号统一更新工具

该脚本用于统一更新项目中的版本号配置，包括：
- backend/config/version.py
- pyproject.toml
- frontend/package.json

保持 PROJECT_VERSION、FRONTEND_VERSION、BACKEND_VERSION 一致，
API_VERSION 保持手动更新。
"""

import re
import sys
from pathlib import Path
from typing import Dict, Optional


class VersionUpdater:
    """版本号更新器"""
    
    def __init__(self, project_root: Optional[Path] = None):
        """初始化版本更新器
        
        Args:
            project_root: 项目根目录路径，默认为脚本所在目录的父目录
        """
        self.project_root = project_root or Path(__file__).parent.parent
        self.files_to_update = {
            'version_py': self.project_root / 'backend' / 'config' / 'version.py',
            'pyproject': self.project_root / 'pyproject.toml',
            'package_json': self.project_root / 'frontend' / 'package.json'
        }
    
    def validate_version(self, version: str) -> bool:
        """验证版本号格式是否符合语义化版本规范
        
        Args:
            version: 版本号字符串
            
        Returns:
            bool: 版本号格式是否正确
        """
        # 语义化版本号正则表达式：主版本号.次版本号.修订号
        pattern = r'^\d+\.\d+\.\d+$'
        return bool(re.match(pattern, version))
    
    def update_version_py(self, new_version: str) -> bool:
        """更新 backend/config/version.py 文件中的版本号
        
        Args:
            new_version: 新的版本号
            
        Returns:
            bool: 更新是否成功
        """
        version_file = self.files_to_update['version_py']
        
        try:
            with open(version_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 更新 PROJECT_VERSION、FRONTEND_VERSION、BACKEND_VERSION
            content = re.sub(
                r'PROJECT_VERSION = ".*?"',
                f'PROJECT_VERSION = "{new_version}"',
                content
            )
            content = re.sub(
                r'FRONTEND_VERSION = ".*?"',
                f'FRONTEND_VERSION = "{new_version}"',
                content
            )
            content = re.sub(
                r'BACKEND_VERSION = ".*?"',
                f'BACKEND_VERSION = "{new_version}"',
                content
            )
            
            with open(version_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
            
        except Exception as e:
            print(f"更新 version.py 失败: {e}")
            return False
    
    def update_pyproject_toml(self, new_version: str) -> bool:
        """更新 pyproject.toml 文件中的版本号
        
        Args:
            new_version: 新的版本号
            
        Returns:
            bool: 更新是否成功
        """
        pyproject_file = self.files_to_update['pyproject']
        
        try:
            with open(pyproject_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 更新 version = "x.x.x"
            content = re.sub(
                r'version = ".*?"',
                f'version = "{new_version}"',
                content
            )
            
            with open(pyproject_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
            
        except Exception as e:
            print(f"更新 pyproject.toml 失败: {e}")
            return False
    
    def update_package_json(self, new_version: str) -> bool:
        """更新 frontend/package.json 文件中的版本号
        
        Args:
            new_version: 新的版本号
            
        Returns:
            bool: 更新是否成功
        """
        package_file = self.files_to_update['package_json']
        
        try:
            with open(package_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 更新 "version": "x.x.x"
            content = re.sub(
                r'"version": ".*?"',
                f'"version": "{new_version}"',
                content
            )
            
            with open(package_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
            
        except Exception as e:
            print(f"更新 package.json 失败: {e}")
            return False
    
    def get_current_versions(self) -> Dict[str, str]:
        """获取当前各文件的版本号
        
        Returns:
            Dict[str, str]: 各文件中的版本号
        """
        versions = {}
        
        # 从 version.py 获取版本号
        try:
            version_file = self.files_to_update['version_py']
            with open(version_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            project_match = re.search(r'PROJECT_VERSION = "(.*?)"', content)
            frontend_match = re.search(r'FRONTEND_VERSION = "(.*?)"', content)
            backend_match = re.search(r'BACKEND_VERSION = "(.*?)"', content)
            api_match = re.search(r'API_VERSION = "(.*?)"', content)
            
            versions['version_py_project'] = project_match.group(1) if project_match else '未找到'
            versions['version_py_frontend'] = frontend_match.group(1) if frontend_match else '未找到'
            versions['version_py_backend'] = backend_match.group(1) if backend_match else '未找到'
            versions['version_py_api'] = api_match.group(1) if api_match else '未找到'
            
        except Exception as e:
            versions['version_py'] = f'读取失败: {e}'
        
        # 从 pyproject.toml 获取版本号
        try:
            pyproject_file = self.files_to_update['pyproject']
            with open(pyproject_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            match = re.search(r'version = "(.*?)"', content)
            versions['pyproject'] = match.group(1) if match else '未找到'
            
        except Exception as e:
            versions['pyproject'] = f'读取失败: {e}'
        
        # 从 package.json 获取版本号
        try:
            package_file = self.files_to_update['package_json']
            with open(package_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            match = re.search(r'"version": "(.*?)"', content)
            versions['package_json'] = match.group(1) if match else '未找到'
            
        except Exception as e:
            versions['package_json'] = f'读取失败: {e}'
        
        return versions
    
    def update_all_versions(self, new_version: str) -> Dict[str, bool]:
        """统一更新所有版本号
        
        Args:
            new_version: 新的版本号
            
        Returns:
            Dict[str, bool]: 各文件更新结果
        """
        if not self.validate_version(new_version):
            raise ValueError(f"版本号格式错误: {new_version}。请使用语义化版本号格式 (如: 1.2.3)")
        
        results = {}
        results['version_py'] = self.update_version_py(new_version)
        results['pyproject_toml'] = self.update_pyproject_toml(new_version)
        results['package_json'] = self.update_package_json(new_version)
        
        return results


def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("用法: python update_version.py <版本号>")
        print("示例: python update_version.py 1.2.3")
        print("\n当前版本号:")
        
        updater = VersionUpdater()
        versions = updater.get_current_versions()
        
        print(f"  version.py:")
        print(f"    PROJECT_VERSION: {versions.get('version_py_project', '未知')}")
        print(f"    FRONTEND_VERSION: {versions.get('version_py_frontend', '未知')}")
        print(f"    BACKEND_VERSION: {versions.get('version_py_backend', '未知')}")
        print(f"    API_VERSION: {versions.get('version_py_api', '未知')}")
        print(f"  pyproject.toml: {versions.get('pyproject', '未知')}")
        print(f"  package.json: {versions.get('package_json', '未知')}")
        
        sys.exit(1)
    
    new_version = sys.argv[1]
    
    try:
        updater = VersionUpdater()
        
        # 显示当前版本
        print("当前版本号:")
        versions = updater.get_current_versions()
        print(f"  version.py - PROJECT_VERSION: {versions.get('version_py_project', '未知')}")
        print(f"  version.py - FRONTEND_VERSION: {versions.get('version_py_frontend', '未知')}")
        print(f"  version.py - BACKEND_VERSION: {versions.get('version_py_backend', '未知')}")
        print(f"  pyproject.toml: {versions.get('pyproject', '未知')}")
        print(f"  package.json: {versions.get('package_json', '未知')}")
        
        # 确认更新
        response = input(f"\n是否要将所有版本号更新为 {new_version}? (y/N): ")
        if response.lower() != 'y':
            print("取消更新")
            sys.exit(0)
        
        # 执行更新
        print(f"\n正在更新版本号至 {new_version}...")
        results = updater.update_all_versions(new_version)
        
        # 显示结果
        print("\n更新结果:")
        for file_name, success in results.items():
            status = "✓ 成功" if success else "✗ 失败"
            print(f"  {file_name}: {status}")
        
        # 验证更新
        print(f"\n验证更新后的版本号:")
        updated_versions = updater.get_current_versions()
        print(f"  version.py - PROJECT_VERSION: {updated_versions.get('version_py_project', '未知')}")
        print(f"  version.py - FRONTEND_VERSION: {updated_versions.get('version_py_frontend', '未知')}")
        print(f"  version.py - BACKEND_VERSION: {updated_versions.get('version_py_backend', '未知')}")
        print(f"  pyproject.toml: {updated_versions.get('pyproject', '未知')}")
        print(f"  package.json: {updated_versions.get('package_json', '未知')}")
        
        # 检查是否所有更新都成功
        all_success = all(results.values())
        if all_success:
            print(f"\n✓ 所有版本号已成功更新至 {new_version}")
        else:
            print(f"\n✗ 部分文件更新失败，请检查错误信息")
            sys.exit(1)
            
    except ValueError as e:
        print(f"错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"发生未知错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
