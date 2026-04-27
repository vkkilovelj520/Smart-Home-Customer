"""
test_file_handler.py - 文件处理功能测试

📚 Java 对照：
- 测试纯函数（无副作用）≈ JUnit 里最简单的单元测试
- 不需要 mock，直接调用

测试目标：utils/file_handler.py
"""
import pytest
import os
import tempfile
from utils.file_handler import get_file_md5_hex, listdir_with_allowed_type


class TestFileMD5:
    """测试文件 MD5 计算功能"""

    def test_md5_of_known_file(self):
        """测试：已知内容的文件 MD5 计算正确"""
        # 📚 Java 对照：类似创建一个临时文件然后测试
        
        # 创建一个临时文件
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("hello")
            temp_path = f.name
        
        try:
            # "hello" 的 MD5 是 5d41402abc4b2a76b9719d911017c592
            result = get_file_md5_hex(temp_path)
            
            assert result == "5d41402abc4b2a76b9719d911017c592"
        finally:
            os.unlink(temp_path)  # 清理临时文件

    def test_md5_file_not_exists(self):
        """测试：不存在的文件返回 None"""
        result = get_file_md5_hex("/this/file/does/not/exist.txt")
        
        # 📚 Java 对照：assertNull(result)
        assert result is None

    def test_md5_not_a_file(self):
        """测试：传入文件夹路径返回 None"""
        result = get_file_md5_hex("D:\\zhisaotong-Agent-master\\data")
        
        assert result is None


class TestListdirWithAllowedType:
    """测试文件夹文件列表功能"""

    def test_list_txt_files(self):
        """测试：能正确列出 .txt 文件"""
        data_dir = os.path.join("D:\\zhisaotong-Agent-master", "data")
        
        result = listdir_with_allowed_type(data_dir, (".txt",))
        
        assert isinstance(result, tuple)
        # data 目录下应该有 .txt 文件
        for file_path in result:
            assert file_path.endswith(".txt")

    def test_list_pdf_files(self):
        """测试：能正确列出 .pdf 文件"""
        data_dir = os.path.join("D:\\zhisaotong-Agent-master", "data")
        
        result = listdir_with_allowed_type(data_dir, (".pdf",))
        
        assert isinstance(result, tuple)

    def test_list_multiple_types(self):
        """测试：能同时列出多种类型文件"""
        data_dir = os.path.join("D:\\zhisaotong-Agent-master", "data")
        
        result = listdir_with_allowed_type(data_dir, (".txt", ".pdf"))
        
        for file_path in result:
            assert file_path.endswith((".txt", ".pdf"))

    def test_not_a_directory(self):
        """测试：传入文件路径而不是目录"""
        result = listdir_with_allowed_type("D:\\zhisaotong-Agent-master\\app.py", (".py",))
        
        # 函数在不是目录时返回 allowed_types
        assert result == (".py",)

    def test_empty_result_for_no_match(self):
        """测试：没有匹配的文件时返回空元组"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # 创建一个 .txt 文件
            open(os.path.join(temp_dir, "test.txt"), 'w').close()
            
            result = listdir_with_allowed_type(temp_dir, (".pdf",))
            
            assert result == ()
