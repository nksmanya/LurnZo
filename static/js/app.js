(function(){
  const messagesEl = document.getElementById('messages');
  const suggestionsEl = document.getElementById('suggestions');
  const subjectSelect = document.getElementById('subjectSelect');
  const form = document.getElementById('composer');
  const input = document.getElementById('questionInput');
  const sendBtn = document.getElementById('sendBtn');
  const clearBtn = document.getElementById('clearChatBtn');
  const themeBtn = document.getElementById('themeToggleBtn');

  const EXAMPLES = {
    General: [
      'What is time complexity with an example?',
      'Explain binary search step-by-step.',
      'Summarize Newton\'s laws in simple words.',
      'How do I structure an essay introduction?'
    ],
    'Computer Science': [
      'What is the difference between a stack and a queue?',
      'Explain Big-O for quicksort.',
      'How does a hash table handle collisions?',
      'What is overfitting in ML?'
    ],
    Mathematics: [
      'Derive the quadratic formula.',
      'What is the binomial theorem?',
      'Explain limits intuitively.',
      'How to prove the Pythagorean theorem?'
    ],
    Physics: [
      'Difference between speed and velocity?',
      'Explain conservation of momentum.',
      'What is simple harmonic motion?'
    ],
    Chemistry: [
      'What is a buffer solution?',
      'Explain periodic trends.',
      'What defines an acid vs base?'
    ],
    Biology: [
      'Explain DNA replication in short.',
      'What is osmosis?',
      'Difference between mitosis and meiosis?'
    ],
    English: [
      'Tips to write a thesis statement?',
      'What is active vs passive voice?',
      'How to avoid plagiarism?'
    ]
  };

  const STORAGE_KEY = 'ssb_chat_v1';
  let chat = loadChat();

  function loadChat(){
    try{ const raw = localStorage.getItem(STORAGE_KEY); return raw ? JSON.parse(raw) : []; }catch{ return []; }
  }
  function saveChat(){
    try{ localStorage.setItem(STORAGE_KEY, JSON.stringify(chat)); }catch{ /* ignore */ }
  }

  function createMessage({ role, content }){
    const tpl = document.getElementById('messageTemplate');
    const node = tpl.content.firstElementChild.cloneNode(true);
    node.classList.toggle('message--user', role === 'user');
    node.classList.toggle('message--bot', role === 'bot');
    node.querySelector('.message__avatar').textContent = role === 'user' ? '🧑‍🎓' : '🤖';
    node.querySelector('.message__content').textContent = content;
    return node;
  }

  function createTyping(){
    const tpl = document.getElementById('typingTemplate');
    return tpl.content.firstElementChild.cloneNode(true);
  }

  function scrollToBottom(){
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function renderChat(){
    messagesEl.innerHTML = '';
    chat.forEach(m => messagesEl.appendChild(createMessage(m)));
    scrollToBottom();
  }

  function renderSuggestions(){
    suggestionsEl.innerHTML = '';
    const list = EXAMPLES[subjectSelect.value] || EXAMPLES.General;
    list.forEach(txt => {
      const chip = document.createElement('button');
      chip.className = 'suggestions__chip';
      chip.type = 'button';
      chip.textContent = txt;
      chip.addEventListener('click', () => {
        input.value = txt;
        input.focus();
      });
      suggestionsEl.appendChild(chip);
    });
  }

  async function askBackend(question, subject){
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 20000);
    try{
      const res = await fetch('/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, subject }),
        signal: controller.signal
      });
      if(!res.ok) throw new Error('Request failed');
      const data = await res.json();
      return data;
    }catch(err){
      return 'Backend not available yet. This is the frontend stub. Once the Flask API is live at /api/ask, answers will appear here.';
    }finally{
      clearTimeout(timeout);
    }
  }

  async function handleSubmit(event){
    event.preventDefault();
    const question = (input.value || '').trim();
    if(!question) return;
    const subject = subjectSelect.value;

    input.value = '';
    const userMsg = { role: 'user', content: question };
    chat.push(userMsg); saveChat();
    messagesEl.appendChild(createMessage(userMsg));
    const typing = createTyping();
    messagesEl.appendChild(typing);
    scrollToBottom();

    sendBtn.disabled = true;
    try{
      const data = await askBackend(question, subject);
      typing.remove();
      const answerText = typeof data === 'string' ? data : (data.answer || 'I could not find an answer.');
      const botMsg = { role: 'bot', content: answerText };
      chat.push(botMsg); saveChat();
      messagesEl.appendChild(createMessage(botMsg));
      if(data && data.sources && Array.isArray(data.sources)){
        const cite = document.createElement('div');
        cite.style.margin = '6px 0 0 46px';
        cite.style.color = 'var(--muted)';
        cite.style.fontSize = '12px';
        cite.textContent = 'Sources: ' + data.sources.slice(0,3).map(s => `${s.subject}: ${s.question}`).join(' | ');
        messagesEl.appendChild(cite);
      }
      scrollToBottom();
    } finally {
      sendBtn.disabled = false;
    }
  }

  function clearChat(){
    chat = []; saveChat(); renderChat();
  }

  function initTheme(){
    const key = 'ssb_theme';
    const set = val => { document.documentElement.dataset.theme = val; localStorage.setItem(key, val); };
    const current = localStorage.getItem(key) || 'dark';
    set(current);
    themeBtn.addEventListener('click', () => set((document.documentElement.dataset.theme === 'dark') ? 'light' : 'dark'));
  }

  // Light theme vars applied when data-theme="light"
  const style = document.createElement('style');
  style.textContent = '[data-theme="light"]{--bg:#f5f7ff;--panel:#ffffff;--text:#0e1330;--muted:#5b6185;--primary:#4f6bed;--primary-700:#405ad6;--border:rgba(0,0,0,.08);}';
  document.head.appendChild(style);

  // Events
  form.addEventListener('submit', handleSubmit);
  clearBtn.addEventListener('click', clearChat);
  subjectSelect.addEventListener('change', renderSuggestions);

  // Initial render
  initTheme();
  renderChat();
  renderSuggestions();
})();


