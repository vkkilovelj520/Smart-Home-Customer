"""
test_prompt_loader.py - 提示词加载测试

📚 Java 对照：
- test_ 函数 ≈ @Test 方法
- assert 表达式 ≈ assertEquals/assertTrue
- pytest.raises() ≈ assertThrows()

测试目标：utils/prompt_loader.py
"""
import pytest
import os
from utils.prompt_loader import load_system_prompts, load_rag_prompts, load_report_prompts


class TestPromptLoader:
    """测试提示词加载功能"""

    def test_load_system_prompts_returns_string(self):
        """测试：主系统提示词能正确加载为字符串"""
        # 📚 Java 对照：assertInstanceOf(loadSystemPrompts(), String.class)
        result = load_system_prompts()
        
        assert isinstance(result, str)
        assert len(result) > 0

    def test_load_system_prompts_not_empty(self):
        """测试：主系统提示词不为空"""
        result = load_system_prompts()
        
        # 📚 Java 对照：assertFalse(result.isEmpty())
        assert result.strip(), "主系统提示词为空！"

    def test_load_rag_prompts_returns_string(self):
        """测试：RAG 提示词能正确加载"""
        result = load_rag_prompts()
        
        assert isinstance(result, str)
        assert len(result) > 0

    def test_load_report_prompts_returns_string(self):
        """测试：报告提示词能正确加载"""
        result = load_report_prompts()
        
        assert isinstance(result, str)
        assert len(result) > 0

    def test_system_prompts_contains_keywords(self):
        """测试：主系统提示词包含预期的关键词"""
        result = load_system_prompts()
        
        # 你可以根据实际提示词内容调整这些关键词
        keywords = ["智能家居", "客服"]  # 根据你的实际提示词修改
        
        for keyword in keywords:
            assert keyword in result, f"主系统提示词中缺少关键词：{keyword}"
