import os
from abc import ABC, abstractmethod
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_community.chat_models.tongyi import BaseChatModel
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models.tongyi import ChatTongyi
from utils.config_handler import rag_conf


def _dashscope_api_key() -> str:
    """通义千问 / DashScope Embedding 共用；优先读环境变量，其次 config/rag.yml。"""
    key = (os.environ.get("DASHSCOPE_API_KEY") or "").strip()
    if key:
        return key
    cfg = rag_conf.get("dashscope_api_key")
    if cfg is not None and str(cfg).strip():
        return str(cfg).strip()
    raise ValueError(
        "未找到 DashScope API Key，无法初始化 ChatTongyi / DashScopeEmbeddings。\n"
        "请任选其一：\n"
        "  1) 设置环境变量 DASHSCOPE_API_KEY（推荐，密钥不要写进代码仓库）\n"
        "  2) 在 config/rag.yml 中增加一行：dashscope_api_key: 你的密钥\n"
        "申请地址：https://bailian.console.aliyun.com/\n"
        "PowerShell 临时设置示例：$env:DASHSCOPE_API_KEY=\"sk-你的密钥\""
    )


class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass


class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return ChatTongyi(
            model=rag_conf["chat_model_name"],
            dashscope_api_key=_dashscope_api_key(),
        )


class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return DashScopeEmbeddings(
            model=rag_conf["embedding_model_name"],
            dashscope_api_key=_dashscope_api_key(),
        )


_chat_model_singleton: BaseChatModel | None = None
_embed_model_singleton: Embeddings | None = None


def get_chat_model() -> BaseChatModel:
    global _chat_model_singleton
    if _chat_model_singleton is None:
        _chat_model_singleton = ChatModelFactory().generator()
    return _chat_model_singleton  # type: ignore[return-value]


def get_embed_model() -> Embeddings:
    global _embed_model_singleton
    if _embed_model_singleton is None:
        _embed_model_singleton = EmbeddingsFactory().generator()
    return _embed_model_singleton  # type: ignore[return-value]


def __getattr__(name: str):
    """延迟创建模型，避免 import 阶段失败时被误报为「无法导入 ReactAgent」。"""
    if name == "chat_model":
        return get_chat_model()
    if name == "embed_model":
        return get_embed_model()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
