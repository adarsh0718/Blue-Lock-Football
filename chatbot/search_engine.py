import os
import re
import urllib.parse
import requests
from html.parser import HTMLParser

class MojeekParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.results = []
        self.current_result = {}
        self.in_result = False
        self.in_title = False
        self.in_snippet = False
        self.title_data = []
        self.snippet_data = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        class_name = attrs_dict.get('class', '')

        # Mojeek results are in <li> elements with class starting with r followed by a number
        if tag == 'li' and re.match(r'^r\d+', class_name):
            self.in_result = True
            self.current_result = {'title': '', 'link': '', 'snippet': ''}
        elif self.in_result and tag == 'a' and class_name == 'title':
            self.in_title = True
            self.current_result['link'] = attrs_dict.get('href', '')
            self.title_data = []
        elif self.in_result and tag == 'p' and class_name == 's':
            self.in_snippet = True
            self.snippet_data = []

    def handle_endtag(self, tag):
        if tag == 'li' and self.in_result:
            if self.title_data:
                self.current_result['title'] = "".join(self.title_data).strip()
            if self.snippet_data:
                self.current_result['snippet'] = "".join(self.snippet_data).strip()
            
            # Save if valid
            if self.current_result.get('title') and self.current_result.get('link'):
                self.results.append(self.current_result)
            self.in_result = False
            self.current_result = {}
            self.title_data = []
            self.snippet_data = []
        elif tag == 'a' and self.in_title:
            self.in_title = False
        elif tag == 'p' and self.in_snippet:
            self.in_snippet = False

    def handle_data(self, data):
        if self.in_title:
            self.title_data.append(data)
        elif self.in_snippet:
            self.snippet_data.append(data)


def clean_and_simplify_query(query):
    """
    Cleans common typos and strips conversational question starters
    to extract core keywords for search engines.
    """
    # Fix spelling typos
    query = re.sub(r'\byeasterday\'?s\b', 'yesterday', query, flags=re.IGNORECASE)
    query = re.sub(r'\byeasterday\b', 'yesterday', query, flags=re.IGNORECASE)
    query = re.sub(r'\btommorrow\b', 'tomorrow', query, flags=re.IGNORECASE)
    
    # Strip common question prefix phrases to isolate core subject
    cleaned = re.sub(
        r'\b(who won yesterday\'s match|who won the yesterday\'s match|who won the match|who won|what is the definition of|what is|how to make|how to|where can i find|where is|why is|explain the|tell me about|yesterday\'s match|yesterday match)\b',
        '',
        query,
        flags=re.IGNORECASE
    )
    cleaned = cleaned.strip('? .!,')
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


def web_search(query, max_results=5, is_retry=False):
    """
    Queries Mojeek search engine and returns clean search results.
    If 0 results are found, it simplifies the query and retries once.
    """
    url = "https://www.mojeek.com/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    params = {"q": query}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code != 200:
            return [{"title": "Search Error", "link": "", "snippet": f"HTTP error {response.status_code} while contacting Mojeek."}]
        
        parser = MojeekParser()
        parser.feed(response.text)
        
        # Deduplicate and filter empty links
        seen_links = set()
        unique_results = []
        for r in parser.results:
            link = r.get('link', '')
            if link and link not in seen_links:
                seen_links.add(link)
                unique_results.append(r)
                
        results = unique_results[:max_results]
        
        # If no results found, try to simplify and retry once
        if not results and not is_retry:
            simplified = clean_and_simplify_query(query)
            if simplified and simplified.lower() != query.lower():
                print(f"No results for '{query}'. Retrying with simplified: '{simplified}'")
                return web_search(simplified, max_results=max_results, is_retry=True)
                
        return results
    except Exception as e:
        return [{"title": "Search Exception", "link": "", "snippet": f"An error occurred: {str(e)}"}]


def search_codebase(query, root_dir=None):
    """
    Searches Python codebase files in the specified directory.
    Returns matching files, line numbers, and snippets with context.
    """
    if root_dir is None:
        # Default to parent of chatbot directory (which is workspace root)
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        
    results = []
    # Files we want to search
    target_files = ['game.py', 'entities.py', 'physics.py', 'ai.py', 'README.md']
    
    # Compile regex or match case-insensitive
    try:
        rx = re.compile(query, re.IGNORECASE)
    except re.error:
        # Fallback to literal search if regex is invalid
        rx = re.compile(re.escape(query), re.IGNORECASE)
        
    for filename in target_files:
        filepath = os.path.join(root_dir, filename)
        if not os.path.isfile(filepath):
            continue
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for idx, line in enumerate(lines):
                if rx.search(line):
                    line_num = idx + 1
                    
                    # Extract surrounding context (3 lines before, 3 lines after)
                    start_ctx = max(0, idx - 3)
                    end_ctx = min(len(lines), idx + 4)
                    
                    context_lines = []
                    for c_idx in range(start_ctx, end_ctx):
                        c_line_num = c_idx + 1
                        prefix = ">>> " if c_idx == idx else "    "
                        context_lines.append(f"{c_line_num}:{prefix}{lines[c_idx].rstrip()}")
                        
                    results.append({
                        "file": filename,
                        "line": line_num,
                        "match": line.strip(),
                        "context": "\n".join(context_lines)
                    })
        except Exception as e:
            # Skip if error reading file
            continue
            
    # Limit to top 15 matches to prevent context explosion
    return results[:15]


def call_gemini_api(api_key, query, web_results, codebase_results, chat_history=None, model="gemini-2.0-flash", mode="ai"):
    """
    Communicates with Google Gemini API using raw POST requests.
    Injects web search and codebase search context.
    """
    # Use v1beta endpoint to support systemInstruction properly on all models
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    # 1. Prepare system instruction
    if mode == "recruitment":
        system_instruction = (
            "You are SAP-CHAT-BOT in Recruitment Assistant mode. You are an expert HR manager, recruiter, "
            "technical interviewer, and career coach. Your goal is to help the user with career planning, "
            "resume building, cover letter drafting, interview preparation, and job searching.\n\n"
            "Analyze the user's queries and provide highly professional advice. "
            "If provided with web search results, use them to find current job opportunities, salary trends, or hiring metrics. "
            "Structure your output cleanly with bullet points and bold section headers (ChatGPT style)."
        )
    else:
        system_instruction = (
            "You are SAP-CHAT-BOT, an advanced and intelligent AI search assistant. "
            "You specialize in software engineering, general knowledge, web research, and code analysis.\n\n"
            "To help you answer the user's query, you will be provided with real-time web search results "
            "and local codebase file search matches if applicable. Synthesize this information cleanly.\n"
            "Cite web search results using brackets like [1], [2] next to their relevant information. "
            "Cite codebase references using file names and line numbers. "
            "Be helpful, concise, accurate, and well-structured in your explanations."
        )
    
    # 2. Build context blocks
    context_str = ""
    
    if web_results:
        context_str += "### WEB SEARCH RESULTS:\n"
        for i, r in enumerate(web_results):
            context_str += f"[{i+1}] Title: {r.get('title')}\nURL: {r.get('link')}\nSnippet: {r.get('snippet')}\n\n"
            
    if codebase_results:
        context_str += "### LOCAL CODEBASE MATCHES:\n"
        for r in codebase_results:
            context_str += f"File: {r['file']} (Line {r['line']})\nMatched line: {r['match']}\nContext:\n```python\n{r['context']}\n```\n\n"
            
    # 3. Assemble chat contents payload
    contents = []
    
    # Load chat history
    if chat_history:
        for msg in chat_history:
            contents.append({
                "role": "user" if msg["role"] == "user" else "model",
                "parts": [{"text": msg["content"]}]
            })
            
    # Inject current message with context
    current_prompt = query
    if context_str:
        current_prompt = f"Here is the context for the query:\n{context_str}\nUser Question: {query}"
        
    contents.append({
        "role": "user",
        "parts": [{"text": current_prompt}]
    })
    
    payload = {
        "contents": contents,
        "systemInstruction": {
            "parts": [{"text": system_instruction}]
        },
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 2048
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response_json = response.json()
        
        if response.status_code == 200:
            try:
                text = response_json["candidates"][0]["content"]["parts"][0]["text"]
                return text
            except (KeyError, IndexError):
                return "GEMINI_API_ERROR: 200 - Could not parse response content from Gemini API."
        else:
            error_details = response_json.get("error", {})
            error_msg = error_details.get("message", "Unknown error")
            
            # If the error is clearly an invalid API key, do not retry with another model.
            # Return the error immediately so that the self-healing system can detect it and clear it.
            err_lower = error_msg.lower()
            if any(term in err_lower for term in ["api key not valid", "invalid", "key not found", "unauthorized", "not valid"]):
                return f"GEMINI_API_ERROR: {response.status_code} - {error_msg}"
            
            # Auto-fallback to gemini-1.5-flash if the current model failed and is not already gemini-1.5-flash
            stable_model = "gemini-1.5-flash"
            if model != stable_model:
                print(f"Model {model} failed with code {response.status_code}. Retrying with {stable_model}...")
                return call_gemini_api(api_key, query, web_results, codebase_results, chat_history, model=stable_model, mode=mode)
            
            return f"GEMINI_API_ERROR: {response.status_code} - {error_msg}"
            
    except Exception as e:
        # Auto-fallback to gemini-1.5-flash on network exception if not already trying it
        stable_model = "gemini-1.5-flash"
        if model != stable_model:
            print(f"Failed to connect to {model} ({str(e)}). Retrying with {stable_model}...")
            return call_gemini_api(api_key, query, web_results, codebase_results, chat_history, model=stable_model, mode=mode)
        return f"GEMINI_API_ERROR: 500 - Failed to connect to Gemini API: {str(e)}"


def get_wikipedia_summary(query):
    """
    Fetches Wikipedia page summary for the query using search + REST summary API.
    """
    try:
        # Filter query to check relevance
        stop_words = {'what', 'who', 'is', 'are', 'was', 'were', 'the', 'a', 'an', 'and', 'or', 'of', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'how', 'why', 'where', 'when', 'method', 'function', 'class', 'python', 'code', 'file', 'explain', 'describe', 'about', 'def', 'import', 'from', 'return', 'self', 'init', 'str', 'main', 'if', 'else', 'elif', 'for', 'while', 'try', 'except', 'pass'}
        query_words = set(re.findall(r'\b\w+\b', query.lower())) - stop_words
        
        search_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "utf8": 1
        }
        headers = {"User-Agent": "SAP-CHAT-BOT/1.0 (contact@sapchatbot.com)"}
        res = requests.get(search_url, params=params, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            search_results = data.get("query", {}).get("search", [])
            if search_results:
                best_title = search_results[0]["title"]
                
                # Check if the title is relevant to the query words
                is_relevant = False
                if not query_words:
                    is_relevant = True
                else:
                    for q_word in query_words:
                        if len(q_word) >= 2 and q_word in best_title.lower():
                            is_relevant = True
                            break
                            
                if not is_relevant:
                    return None
                    
                summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(best_title)}"
                res_summary = requests.get(summary_url, headers=headers, timeout=5)
                if res_summary.status_code == 200:
                    summary_data = res_summary.json()
                    return {
                        "title": summary_data.get("title"),
                        "extract": summary_data.get("extract"),
                        "url": summary_data.get("content_urls", {}).get("desktop", {}).get("page")
                    }
    except Exception:
        pass
    return None


def get_ddg_instant_answer(query):
    """
    Fetches DuckDuckGo instant answer/abstract for the query.
    """
    try:
        url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1&skip_disambig=1"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code in [200, 202]:
            data = res.json()
            abstract = data.get("AbstractText", "")
            answer = data.get("Answer", "")
            definition = data.get("Definition", "")
            text = abstract or answer or definition
            if text:
                return {
                    "text": text,
                    "url": data.get("AbstractURL", "") or data.get("DefinitionURL", "")
                }
    except Exception:
        pass
    return None


def detect_conversational_query(query, mode="all"):
    """
    Detects basic conversational messages (greetings, small talk, identity questions)
    and returns a helpful, formatted ChatGPT-style response.
    Returns None if the query is not a basic conversational query.
    """
    clean_query = query.strip().lower()
    
    # Strip basic punctuation
    clean_query = re.sub(r'[?.!,]', '', clean_query).strip()
    
    # 1. Greetings
    greetings = [
        r'\b(hi|hello|hey|yo|sup|hola|greetings|howdy|hiya|heyy+)\b',
        r'\b(good\s+(morning|afternoon|evening|night))\b',
        r'^hi$'
    ]
    if any(re.search(pat, clean_query) for pat in greetings):
        if mode == "recruitment":
            return (
                "### 💼 Recruitment Assistant: Welcome! 👋\n\n"
                "Hello there! I am your dedicated **Recruitment & Career Coach** operating in local helper mode.\n\n"
                "I can assist you with:\n"
                "- 📝 **Resumes & CVs**: Formatting, content optimization, ATS compatibility tips.\n"
                "- ✉️ **Cover Letters**: Structure, templates, drafting advice.\n"
                "- 🤝 **Interview Prep**: Mock interview questions, strategy checklists, behavioral STAR method guidance.\n"
                "- 📄 **Job Descriptions**: Writing specs, defining core competencies.\n\n"
                "**How would you like to start?** Tell me about the role you are targeting or paste a section of your resume!\n\n"
                "--- \n"
                "🔑 *Note: To unlock custom AI suggestions and full conversational reviews, enter your free **Gemini API Key** in Settings (⚙️).* "
                "You can get one at [Google AI Studio](https://aistudio.google.com/app/apikey)."
            )
        else:
            return (
                "### 🤖 Welcome to SAP-CHAT-BOT! 👋\n\n"
                "Hello! I'm your smart assistant, running in **Local Fallback Mode**.\n\n"
                "Since you haven't added a Gemini API key yet, I can still help you with:\n"
                "- 🔍 **Deep Search**: Combined web search (via Mojeek) + local game codebase analysis.\n"
                "- 🌐 **Web Search**: Real-time summaries of current internet topics.\n"
                "- 📂 **Codebase Scan**: Match keywords/regex across your local python files (`game.py`, `entities.py`, etc.).\n"
                "- 💼 **Recruitment**: Professional resume, cover letter, and interview prep guides.\n\n"
                "Ask me anything, or type a query to search!\n\n"
                "--- \n"
                "🔑 *Tip: For full conversational AI capability like ChatGPT, grab a free **Gemini API Key** from [Google AI Studio](https://aistudio.google.com/app/apikey) "
                "and paste it in Settings (⚙️).* "
            )

    # 2. Well-being / How are you
    well_being = [
        r'\b(how\s+are\s+you|how\s+r\s+u|hows\s+it\s+going|how\'s\s+it\s+going|how\s+do\s+you\s+do|whats\s+up|what\'s\s+up|are\s+you\s+(ok|okay|well))\b'
    ]
    if any(re.search(pat, clean_query) for pat in well_being):
        return (
            "### 🤖 System Status: Fully Operational! 🚀\n\n"
            "I'm doing great, thank you for asking! As an AI assistant, I'm ready to search, analyze, and assist with your codebase or career needs.\n\n"
            "How can I help you today? Would you like to:\n"
            "- Scan the goalkeeper AI logic in `ai.py`?\n"
            "- Build a resume or practice for an interview?\n"
            "- Search the web for recent soccer match details?\n\n"
            "--- \n"
            "🔑 *Friendly reminder: Enter a free Gemini API Key via ⚙️ to experience full ChatGPT-like cognitive responses!*"
        )

    # 3. Identity / Creator
    identity = [
        r'\b(who\s+are\s+you|what\s+is\s+your\s+name|your\s+name|what\'s\s+your\s+name|who\s+made\s+you|who\s+created\s+you|are\s+you\s+human|what\s+are\s+you|who\s+is\s+your\s+creator|who\s+is\s+your\s+maker)\b'
    ]
    if any(re.search(pat, clean_query) for pat in identity):
        return (
            "### 🤖 Identity Profile: SAP-CHAT-BOT\n\n"
            "I am **SAP-CHAT-BOT**, a premium AI search assistant and developer companion.\n\n"
            "**Key Specifications:**\n"
            "- **Developer**: Custom-tailored for the Blue Lock Football game development workspace.\n"
            "- **Capabilities**: Web parsing (Mojeek + Wikipedia + DuckDuckGo), local code regex indexing, and recruitment templates.\n"
            "- **AI Engine**: Supports Google Gemini API integration (1.5 Flash, 2.0 Flash, 1.5 Pro) for advanced logical reasoning.\n\n"
            "--- \n"
            "🔑 *Need full ChatGPT capabilities?* Generate a free API key at [Google AI Studio](https://aistudio.google.com/app/apikey) and insert it into the **Settings (⚙️)** panel."
        )

    # 4. Capabilities / Help / Features
    capabilities = [
        r'\b(what\s+can\s+you\s+do|help|help\s+me|features|capabilities|commands|how\s+to\s+use|explain\s+yourself)\b',
        r'^help$'
    ]
    if any(re.search(pat, clean_query) for pat in capabilities):
        return (
            "### 🛠️ SAP-CHAT-BOT Capability Guide\n\n"
            "I am designed to serve as a high-fidelity assistant in two modes: **Local Fallback Mode** (no API key) and **Gemini AI Mode** (with API key).\n\n"
            "#### 🔌 1. Local Fallback Mode (Current Mode)\n"
            "- **🌐 Web Search**: Simply enter a query (e.g. *'latest AI news'*). I will scrape Mojeek and compile key snippets.\n"
            "- **📚 Knowledge Lookup**: Queries Wikipedia & DuckDuckGo APIs instantly to fetch summaries.\n"
            "- **📂 Codebase Indexing**: Matches queries against files like `game.py` and `entities.py`. (Try: *'goalkeeper physics'*).\n"
            "- **💼 Recruitment**: Provides comprehensive offline templates for resumes, cover letters, and mock interviews.\n\n"
            "#### 🚀 2. Gemini AI Mode (With API Key)\n"
            "- **🧠 Smart Synthesis**: Synthesizes search results and codebase context with advanced reasoning.\n"
            "- **✍️ Writing & Coding**: Fully drafts scripts, custom cover letters, and handles general logical queries like ChatGPT.\n"
            "- **💬 Thread Context**: Remembers conversation history within the thread.\n\n"
            "--- \n"
            "🔑 **Quick Setup**: Get your free Gemini API Key [here](https://aistudio.google.com/app/apikey) and enter it in Settings (⚙️)!"
        )

    # 5. Gratitude / Appreciation
    gratitude = [
        r'\b(thank\s+you|thanks|ty|thx|thank\s+u|appreciate\s+it|great\s+job|awesome|cool|perfect|wonderful|nice)\b'
    ]
    if any(re.search(pat, clean_query) for pat in gratitude):
        return (
            "### 🤖 You're Welcome! 😊\n\n"
            "It is my pleasure to help! Let me know if there's anything else you'd like to search, code to review, or templates to draft.\n\n"
            "If you want to keep talking, feel free to ask your next question!"
        )

    # 6. Farewell
    farewell = [
        r'\b(bye|goodbye|see\s+you|cya|talk\s+to\s+you\s+later|later|exit|quit|goodnight)\b'
    ]
    if any(re.search(pat, clean_query) for pat in farewell):
        return (
            "### 🤖 Goodbye! 👋\n\n"
            "Have a great day! Don't hesitate to reach out if you need more codebase analysis or web search assistance in the future. "
            "You can start a new conversation using the **➕ New Chat** button in the sidebar. See you next time!"
        )

    # 7. Jokes / Entertainment
    jokes = [
        r'\b(joke|jokes|tell\s+me\s+a\s+joke|make\s+me\s+laugh|funny)\b'
    ]
    if any(re.search(pat, clean_query) for pat in jokes):
        import random
        jokes_list = [
            "**Why do programmers wear glasses?**\n\n*Because they can't C#!* 🤓",
            "**How many programmers does it take to change a lightbulb?**\n\n*None, that's a hardware problem!* 💡",
            "**Why do Java developers wear glasses?**\n\n*Because they don't C#!* ☕",
            "**['hip', 'hip']**\n\n*(hip hip array!)* 🥳",
            "**There are 10 types of people in this world:**\n\n*Those who understand binary, and those who don't.* 🔢",
            "**Why did the computer go to the doctor?**\n\n*Because it had a virus!* 🦠",
            "**What is a programmer's favorite place to hang out?**\n\n*The Foo Bar.* 🍻"
        ]
        selected_joke = random.choice(jokes_list)
        return (
            f"### 🤖 Humor Module: Active! 🎭\n\n"
            f"{selected_joke}\n\n"
            f"--- \n"
            f"🔑 *Want more complex AI-generated humor or creative writing? Add a Gemini API Key via ⚙️ Settings!*"
        )

    # 8. General Knowledge / Small Talk prompts
    general_short = [
        r'\b(what\s+is\s+love|tell\s+me\s+about\s+yourself|who\s+are\s+we|are\s+you\s+sentient|what\s+do\s+you\s+think|do\s+you\s+have\s+feelings)\b'
    ]
    if any(re.search(pat, clean_query) for pat in general_short):
        return (
            "### 🤖 Conversational Fallback\n\n"
            "I'm operating in **Local Fallback Mode**, which means I don't have active generative reasoning for deep philosophical or conversational topics.\n\n"
            "However, you can:\n"
            "1. 🌐 **Search the web** about this topic by adding search keywords.\n"
            "2. 🔑 **Unlock full AI responses** like ChatGPT by adding a free Gemini API Key in the **Settings (⚙️)** panel. "
            "Get yours at [Google AI Studio](https://aistudio.google.com/app/apikey) in under a minute!"
        )

    # 9. Code templates or coding prompts
    code_prompts = [
        r'\b(write\s+code|code\s+template|coding\s+help|programming\s+help|python\s+code|html\s+code|css\s+code|javascript\s+code|write\s+a\s+python|write\s+a\s+function|write\s+a\s+program|how\s+to\s+program|how\s+to\s+code|code\s+for)\b'
    ]
    if any(re.search(pat, clean_query) for pat in code_prompts):
        return (
            "### 💻 Local Coding Assistant (Offline)\n\n"
            "To write code or get expert programming assistance, we highly recommend setting up a **Gemini API Key** (click ⚙️ in the header).\n\n"
            "In offline fallback mode, I can help you search the current game workspace files for inspiration. Here are the files we can scan:\n"
            "- `game.py`: Main game loop, rendering, screen setup, game state management.\n"
            "- `entities.py`: Player, Ball, and Opponent classes and attributes.\n"
            "- `physics.py`: Collision detection, velocity updates, and boundary conditions.\n"
            "- `ai.py`: Bot AI, goalkeeper actions, and movement state machines.\n\n"
            "**Try querying a specific code keyword** like: `def update` or `class Player` to view matching code blocks!"
        )

    return None


def local_synthesis_fallback(query, web_results, codebase_results, mode="all"):
    """
    Generates a structured answer when no Gemini API key is available.
    Combines Wikipedia summaries, DDG instant answers, search results, and codebase matches.
    """
    # Check for basic conversational queries first
    conv_response = detect_conversational_query(query, mode)
    if conv_response:
        return conv_response

    response_parts = []
    
    if mode == "recruitment":
        response_parts.append("### 💼 Recruitment & Career Assistant (Offline/Fallback Mode)")
        response_parts.append("_Note: To enable full AI evaluations and customized answers, please enter your Gemini API Key in the configurations._\n")
    else:
        response_parts.append("### 🤖 Local Synthesis Engine (Offline/Fallback Mode)")
        response_parts.append("_Note: To enable full conversational AI summaries, please add a Gemini API Key in the UI settings._\n")
    
    # 1. Fetch Wikipedia summary
    wiki_info = get_wikipedia_summary(query)
    if wiki_info and wiki_info.get("extract"):
        response_parts.append(f"#### 📚 Wikipedia Knowledge: **{wiki_info['title']}**")
        response_parts.append(f"{wiki_info['extract']}")
        if wiki_info.get("url"):
            response_parts.append(f"> 🔗 **Read more**: [Wikipedia Article]({wiki_info['url']})")
        response_parts.append("")

    # 2. Fetch DDG instant answer (if different from Wikipedia or if Wikipedia wasn't found)
    ddg_info = get_ddg_instant_answer(query)
    if ddg_info and ddg_info.get("text"):
        # Avoid duplicating if Wiki is already showing it
        wiki_text_sample = wiki_info.get("extract", "").lower()[:50] if wiki_info else ""
        ddg_text_sample = ddg_info["text"].lower()[:50]
        if wiki_text_sample != ddg_text_sample:
            response_parts.append("#### 💡 Quick Fact:")
            response_parts.append(f"{ddg_info['text']}")
            if ddg_info.get("url"):
                response_parts.append(f"> 🔗 **Source**: [DuckDuckGo Link]({ddg_info['url']})")
            response_parts.append("")

    # 3. Recruitment Assistant specialized templates
    if mode == "recruitment":
        q_lower = query.lower()
        if "resume" in q_lower or "cv" in q_lower or "curriculum" in q_lower:
            response_parts.append("#### 📝 ATS-Optimized Resume Template:")
            response_parts.append(
                "A proper resume should be structured as follows to maximize ATS performance:\n"
                "- **Header**: Full Name, Professional Email, LinkedIn Profile, GitHub Link, Phone Number.\n"
                "- **Professional Summary**: A 3-4 sentence paragraph highlighting key accomplishments, core technologies, and career direction.\n"
                "- **Technical Skills**: Categorized lists of programming languages, frameworks, developer tools, and databases.\n"
                "- **Professional Experience**:\n"
                "  - *Job Title*, *Company* (Dates of employment)\n"
                "  - Format bullet points using Google's X-Y-Z formula: *'Accomplished [X], as measured by [Y], by doing [Z]'*.\n"
                "- **Key Projects**: Highlight 2-3 personal or open-source projects with active links and lists of technologies used.\n"
                "- **Education**: Degree, major, institution, graduation date, and honors."
            )
            response_parts.append("")
        elif "interview" in q_lower or "mock" in q_lower or "questions" in q_lower:
            response_parts.append("#### 📝 Interview Prep Checklist:")
            response_parts.append(
                "Be prepared for technical and behavioral interviews using this checklist:\n"
                "1. **Company Research**: Analyze their product offering, tech stack, and corporate values.\n"
                "2. **STAR Framework**: Structure stories for behavioral questions (Situation, Task, Action, Result).\n"
                "3. **Technical Preparation**: Review core concepts (data structures, system design patterns, or engineering standards).\n"
                "4. **Questions to Ask**: Prepare 3-4 insightful questions regarding team dynamics, challenges, or roadmap plans.\n"
                "5. **Technical Interview Questions (General)**:\n"
                "   - *'Can you walk me through a complex technical challenge you solved?'*\n"
                "   - *'How do you handle technical debt or refactoring priorities under tight deadlines?'*"
            )
            response_parts.append("")
        elif "cover letter" in q_lower or "letter" in q_lower:
            response_parts.append("#### 📝 Professional Cover Letter Template:")
            response_parts.append(
                "A standard cover letter should follow this professional structure:\n"
                "- **Salutation**: *'Dear [Hiring Manager Name / Recruiting Team Name],'*\n"
                "- **Introductory Paragraph**: Declare the position you are applying for, express why the company's mission resonates with you, and give a brief overview of your fitness.\n"
                "- **Core Body Paragraph**: Focus on a major quantitative achievement that shows you can solve their current problems.\n"
                "- **Secondary Body Paragraph**: Discuss key skills, adaptability, and cultural alignment.\n"
                "- **Call to Action**: Thank them for their time, reference your portfolio, and state your availability for a call.\n"
                "- **Sign-off**: *'Sincerely, [Your Name]'*"
            )
            response_parts.append("")
        elif "job description" in q_lower or "jd" in q_lower or "hire" in q_lower or "recru" in q_lower:
            response_parts.append("#### 📝 Competency-Based Job Description Layout:")
            response_parts.append(
                "Use this framework to write compelling job descriptions that attract top talent:\n"
                "- **Job Title & Level**: (e.g. Senior Backend Engineer)\n"
                "- **About the Role**: A summary paragraph of the role's mission and how they fit into the company.\n"
                "- **Core Responsibilities**:\n"
                "  - Design, develop, and maintain clean, performant code.\n"
                "  - Collaborate in cross-functional design sprints and code reviews.\n"
                "  - Identify bottlenecks and optimize API latency.\n"
                "- **Must-Have Requirements**: Years of experience in specific languages, frameworks, or database structures.\n"
                "- **Preferred Qualifications**: Nice-to-have items, soft skills, or experience with devops/cloud infrastructure."
            )
            response_parts.append("")

    # 4. Add codebase matches
    if codebase_results:
        response_parts.append("#### 📂 Codebase Search Matches:")
        files_matched = {}
        for r in codebase_results:
            files_matched.setdefault(r['file'], []).append(r)
            
        for filename, matches in files_matched.items():
            response_parts.append(f"- **{filename}** (found {len(matches)} occurrences):")
            for m in matches[:2]:  # Limit context window to 2 matches to prevent page bloat
                response_parts.append(f"  - **Line {m['line']}**: `{m['match']}`")
                response_parts.append(f"    ```python\n{m['context']}\n    ```")
            if len(matches) > 2:
                response_parts.append(f"  - _and {len(matches) - 2} more occurrences in this file..._")
        response_parts.append("")

    # 5. Add web search summary and results
    if web_results:
        response_parts.append("#### 🌐 Web Search Synthesis:")
        response_parts.append("Based on top search results:")
        for idx, r in enumerate(web_results[:3]):
            title = r.get('title', 'No Title')
            link = r.get('link', '')
            snippet = r.get('snippet', 'No snippet available.')
            link_markdown = f"[{title}]({link})" if link else title
            response_parts.append(f"- **{link_markdown}**: {snippet}")
        
        # List other web results as reference
        if len(web_results) > 3:
            response_parts.append("\n**Other Reference Results:**")
            for idx, r in enumerate(web_results[3:], start=4):
                title = r.get('title', 'No Title')
                link = r.get('link', '')
                link_markdown = f"[{title}]({link})" if link else title
                response_parts.append(f"{idx}. {link_markdown}")
        response_parts.append("")
        
    if not wiki_info and not ddg_info and not web_results and not codebase_results:
        response_parts.append(f"No results found for query: **{query}**.\n\nTry adjusting your search terms.")
        
    return "\n".join(response_parts)
