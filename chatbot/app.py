import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flask import Flask, request, jsonify, render_template, send_from_directory
from search_engine import web_search, search_codebase, call_gemini_api, local_synthesis_fallback, detect_conversational_query

app = Flask(__name__, 
            static_folder='static', 
            template_folder='templates')

# Create static and templates folders if they don't exist
os.makedirs(os.path.join(os.path.dirname(__file__), 'static'), exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(__file__), 'templates'), exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json or {}
    query = data.get('query', '').strip()
    mode = data.get('mode', 'all')  # 'web', 'codebase', 'ai', 'all'
    api_key = data.get('apiKey', '').strip()
    model = data.get('model', 'gemini-1.5-flash').strip()
    history = data.get('history', [])

    if not query:
        return jsonify({"response": "Please enter a valid query."}), 400

    # Bypassing slow web/codebase searches for basic local greetings/prompts if no api_key
    if not api_key:
        conv_response = detect_conversational_query(query, mode)
        if conv_response:
            return jsonify({
                "response": conv_response,
                "web_results": [],
                "codebase_results": [],
                "invalid_api_key": False
            })

    web_results = []
    codebase_results = []
    is_invalid_key = False

    # 1. Fetch relevant contexts based on mode
    if mode in ['web', 'all', 'recruitment']:
        web_results = web_search(query)
        
    if mode in ['codebase', 'all']:
        codebase_results = search_codebase(query)

    # 2. Generate final answer
    if mode == 'ai' or api_key:
        # If user selected AI mode or provided an API key in other modes, use Gemini
        if not api_key:
            return jsonify({
                "response": "⚠️ **Error**: AI mode requires a Google Gemini API Key. Please click the Settings icon in the header to enter your API key, or switch to Web/Codebase modes to use the fallback engine.",
                "web_results": [],
                "codebase_results": []
            })
        
        response_text = call_gemini_api(
            api_key=api_key,
            query=query,
            web_results=web_results,
            codebase_results=codebase_results,
            chat_history=history,
            model=model,
            mode=mode
        )
        
        # Check if Gemini failed due to quota/invalid key, and fallback to synthesis
        if response_text.startswith("GEMINI_API_ERROR:"):
            err_details = response_text.replace("GEMINI_API_ERROR: ", "")
            err_lower = err_details.lower()
            
            if "api key not valid" in err_lower or "invalid" in err_lower or "key not found" in err_lower or "unauthorized" in err_lower or ("key" in err_lower and "not valid" in err_lower):
                is_invalid_key = True
                fallback_warning = (
                    f"⚠️ **Invalid Gemini API Key Cleared**\n\n"
                    f"_The API key saved in your settings is invalid ({err_details})._\n\n"
                    f"👉 **Self-Healed**: We detected this key was invalid and have automatically cleared it from your browser settings so you won't see this warning again. "
                    f"Fell back to the Local Synthesis Engine for this request.\n\n"
                )
            else:
                fallback_warning = (
                    f"⚠️ **Gemini API Error ({err_details})**\n\n"
                    f"_Your API key daily quota was exceeded, or it doesn't support the selected model. "
                    f"Automatically fell back to the Local Synthesis Engine so you still get a response!_\n\n"
                )
            local_response = local_synthesis_fallback(
                query=query,
                web_results=web_results,
                codebase_results=codebase_results,
                mode=mode
            )
            response_text = fallback_warning + local_response
    else:
        # Standard search fallback synthesis
        response_text = local_synthesis_fallback(
            query=query,
            web_results=web_results,
            codebase_results=codebase_results,
            mode=mode
        )

    return jsonify({
        "response": response_text,
        "web_results": web_results,
        "codebase_results": codebase_results,
        "invalid_api_key": is_invalid_key
    })

@app.route('/api/codebase-files', methods=['GET'])
def codebase_files():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    target_files = ['game.py', 'entities.py', 'physics.py', 'ai.py', 'README.md']
    files_info = []
    
    for filename in target_files:
        filepath = os.path.join(root_dir, filename)
        if os.path.isfile(filepath):
            size = os.path.getsize(filepath)
            files_info.append({
                "name": filename,
                "size_kb": round(size / 1024, 2),
                "path": filepath
            })
            
    return jsonify({"files": files_info})

@app.route('/api/validate-key', methods=['POST'])
def validate_key():
    import requests
    data = request.json or {}
    api_key = data.get('apiKey', '').strip()
    model = data.get('model', 'gemini-1.5-flash').strip()
    
    if not api_key:
        return jsonify({"valid": False, "error": "API Key is empty."})
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"role": "user", "parts": [{"text": "Hello"}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            return jsonify({"valid": True})
        else:
            try:
                error_msg = response.json().get("error", {}).get("message", "Unknown API error")
            except Exception:
                error_msg = f"HTTP Error {response.status_code}"
            return jsonify({"valid": False, "error": error_msg})
    except Exception as e:
        return jsonify({"valid": False, "error": str(e)})

if __name__ == '__main__':
    print("--------------------------------------------------")
    print("SAP-CHAT-BOT - Smart AI Search Assistant Running!")
    print("Open http://127.0.0.1:5000 in your browser")
    print("--------------------------------------------------")
    app.run(debug=True, host='127.0.0.1', port=5000)
