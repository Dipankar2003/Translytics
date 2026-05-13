# Article Translation - Quick Start Guide

Get your Article Translation tool running in 5 minutes!

## Step 1: Get Gemini API Key (2 minutes)

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **"Get API Key"** button
3. Create a new API key
4. Copy the key (you'll use it soon)

## Step 2: Setup Project (2 minutes)

### On Windows (PowerShell):

```powershell
# Navigate to project directory
cd "c:\Users\Dipankar Dubey\Desktop\LangChain Practice\langchain_In_Detail"

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### On macOS/Linux:

```bash
cd langchain_In_Detail
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 3: Configure API Key (1 minute)

Create a `.env` file in the project folder with:

```env
GEMINI_API_KEY=paste_your_api_key_here
```

**Replace `paste_your_api_key_here` with your actual Gemini API key**

## Step 4: Run the Application

```bash
python app.py
```

You'll see:

```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

## Step 5: Open in Browser

Open your browser and go to:

```
http://localhost:5000
```

You should see the Article Translation interface!

---

## ✅ You're All Set!

### Try a Test Translation:

1. **Paste Sample Text:**

   ```
   Artificial Intelligence is transforming how we work,
   learn, and communicate. Machine learning models can
   now understand context and nuance like never before.
   ```

2. **Select Language:** Spanish

3. **Click:** "🚀 Translate Article"

4. **Wait 2-3 seconds** for the magic to happen!

---

## Troubleshooting Quick Fixes

### "GEMINI_API_KEY not found" error?

- ✅ Check if `.env` file exists in the project root
- ✅ Verify the API key is copied correctly
- ✅ Restart the Flask app after creating `.env`

### "ModuleNotFoundError" when starting?

```bash
# Make sure you're in virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Then install again
pip install -r requirements.txt
```

### Port 5000 already in use?

Edit `app.py` last line:

```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change to 5001
```

---

## Key Features Ready to Use

✨ **Text Input** - Paste articles directly  
📤 **File Upload** - Upload .txt or .pdf files  
🌍 **12+ Languages** - Spanish, French, German, Chinese, Japanese, Hindi, Portuguese, Russian, Italian, Arabic, Dutch, Korean  
📊 **Metrics** - Track token usage and processing time  
✅ **Accuracy Check** - Compare with expected translations  
🎨 **Modern Design** - Beautiful, responsive interface

---

## Next Steps

1. **Test with different languages** from the dropdown
2. **Upload a PDF or TXT file** to translate entire documents
3. **Add expected output** to see accuracy calculations
4. **Check token usage** to track API costs

---

## Need Help?

Check the full `README.md` for:

- Detailed feature overview
- Configuration options
- Deployment instructions
- Advanced customization

---

**Happy Translating! 🚀📝🌍**
