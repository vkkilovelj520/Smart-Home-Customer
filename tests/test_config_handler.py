"""
test_config_handler.py - 配置文件加载测试

📚 Java 对照：
- 每个 test_ 函数 ≈ 一个 @Test 方法
- assert 表达式  ≈  assertEquals/assertTrue 等断言方法
- pytest.raises()  ≈  assertThrows()

测试目标：utils/config_handler.py
"""
import pytest
import yaml
import os
from utils.config_handler import (
    load_rag_config,
    load_chroma_config,
    load_prompts_config,
    load_agent_config,
    rag_conf,
    chroma_conf,
    prompts_conf,
    agent_conf
)


class TestConfigLoading:
    """
    📚 Java 对照：类似 JUnit 的测试类
    
    在 pytest 中，测试类不是必须的，函数也可以直接写测试。
    但用类的好处是可以共享 setup（类似 @BeforeEach）。
    """

    def test_load_rag_config_returns_dict(self):
        """测试：RAG 配置加载返回的是字典"""
        config = load_rag_config()
        
        # 📚 Java 对照：assertInstanceOf(config, Map.class)
        assert isinstance(config, dict)
    
    def test_load_rag_config_has_required_keys(self):
        """测试：RAG 配置包含必要的 key"""
        config = load_rag_config()
        
        # 📚 Java 对照：assertTrue(config.containsKey("chat_model_name"))
        assert "chat_model_name" in config
        assert "embedding_model_name" in config
    
    def test_load_rag_config_model_name(self):
        """测试：RAG 配置的模型名称是否正确"""
        config = load_rag_config()
        
        # 📚 Java 对照：assertEquals("qwen3-max", config.get("chat_model_name"))
        assert config["chat_model_name"] == "qwen3-max"
        assert config["embedding_model_name"] == "text-embedding-v4"

    def test_load_chroma_config_returns_dict(self):
        """测试：Chroma 配置加载返回的是字典"""
        config = load_chroma_config()
        
        assert isinstance(config, dict)
        assert "collection_name" in config
        assert "persist_directory" in config

    def test_load_chroma_config_values(self):
        """测试：Chroma 配置的值是否正确"""
        config = load_chroma_config()
        
        assert config["collection_name"] == "agent"
        assert config["persist_directory"] == "chroma_db"
        assert config["k"] == 3  # 检索返回文档数量

    def test_load_prompts_config_returns_dict(self):
        """测试：提示词配置加载返回的是字典"""
        config = load_prompts_config()
        
        assert isinstance(config, dict)
        assert "main_prompt_path" in config

    def test_load_agent_config_returns_dict(self):
        """测试：Agent 配置加载返回的是字典"""
        config = load_agent_config()
        
        assert isinstance(config, dict)
        assert "gaodekey" in config
        assert "external_data_path" in config

    def test_agent_config_gaode_key_not_placeholder(self):
        """测试：高德地图 Key 不是默认占位符"""
        config = load_agent_config()
        
        # 📚 Java 对照：assertNotEquals("你的高德key!", config.get("gaodekey"))
        assert config["gaodekey"] != "你的高德key!", "高德地图 Key 还是默认占位符，需要替换！"


class TestConfigGlobals:
    """测试全局配置变量（模块加载时自动初始化的那些）"""

    def test_rag_conf_is_dict(self):
        """测试：全局 rag_conf 变量是字典"""
        assert isinstance(rag_conf, dict)

    def test_chroma_conf_is_dict(self):
        """测试：全局 chroma_conf 变量是字典"""
        assert isinstance(chroma_conf, dict)

    def test_prompts_conf_is_dict(self):
        """测试：全局 prompts_conf 变量是字典"""
        assert isinstance(prompts_conf, dict)

    def test_agent_conf_is_dict(self):
        """测试：全局 agent_conf 变量是字典"""
        assert isinstance(agent_conf, dict)
