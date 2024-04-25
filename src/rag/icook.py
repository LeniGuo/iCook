"""
由于Langchain未支持InternLM, 需要自定义LLM类
https://github.com/langchain-ai/langchain/tree/master/libs/community/langchain_community/llms
"""


from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from typing import Any, List, Optional
from transformers import AutoTokenizer, AutoModelForCausalLM


"""源代码参考:
LLM(BaseLLM):
https://github.com/langchain-ai/langchain/blob/master/libs/core/langchain_core/language_models/llms.py
"""
# TODO: 完善icook类
class icook(LLM):
    def __init__(self, model: AutoModelForCausalLM=None, tokenizer: AutoTokenizer=None):
        super().__init__()
        self.tokenizer = tokenizer
        self.model = model

    def _call(
        self, 
        prompt: str, 
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any
    ) -> str:
        response, history = self.model.chat(self.tokenizer, prompt, history=[])
        return response

    @property
    def _llm_type(self) -> str:
        return "InternLM2"
