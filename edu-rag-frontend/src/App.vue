<template>
  <div id="app" :data-theme="theme">
    <header class="header">
      <h1>EduRAG 问答系统</h1>
      <button class="theme-toggle" @click="toggleTheme">
        {{ theme === 'light' ? '🌙' : '☀️' }}
      </button>
    </header>

    <div class="layout">
      <aside class="sidebar">
        <div class="sidebar-section">
          <h3>学科选择</h3>
          <select class="subject-selector" v-model="currentSubject">
            <option value="">全部</option>
            <option value="ai">AI</option>
            <option value="java">Java</option>
            <option value="test">Test</option>
            <option value="ops">Ops</option>
            <option value="bigdata">BigData</option>
          </select>
        </div>

        <div class="sidebar-section" style="flex: 1; overflow-y: auto;">
          <h3>会话记录</h3>
          <button class="new-session-btn" @click="createNewSession">+ 新建会话</button>
          <ul class="session-list" style="margin-top: 12px;">
            <li
              v-for="session in sessions"
              :key="session.sessionId"
              class="session-item"
              :class="{ active: session.sessionId === currentSessionId }"
              @click="switchSession(session.sessionId)"
            >
              <div class="session-question">{{ session.firstQuestion }}</div>
              <div class="session-time">{{ formatTime(session.timestamp) }}</div>
            </li>
          </ul>
        </div>
      </aside>

      <main class="main-content">
        <div class="message-list" ref="messageListRef">
          <div v-if="messages.length === 0" class="empty-state">
            <div class="empty-state-icon">💬</div>
            <p>开始提问吧！</p>
          </div>

          <div
            v-for="(msg, index) in messages"
            :key="index"
            class="message"
            :class="msg.role"
          >
            <div class="message-content">
              {{ msg.content }}
              <span v-if="msg.role === 'assistant' && isStreaming && index === messages.length - 1" class="streaming-indicator">...</span>
              <div v-if="msg.sources && msg.sources.length > 0" class="source-display">
                <h4>参考文档</h4>
                <div v-for="(source, sIdx) in msg.sources" :key="sIdx" class="source-item">
                  <div class="source-header" @click="toggleSource(index, sIdx)">
                    <span class="source-subject">{{ source.subject || '通用' }}</span>
                    <button class="expand-btn">{{ source.expanded ? '收起' : '展开' }}</button>
                  </div>
                  <div class="source-summary">{{ source.summary }}</div>
                  <div v-if="source.expanded" class="source-full">{{ source.full }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="input-area">
          <div class="input-wrapper">
            <textarea
              class="input-field"
              v-model="inputValue"
              placeholder="输入您的问题..."
              rows="1"
              @keydown.enter.exact.prevent="sendMessage"
              @input="autoResize"
              ref="inputRef"
            ></textarea>
            <button class="send-btn" @click="sendMessage" :disabled="isStreaming || !inputValue.trim()">
              发送
            </button>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, nextTick, onMounted } from 'vue'

const theme = ref('light')
const currentSubject = ref('')
const currentSessionId = ref(null)
const sessions = ref([])
const messages = ref([])
const inputValue = ref('')
const isStreaming = ref(false)

const messageListRef = ref(null)
const inputRef = ref(null)

const sourceExpanded = reactive({})

function toggleTheme() {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
  localStorage.setItem('edu-rag-theme', theme.value)
}

function createNewSession() {
  currentSessionId.value = generateSessionId()
  messages.value = []
  Object.keys(sourceExpanded).forEach(k => delete sourceExpanded[k])
  sessions.value.unshift({
    sessionId: currentSessionId.value,
    firstQuestion: '新会话',
    timestamp: Date.now()
  })
}

function generateSessionId() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
    const r = Math.random() * 16 | 0
    const v = c === 'x' ? r : (r & 0x3 | 0x8)
    return v.toString(16)
  })
}

function switchSession(sessionId) {
  currentSessionId.value = sessionId
}

function formatTime(timestamp) {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date

  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)} 分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)} 小时前`

  return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`
}

function toggleSource(msgIndex, srcIndex) {
  const key = `${msgIndex}-${srcIndex}`
  sourceExpanded[key] = !sourceExpanded[key]
}

function autoResize() {
  const textarea = inputRef.value
  if (textarea) {
    textarea.style.height = 'auto'
    textarea.style.height = textarea.scrollHeight + 'px'
  }
}

async function sendMessage() {
  const query = inputValue.value.trim()
  if (!query || isStreaming.value) return

  if (!currentSessionId.value) {
    createNewSession()
  }

  const userMessage = { role: 'user', content: query, timestamp: Date.now() }
  messages.value.push(userMessage)

  const session = sessions.value.find(s => s.sessionId === currentSessionId.value)
  if (session && session.firstQuestion === '新会话') {
    session.firstQuestion = query.slice(0, 20)
  }

  inputValue.value = ''
  if (inputRef.value) {
    inputRef.value.style.height = 'auto'
  }

  isStreaming.value = true

  const assistantMessage = { role: 'assistant', content: '', sources: [], timestamp: Date.now() }
  messages.value.push(assistantMessage)

  scrollToBottom()

  try {
    const response = await fetch('/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query,
        source_filter: currentSubject.value || undefined,
        session_id: currentSessionId.value
      })
    })

    if (!response.ok) throw new Error('请求失败')

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6))
            if (data.error) {
              assistantMessage.content = '抱歉，发生了错误：' + data.error
            } else if (data.token) {
              assistantMessage.content += data.token
              if (data.session_id && !currentSessionId.value) {
                currentSessionId.value = data.session_id
              }
            }
            if (data.is_complete) {
              isStreaming.value = false
            }
          } catch (e) {
            // ignore parse errors for incomplete JSON
          }
        }
      }
    }
  } catch (error) {
    assistantMessage.content = '抱歉，网络发生了错误。请稍后重试。'
    isStreaming.value = false
  }

  scrollToBottom()
}

function scrollToBottom() {
  nextTick(() => {
    if (messageListRef.value) {
      messageListRef.value.scrollTop = messageListRef.value.scrollHeight
    }
  })
}

onMounted(() => {
  const savedTheme = localStorage.getItem('edu-rag-theme')
  if (savedTheme) {
    theme.value = savedTheme
  }
})
</script>