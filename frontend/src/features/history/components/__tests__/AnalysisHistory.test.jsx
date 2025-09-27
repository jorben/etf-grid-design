import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import AnalysisHistory from '../AnalysisHistory';

// Mock localStorage
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: jest.fn((key) => store[key] || null),
    setItem: jest.fn((key, value) => {
      store[key] = value.toString();
    }),
    removeItem: jest.fn((key) => {
      delete store[key];
    }),
    clear: jest.fn(() => {
      store = {};
    }),
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

// Mock useNavigate
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

describe('AnalysisHistory Component', () => {
  beforeEach(() => {
    localStorageMock.clear();
    mockNavigate.mockClear();
  });

  const mockHistoryData = [
    {
      etfCode: '510300',
      params: {
        totalCapital: 100000,
        gridType: '等比',
        riskPreference: '均衡',
        adjustmentCoefficient: 1.0,
      },
      timestamp: Date.now(),
      url: '/analysis/510300?capital=100000&grid=geometric&risk=balanced&adjustment=1.0',
    },
    {
      etfCode: '510500',
      params: {
        totalCapital: 200000,
        gridType: '等差',
        riskPreference: '高频',
        adjustmentCoefficient: 1.5,
      },
      timestamp: Date.now() - 3600000, // 1小时前
      url: '/analysis/510500?capital=200000&grid=arithmetic&risk=aggressive&adjustment=1.5',
    },
  ];

  const mockOldHistoryData = [
    {
      etfCode: '159915',
      params: {
        totalCapital: 150000,
        gridType: '等比',
        riskPreference: '低频',
        // 缺少 adjustmentCoefficient 字段
      },
      timestamp: Date.now() - 86400000, // 1天前
      url: '/analysis/159915?capital=150000&grid=geometric&risk=conservative',
    },
  ];

  const renderWithRouter = (component) => {
    return render(<BrowserRouter>{component}</BrowserRouter>);
  };

  test('应该正确显示历史记录，包含调节系数信息', async () => {
    localStorageMock.setItem('analysisHistory', JSON.stringify(mockHistoryData));

    renderWithRouter(<AnalysisHistory />);

    // 等待历史记录加载
    await waitFor(() => {
      expect(screen.getByText('分析历史')).toBeInTheDocument();
    });

    // 点击展开历史记录
    fireEvent.click(screen.getByText('分析历史'));

    // 验证历史记录内容
    expect(screen.getByText('ETF 510300')).toBeInTheDocument();
    expect(screen.getByText('资金: 100,000元')).toBeInTheDocument();
    expect(screen.getByText('等比')).toBeInTheDocument();
    expect(screen.getByText('均衡')).toBeInTheDocument();
    expect(screen.getByText('调节: 1')).toBeInTheDocument(); // 1.0 显示为 1

    expect(screen.getByText('ETF 510500')).toBeInTheDocument();
    expect(screen.getByText('资金: 200,000元')).toBeInTheDocument();
    expect(screen.getByText('等差')).toBeInTheDocument();
    expect(screen.getByText('高频')).toBeInTheDocument();
    expect(screen.getByText('调节: 1.5')).toBeInTheDocument();
  });

  test('应该正确处理旧历史记录的兼容性', async () => {
    localStorageMock.setItem('analysisHistory', JSON.stringify(mockOldHistoryData));

    renderWithRouter(<AnalysisHistory />);

    // 等待历史记录加载
    await waitFor(() => {
      expect(screen.getByText('分析历史')).toBeInTheDocument();
    });

    // 点击展开历史记录
    fireEvent.click(screen.getByText('分析历史'));

    // 验证旧记录被正确处理，显示默认调节系数
    expect(screen.getByText('ETF 159915')).toBeInTheDocument();
    expect(screen.getByText('调节: 1')).toBeInTheDocument(); // 默认值 1.0
  });

  test('点击历史记录应该正确跳转，包含调节系数参数', async () => {
    localStorageMock.setItem('analysisHistory', JSON.stringify(mockHistoryData));

    renderWithRouter(<AnalysisHistory />);

    // 等待历史记录加载并展开
    await waitFor(() => {
      expect(screen.getByText('分析历史')).toBeInTheDocument();
    });
    fireEvent.click(screen.getByText('分析历史'));

    // 点击第一条历史记录
    const firstRecord = screen.getByText('ETF 510300').closest('div[class*="bg-gray-50"]');
    fireEvent.click(firstRecord);

    // 验证跳转URL包含调节系数参数
    expect(mockNavigate).toHaveBeenCalledWith(
      '/analysis/510300?capital=100000&grid=geometric&risk=balanced&adjustment=1.0'
    );
  });

  test('应该正确处理旧记录的跳转，使用默认调节系数', async () => {
    localStorageMock.setItem('analysisHistory', JSON.stringify(mockOldHistoryData));

    renderWithRouter(<AnalysisHistory />);

    // 等待历史记录加载并展开
    await waitFor(() => {
      expect(screen.getByText('分析历史')).toBeInTheDocument();
    });
    fireEvent.click(screen.getByText('分析历史'));

    // 点击旧记录
    const oldRecord = screen.getByText('ETF 159915').closest('div[class*="bg-gray-50"]');
    fireEvent.click(oldRecord);

    // 验证跳转URL包含默认调节系数参数
    expect(mockNavigate).toHaveBeenCalledWith(
      '/analysis/159915?capital=150000&grid=geometric&risk=conservative&adjustment=1.0'
    );
  });

  test('没有历史记录时不应该显示组件', async () => {
    localStorageMock.setItem('analysisHistory', JSON.stringify([]));

    const { container } = renderWithRouter(<AnalysisHistory />);

    // 等待组件渲染
    await waitFor(() => {
      // 组件应该返回 null，所以容器应该是空的
      expect(container.firstChild).toBeNull();
    });
  });

  test('应该正确处理无效的历史记录数据', async () => {
    const invalidData = [
      {
        // 缺少必需字段
        params: {
          totalCapital: 100000,
        },
        timestamp: Date.now(),
      },
    ];

    localStorageMock.setItem('analysisHistory', JSON.stringify(invalidData));

    renderWithRouter(<AnalysisHistory />);

    // 等待组件渲染
    await waitFor(() => {
      // 无效记录应该被过滤掉，组件应该返回 null
      expect(screen.queryByText('分析历史')).not.toBeInTheDocument();
    });
  });
});