"""
LLM客户端封装
统一使用OpenAI格式调用
"""

import json
import re
from typing import Optional, Dict, Any, List
from openai import OpenAI

from ..config import Config


class LLMClient:
    """LLM客户端"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.api_key = api_key or Config.LLM_API_KEY
        self.base_url = base_url or Config.LLM_BASE_URL
        self.model = model or Config.LLM_MODEL_NAME
        
        if self.base_url and not self.base_url.startswith("http://") and not self.base_url.startswith("https://"):
            self.base_url = "https://" + self.base_url
        
        if not self.api_key:
            raise ValueError("LLM_API_KEY 未配置")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 3000,
        response_format: Optional[Dict] = None
    ) -> str:
        """
        发送聊天请求
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            response_format: 响应格式（如JSON模式）
            
        Returns:
            模型响应文本
        """
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        if response_format:
            kwargs["response_format"] = response_format
        
        import time
        import re
        import logging
        logger = logging.getLogger(__name__)
        
        # Tingkatkan retry ke 6 untuk menahan gempuran antrean Google
        max_attempts = 6
        last_error = None
        
        for attempt in range(max_attempts):
            try:
                response = self.client.chat.completions.create(**kwargs)
                content = response.choices[0].message.content
                if content:
                    content = re.sub(r'<think>[\s\S]*?</think>', '', content).strip()
                return content or ""
            except Exception as e:
                error_msg = str(e)
                logger.warning(f"LLM调用失败 (attempt {attempt+1}/{max_attempts}): {error_msg[:100]}")
                last_error = e
                
                if attempt < max_attempts - 1:
                    # Cek apakah ada informasi "retry in X.XXs"
                    retry_match = re.search(r'retry in (\d+\.?\d*)s', error_msg)
                    if retry_match:
                        sleep_time = float(retry_match.group(1)) + 1.0
                        logger.info(f"Rate limit API terdeteksi di LLMClient! Sistem jeda selama {sleep_time:.1f} detik...")
                        time.sleep(sleep_time)
                    else:
                        time.sleep(2 * (attempt + 1))
        
        raise last_error or Exception("LLM调用失败")
    
    def chat_json(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 3000
    ) -> Dict[str, Any]:
        """
        发送聊天请求并返回JSON
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            解析后的JSON对象
        """
        response = self.chat(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"}
        )
        # 尝试提取JSON块 (处理LLM返回额外文本的情况)
        cleaned_response = response.strip()
        start_idx = cleaned_response.find('{')
        end_idx = cleaned_response.rfind('}')
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            cleaned_response = cleaned_response[start_idx:end_idx+1]
            
        try:
            return json.loads(cleaned_response)
        except json.JSONDecodeError:
            raise ValueError(f"LLM返回的JSON格式无效: {cleaned_response}")

