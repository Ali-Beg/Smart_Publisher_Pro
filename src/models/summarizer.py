import re
import time
import streamlit as st
import google.generativeai as genai
from typing import Optional
# from config.settings import GEMINI_API_KEYS
from config.settings import MAX_RETRIES, INITIAL_BACKOFF, MAX_CONTENT_LENGTH, INTRO_LENGTH, CONCLUSION_LENGTH
from src.utils.quota import QuotaManager

class ContentSummarizer:
    def __init__(self, max_retries=MAX_RETRIES, initial_backoff=INITIAL_BACKOFF):
        """
        Initialize the ContentSummarizer with retry and backoff settings.

        Args:
            max_retries (int): Maximum number of retries for API calls.
            initial_backoff (int): Initial backoff time in seconds for retries.
        """
        self.max_retries = max_retries
        self.initial_backoff = initial_backoff
        self.quota_manager = QuotaManager()
        self.cache = {}
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize model with current API key"""
        try:
            api_key = self.quota_manager.get_current_api_key()
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-1.5-pro")
        except Exception as e:
            st.error(f"Error initializing model: {str(e)}")
            raise e
    
    def clean_content(self, text: str) -> str:
        """Clean and prepare content for summarization"""
        try:
            text = re.sub(r'http\S+', '', text)
            text = re.sub(r'[^\w\s.,!?-]', '', text)
            text = ' '.join(text.split())
            
            if len(text) > MAX_CONTENT_LENGTH:
                # intro = text[:2000]
                # conclusion = text[-2000:]
                intro = text[:INTRO_LENGTH]
                conclusion = text[-CONCLUSION_LENGTH:]
                text = f"{intro}...\n[Content truncated]...\n{conclusion}"         
            return text
        except Exception as e:
            st.warning(f"Warning during content cleaning: {str(e)}")
            return text

    def generate_summary(self, content: str, title: str = "") -> str:
        """Generate summary with enhanced quota handling"""
        cache_key = f"{title}_{hash(content)}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        current_retry = 0
        while current_retry < self.max_retries:
            try:
                api_key = self.quota_manager.get_current_api_key()
                
                if not self.quota_manager.is_key_available(api_key):
                    if self.quota_manager.rotate_api_key():
                        self._initialize_model()
                        continue
                    else:
                        return self._generate_fallback_summary(title, content)
                
                cleaned_content = self.clean_content(content)
                prompt = self._create_prompt(cleaned_content, title)
                
                response = self.model.generate_content(prompt)
                summary = response.text
                
                self.cache[cache_key] = summary
                return summary
                
            except Exception as e:
                error_str = str(e)
                
                # Handle quota exceeded error
                if "429" in error_str or "quota" in error_str.lower():
                    self.quota_manager.mark_quota_exceeded(api_key)
                    if self.quota_manager.rotate_api_key():
                        self._initialize_model()
                        continue
                    else:
                        return self._generate_fallback_summary(title, content)
                
                # Handle other errors with backoff
                current_retry += 1
                if current_retry == self.max_retries:
                    return self._generate_fallback_summary(title, content)
                
                backoff_time = self.initial_backoff * (2 ** current_retry)
                time.sleep(backoff_time)
        
        return self._generate_fallback_summary(title, content)
    
    def _generate_fallback_summary(self, title: str, content: str) -> str:
        """Generate a more sophisticated fallback summary"""
        try:
            # Split into sentences and clean them
            sentences = [s.strip() for s in content.split('.') if len(s.strip()) > 20]
            
            if len(sentences) <= 3:
                return content            
            # Select key sentences based on position and length
            intro = sentences[0]
            body_sentences = sentences[1:-1]
            conclusion = sentences[-1]          
            # Select 1-2 body sentences based on length and keywords
            key_sentences = []
            for sent in body_sentences:
                if len(sent.split()) > 10 and any(kw in sent.lower() for kw in ['important', 'significant', 'key', 'main', 'crucial']):
                    key_sentences.append(sent)
                    if len(key_sentences) == 2:
                        break
            
            # Construct the summary
            summary_parts = [intro]
            if key_sentences:
                summary_parts.extend(key_sentences)
            summary_parts.append(conclusion)
            
            summary = '. '.join(summary_parts) + '.'
            return f"Summary of '{title}': {summary}"
            
        except Exception as e:
            return f"Unable to summarize '{title}' due to an error: {str(e)}"

    # --------------------------------
    def _create_prompt(self, content: str, title: str) -> str:
        # return f"""You are an experienced content curator and storyteller. Read the following article and create a natural, engaging summary that feels like it was written by a human expert. Imagine you're explaining this to a friend or colleague over coffee.

        # Article Title: {title}
        # Key Points to Consider:
        # - Write in a conversational yet professional tone
        # - Use natural transitions and flowing sentences
        # - Include interesting details that make the content memorable
        # - Avoid formal or robotic language
        # - Make it feel like a story, not a report
        # - Keep the length to 1-2 short paragraphs

        # The article to summarize:
        # {content}
        # Remember to make it sound natural and engaging, like a human would tell it."""
    
        """Create enhanced prompt for more natural, human-like summaries"""
        return f"""
        Role: You are an expert and experienced content curator and writer who specializes in creating engaging, natural-sounding article summaries.

        Task: Create a concise, engaging summary of the following article that sounds like it was written by a human writer, not an AI.
        Article Title: {title}
        Guidelines:
        - Write in a natural, conversational tone while maintaining professionalism
        - Focus on the most interesting and important points
        - Use varied sentence structures and transitions
        - Include specific details and numbers when relevant
        - Avoid formulaic or robotic language
        - Keep the summary to 1-2 short paragraphs "short"
        - Add contextual insights where appropriate
        - Use light narrative elements to make the summary more engaging      
        Remember: The summary should flow naturally and feel like it was written by a human journalist or content writer, not an AI system.
        
        Content: {content}

        Please provide a summary that captures both the substance and the human interest of this article.
        """
