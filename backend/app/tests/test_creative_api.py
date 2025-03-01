from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_generate_product_pdf():
    response = client.post(
        "/api/v1/creative/generate-product-pdf",
        json={
            "filename": "API测试产品方案",
            "product_requirements": "这是产品需求",
            "product_features": "这是产品特点",
            "product_image_url": "https://placekitten.com/800/400",
            "marketing_copy": "这是营销文案"
        }
    )
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf" 