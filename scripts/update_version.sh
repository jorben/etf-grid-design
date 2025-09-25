#!/bin/bash
# 版本号统一更新工具
#
# 该脚本用于统一更新项目中的版本号配置，包括：
# - backend/config/version.py
# - pyproject.toml
# - frontend/package.json
#
# 保持 PROJECT_VERSION、FRONTEND_VERSION、BACKEND_VERSION 一致，
# API_VERSION 保持手动更新。

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# 文件路径
VERSION_PY="$PROJECT_ROOT/backend/config/version.py"
PYPROJECT_TOML="$PROJECT_ROOT/pyproject.toml"
PACKAGE_JSON="$PROJECT_ROOT/frontend/package.json"

# 验证版本号格式
validate_version() {
    local version="$1"
    if [[ ! "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo -e "${RED}错误: 版本号格式错误: $version${NC}"
        echo "请使用语义化版本号格式 (如: 1.2.3)"
        return 1
    fi
    return 0
}

# 获取当前版本号
get_current_versions() {
    echo -e "${YELLOW}当前版本号:${NC}"
    
    # 从 version.py 获取版本号
    if [[ -f "$VERSION_PY" ]]; then
        local project_version=$(grep 'PROJECT_VERSION.*=' "$VERSION_PY" | sed -E 's/.*PROJECT_VERSION[^"]*"([^"]+)".*/\1/' 2>/dev/null || echo "未找到")
        local frontend_version=$(grep 'FRONTEND_VERSION.*=' "$VERSION_PY" | sed -E 's/.*FRONTEND_VERSION[^"]*"([^"]+)".*/\1/' 2>/dev/null || echo "未找到")
        local backend_version=$(grep 'BACKEND_VERSION.*=' "$VERSION_PY" | sed -E 's/.*BACKEND_VERSION[^"]*"([^"]+)".*/\1/' 2>/dev/null || echo "未找到")
        local api_version=$(grep 'API_VERSION.*=' "$VERSION_PY" | sed -E 's/.*API_VERSION[^"]*"([^"]+)".*/\1/' 2>/dev/null || echo "未找到")
        
        echo "  version.py:"
        echo "    PROJECT_VERSION: $project_version"
        echo "    FRONTEND_VERSION: $frontend_version"
        echo "    BACKEND_VERSION: $backend_version"
        echo "    API_VERSION: $api_version"
    else
        echo "  version.py: 文件不存在"
    fi
    
    # 从 pyproject.toml 获取版本号
    if [[ -f "$PYPROJECT_TOML" ]]; then
        local pyproject_version=$(grep '^version.*=' "$PYPROJECT_TOML" | sed -E 's/.*version[^"]*"([^"]+)".*/\1/' 2>/dev/null || echo "未找到")
        echo "  pyproject.toml: $pyproject_version"
    else
        echo "  pyproject.toml: 文件不存在"
    fi
    
    # 从 package.json 获取版本号
    if [[ -f "$PACKAGE_JSON" ]]; then
        local package_version=$(grep '"version".*:' "$PACKAGE_JSON" | sed -E 's/.*"version"[^"]*"([^"]+)".*/\1/' 2>/dev/null || echo "未找到")
        echo "  package.json: $package_version"
    else
        echo "  package.json: 文件不存在"
    fi
}

# 更新 version.py 文件
update_version_py() {
    local new_version="$1"
    echo -e "${YELLOW}正在更新 version.py...${NC}"
    
    if [[ ! -f "$VERSION_PY" ]]; then
        echo -e "${RED}错误: version.py 文件不存在: $VERSION_PY${NC}"
        return 1
    fi
    
    # 备份原文件
    cp "$VERSION_PY" "${VERSION_PY}.bak"
    
    # 更新 PROJECT_VERSION、FRONTEND_VERSION、BACKEND_VERSION
    sed -i.bak -E 's/PROJECT_VERSION = "[0-9]+\.[0-9]+\.[0-9]+"/PROJECT_VERSION = "'"$new_version"'"/g' "$VERSION_PY"
    sed -i.bak -E 's/FRONTEND_VERSION = "[0-9]+\.[0-9]+\.[0-9]+"/FRONTEND_VERSION = "'"$new_version"'"/g' "$VERSION_PY"
    sed -i.bak -E 's/BACKEND_VERSION = "[0-9]+\.[0-9]+\.[0-9]+"/BACKEND_VERSION = "'"$new_version"'"/g' "$VERSION_PY"
    
    # 清理备份文件
    rm -f "${VERSION_PY}.bak"
    
    echo -e "${GREEN}✓ version.py 更新成功${NC}"
    return 0
}

# 更新 pyproject.toml 文件
update_pyproject_toml() {
    local new_version="$1"
    echo -e "${YELLOW}正在更新 pyproject.toml...${NC}"
    
    if [[ ! -f "$PYPROJECT_TOML" ]]; then
        echo -e "${RED}错误: pyproject.toml 文件不存在: $PYPROJECT_TOML${NC}"
        return 1
    fi
    
    # 备份原文件
    cp "$PYPROJECT_TOML" "${PYPROJECT_TOML}.bak"
    
    # 更新 version = "x.x.x"
    sed -i.bak -E 's/^version = "[0-9]+\.[0-9]+\.[0-9]+"/version = "'"$new_version"'"/g' "$PYPROJECT_TOML"
    
    # 清理备份文件
    rm -f "${PYPROJECT_TOML}.bak"
    
    echo -e "${GREEN}✓ pyproject.toml 更新成功${NC}"
    return 0
}

# 更新 package.json 文件
update_package_json() {
    local new_version="$1"
    echo -e "${YELLOW}正在更新 package.json...${NC}"
    
    if [[ ! -f "$PACKAGE_JSON" ]]; then
        echo -e "${RED}错误: package.json 文件不存在: $PACKAGE_JSON${NC}"
        return 1
    fi
    
    # 备份原文件
    cp "$PACKAGE_JSON" "${PACKAGE_JSON}.bak"
    
    # 更新 "version": "x.x.x"
    sed -i.bak -E 's/"version": "[0-9]+\.[0-9]+\.[0-9]+"/"version": "'"$new_version"'"/g' "$PACKAGE_JSON"
    
    # 清理备份文件
    rm -f "${PACKAGE_JSON}.bak"
    
    echo -e "${GREEN}✓ package.json 更新成功${NC}"
    return 0
}

# 执行后续命令
execute_post_update_commands() {
    echo -e "${YELLOW}正在执行后续更新命令...${NC}"
    
    # 在项目根目录执行命令
    echo -e "${YELLOW}执行: uv sync${NC}"
    if ! uv sync; then
        echo -e "${RED}错误: uv sync 执行失败${NC}"
        return 1
    fi
    
    echo -e "${YELLOW}执行: uv pip compile pyproject.toml --no-deps -o requirements.txt${NC}"
    if ! uv pip compile pyproject.toml --no-deps -o requirements.txt; then
        echo -e "${RED}错误: uv pip compile 执行失败${NC}"
        return 1
    fi
    
    # 在 frontend 目录执行命令
    echo -e "${YELLOW}执行: cd frontend && npm install${NC}"
    if ! (cd frontend && npm install); then
        echo -e "${RED}错误: npm install 执行失败${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✓ 所有后续命令执行成功${NC}"
    return 0
}

# 显示帮助信息
show_help() {
    echo "用法: $0 <版本号>"
    echo "示例: $0 1.2.3"
    echo ""
    echo "选项:"
    echo "  -h, --help    显示此帮助信息"
    echo "  -c, --current 显示当前版本号"
}

# 主函数
main() {
    # 解析命令行参数
    case "${1:-}" in
        -h|--help)
            show_help
            exit 0
            ;;
        -c|--current)
            get_current_versions
            exit 0
            ;;
        "")
            echo -e "${RED}错误: 请提供版本号${NC}"
            show_help
            exit 1
            ;;
    esac
    
    local new_version="$1"
    
    # 验证版本号格式
    if ! validate_version "$new_version"; then
        exit 1
    fi
    
    # 显示当前版本
    get_current_versions
    
    # 确认更新
    echo ""
    read -p "是否要将所有版本号更新为 $new_version? (y/N): " -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "取消更新"
        exit 0
    fi
    
    # 执行更新
    echo -e "\n${YELLOW}正在更新版本号至 $new_version...${NC}"
    
    local failed=0
    
    # 更新各个文件
    if ! update_version_py "$new_version"; then
        failed=1
    fi
    
    if ! update_pyproject_toml "$new_version"; then
        failed=1
    fi
    
    if ! update_package_json "$new_version"; then
        failed=1
    fi
    
    # 如果有任何更新失败，退出
    if [[ $failed -ne 0 ]]; then
        echo -e "${RED}✗ 部分文件更新失败${NC}"
        exit 1
    fi
    
    # 执行后续命令
    if ! execute_post_update_commands; then
        echo -e "${RED}✗ 后续命令执行失败${NC}"
        exit 1
    fi
    
    # 验证更新结果
    echo -e "\n${YELLOW}验证更新后的版本号:${NC}"
    get_current_versions
    
    echo -e "\n${GREEN}✓ 所有版本号已成功更新至 $new_version${NC}"
    echo -e "${GREEN}✓ 所有后续命令执行完成${NC}"
}

# 运行主函数
main "$@"
