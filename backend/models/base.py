"""
基础模型类
定义所有数据模型的基类和通用功能
"""

from typing import Any, Dict, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, validator
import uuid


class BaseETFModel(BaseModel):
    """ETF模型基类"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="唯一标识")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")
    version: str = Field(default="1.0", description="模型版本")
    
    class Config:
        """Pydantic配置"""
        validate_assignment = True
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        allow_population_by_field_name = True
    
    def update_timestamp(self) -> None:
        """更新时间戳"""
        self.updated_at = datetime.now()
    
    def to_dict(self, exclude_none: bool = True, **kwargs) -> Dict[str, Any]:
        """转换为字典"""
        if exclude_none:
            return self.dict(exclude_none=True, **kwargs)
        return self.dict(**kwargs)
    
    def to_json(self, **kwargs) -> str:
        """转换为JSON字符串"""
        return self.json(**kwargs)


class PaginatedResponse(BaseModel):
    """分页响应模型"""
    
    items: List[Any] = Field(..., description="数据项列表")
    total: int = Field(..., description="总数量")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页大小")
    total_pages: int = Field(..., description="总页数")
    has_next: bool = Field(..., description="是否有下一页")
    has_prev: bool = Field(..., description="是否有上一页")
    
    @classmethod
    def create(
        cls, 
        items: List[Any], 
        total: int, 
        page: int, 
        page_size: int
    ) -> 'PaginatedResponse':
        """创建分页响应"""
        total_pages = (total + page_size - 1) // page_size
        has_next = page < total_pages
        has_prev = page > 1
        
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=has_next,
            has_prev=has_prev
        )


class ErrorResponse(BaseModel):
    """错误响应模型"""
    
    error_code: int = Field(..., description="错误码")
    error_message: str = Field(..., description="错误消息")
    detail: Optional[str] = Field(None, description="详细错误信息")
    timestamp: datetime = Field(default_factory=datetime.now, description="错误时间")
    request_id: Optional[str] = Field(None, description="请求ID")
    
    @classmethod
    def from_exception(
        cls, 
        error_code: int, 
        error_message: str, 
        detail: Optional[str] = None,
        request_id: Optional[str] = None
    ) -> 'ErrorResponse':
        """从异常创建错误响应"""
        return cls(
            error_code=error_code,
            error_message=error_message,
            detail=detail,
            request_id=request_id
        )


class SuccessResponse(BaseModel):
    """成功响应模型"""
    
    success: bool = Field(default=True, description="是否成功")
    message: str = Field(..., description="成功消息")
    data: Optional[Any] = Field(None, description="响应数据")
    timestamp: datetime = Field(default_factory=datetime.now, description="响应时间")
    request_id: Optional[str] = Field(None, description="请求ID")
    
    @classmethod
    def create(
        cls, 
        message: str, 
        data: Optional[Any] = None,
        request_id: Optional[str] = None
    ) -> 'SuccessResponse':
        """创建成功响应"""
        return cls(
            message=message,
            data=data,
            request_id=request_id
        )


class ValidationErrorDetail(BaseModel):
    """验证错误详情"""
    
    field: str = Field(..., description="字段名")
    message: str = Field(..., description="错误消息")
    value: Optional[Any] = Field(None, description="错误值")
    type: str = Field(..., description="错误类型")


class ValidationErrorResponse(BaseModel):
    """验证错误响应"""
    
    error_code: int = Field(..., description="错误码")
    error_message: str = Field(..., description="错误消息")
    validation_errors: List[ValidationErrorDetail] = Field(..., description="验证错误详情")
    timestamp: datetime = Field(default_factory=datetime.now, description="错误时间")
    
    @classmethod
    def from_validation_errors(
        cls, 
        validation_errors: List[Dict[str, Any]]
    ) -> 'ValidationErrorResponse':
        """从验证错误创建响应"""
        details = []
        for error in validation_errors:
            details.append(ValidationErrorDetail(
                field=error.get('field', 'unknown'),
                message=error.get('message', 'Validation error'),
                value=error.get('value'),
                type=error.get('type', 'validation')
            ))
        
        return cls(
            error_code=400,
            error_message="数据验证失败",
            validation_errors=details
        )


class HealthCheckResponse(BaseModel):
    """健康检查响应"""
    
    status: str = Field(..., description="状态")
    timestamp: datetime = Field(default_factory=datetime.now, description="检查时间")
    version: str = Field(..., description="应用版本")
    uptime: float = Field(..., description="运行时间（秒）")
    dependencies: Dict[str, str] = Field(..., description="依赖服务状态")
    
    @classmethod
    def create(
        cls, 
        status: str, 
        version: str, 
        uptime: float, 
        dependencies: Dict[str, str]
    ) -> 'HealthCheckResponse':
        """创建健康检查响应"""
        return cls(
            status=status,
            version=version,
            uptime=uptime,
            dependencies=dependencies
        )


class PerformanceMetrics(BaseModel):
    """性能指标模型"""
    
    request_count: int = Field(..., description="请求数量")
    average_response_time: float = Field(..., description="平均响应时间")
    error_rate: float = Field(..., description="错误率")
    throughput: float = Field(..., description="吞吐量")
    timestamp: datetime = Field(default_factory=datetime.now, description="统计时间")
    
    @validator('error_rate')
    def validate_error_rate(cls, v):
        """验证错误率"""
        if v < 0 or v > 1:
            raise ValueError("错误率必须在0-1之间")
        return v


class CacheMetrics(BaseModel):
    """缓存指标模型"""
    
    cache_hits: int = Field(..., description="缓存命中数")
    cache_misses: int = Field(..., description="缓存未命中数")
    cache_size: int = Field(..., description="缓存大小")
    hit_rate: float = Field(..., description="命中率")
    timestamp: datetime = Field(default_factory=datetime.now, description="统计时间")
    
    @validator('hit_rate')
    def validate_hit_rate(cls, v):
        """验证命中率"""
        if v < 0 or v > 1:
            raise ValueError("命中率必须在0-1之间")
        return v
