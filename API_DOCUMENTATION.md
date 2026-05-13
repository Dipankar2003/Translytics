# API Documentation - Article Translation

Complete API reference for the Article Translation application.

## Base URL

```
http://localhost:5000
```

## Endpoints

### 1. GET `/`

**Description:** Serves the main application interface

**Response:** HTML page of Article Translation application

**Example:**

```bash
curl http://localhost:5000/
```

---

### 2. POST `/api/translate`

**Description:** Translates article text to specified language

#### Request

**Method:** `POST`

**Content-Type:** `multipart/form-data`

**Parameters:**

| Parameter        | Type   | Required    | Description                                                  |
| ---------------- | ------ | ----------- | ------------------------------------------------------------ |
| `text`           | string | Conditional | Article text to translate (required if file not provided)    |
| `file`           | file   | Conditional | PDF or TXT file to translate (required if text not provided) |
| `targetLanguage` | string | Yes         | Target language for translation                              |
| `expectedOutput` | string | No          | Expected translation for accuracy comparison                 |

**Request Examples:**

**Example 1: Text Translation**

```bash
curl -X POST http://localhost:5000/api/translate \
  -F "text=Artificial Intelligence is transforming the world" \
  -F "targetLanguage=Spanish"
```

**Example 2: File Upload**

```bash
curl -X POST http://localhost:5000/api/translate \
  -F "file=@article.pdf" \
  -F "targetLanguage=French"
```

**Example 3: With Accuracy Check**

```bash
curl -X POST http://localhost:5000/api/translate \
  -F "text=Hello world" \
  -F "targetLanguage=German" \
  -F "expectedOutput=Hallo Welt"
```

**JavaScript Fetch Example:**

```javascript
const formData = new FormData();
formData.append("text", "Your article text here");
formData.append("targetLanguage", "Spanish");
formData.append("expectedOutput", "Your expected translation");

fetch("/api/translate", {
  method: "POST",
  body: formData,
})
  .then((response) => response.json())
  .then((data) => console.log(data));
```

**Python Requests Example:**

```python
import requests

files = {
    'text': (None, 'Article text to translate'),
    'targetLanguage': (None, 'Spanish'),
    'expectedOutput': (None, 'Expected translation optional')
}

response = requests.post('http://localhost:5000/api/translate', files=files)
data = response.json()
print(data)
```

#### Response

**Success (200 OK):**

```json
{
  "original_text": "The quick brown fox jumps over the lazy dog",
  "translated_text": "El rápido zorro marrón salta sobre el perro perezoso",
  "target_language": "Spanish",
  "tokens_used": 47,
  "accuracy": 0.92,
  "expected_output": "El zorro marrón rápido salta sobre el perro perezoso"
}
```

**Field Descriptions:**
| Field | Type | Description |
|-------|------|-------------|
| `original_text` | string | The original article text |
| `translated_text` | string | The translated article text |
| `target_language` | string | Language used for translation |
| `tokens_used` | integer | Total tokens used (input + output) |
| `accuracy` | float | Similarity score (0.0 - 1.0), null if no expected output |
| `expected_output` | string | The expected output provided (or null) |

**Error Responses:**

**400 Bad Request:**

```json
{
  "error": "Target language is required"
}
```

**Possible Error Messages:**

- "Target language is required" - No target language provided
- "No text provided to translate" - Neither text nor file provided
- "Only .txt and .pdf files are allowed" - Wrong file format
- "Text is too long. Maximum 10000 characters allowed" - Text exceeds limit
- "File is too large. Maximum 16MB allowed" - File exceeds size limit
- "Error extracting text from file: ..." - PDF/file reading error
- "Translation failed: ..." - Gemini API error

**500 Internal Server Error:**

```json
{
  "error": "Internal server error message"
}
```

---

## Supported Languages

### Language Code Reference

Use these exact language names in `targetLanguage` parameter:

```
Spanish          (Español)
French           (Français)
German           (Deutsch)
Chinese          (中文)
Japanese         (日本語)
Hindi            (हिंदी)
Portuguese       (Português)
Russian          (Русский)
Italian          (Italiano)
Arabic           (العربية)
Dutch            (Nederlands)
Korean           (한국어)
```

**Important:** Language names must match exactly (case-sensitive)

---

## Data Specifications

### Text Input

- **Minimum length:** 1 character
- **Maximum length:** 10,000 characters (configurable)
- **Supported encodings:** UTF-8, UTF-16, ASCII, etc.
- **Special characters:** Fully supported

### File Upload

- **Supported formats:** .txt, .pdf
- **Maximum file size:** 16 MB (configurable)
- **Text extraction:** Automatic for both formats
- **Character limit:** Same as text input (10,000 chars)

### Accuracy Score

- **Range:** 0.0 to 1.0
- **Meaning:**
  - 1.0 = Perfect match (100%)
  - 0.5 = 50% similarity
  - 0.0 = No match (0%)
- **Calculation:** Semantic similarity using sequence matching

### Token Usage

- **Estimation:** Roughly 1 token = 4 characters
- **Includes:** Input text + Output translation
- **Purpose:** Cost estimation for API usage
- **Billing:** Charged by Google Gemini API

---

## Rate Limiting

**Current Limits (Free Tier):**

- 60 requests per minute
- Streaming responses supported
- Batch processing recommended for high volume

**Recommended Practices:**

- Implement request queuing
- Add delays between requests
- Cache translations when possible
- Monitor token usage

---

## Authentication

**Current Implementation:** None (Local development)

**For Production:** Add authentication:

```python
from functools import wraps
from flask import request

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {'error': 'Missing authorization'}, 401
        # Validate token...
        return f(*args, **kwargs)
    return decorated
```

---

## Error Handling

### Error Response Format

All errors follow this format:

```json
{
  "error": "Description of what went wrong"
}
```

### Common Error Codes

| Code | Meaning          | Solution                     |
| ---- | ---------------- | ---------------------------- |
| 200  | OK               | Request successful           |
| 400  | Bad Request      | Check parameters             |
| 413  | Entity Too Large | File/text is too large       |
| 500  | Server Error     | Try again or contact support |

### Debugging Tips

- Check request parameters
- Verify API key is valid
- Check logs for detailed errors
- Ensure proper Content-Type header
- Validate file format and size

---

## Practical Examples

### Example 1: Simple Translation

```javascript
async function translateText() {
  const formData = new FormData();
  formData.append("text", "Hello, how are you?");
  formData.append("targetLanguage", "French");

  const response = await fetch("/api/translate", {
    method: "POST",
    body: formData,
  });

  const result = await response.json();
  console.log(result.translated_text);
  // Output: Bonjour, comment allez-vous?
}
```

### Example 2: File Translation with cURL

```bash
curl -X POST \
  -F "file=@document.pdf" \
  -F "targetLanguage=German" \
  http://localhost:5000/api/translate | python -m json.tool
```

### Example 3: Accuracy Check

```python
import requests

data = {
    'text': 'Machine learning is powerful',
    'targetLanguage': 'Spanish',
    'expectedOutput': 'El aprendizaje automático es poderoso'
}

response = requests.post('http://localhost:5000/api/translate',
                        files={(k, (None, v)) for k, v in data.items()})
result = response.json()

accuracy_percent = result['accuracy'] * 100
print(f"Accuracy: {accuracy_percent:.2f}%")
```

### Example 4: Batch Translation (Multiple Languages)

```javascript
async function translateMultiple(text) {
  const languages = ["Spanish", "French", "German", "Chinese"];
  const results = {};

  for (const lang of languages) {
    const formData = new FormData();
    formData.append("text", text);
    formData.append("targetLanguage", lang);

    const response = await fetch("/api/translate", {
      method: "POST",
      body: formData,
    });

    results[lang] = await response.json();

    // Add delay to respect rate limits
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }

  return results;
}
```

---

## Performance Optimization

### Best Practices

1. **Text Size:** Keep under 5000 characters for optimal speed
2. **Batch Processing:** Group similar translations
3. **Caching:** Cache repeated translations
4. **Async Requests:** Use async/await for non-blocking calls
5. **Error Handling:** Implement retry logic

### Response Time Expectations

- Small text (< 500 chars): 2-3 seconds
- Medium text (500-2000): 3-4 seconds
- Large text (2000-10000): 5-10 seconds

---

## Webhooks (Future Feature)

Planned webhook support:

```javascript
// Coming soon
POST /api/webhooks
Content-Type: application/json

{
  "url": "https://your-app.com/translations",
  "events": ["translation.completed", "translation.failed"]
}
```

---

## CORS Configuration

For cross-origin requests, add to Flask:

```python
from flask_cors import CORS

CORS(app, resources={r"/api/*": {"origins": "*"}})
```

---

## Changelog

**Version 1.0.0**

- Initial API release
- Translation endpoint
- File upload support
- Accuracy calculation
- Token tracking

---

## Support

For API issues:

1. Check error message carefully
2. Review examples above
3. Verify parameters
4. Check Gemini API status
5. Test with test_api.py

---

**Last Updated:** May 2026  
**API Version:** 1.0.0  
**Status:** Production Ready
