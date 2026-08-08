# 🤖 AI Agent Tutorial - Step by Step

A comprehensive, beginner-friendly tutorial for building AI agents from scratch! This repository walks you through creating an intelligent agent step-by-step, from basic structure to a fully functional AI system powered by LLM.

## 📚 Tutorial Overview

| Step | Title | Concepts | File |
|------|-------|----------|------|
| 1 | Basic Agent Structure | Perceive → Think → Act cycle | `step1_basic_agent.py` |
| 2 | Memory Management | Short-term & long-term memory | `step2_memory_agent.py` |
| 3 | LLM Integration | Connect to OpenAI GPT API | `step3_llm_agent.py` |
| 4 | Tools & Actions | Tool registry and execution | `step4_tools_agent.py` |
| 5 | Complete Agent | Full-featured intelligent agent | `step5_complete_agent.py` |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API Key (for steps 3-5)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/dasbairagya/hello-world.git
cd hello-world

# 2. Checkout the ai-agent-tutorial branch
git checkout ai-agent-tutorial

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Running the Examples

```bash
# Step 1: Basic Agent
python step1_basic_agent.py

# Step 2: Agent with Memory
python step2_memory_agent.py

# Step 3: LLM-Powered Agent (requires API key)
python step3_llm_agent.py

# Step 4: Agent with Tools
python step4_tools_agent.py

# Step 5: Complete Intelligent Agent
python step5_complete_agent.py
```

---

## 📖 Detailed Step Guide

### Step 1: Basic Agent Structure
**File:** `step1_basic_agent.py`

Introduces the fundamental agent architecture:

```
USER INPUT → [PERCEIVE] → [THINK] → [ACT] → OUTPUT
```

**Key Concepts:**
- Perception: Receive and process input
- Thinking: Process and decide
- Action: Generate and deliver response
- Conversation history

**Example:**
```python
agent = SimpleAgent("BasicBot")
agent.run("Hello!")  # Output: You said: Hello!
```

---

### Step 2: Memory Management
**File:** `step2_memory_agent.py`

Adds memory capabilities for context-aware responses:

- **Short-term memory**: Recent conversation history (sliding window)
- **Long-term memory**: Important facts and knowledge
- **Memory recall**: Access stored information

**Key Concepts:**
- Conversation context
- Fact storage and retrieval
- Memory limits for efficiency

**Example:**
```python
agent = MemoryAgent("MemoryBot", max_memory_size=5)
agent.run("Hi, my name is Alice")
agent.store_long_term_memory("user_name", "Alice")
agent.run("Can you remember me?")  # Recalls stored name
```

---

### Step 3: LLM Integration
**File:** `step3_llm_agent.py`

Connects the agent to OpenAI's GPT for intelligent responses:

**Setup:**
1. Get API key: https://platform.openai.com/api-keys
2. Create `.env` file: `OPENAI_API_KEY=your_key_here`
3. Install: `pip install openai python-dotenv`

**Key Concepts:**
- LLM API integration
- System prompts for behavior control
- Token usage tracking
- Multi-turn conversations

**Example:**
```python
agent = LLMAgent("IntelligentBot", model="gpt-3.5-turbo")
agent.run("What is artificial intelligence?")
agent.run("Can you explain in simpler terms?")  # Remembers context
```

---

### Step 4: Tools & Actions
**File:** `step4_tools_agent.py`

Enables the agent to use external tools:

**Built-in Tools:**
- **calculator**: Math operations (add, subtract, multiply, divide)
- **get_current_time**: Get current date/time
- **read_file**: Read text files

**Key Concepts:**
- Tool registry system
- Function calling via LLM
- Tool execution and results
- Extensible architecture

**Example:**
```python
agent = ToolUsingAgent("ToolBot")
agent.run("What is 25 * 4?")  # Uses calculator tool
agent.run("What's the current time?")  # Uses time tool
```

---

### Step 5: Complete Intelligent Agent
**File:** `step5_complete_agent.py`

The complete agent combining all features:

**Features:**
- ✅ Smart perception and action cycle
- ✅ Short-term and long-term memory
- ✅ LLM-powered reasoning
- ✅ Multiple tools with function calling
- ✅ Interactive conversation mode
- ✅ Statistics tracking

**Available Tools:**
- `calculator`: Math operations
- `get_time`: Current date/time
- `save_memory`: Store important facts
- `recall_memory`: Access stored facts

**Example - Programmatic:**
```python
agent = CompleteIntelligentAgent("IntelliBot")
agent.run("Hello! My name is Alice")
agent.run("Calculate 100 + 50")
agent.run("What's the current time?")

# View statistics
stats = agent.get_stats()
print(stats)
```

**Example - Interactive:**
```python
agent = CompleteIntelligentAgent("IntelliBot")
agent.interactive_mode()
# Type your messages, 'history' for chat, 'memory' for facts, 'exit' to quit
```

---

## 🔧 Configuration

### Environment Variables (.env)

```env
# Required for steps 3-5
OPENAI_API_KEY=sk-...

# Optional
OPENAI_MODEL=gpt-3.5-turbo
AGENT_TEMPERATURE=0.7
AGENT_MAX_MEMORY=20
```

### Customization

```python
# Change model
agent = LLMAgent("MyBot", model="gpt-4")

# Adjust creativity (0=precise, 1=creative)
agent = LLMAgent("MyBot", temperature=0.3)

# Increase memory
agent = CompleteIntelligentAgent("MyBot", max_memory=50)
```

---

## 💡 Key Concepts Explained

### The Agent Cycle: PERCEIVE → THINK → ACT

```python
def run(self, user_input):
    # 1. PERCEIVE: Receive input
    perceived = self.perceive(user_input)
    
    # 2. THINK: Process and decide
    response = self.think(perceived)
    
    # 3. ACT: Generate output
    final = self.act(response)
```

### Memory Types

**Short-term Memory (Conversation History)**
- Recent messages from current session
- Limited size (sliding window)
- Used for context in LLM calls

**Long-term Memory (Knowledge Store)**
- Important facts to remember
- Persists across conversation turns
- Manually stored/retrieved

### Tool Calling

The LLM decides when to use tools:
```
User Question → LLM → Decide Tool → Execute → Get Result → Final Response
```

---

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│          User Input / Questions                 │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
            ┌────────────────┐
            │   PERCEIVE     │
            │  Store input   │
            └────────┬───────┘
                     │
                     ▼
            ┌────────────────────────────┐
            │      THINK (LLM)           │
            │  Process with memory       │
            │  Consider tools            │
            └────────┬───────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
   ┌─────────┐         ┌──────────────────┐
   │  Direct │         │  Use Tools       │
   │Response │         │  (Calculator,    │
   │         │         │   File ops, etc) │
   └────┬────┘         └────────┬─────────┘
        │                       │
        └───────────┬───────────┘
                    │
                    ▼
            ┌────────────────┐
            │     ACT        │
            │  Output result │
            │  Update memory │
            └────────┬───────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  Agent Response       │
         │  to User              │
         └───────────────────────┘
```

---

## 🎯 Learning Progression

1. **Start here**: `step1_basic_agent.py` - Understand the core cycle
2. **Next**: `step2_memory_agent.py` - Add memory for context
3. **Then**: `step3_llm_agent.py` - Make it intelligent with LLM
4. **Continue**: `step4_tools_agent.py` - Enable external tools
5. **Master**: `step5_complete_agent.py` - Production-ready agent

---

## 🔌 Integration Examples

### With Web Framework (Flask)

```python
from flask import Flask, request
from step5_complete_agent import CompleteIntelligentAgent

app = Flask(__name__)
agent = CompleteIntelligentAgent("WebBot")

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    response = agent.run(user_message)
    return {'response': response}
```

### With Discord Bot

```python
import discord
from step5_complete_agent import CompleteIntelligentAgent

agent = CompleteIntelligentAgent("DiscordBot")

@bot.event
async def on_message(message):
    if message.author != bot.user:
        response = agent.run(message.content)
        await message.channel.send(response)
```

### With Slack Bot

```python
from slack_bolt import App
from step5_complete_agent import CompleteIntelligentAgent

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
agent = CompleteIntelligentAgent("SlackBot")

@app.message(".*")
def message_handler(message, say):
    response = agent.run(message["text"])
    say(response)
```

---

## 🛠️ Custom Tools

Add your own tools to the agent:

```python
agent = CompleteIntelligentAgent("CustomBot")

# Add a custom tool to the registry
def weather_tool(city):
    # Your implementation
    return f"Weather in {city}: 72°F"

# Register it
agent.tool_registry.register_tool(
    name="get_weather",
    description="Get weather for a city",
    func=weather_tool,
    params={"city": "City name"}
)
```

---

## 📝 Files Overview

```
.
├── step1_basic_agent.py          # 3.0 KB - Basic agent structure
├── step2_memory_agent.py         # 4.5 KB - Memory management
├── step3_llm_agent.py            # 6.5 KB - LLM integration
├── step4_tools_agent.py          # 10.5 KB - Tools & actions
├── step5_complete_agent.py       # 15.1 KB - Complete agent
├── requirements.txt              # Dependencies
├── .env.example                  # Environment template
└── README.md                     # This file
```

---

## 🐛 Troubleshooting

### "OPENAI_API_KEY not found"
**Solution**: Create `.env` file with your API key
```bash
echo "OPENAI_API_KEY=sk-..." > .env
```

### "ModuleNotFoundError: No module named 'openai'"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### "API rate limit exceeded"
**Solution**: Wait a moment or upgrade your OpenAI plan

### "Tool not found" error
**Solution**: Ensure tool is registered before use
```python
agent.tool_registry.register_tool(...)
```

---

## 📚 Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [GPT-3.5 vs GPT-4](https://platform.openai.com/docs/models)
- [Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [AI Agent Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)

---

## 🤝 Contributing

Found a bug or want to improve? Feel free to:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## 📄 License

This tutorial is open source and available under the MIT License.

---

## 🎓 Learning Outcomes

After completing this tutorial, you'll understand:

- ✅ How to build an AI agent from scratch
- ✅ The Perceive → Think → Act cycle
- ✅ Memory management strategies
- ✅ LLM integration and API usage
- �� Function calling and tool management
- ✅ Building production-ready agents
- ✅ Common patterns and best practices
- ✅ How to customize and extend agents

---

## 🚀 Next Steps

1. **Try different models** - Replace `gpt-3.5-turbo` with `gpt-4`
2. **Add more tools** - Create custom tools for your use case
3. **Build a UI** - Add a web interface using Flask/FastAPI
4. **Deploy** - Host on AWS, Heroku, or your preferred platform
5. **Experiment** - Modify prompts and parameters to see effects

---

## ❓ FAQ

**Q: Can I use a different LLM provider?**
A: Yes! The architecture is flexible. Replace OpenAI with Anthropic, Cohere, etc.

**Q: What's the cost of using OpenAI API?**
A: GPT-3.5-turbo is ~$0.0005 per 1000 tokens. Check [OpenAI pricing](https://openai.com/pricing).

**Q: Can I run this offline?**
A: Steps 1-2 work offline. Steps 3-5 require an internet connection and API key.

**Q: How do I make the agent faster?**
A: Use `gpt-3.5-turbo` instead of `gpt-4`, or implement caching.

**Q: Can I deploy this to production?**
A: Yes! See "Integration Examples" section for Flask, Discord, Slack patterns.

---

## 📞 Support

Have questions? Open an issue on GitHub or check the discussion section!

---

**Happy Learning! 🎉**

Start with Step 1 and work your way through. Each step builds on the previous one!
