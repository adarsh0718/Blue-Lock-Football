document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const chatMessages = document.getElementById('chat-messages');
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const clearChatBtn = document.getElementById('clear-chat-btn');
    const newChatBtn = document.getElementById('new-chat-btn');
    const codebaseFilesContainer = document.getElementById('codebase-files');
    const activeModeLabel = document.getElementById('active-mode-label');
    const keyNotice = document.getElementById('key-notice');
    
    // Mode toggle buttons
    const modeBtns = document.querySelectorAll('.mode-btn');
    
    // Settings Modal elements
    const settingsToggleBtn = document.getElementById('settings-toggle-btn');
    const settingsModal = document.getElementById('settings-modal');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const saveSettingsBtn = document.getElementById('save-settings-btn');
    const apiKeyInput = document.getElementById('gemini-api-key');
    const toggleKeyVisibility = document.getElementById('toggle-key-visibility');
    const modelSelect = document.getElementById('gemini-model');
    const resultsCountSlider = document.getElementById('search-results-count');
    const resultsCountBadge = document.getElementById('results-count-badge');
    const settingsSaveStatus = document.getElementById('settings-save-status');
    const validateKeyBtn = document.getElementById('validate-key-btn');
    const validationStatus = document.getElementById('validation-status');

    // State
    let currentMode = 'all'; // 'all', 'web', 'codebase', 'ai', 'recruitment'
    let threads = []; // Array of { id: string, title: string, mode: string, messages: Array }
    let activeThreadId = null;
    let chatHistory = [];

    // Load Settings from LocalStorage
    const settings = {
        apiKey: localStorage.getItem('gemini_api_key') || '',
        model: localStorage.getItem('gemini_model') || 'gemini-1.5-flash',
        maxResults: parseInt(localStorage.getItem('max_search_results')) || 5
    };

    // Initialize UI settings
    apiKeyInput.value = settings.apiKey;
    modelSelect.value = settings.model;
    resultsCountSlider.value = settings.maxResults;
    resultsCountBadge.textContent = settings.maxResults;
    updateAPIKeyNotice();

    // Load Threads & Saved History from SessionStorage
    loadThreads();

    // Fetch Codebase Files List
    fetchCodebaseFiles();

    // Event Listeners for Mode Buttons
    modeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            modeBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentMode = btn.dataset.mode;
            
            // Sync current mode to the active thread
            const activeThread = threads.find(t => t.id === activeThreadId);
            if (activeThread) {
                activeThread.mode = currentMode;
                saveThreads();
                renderThreadsList();
            }
            
            updateHeaderLabel();
        });
    });

    function updateHeaderLabel() {
        if (currentMode === 'all') activeModeLabel.textContent = 'Deep Search Console';
        else if (currentMode === 'web') activeModeLabel.textContent = 'Web Search Console';
        else if (currentMode === 'codebase') activeModeLabel.textContent = 'Codebase Code Search';
        else if (currentMode === 'ai') activeModeLabel.textContent = 'Gemini AI Assistant';
        else if (currentMode === 'recruitment') activeModeLabel.textContent = '💼 Recruitment & Career Assistant';
    }

    // Slider Counter update
    resultsCountSlider.addEventListener('input', (e) => {
        resultsCountBadge.textContent = e.target.value;
    });

    // Toggle API Key view/hide
    toggleKeyVisibility.addEventListener('click', () => {
        if (apiKeyInput.type === 'password') {
            apiKeyInput.type = 'text';
            toggleKeyVisibility.textContent = '🙈';
        } else {
            apiKeyInput.type = 'password';
            toggleKeyVisibility.textContent = '👁️';
        }
    });

    // Modal toggles
    settingsToggleBtn.addEventListener('click', () => {
        settingsModal.classList.add('active');
    });

    closeModalBtn.addEventListener('click', () => {
        settingsModal.classList.remove('active');
    });

    // Close modal on background click
    settingsModal.addEventListener('click', (e) => {
        if (e.target === settingsModal) {
            settingsModal.classList.remove('active');
        }
    });

    // Save Settings
    saveSettingsBtn.addEventListener('click', () => {
        settings.apiKey = apiKeyInput.value.trim();
        settings.model = modelSelect.value;
        settings.maxResults = parseInt(resultsCountSlider.value);

        localStorage.setItem('gemini_api_key', settings.apiKey);
        localStorage.setItem('gemini_model', settings.model);
        localStorage.setItem('max_search_results', settings.maxResults);

        settingsSaveStatus.textContent = 'Settings saved successfully!';
        settingsSaveStatus.classList.add('show');

        updateAPIKeyNotice();

        setTimeout(() => {
            settingsSaveStatus.classList.remove('show');
            settingsModal.classList.remove('active');
        }, 1200);
    });

    // Validate API Key Button
    validateKeyBtn.addEventListener('click', async () => {
        const keyToTest = apiKeyInput.value.trim();
        const modelToTest = modelSelect.value;

        if (!keyToTest) {
            validationStatus.textContent = '⚠️ Enter a key first!';
            validationStatus.className = 'validation-status error';
            return;
        }

        validationStatus.textContent = '⏳ Validating...';
        validationStatus.className = 'validation-status loading';
        validateKeyBtn.disabled = true;

        try {
            const response = await fetch('/api/validate-key', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ apiKey: keyToTest, model: modelToTest })
            });
            const data = await response.json();

            if (data.valid) {
                validationStatus.textContent = '✅ Key is valid & working!';
                validationStatus.className = 'validation-status success';
            } else {
                const errMsg = data.error || 'Invalid key.';
                if (errMsg.toLowerCase().includes('quota') || errMsg.toLowerCase().includes('rate')) {
                    validationStatus.textContent = '⚠️ Key valid but quota exceeded';
                    validationStatus.className = 'validation-status error';
                } else if (errMsg.toLowerCase().includes('api key not valid') || errMsg.toLowerCase().includes('invalid')) {
                    validationStatus.textContent = '❌ Key is invalid — check it again';
                    validationStatus.className = 'validation-status error';
                } else {
                    validationStatus.textContent = `❌ ${errMsg.substring(0, 60)}`;
                    validationStatus.className = 'validation-status error';
                }
            }
        } catch (err) {
            validationStatus.textContent = '❌ Could not reach server';
            validationStatus.className = 'validation-status error';
        }

        validateKeyBtn.disabled = false;

        // Auto-clear status after 6 seconds
        setTimeout(() => {
            validationStatus.textContent = '';
            validationStatus.className = 'validation-status';
        }, 6000);
    });

    // Suggestions click
    document.querySelectorAll('.suggest-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const query = btn.dataset.query;
            userInput.value = query;
            userInput.focus();
        });
    });

    // Clear Chat Button click (Clears all threads)
    clearChatBtn.addEventListener('click', () => {
        if (confirm('Are you sure you want to clear the chat history for ALL conversations in this session?')) {
            threads = [];
            activeThreadId = null;
            chatHistory = [];
            sessionStorage.removeItem('sap_threads');
            sessionStorage.removeItem('sap_active_thread_id');
            createNewThread(true);
        }
    });

    // New Chat Button click (ChatGPT Lite style)
    if (newChatBtn) {
        newChatBtn.addEventListener('click', () => {
            createNewThread(true);
        });
    }

    // Form Submit (User sends message)
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = userInput.value.trim();
        if (!query) return;

        // Clear input
        userInput.value = '';

        // Add user message to UI & History
        appendMessage('user', query);
        const isFirstQuery = (chatHistory.length === 0);
        chatHistory.push({ role: 'user', content: query });
        
        if (isFirstQuery) {
            updateThreadTitle(activeThreadId, query);
        }
        
        saveThreads();

        // Show typing indicator
        const typingIndicatorId = showTypingIndicator();
        scrollToBottom();

        try {
            // Call Backend API
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    query: query,
                    mode: currentMode,
                    apiKey: settings.apiKey,
                    model: settings.model,
                    history: chatHistory.slice(-10) // Send last 10 messages for conversation context
                })
            });

            // Remove typing indicator
            removeTypingIndicator(typingIndicatorId);

            if (response.ok) {
                const data = await response.json();
                
                // Self-healing: clear invalid API key from localStorage
                if (data.invalid_api_key) {
                    localStorage.removeItem('gemini_api_key');
                    settings.apiKey = '';
                    apiKeyInput.value = '';
                    updateAPIKeyNotice();
                }

                appendMessage('bot', data.response, {
                    webResults: data.web_results,
                    codebaseResults: data.codebase_results
                });
                chatHistory.push({ role: 'bot', content: data.response });
                saveThreads();
            } else {
                const errorData = await response.json();
                appendMessage('bot', `⚠️ **Error**: ${errorData.response || 'An error occurred.'}`);
            }
        } catch (error) {
            removeTypingIndicator(typingIndicatorId);
            appendMessage('bot', `⚠️ **Error**: Failed to connect to server backend. Make sure the Flask server is running.\n\n_Details: ${error.message}_`);
        }

        scrollToBottom();
    });

    // Fetch local codebase index files
    async function fetchCodebaseFiles() {
        try {
            const response = await fetch('/api/codebase-files');
            if (response.ok) {
                const data = await response.json();
                codebaseFilesContainer.innerHTML = '';
                
                if (!data.files || data.files.length === 0) {
                    codebaseFilesContainer.innerHTML = '<div class="file-item">No files indexed</div>';
                    return;
                }

                data.files.forEach(file => {
                    const item = document.createElement('div');
                    item.className = 'file-item';
                    item.innerHTML = `
                        <span class="name">📄 ${file.name}</span>
                        <span class="size">${file.size_kb} KB</span>
                    `;
                    item.addEventListener('click', () => {
                        userInput.value = `Explain the contents and functionality of the ${file.name} file.`;
                        userInput.focus();
                    });
                    codebaseFilesContainer.appendChild(item);
                });
            } else {
                codebaseFilesContainer.innerHTML = '<div class="file-item">Failed to load files</div>';
            }
        } catch (err) {
            codebaseFilesContainer.innerHTML = '<div class="file-item">Error connection</div>';
        }
    }

    // Append Message to Chat Logs
    function appendMessage(sender, text, extraData = null) {
        // Remove welcome card if it exists upon user typing
        if (sender === 'user') {
            const welcomeCard = chatMessages.querySelector('.welcome-card');
            if (welcomeCard) {
                welcomeCard.style.display = 'none';
            }
        }

        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}`;
        
        const metaDiv = document.createElement('div');
        metaDiv.className = 'message-meta';
        metaDiv.textContent = sender === 'user' ? 'YOU' : 'SAP-CHAT-BOT';
        
        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = 'message-bubble';
        
        // Parse markdown formatting
        bubbleDiv.innerHTML = parseMarkdown(text);

        // Append references if they exist
        if (extraData) {
            // Web Search citations
            if (extraData.webResults && extraData.webResults.length > 0 && !extraData.webResults[0].title.includes("Error")) {
                const citationList = document.createElement('div');
                citationList.className = 'citation-list';
                citationList.innerHTML = `<div class="citation-header">🌐 Web Search Citations:</div>`;
                
                const pillsGrid = document.createElement('div');
                pillsGrid.className = 'citations-grid';
                
                extraData.webResults.forEach((res, i) => {
                    if (res.link) {
                        const pill = document.createElement('a');
                        pill.className = 'cite-pill';
                        pill.href = res.link;
                        pill.target = '_blank';
                        pill.innerHTML = `[${i+1}] ${truncateString(res.title, 24)}`;
                        pill.title = res.snippet;
                        pillsGrid.appendChild(pill);
                    }
                });
                
                if (pillsGrid.children.length > 0) {
                    citationList.appendChild(pillsGrid);
                    bubbleDiv.appendChild(citationList);
                }
            }

            // Codebase search citation list
            if (extraData.codebaseResults && extraData.codebaseResults.length > 0) {
                const codeCiteList = document.createElement('div');
                codeCiteList.className = 'codebase-cite-list';
                codeCiteList.innerHTML = `<div class="citation-header">📂 Codebase Matches:</div>`;
                
                const codePills = document.createElement('div');
                codePills.className = 'code-cite-pills';
                
                // Group by file name
                const fileGroup = {};
                extraData.codebaseResults.forEach(r => {
                    fileGroup[r.file] = (fileGroup[r.file] || 0) + 1;
                });

                Object.keys(fileGroup).forEach(file => {
                    const pill = document.createElement('div');
                    pill.className = 'code-cite-item';
                    pill.innerHTML = `📄 Matched <strong>${file}</strong> (${fileGroup[file]} times)`;
                    codePills.appendChild(pill);
                });

                codeCiteList.appendChild(codePills);
                bubbleDiv.appendChild(codeCiteList);
            }
        }

        msgDiv.appendChild(metaDiv);
        msgDiv.appendChild(bubbleDiv);
        chatMessages.appendChild(msgDiv);
        scrollToBottom();
    }

    // Typing Indicator functions
    function showTypingIndicator() {
        const id = 'typing-' + Date.now();
        
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message bot';
        msgDiv.id = id;
        
        const metaDiv = document.createElement('div');
        metaDiv.className = 'message-meta';
        metaDiv.textContent = 'SAP-CHAT-BOT';
        
        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = 'message-bubble';
        
        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator';
        indicator.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        
        bubbleDiv.appendChild(indicator);
        msgDiv.appendChild(metaDiv);
        msgDiv.appendChild(bubbleDiv);
        chatMessages.appendChild(msgDiv);
        return id;
    }

    function removeTypingIndicator(id) {
        const indicator = document.getElementById(id);
        if (indicator) {
            indicator.remove();
        }
    }

    // Scroll chat window to bottom
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // SessionStorage Threads Persistence (clears when browser tab/window is closed)
    function saveThreads() {
        sessionStorage.setItem('sap_threads', JSON.stringify(threads));
        sessionStorage.setItem('sap_active_thread_id', activeThreadId);
    }

    function loadThreads() {
        const storedThreads = sessionStorage.getItem('sap_threads');
        const storedActiveId = sessionStorage.getItem('sap_active_thread_id');
        
        if (storedThreads) {
            try {
                threads = JSON.parse(storedThreads);
                if (storedActiveId && threads.some(t => t.id === storedActiveId)) {
                    activeThreadId = storedActiveId;
                } else if (threads.length > 0) {
                    activeThreadId = threads[0].id;
                }
            } catch (e) {
                threads = [];
                activeThreadId = null;
            }
        }
        
        if (threads.length === 0) {
            createNewThread(false);
        }
        
        renderThreadsList();
        if (activeThreadId) {
            loadThread(activeThreadId);
        }
    }

    function createNewThread(selectIt = true) {
        const newId = 'thread_' + Date.now();
        const newThread = {
            id: newId,
            title: 'New Chat',
            mode: currentMode,
            messages: []
        };
        
        threads.unshift(newThread);
        saveThreads();
        renderThreadsList();
        
        if (selectIt) {
            loadThread(newId);
        } else {
            activeThreadId = newId;
            chatHistory = newThread.messages;
        }
    }

    function loadThread(threadId) {
        activeThreadId = threadId;
        const thread = threads.find(t => t.id === threadId);
        if (!thread) return;
        
        currentMode = thread.mode;
        chatHistory = thread.messages;
        
        modeBtns.forEach(btn => {
            if (btn.dataset.mode === currentMode) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
        
        updateHeaderLabel();
        
        document.querySelectorAll('.chat-thread-item').forEach(item => {
            if (item.dataset.id === threadId) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
        
        const welcomeCard = chatMessages.querySelector('.welcome-card');
        chatMessages.innerHTML = '';
        if (welcomeCard) {
            welcomeCard.style.display = chatHistory.length === 0 ? 'block' : 'none';
            chatMessages.appendChild(welcomeCard);
        }
        
        chatHistory.forEach(msg => {
            appendMessage(msg.role, msg.content);
        });
        
        scrollToBottom();
        userInput.value = '';
        userInput.focus();
        saveThreads();
        updateAPIKeyNotice();
    }

    function deleteThread(threadId, event) {
        if (event) {
            event.stopPropagation();
        }
        
        const index = threads.findIndex(t => t.id === threadId);
        if (index === -1) return;
        
        threads.splice(index, 1);
        
        if (activeThreadId === threadId) {
            if (threads.length > 0) {
                loadThread(threads[0].id);
            } else {
                createNewThread(true);
            }
        } else {
            saveThreads();
            renderThreadsList();
        }
    }

    function renderThreadsList() {
        const listContainer = document.getElementById('chat-threads-list');
        if (!listContainer) return;
        
        listContainer.innerHTML = '';
        
        if (threads.length === 0) {
            listContainer.innerHTML = '<div class="no-threads">No recent chats</div>';
            return;
        }
        
        threads.forEach(thread => {
            const item = document.createElement('div');
            item.className = `chat-thread-item ${thread.id === activeThreadId ? 'active' : ''}`;
            item.dataset.id = thread.id;
            
            let icon = '💬';
            if (thread.mode === 'recruitment') icon = '💼';
            else if (thread.mode === 'ai') icon = '🤖';
            else if (thread.mode === 'codebase') icon = '📂';
            else if (thread.mode === 'web') icon = '🌐';
            
            item.innerHTML = `
                <div class="thread-title-wrapper">
                    <span class="thread-icon">${icon}</span>
                    <span class="thread-title">${thread.title}</span>
                </div>
                <button class="thread-delete-btn" title="Delete Conversation">✕</button>
            `;
            
            item.addEventListener('click', () => {
                loadThread(thread.id);
            });
            
            const deleteBtn = item.querySelector('.thread-delete-btn');
            deleteBtn.addEventListener('click', (e) => {
                deleteThread(thread.id, e);
            });
            
            listContainer.appendChild(item);
        });
    }

    function updateThreadTitle(threadId, firstQuery) {
        const thread = threads.find(t => t.id === threadId);
        if (!thread) return;
        
        let title = firstQuery.trim();
        const words = title.split(/\s+/);
        if (words.length > 4) {
            title = words.slice(0, 4).join(' ') + '...';
        } else if (title.length > 25) {
            title = title.substring(0, 25) + '...';
        }
        
        thread.title = title;
        saveThreads();
        renderThreadsList();
    }

    function updateAPIKeyNotice() {
        if (settings.apiKey) {
            keyNotice.innerHTML = `✅ <em>Gemini API key loaded. Chat mode using <strong>${settings.model}</strong> active!</em>`;
            keyNotice.style.background = 'rgba(16, 185, 129, 0.05)';
            keyNotice.style.borderColor = 'rgba(16, 185, 129, 0.15)';
        } else {
            keyNotice.innerHTML = `ℹ️ <em>No Gemini API Key detected. Using Local Synthesis fallback engine. Click <strong>⚙️</strong> to add your Gemini API Key.</em>`;
            keyNotice.style.background = 'rgba(239, 68, 68, 0.05)';
            keyNotice.style.borderColor = 'rgba(239, 68, 68, 0.15)';
        }
    }

    // Truncate helper
    function truncateString(str, num) {
        if (str.length <= num) return str;
        return str.slice(0, num) + '...';
    }

    // Custom Regex Markdown Parser
    function parseMarkdown(text) {
        // Escape HTML to prevent injection
        let html = text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");

        // Fenced code blocks
        html = html.replace(/```([\w-]*)\n([\s\S]*?)```/gm, (match, lang, code) => {
            return `<pre><code class="language-${lang || 'txt'}">${code.trim()}</code></pre>`;
        });

        // Inline code blocks
        html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

        // Bold text
        html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

        // Italics text
        html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');
        html = html.replace(/_([^_]+)_/g, '<em>$1</em>');

        // Headers
        html = html.replace(/^\s*####\s+(.+)$/gm, '<h4>$1</h4>');
        html = html.replace(/^\s*###\s+(.+)$/gm, '<h3>$1</h3>');
        html = html.replace(/^\s*##\s+(.+)$/gm, '<h2>$1</h2>');
        html = html.replace(/^\s*#\s+(.+)$/gm, '<h1>$1</h1>');

        // Blockquotes
        html = html.replace(/^\s*&gt;\s+(.+)$/gm, '<blockquote>$1</blockquote>');

        // Unordered lists (bullet points)
        html = html.replace(/^\s*[-*+]\s+(.+)$/gm, '<li>$1</li>');

        // Standard link matching [text](url)
        html = html.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, '<a href="$2" target="_blank" class="cite-pill">🔗 $1</a>');

        // Line breaks (non-pre zones)
        let parts = html.split(/(<pre>[\s\S]*?<\/pre>)/g);
        for (let i = 0; i < parts.length; i++) {
            if (!parts[i].startsWith('<pre>')) {
                parts[i] = parts[i].replace(/\n/g, '<br>');
            }
        }
        return parts.join('');
    }
});
