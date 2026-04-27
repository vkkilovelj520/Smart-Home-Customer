"""
test_logger_handler.py - 日志功能测试

📚 Java 对照：
- 类似测试 SLF4J/Log4j 配置是否正确
- Python 的 logging 比 Java 的日志简单很多

测试目标：utils/logger_handler.py
"""
import pytest
import logging
from utils.logger_handler import logger


class TestLogger:
    """测试日志记录功能"""

    def test_logger_exists(self):
        """测试：logger 对象存在"""
        # 📚 Java 对照：assertNotNull(logger)
        assert logger is not None

    def test_logger_is_logger_instance(self):
        """测试：logger 是 logging.Logger 实例"""
        # 📚 Java 对照：assertInstanceOf(logger, Logger.class)
        assert isinstance(logger, logging.Logger)

    def test_logger_can_log_info(self):
        """测试：logger 能正常输出 INFO 级别日志"""
        # 这个测试只是确认 logger 不会报错
        try:
            logger.info("[TEST] 这是一条测试日志，可以忽略")
            passed = True
        except Exception:
            passed = False
        
        assert passed, "logger.info() 抛出异常！"

    def test_logger_can_log_error(self):
        """测试：logger 能正常输出 ERROR 级别日志"""
        try:
            logger.error("[TEST] 这是一条错误日志测试")
            passed = True
        except Exception:
            passed = False
        
        assert passed, "logger.error() 抛出异常！"

    def test_logger_has_handlers(self):
        """测试：logger 有处理器（能输出到控制台或文件）"""
        assert len(logger.handlers) > 0, "logger 没有配置任何 handler！"

    def test_logger_level(self):
        """测试：logger 的日志级别设置合理"""
        # INFO 或 DEBUG 都是合理的，NOTSET 可能有问题
        assert logger.level in (logging.DEBUG, logging.INFO, logging.WARNING), \
            f"logger 级别异常：{logger.level}"
