from ..LLMInterface import LLMInterface
from ..LLMEnums import GeminiEnums, DocumentTypeEnum
import google.generativeai as genai
import logging
from typing import List, Union

class GeminiProvider(LLMInterface):

    def __init__(self, api_key: str,
                       default_input_max_characters: int=1000,
                       default_generation_max_output_tokens: int=1000,
                       default_generation_temperature: float=0.1):
        
        self.api_key = api_key

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        # تهيئة الاتصال بسيرفرات جوجل
        genai.configure(api_key=self.api_key)
        self.client = genai
        self.enums = GeminiEnums
        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()

    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int=None,
                            temperature: float = None):

        if not self.client:
            self.logger.error("Gemini client was not set")
            return None

        if not self.generation_model_id:
            self.logger.error("Generation model for Gemini was not set")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature

        # إضافة السؤال الجديد للذاكرة
        chat_history.append(
            self.construct_prompt(prompt=prompt, role=GeminiEnums.USER.value)
        )

        try:
            # تجهيز الموديل للإجابة
            model = self.client.GenerativeModel(self.generation_model_id)
            
            # إعدادات التوليد
            generation_config = self.client.GenerationConfig(
                max_output_tokens=max_output_tokens,
                temperature=temperature,
            )

            # إرسال المحادثة بالكامل
            response = model.generate_content(
                chat_history,
                generation_config=generation_config
            )

            if not response or not response.text:
                self.logger.error("Error while generating text with Gemini")
                return None
            
            return response.text

        except Exception as e:
            self.logger.error(f"Gemini generation error: {e}")
            return None

    def embed_text(self, text: Union[str, List[str]], document_type: str = None):
        
        if not self.client:
            self.logger.error("Gemini client was not set")
            return None

        if isinstance(text, str):
            text = [text]

        if not self.embedding_model_id:
            self.logger.error("Embedding model for Gemini was not set")
            return None
        
        task_type = "RETRIEVAL_DOCUMENT"
        if document_type == DocumentTypeEnum.QUERY.value:
            task_type = "RETRIEVAL_QUERY"

        try:
            processed_content = [self.process_text(t) for t in text]

            response = self.client.embed_content(
                model = self.embedding_model_id,
                content = processed_content,
                task_type = task_type
            )

            if not response or "embedding" not in response:
                self.logger.error("Error while embedding text with Gemini")
                return None
            
            embeddings = response["embedding"]

            if len(embeddings) > 0 and isinstance(embeddings[0], (float, int)):
                return [embeddings]

            return embeddings
            
        except Exception as e:
            self.logger.error(f"Gemini embedding error: {e}")
            return None

    def construct_prompt(self, prompt: str, role: str):

        return {
            "role": role,
            "parts": prompt
        }