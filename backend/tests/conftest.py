"""
pytest配置文件
定义测试配置、fixture和插件
"""

import pytest
import asyncio
import tempfile
import shutil
import os
import sys
from pathlib import Path
from typing import Generator, Any, Dict

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.config import TestingSettings, get_settings
from backend.utils.exceptions import exception_factory


@pytest.fixture(scope="session")
def test_settings() -> TestingSettings:
    """测试环境配置"""
    # 设置测试环境
    os.environ["ENVIRONMENT"] = "testing"
    return get_settings()


@pytest.fixture(scope="session")
def event_loop():
    """为异步测试创建事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir() -> Generator[str, None, None]:
    """临时目录fixture"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # 清理临时目录
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@pytest.fixture
def sample_etf_data() -> Dict[str, Any]:
    """示例ETF数据"""
    return {
        "code": "510300",
        "name": "沪深300ETF",
        "current_price": 3.85,
        "change_pct": 0.52,
        "volume": 15000000,
        "amount": 57750000.0,
        "setup_date": "2012-05-28",
        "list_date": "2012-05-28",
        "fund_type": "ETF",
        "status": "L",
        "trade_date": "2024-01-15",
        "data_age_days": 1
    }


@pytest.fixture
def sample_price_data() -> Dict[str, Any]:
    """示例价格数据"""
    return {
        "date": "2024-01-15",
        "open": 3.82,
        "high": 3.87,
        "low": 3.80,
        "close": 3.85,
        "volume": 15000000,
        "amount": 57750000.0
    }


@pytest.fixture
def sample_analysis_input() -> Dict[str, Any]:
    """示例分析输入参数"""
    return {
        "etf_code": "510300",
        "total_capital": 1000000.0,
        "grid_type": "等差",
        "risk_preference": "稳健",
        "analysis_days": 365
    }


@pytest.fixture
def mock_tushare_client():
    """模拟Tushare客户端"""
    class MockTushareClient:
        def __init__(self):
            self.calls = []
        
        async def get_etf_basic_info(self, etf_code: str):
            self.calls.append(("get_etf_basic_info", etf_code))
            return {
                "code": etf_code,
                "name": f"模拟ETF{etf_code}",
                "current_price": 3.85,
                "change_pct": 0.52,
                "volume": 15000000,
                "amount": 57750000.0
            }
        
        async def get_etf_daily_data(self, etf_code: str, start_date: str, end_date: str):
            self.calls.append(("get_etf_daily_data", etf_code, start_date, end_date))
            # 返回模拟数据
            return [
                {
                    "date": "2024-01-15",
                    "open": 3.82,
                    "high": 3.87,
                    "low": 3.80,
                    "close": 3.85,
                    "volume": 15000000,
                    "amount": 57750000.0
                }
            ]
    
    return MockTushareClient()


@pytest.fixture
def mock_cache_service():
    """模拟缓存服务"""
    class MockCacheService:
        def __init__(self):
            self.cache = {}
            self.calls = []
        
        async def get(self, key: str):
            self.calls.append(("get", key))
            return self.cache.get(key)
        
        async def set(self, key: str, value: Any, ttl: int = 3600):
            self.calls.append(("set", key, value, ttl))
            self.cache[key] = value
        
        async def delete(self, key: str):
            self.calls.append(("delete", key))
            if key in self.cache:
                del self.cache[key]
    
    return MockCacheService()


class MockResponse:
    """模拟HTTP响应"""
    
    def __init__(self, json_data: Dict[str, Any], status_code: int = 200):
        self.json_data = json_data
        self.status_code = status_code
    
    def json(self):
        return self.json_data
    
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP Error: {self.status_code}")


@pytest.fixture
def mock_requests():
    """模拟requests库"""
    class MockRequests:
        def __init__(self):
            self.responses = {}
            self.requests = []
        
        def set_response(self, url: str, response: MockResponse):
            self.responses[url] = response
        
        def get(self, url: str, **kwargs):
            self.requests.append(("GET", url, kwargs))
            return self.responses.get(url, MockResponse({}, 404))
        
        def post(self, url: str, **kwargs):
            self.requests.append(("POST", url, kwargs))
            return self.responses.get(url, MockResponse({}, 404))
    
    return MockRequests()


def pytest_configure(config):
    """pytest配置钩子"""
    # 注册自定义标记
    config.addinivalue_line(
        "markers", "slow: 标记为慢速测试，需要较长时间运行"
    )
    config.addinivalue_line(
        "markers", "integration: 标记为集成测试，需要外部依赖"
    )
    config.addinivalue_line(
        "markers", "unit: 标记为单元测试，不依赖外部服务"
    )
    config.addinivalue_line(
        "markers", "performance: 标记为性能测试"
    )


def pytest_collection_modifyitems(config, items):
    """修改测试项集合"""
    # 如果没有指定标记，默认运行单元测试
    if not any(marker in config.option.markexpr for marker in ['slow', 'integration', 'performance']):
        for item in items:
            if 'slow' in item.keywords or 'integration' in item.keywords or 'performance' in item.keywords:
                item.add_marker(pytest.mark.skip(reason="默认跳过慢速/集成/性能测试"))


@pytest.fixture(autouse=True)
def setup_test_environment():
    """自动设置测试环境"""
    # 设置测试环境变量
    original_env = os.environ.get("ENVIRONMENT")
    os.environ["ENVIRONMENT"] = "testing"
    
    yield
    
    # 恢复原始环境
    if original_env:
        os.environ["ENVIRONMENT"] = original_env
    else:
        os.environ.pop("ENVIRONMENT", None)


class AssertionHelpers:
    """断言辅助类"""
    
    @staticmethod
    def assert_dict_contains(subset: Dict[str, Any], fullset: Dict[str, Any]):
        """断言字典包含关系"""
        for key, value in subset.items():
            assert key in fullset, f"键 '{key}' 不存在于字典中"
            assert fullset[key] == value, f"键 '{key}' 的值不匹配: {fullset[key]} != {value}"
    
    @staticmethod
    def assert_approx_equal(actual: float, expected: float, tolerance: float = 1e-6):
        """断言近似相等"""
        assert abs(actual - expected) <= tolerance, f"{actual} 与 {expected} 的差值超过容差 {tolerance}"
    
    @staticmethod
    def assert_exception_raised(exception_type, callable_obj, *args, **kwargs):
        """断言抛出指定异常"""
        with pytest.raises(exception_type):
            callable_obj(*args, **kwargs)


@pytest.fixture
def assertion_helpers():
    """断言辅助工具fixture"""
    return AssertionHelpers()


# 自定义pytest插件
def pytest_report_teststatus(report, config):
    """自定义测试状态报告"""
    if report.when == "call":
        if report.passed:
            return "PASS", "✓", "PASSED"
        elif report.failed:
            return "FAIL", "✗", "FAILED"
        elif report.skipped:
            return "SKIP", "⏭", "SKIPPED"
    
    return None
