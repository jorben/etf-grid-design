"""
版本配置模块
统一管理项目版本号
"""

# 项目主版本号
PROJECT_VERSION = "0.2.4"

# API版本号
API_VERSION = "v1"

# 前端版本号（与package.json同步）
FRONTEND_VERSION = "0.2.4"

# 后端版本号
BACKEND_VERSION = "0.2.4"

# 完整版本信息
def get_version_info():
    """获取完整的版本信息"""
    return {
        'project': PROJECT_VERSION,
        'api': API_VERSION,
        'frontend': FRONTEND_VERSION,
        'backend': BACKEND_VERSION
    }
