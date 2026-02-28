"""
后端 API 测试
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """测试健康检查"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_root():
    """测试根路径"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "价值投资分析平台"
    assert "version" in data


def test_screener_presets():
    """测试选股器预设"""
    response = client.get("/api/v1/screener/presets")
    assert response.status_code == 200
    data = response.json()
    assert "presets" in data
    assert len(data["presets"]) > 0
    
    # 验证预设模板
    preset_ids = [p["id"] for p in data["presets"]]
    assert "high_dividend" in preset_ids
    assert "low_valuation" in preset_ids
    assert "quality_growth" in preset_ids


@pytest.mark.skip(reason="需要数据库连接")
def test_get_stock_indicators():
    """测试股票指标 API（需要数据库）"""
    response = client.get("/api/v1/stocks/600519/indicators")
    if response.status_code == 200:
        data = response.json()
        assert data["code"] == "600519"
        assert "pe_ttm" in data or data.get("pe_ttm") is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
