"""
conftest.py - pytest 共享 fixtures 配置文件

📚 Java 对照：
- @pytest.fixture  ≈  @BeforeEach（每个测试前执行）
- scope="module"  ≈  @BeforeClass（整个模块只执行一次）
- yield 返回值    ≈  给测试方法注入参数

用法：测试文件会自动发现 conftest.py 里的 fixtures，不需要 import
"""
import pytest
import sys
import os

# 把项目根目录加入 Python 路径（这样测试代码才能 import 项目模块）
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


@pytest.fixture
def project_root():
    """
    返回项目根目录路径
    
    📚 Java 对照：类似一个返回测试资源的 helper 方法
    
    用法示例：
        def test_something(project_root):
            print(project_root)  # D:\zhisaotong-Agent-master
    """
    return PROJECT_ROOT


@pytest.fixture(scope="module")
def sample_config():
    """
    返回示例配置数据（整个测试模块只加载一次）
    
    📚 Java 对照：类似 @BeforeClass 里初始化的共享测试数据
    
    用法示例：
        def test_config(sample_config):
            assert sample_config["chat_model_name"] == "qwen3-max"
    """
    return {
        "chat_model_name": "qwen3-max",
        "embedding_model_name": "text-embedding-v4",
        "dashscope_api_key": "sk-test123456"
    }
