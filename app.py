from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import PyPDF2
import google.generativeai as genai
from difflib import SequenceMatcher
import re
import traceback
from config import app_config  # ✅ Use config

load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = app_config.UPLOAD_FOLDER
ALLOWED_EXTENSIONS = app_config.ALLOWED_EXTENSIONS

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = app_config.MAX_CONTENT_LENGTH

GEMINI_API_KEY = app_config.GEMINI_API_KEY
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=GEMINI_API_KEY)

# ✅ Uses model from config (gemini-2.0-flash)
model = genai.GenerativeModel(app_config.GEMINI_MODEL)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(file_path, file_type):
    try:
        if file_type == 'txt':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        elif file_type == 'pdf':
            text = ""
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    extracted = page.extract_text()
                    if extracted:  # ✅ Guard against None pages
                        text += extracted
            return text
    except Exception as e:
        raise Exception(f"Error extracting text from file: {str(e)}")

def count_tokens(text):
    try:
        response = model.count_tokens([text])  # ✅ Wrap in list
        return response.total_tokens
    except Exception:
        return len(text) // 4  # Fallback estimate

def translate_text(text, target_language):
    try:
        translation_prompt = f"""You are an expert translator with deep understanding of context and nuance. 
Your task is to translate the following text into {target_language} while:
1. Preserving the original meaning and tone
2. Maintaining technical terms accurately
3. Ensuring grammatical correctness
4. Keeping the structure and formatting
5. Using culturally appropriate expressions

Original text to translate:
---
{text}
---

Please provide ONLY the translated text without any explanation or prefix."""

        response = model.generate_content(translation_prompt)
        return response.text.strip()
    except Exception as e:
        raise Exception(f"Translation failed: {str(e)}")

def calculate_similarity(text1, text2):
    try:
        text1_normalized = re.sub(r'\s+', ' ', text1.lower().strip())
        text2_normalized = re.sub(r'\s+', ' ', text2.lower().strip())
        return SequenceMatcher(None, text1_normalized, text2_normalized).ratio()
    except Exception as e:
        raise Exception(f"Error calculating similarity: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/translate', methods=['POST'])
def translate():
    try:
        text = request.form.get('text', '').strip()
        file = request.files.get('file')
        target_language = request.form.get('targetLanguage', '').strip()
        expected_output = request.form.get('expectedOutput', '').strip()

        if not target_language:
            return jsonify({'error': 'Target language is required'}), 400

        if file and file.filename != '':
            if not allowed_file(file.filename):
                return jsonify({'error': 'Only .txt and .pdf files are allowed'}), 400

            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            file_type = filename.rsplit('.', 1)[1].lower()
            text = extract_text_from_file(file_path, file_type)

            try:
                os.remove(file_path)
            except:
                pass

        if not text:
            return jsonify({'error': 'No text provided to translate'}), 400

        if len(text) > app_config.MAX_TEXT_LENGTH:
            return jsonify({'error': f'Text is too long. Maximum {app_config.MAX_TEXT_LENGTH} characters allowed'}), 400

        input_tokens = count_tokens(text)
        translated_text = translate_text(text, target_language)
        output_tokens = count_tokens(translated_text)
        total_tokens = input_tokens + output_tokens

        accuracy = None
        if expected_output:
            accuracy = calculate_similarity(translated_text, expected_output)

        return jsonify({
            'original_text': text,
            'translated_text': translated_text,
            'target_language': target_language,
            'tokens_used': total_tokens,
            'accuracy': accuracy,
            'expected_output': expected_output if expected_output else None
        }), 200

    except Exception as e:
        traceback.print_exc()  # ✅ Full error in terminal
        return jsonify({'error': str(e)}), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'File is too large. Maximum 16MB allowed'}), 413

if __name__ == '__main__':
    app.run(debug=app_config.DEBUG, port=5000)