from src.utils.quota import QuotaManager
from src.models.summarizer import ContentSummarizer
from src.utils.telegram import send_to_telegram
from config.settings import GEMINI_API_KEYS 
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
CHAT_ID =TELEGRAM_CHAT_ID

import streamlit as st
import pandas as pd
import google.generativeai as genai

import requests
from typing import List, Dict, Optional
import random
import time

def main():

    initialize_session_state()
    setup_page()
    
    # Main UI
    st.title("📡 Smart Publisher Pro")
    st.markdown(" #### Autonomous Article Summarization and Telegram Sharing with Multi-Agent AI")
    st.write("Welcome to the Smart Publisher Pro, where you can autonomously summarize articles and distribute them to designated Telegram channels. This platform leverages multi-agent AI and Reinforcement Human Loop Feedback (RHLF) to ensure high-quality summaries that adapt to user feedback.")
    # API Status Indicator in Sidebar
    num_summaries = display_sidebar()
    
    # File upload
    st.markdown("### 📁 Upload Your Articles")
    uploaded_file = st.file_uploader(
        "Upload your CSV file (must contain 'Title' and 'Content' columns)",
        type=['csv'],
        help="Make sure your CSV has 'Title' and 'Content' columns"
    )
    
    if uploaded_file:
        try:
            # Process uploaded file
            df = process_uploaded_file(uploaded_file, num_summaries)
            if df is None:
                return                       
            # Generate Summaries button
            if st.button("Generate Summaries"):
                generate_summaries_bt(df, num_summaries)
                
            # Send to Telegram button
            if st.session_state.summaries:
                handle_telegram_sending()               
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.exception(e)

def initialize_session_state():
    """Initialize session state variables"""
    if 'summaries' not in st.session_state:
        st.session_state.summaries = None
    if 'processed_count' not in st.session_state:
        st.session_state.processed_count = 0

def setup_page():
    """Configure page settings"""
    st.set_page_config(
        page_title="Article Summarizer",
        page_icon="📚",
        layout="wide"
    )

def display_sidebar():
    # API Status Indicator in Sidebar
    """Display and handle sidebar elements"""
    with st.sidebar:
        st.header("⚙️ Settings")
        num_summaries = st.slider(
            "Number of summaries",
            min_value=2,
            max_value=10,
            value=2
        )
        
        st.markdown("---")
        st.markdown("### 🔑 API Status")
        quota_manager = QuotaManager()
        available_keys = sum(1 for key in GEMINI_API_KEYS 
                           if quota_manager.is_key_available(key))
        
        if available_keys > 0:
            st.success(f"✅ API Available ({available_keys} keys ready)")
        else:
            st.error("❌ All API keys exhausted")
            st.info("🔄 Using fallback summarization method")
        
        st.markdown("### 📊 Statistics")
        st.write(f"Total Articles Processed: {st.session_state.processed_count}")
        if st.session_state.summaries:
            st.write(f"Current Batch: {len(st.session_state.summaries)} summaries")
    
    return num_summaries

def process_uploaded_file(file, num_summaries):
    """Process the uploaded CSV file and generate summaries"""
    try:
        df = pd.read_csv(file)
        df.columns = df.columns.str.lower()
        
        if not {'title', 'content'}.issubset(df.columns):
            st.error("❌ CSV must contain 'Title' and 'Content' columns!")
            return None
            
        with st.expander("Preview uploaded data"):
            st.dataframe(df[['title', 'content']].head())            
        return df       
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None

def generate_summaries_bt(df, num_summaries):
    """Generate summaries for the selected articles"""
    if len(df) < num_summaries:
        st.error(f"CSV only contains {len(df)} articles. Please select a smaller number.")
        st.stop()
    
    with st.spinner("Generating summaries... This may take a moment."):
        try:
            summarizer = ContentSummarizer()
            selected_indices = random.sample(range(len(df)), num_summaries)
            summaries = []
            failed_summaries = []
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, index in enumerate(selected_indices):
                row = df.iloc[index]
                status_text.text(f"Processing article {idx + 1}/{num_summaries}")
                
                summary = summarizer.generate_summary(row['content'], row['title'])
                
                if summary:
                    summaries.append({
                        'title': row['title'],
                        'content': row['content'],
                        'summary': summary
                    })
                else:
                    failed_summaries.append(row['title'])
                
                progress_bar.progress((idx + 1) / num_summaries)
            
            st.session_state.summaries = summaries
            st.session_state.processed_count += len(summaries)

            if summaries:
                st.success(f"✅ Successfully generated {len(summaries)} summaries!")
                if failed_summaries:
                    st.warning(f"⚠️ Failed to generate summaries for: {', '.join(failed_summaries)}")
            else:
                st.error("❌ Failed to generate any summaries. Please try again.")
                st.stop() 

            # Display summaries
            for idx, summary in enumerate(summaries, 1):
                with st.expander(f"Summary {idx}: {summary['title']}"):
                    st.write(summary['summary'])
        
        except Exception as e:
            st.error(f"Error during summary generation: {str(e)}")
            st.exception(e)

def handle_telegram_sending():
    """Handle sending summaries to Telegram"""          
    if st.button("📱 Send to Telegram"):
        with st.spinner("Sending to Telegram..."):
            try:
                # Select random summaries for sending
                send_summaries = random.sample(
                    st.session_state.summaries,
                    min(2, len(st.session_state.summaries))
                )
                # Attempt to send to Telegram
                success = send_to_telegram(send_summaries)               
                if success:
                    st.success("✅ Summaries sent to Telegram successfully!")
                    
                    with st.expander("View sent summaries"):
                        for summary in send_summaries:
                            st.markdown(f"**{summary['title']}**")
                            st.write(summary['summary'])
                            st.markdown("---")
                else:
                    st.error("❌ Failed to send summaries to Telegram")
                    
            except Exception as e:
                st.error(f"Error in Telegram sending: {str(e)}")
                st.exception(e)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error("❌ An unexpected error occurred. Please refresh the page and try again.")
        st.exception(e)

