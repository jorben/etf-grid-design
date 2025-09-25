"""
API数据模型定义
包含请求参数验证和响应格式定义
"""

from typing import Dict, Any, Optional, List
from datetime import datetime

class BaseResponse:
    """基础响应模型"""
    
    @staticmethod
    def success(data: Any = None, message: str = "操作成功") -> Dict[str, Any]:
        """成功响应"""
        return {
            'success': True,
            'data': data,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def error(message: str, error_code: int = 500, details: Optional[Dict] = None) -> Dict[str, Any]:
        """错误响应"""
        response = {
            'success': False,
            'error': message,
            'error_code': error_code,
            'timestamp': datetime.now().isoformat()
        }
        if details:
            response['details'] = details
        return response

class ETFRequestSchemas:
    """ETF相关请求参数验证"""
    
    @staticmethod
    def validate_etf_code(etf_code: str) -> bool:
        """验证ETF代码格式"""
        return etf_code and len(etf_code) == 6 and etf_code.isdigit()
    
    @staticmethod
    def validate_capital_amount(amount: float) -> bool:
        """验证投资金额范围"""
        return 100000 <= amount <= 5000000
    
    @staticmethod
    def validate_grid_type(grid_type: str) -> bool:
        """验证网格类型"""
        return grid_type in ['等差', '等比']
    
    @staticmethod
    def validate_risk_preference(risk_preference: str) -> bool:
        """验证风险偏好"""
        return risk_preference in ['保守', '稳健', '激进']

class AnalysisRequest:
    """分析请求参数模型"""
    
    def __init__(self, data: Dict[str, Any]):
        self.etf_code = data.get('etfCode', '').strip()
        self.total_capital = float(data.get('totalCapital', 0))
        self.grid_type = data.get('gridType', '')
        self.risk_preference = data.get('riskPreference', '')
    
    def validate(self) -> Optional[Dict[str, Any]]:
        """验证请求参数"""
        errors = []
        
        if not ETFRequestSchemas.validate_etf_code(self.etf_code):
            errors.append('ETF代码格式错误，请输入6位数字')
        
        if not ETFRequestSchemas.validate_capital_amount(self.total_capital):
            errors.append('投资金额应在10万-500万之间')
        
        if not ETFRequestSchemas.validate_grid_type(self.grid_type):
            errors.append('网格类型只能是"等差"或"等比"')
        
        if not ETFRequestSchemas.validate_risk_preference(self.risk_preference):
            errors.append('风险偏好只能是"保守"、"稳健"或"激进"')
        
        if errors:
            return {'errors': errors}
        return None

class HealthResponse:
    """健康检查响应模型"""
    
    @staticmethod
    def get_response(environment: str = 'development') -> Dict[str, Any]:
        """获取健康检查响应"""
        # 导入版本信息
        from config import PROJECT_VERSION
        return {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'ETF Grid Trading Analysis System',
            'version': PROJECT_VERSION,
            'environment': environment
        }

class CapitalPreset:
    """资金预设模型"""
    
    def __init__(self, value: int, label: str, popular: bool = False):
        self.value = value
        self.label = label
        self.popular = popular
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'value': self.value,
            'label': self.label,
            'popular': self.popular
        }
    
    @staticmethod
    def get_default_presets() -> List[Dict[str, Any]]:
        """获取默认资金预设列表"""
        presets = [
            CapitalPreset(100000, '10万', True),
            CapitalPreset(200000, '20万', True),
            CapitalPreset(300000, '30万', False),
            CapitalPreset(500000, '50万', True),
            CapitalPreset(800000, '80万', False),
            CapitalPreset(1000000, '100万', True),
            CapitalPreset(1500000, '150万', False),
            CapitalPreset(2000000, '200万', False)
        ]
        return [preset.to_dict() for preset in presets]
