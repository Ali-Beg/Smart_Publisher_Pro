# Smart Publisher Pro

**Autonomous Article Summarization and Telegram Sharing with Multi-Agent AI**

Smart Publisher Pro is an AI-driven article summarization and sharing tool that utilizes Google's Gemini API for generating concise, high-quality summaries. Built on Streamlit, this application provides an intuitive interface for users to upload articles, summarize content, and distribute summaries directly to a Telegram group. The platform includes multi-agent quota management for handling multiple API keys, a fallback summarization method for uninterrupted service, and reliable integration with Telegram for seamless content sharing.

## Features

- **CSV File Upload**: Easily upload CSV files with articles for batch summarization.
- **AI-Powered Summarization**: Generate concise summaries with Google's Gemini API.
- **Multi-Agent Quota Management**: Rotates API keys to manage quotas and ensure continuous operation.
- **Fallback Summarization**: Maintains functionality even when API limits are reached.
- **Telegram Integration**: Automatically shares summaries in a specified Telegram group.
- **User-Friendly Interface**: Built with Streamlit for an accessible, seamless experience.

## Project Structure

```
Smart_Publisher_Pro/
├── src/
│   ├── models/
│   │   └── summarizer.py
│   └── utils/
│       ├── quota.py          
│       └── telegram.py       
├── config/
│   └── settings.py           
├── .env                     
├── requirements.txt        
├── README.md                
└── app.py                   
Streamlit application
```

### Overview of Key Modules

- **`src/models/summarizer.py`**: Contains the core logic for generating summaries using the Gemini API. Manages prompting strategies for effective summarization.
- **`src/utils/quota.py`**: Implements quota management to handle multiple API keys, allowing rotation to maintain uninterrupted operation.
- **`src/utils/telegram.py`**: Provides functions for formatting and sending summaries to a Telegram group via the Bot API.
- **`config/settings.py`**: Stores configuration settings for the app, including environment settings and defaults for the Streamlit app.

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/Smart_Publisher_Pro.git
   cd Smart_Publisher_Pro
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   - Copy `.env.template` to `.env`.
   - Add your **Gemini API keys** (comma-separated).
   - Set your **Telegram bot token** and **chat ID** in `.env`.

5. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Launch the App**: Open the app by running `streamlit run app.py` to start the dashboard in your browser.
   
2. **Upload CSV File**:
   - Use the file uploader in the dashboard to select a CSV file with columns **'Title'** and **'Content'** for articles.
   
3. **Generate Summaries**:
   - Set the desired number of summaries to generate.
   - Click **Generate Summaries** to start the summarization process.
   - Summaries are displayed in the app upon completion.

4. **Send Summaries to Telegram**:
   - Click the **Send to Telegram** button to share the generated summaries in your specified Telegram group.
   - A confirmation message will appear once the summaries are successfully sent.

## Core Functionalities

### 1. Summarization with Gemini API
   - **Gemini API Integration**: Uses custom prompts to create concise, readable summaries.
   - **Prompt Engineering**: Prompts are tailored to improve relevance and quality of summaries.
   - **Quota Management**: Rotates API keys to handle rate limits automatically, maintaining continuous service.

### 2. Telegram Integration
   - **Automated Messaging**: Sends summaries directly to a Telegram group using the Bot API.
   - **Retry Mechanism**: Implements retries for reliable message delivery in case of network errors.

### 3. Fallback Summarization
   - Ensures the app continues to generate summaries when API limits are exceeded by using an alternative summarization method.

### 4. Multi-Agent Quota Management
   - Located in `src/utils/quota.py`, this module manages API key rotation based on usage, providing resilience and uptime.

## Example Environment Configuration (.env)

Your `.env` file should include your API keys and Telegram credentials as shown below:
```
GEMINI_API_KEYS="API_KEY_1,API_KEY_2"
TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
TELEGRAM_CHAT_ID="your_telegram_chat_id"
```

## Deployment

The **Smart Publisher Pro** can be deployed on Streamlit Cloud. Follow these steps:

1. **Push to GitHub**: Ensure your code is available in a GitHub repository.
2. **Set Up on Streamlit Cloud**:
   - Go to [Streamlit Cloud](https://streamlit.io/cloud).
   - Create a new app connected to your GitHub repository.
   - Set environment variables for Gemini API keys, Telegram token, and chat ID in Streamlit Cloud’s settings.
3. **Deploy**: Start deployment to make your app accessible with a shareable link.

## Testing

1. **Unit Testing**:
   - Test individual modules, such as `summarizer.py` for API responses, `quota.py` for quota rotation logic, and `telegram.py` for Telegram integration.
   
2. **Integration Testing**:
   - Verify the end-to-end workflow from file upload, summarization, to Telegram message posting.

## Contribution Guidelines

Contributions to improve the project are welcome! Follow these steps to contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a Pull Request with a description of your changes.

## Future Enhancements

1. **Additional Summarization Models**: Expand to include other models for flexibility based on user needs.
2. **User Feedback System**: Add a feedback mechanism for users to rate summaries, feeding data back to the model for improvement.
3. **Scheduled Summarization**: Implement automated summarization and sharing at scheduled times.
4. **Advanced Error Monitoring**: Integrate logging and real-time error monitoring for better diagnostics.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.