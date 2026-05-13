# Article Translation Application

A powerful AI-powered article translation tool built with Flask and Google Gemini API. Translate your articles to multiple languages with context-aware translation and accuracy metrics.

## Features

### Frontend Features

- 📝 **Text Input**: Paste article text directly or upload files (TXT, PDF)
- 🌍 **Language Selection**: Choose from 12+ languages for translation
- 📤 **File Upload Support**: Translate entire documents in .txt and .pdf formats
- ✅ **Expected Output Comparison**: Upload expected translations to calculate accuracy
- 📊 **Detailed Metrics**:
  - Token usage tracking
  - Accuracy percentage (when expected output is provided)
  - Processing time measurement
- 🎨 **Modern UI**: Beautiful, responsive interface with real-time results

### Backend Features

- 🤖 **AI-Powered Translation**: Uses Google Gemini 1.5 Flash model with context understanding
- 🔢 **Token Counting**: Accurate token usage tracking for cost estimation
- 📈 **Accuracy Calculation**: Compares AI translation with expected output using semantic similarity
- 📄 **Multi-Format Support**: Handles plain text and PDF files
- 🚀 **High Performance**: Optimized API calls with proper error handling
- 🔒 **Secure**: File upload validation and size limits

## Supported Languages

- Spanish (Español)
- French (Français)
- German (Deutsch)
- Chinese (中文)
- Japanese (日本語)
- Hindi (हिंदी)
- Portuguese (Português)
- Russian (Русский)
- Italian (Italiano)
- Arabic (العربية)
- Dutch (Nederlands)
- Korean (한국어)

## Project Structure

```
Article_Translation/
├── app.py                 # Main Flask application
├── chatModel.py          # Optional: Helper for older chat functionality
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html       # Frontend HTML with complete UI
├── static/
│   └── style.css        # Frontend styling
└── uploads/             # Temporary file storage (auto-created)
```

## Installation

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key

### 2. Clone/Setup Project

```bash
cd langchain_In_Detail
```

### 3. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Setup Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_DEBUG=True
```

**How to get your Gemini API key:**

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Get API Key"
3. Create a new API key
4. Copy and paste it into your `.env` file

## Running the Application

### Development Mode

```bash
python app.py
```

The application will start at `http://localhost:5000`

### Production Mode

For production deployment:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Usage Guide

### 1. Basic Translation

1. Enter your article text in the input field
2. Select target language from dropdown
3. Click "🚀 Translate Article"
4. View results with token count and processing time

### 2. Upload File for Translation

1. Click "📤 Upload File (TXT, PDF)"
2. Select your document
3. Choose target language
4. Submit for translation
5. Download or copy the translated text

### 3. Calculate Accuracy

1. Enter article text (option 1)
2. Choose target language
3. Paste expected translated text in Step 3
4. Submit translation
5. View accuracy percentage comparing AI output with expected output

### Supported File Formats

- **.txt**: Plain text files (any encoding)
- **.pdf**: PDF documents with extractable text

### Size Limits

- Text input: Maximum 10,000 characters
- File uploads: Maximum 16 MB

## API Endpoints

### POST `/api/translate`

Translates article text to specified language.

**Request (FormData):**

```
text: string (optional if file provided)
file: file (optional, .txt or .pdf)
targetLanguage: string (required)
expectedOutput: string (optional)
```

**Response:**

```json
{
  "original_text": "English article text...",
  "translated_text": "Translated text...",
  "target_language": "Spanish",
  "tokens_used": 245,
  "accuracy": 0.85,
  "expected_output": "Expected translation..."
}
```

**Error Response:**

```json
{
  "error": "Error message describing what went wrong"
}
```

## How It Works

### Translation Process

1. **Text Extraction**: Extracts text from uploaded files or uses provided text
2. **Prompt Engineering**: Creates context-aware translation prompt
3. **API Call**: Sends request to Gemini API with detailed instructions
4. **Token Counting**: Counts input and output tokens for cost tracking
5. **Accuracy Matching**: Compares output with expected text using similarity scoring

### Accuracy Calculation

- Uses Python's `SequenceMatcher` for semantic similarity
- Normalizes text (lowercase, whitespace handling)
- Returns similarity score as percentage (0-100%)
- Higher percentage = closer match to expected output

## Configuration

### Model Settings

The application uses **Google Gemini 1.5 Flash** for optimal performance:

- Fast response times
- Lower API costs
- Excellent translation quality
- Context-aware processing

### Customization Options

**Change Translation Model:**
Edit `app.py` line ~56:

```python
model = genai.GenerativeModel('gemini-1.5-pro')  # For higher quality
```

**Increase Text Limit:**
Edit `app.py` line ~116:

```python
if len(text) > 50000:  # Increase limit
```

## Troubleshooting

### Issue: "GEMINI_API_KEY not found"

**Solution:**

- Ensure `.env` file exists in project root
- Check API key is correctly copied
- Restart Flask after adding .env file

### Issue: "Only .txt and .pdf files are allowed"

**Solution:**

- Convert files to .txt or .pdf format
- Check file extension is correct

### Issue: "Text is too long"

**Solution:**

- Split large articles into smaller parts
- Contact support to increase limit

### Issue: "Translation failed with API error"

**Solution:**

- Check internet connection
- Verify Gemini API key is valid
- Check API quota hasn't exceeded
- Try again after a few moments

## Performance Metrics

**Typical Performance:**

- Small text (< 1000 chars): 2-3 seconds
- Medium text (1000-5000 chars): 3-5 seconds
- Large text (5000-10000 chars): 5-10 seconds

**Token Usage:**

- Typically 1 token per 4 characters
- Input + Output tokens calculated
- Cost estimator available in UI

## Security Features

- ✅ File upload validation (extension & size)
- ✅ Secure filename handling
- ✅ XSS protection in frontend
- ✅ CSRF token support (can be added)
- ✅ Rate limiting (can be added)
- ✅ API key kept secure in .env

## API Rate Limits

Google Gemini API has rate limits:

- Free tier: 60 requests per minute
- Paid tier: Higher limits based on plan

Respect these limits in production deployment.

## Deployment

### Heroku Deployment

1. Create `Procfile`:

```
web: gunicorn app:app
```

2. Deploy:

```bash
git push heroku main
```

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Build and run:

```bash
docker build -t article-translator .
docker run -p 5000:5000 -e GEMINI_API_KEY=your_key article-translator
```

## Future Enhancements

- [ ] User authentication and history tracking
- [ ] Batch translation of multiple files
- [ ] Translation memory for consistent terminology
- [ ] Quality scoring metrics
- [ ] Document format preservation
- [ ] Custom glossary support
- [ ] Language detection
- [ ] Collaborative translation mode

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:

1. Check the troubleshooting section
2. Review error messages carefully
3. Check Gemini API documentation
4. Open an issue with detailed description

## Changelog

### Version 1.0.0 (Initial Release)

- Core translation functionality
- File upload support (TXT, PDF)
- Accuracy calculation
- Token counting
- Modern responsive UI
- 12+ language support

---

**Built with ❤️ using Flask and Google Gemini API**
#   T r a n s l y t i c s  
 