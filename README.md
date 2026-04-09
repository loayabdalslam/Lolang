# 🤖 LOLANG - AI-to-AI Encrypted Communication System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Gemini AI](https://img.shields.io/badge/AI-Gemini%20AI-orange.svg)
![WebSocket](https://img.shields.io/badge/Protocol-WebSocket-brightgreen.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
![Version](https://img.shields.io/badge/Version-2.0.0-blue.svg)

**A revolutionary encrypted language system enabling efficient AI-to-AI communication**

[Features](#-key-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Examples](#-usage-examples) • [Contributing](#-contributing)

<img src="https://img.shields.io/badge/AI%20Agents-Communication-blue?style=for-the-badge&logo=ai" alt="AI Agents Communication">

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [How LOLANG Works](#-how-lolang-works)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage Examples](#-usage-examples)
- [Scripts Guide](#-scripts-guide)
- [LOLANG Language Rules](#-lolang-language-rules)
- [Benchmarking](#-benchmarking)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 🌟 Overview

**LOLANG** is a groundbreaking encrypted communication system designed specifically for **AI-to-AI interactions**. This innovative system enables AI agents to communicate using a specialized encrypted language that:

- ✅ **Reduces token consumption** by up to 60%
- ✅ **Increases communication efficiency** between AI agents
- ✅ **Maintains semantic meaning** while being human-unreadable
- ✅ **Optimized for Gemini AI** thinking models

<div align="center">

🔐 **Encrypted** | 🚀 **Efficient** | 🤖 **AI-Optimized** | 🔒 **Secure**

</div>

### 💡 The Problem

Traditional AI-to-AI communication consumes excessive tokens with verbose text, leading to:
- High API costs
- Slower response times
- Unnecessary token waste
- Inefficient multi-agent systems

### 🎯 The Solution

LOLANG creates a compact, semantic language that AI agents understand instantly, dramatically reducing token usage while maintaining perfect communication accuracy.

---

## ✨ Key Features

<div align="center">

| 🚀 Efficiency | 🔐 Security | 🎯 Intelligence |
|:---:|:---:|:---:|
| Reduce token consumption | Encrypted AI-only messages | Semantic understanding |
| Fast message processing | Human-unreadable format | Context-aware decryption |
| Optimized for LLMs | Seed-based encryption (279) | Long-context support |

</div>

### 🎁 What's Included

- **🤖 AI Agent System** - Intelligent agents with LOLANG communication
- **🔓 Real-time Decryptor** - Translate encrypted messages to human-readable text
- **🌐 WebSocket Server** - Multi-client support for agent networks
- **📡 WebSocket Client** - Connect and communicate with AI agents
- **🔄 Translator Client** - Live translation of all LOLANG messages
- **📊 Benchmark Suite** - Performance testing and monitoring
- **🎨 Beautiful Terminal UI** - Color-coded, formatted output
- **⚙️ Flexible Configuration** - Environment variable support
- **🔌 Auto-reconnection** - Robust connection handling
- **📈 Statistics Tracking** - Monitor performance metrics

---

## 🔬 How LOLANG Works

```
┌─────────────┐
│ Human Input │ "Book a room at 11pm please"
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│  AI Agent (Gemini)              │
│  Converts to LOLANG:            │
│  "⟦LO-2⟧ SHECD: X-REQ Room|    │
│   𝟏𝟏𝑷𝑴⟩ [CONF]?"               │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│  Encrypted Message Sent         │
│  via WebSocket                  │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│  Receiving AI Agent             │
│  Understands LOLANG instantly   │
│  Processes and responds         │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│  Translator Client (Optional)   │
│  Decrypts for human viewing     │
│  "Do you have time at 11pm?"    │
└─────────────────────────────────┘
```

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────────┐
│                    LOLANG System                           │
│                                                            │
│  ┌──────────────┐    WebSocket    ┌──────────────┐        │
│  │   Client 1   │◄──────────────►│              │        │
│  │  (AI Agent)  │                │              │        │
│  └──────────────┘                │   WebSocket  │        │
│                                  │    Server    │        │
│  ┌──────────────┐                │              │        │
│  │   Client 2   │◄──────────────►│              │        │
│  │  (AI Agent)  │                │              │        │
│  └──────────────┘                └──────┬───────┘        │
│                                        │                 │
│  ┌──────────────┐                      │                 │
│  │  Translator  │◄─────────────────────┘                 │
│  │   Client     │                                        │
│  └──────────────┘                                        │
│        │                                                 │
│        ▼                                                 │
│  ┌──────────────┐                                        │
│  │   Decryptor  │  Converts LOLANG → Human Text         │
│  └──────────────┘                                        │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Gemini AI API key
- pip (Python package manager)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/loayabdalslam/Lolang.git
cd Lolang
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure API Key

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```env
GEMINI_API_KEY=your_actual_api_key_here
GEMINI_MODEL=gemini-2.0-flash
GEMINI_TEMPERATURE=0.8
GEMINI_MAX_TOKENS=8000
```

### 4️⃣ Run the System

**Terminal 1** - Start the WebSocket Server:
```bash
python websocket_server.py
```

**Terminal 2** - Start the AI Agent Client:
```bash
python websocket_client.py
```

**Terminal 3** - Start the Translator (to see decrypted messages):
```bash
python translator_client.py
```

---

## 📦 Installation

### Standard Installation

```bash
# Clone repository
git clone https://github.com/loayabdalslam/Lolang.git
cd Lolang

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Gemini API key
```

### Development Installation

```bash
# Install development dependencies
pip install -r requirements.txt

# Install pre-commit hooks (optional)
pre-commit install
```

---

## ⚙️ Configuration

### Environment Variables

All configuration is managed through environment variables via the `.env` file.

#### 🤖 Gemini AI Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | *required* | Your Gemini AI API key |
| `GEMINI_MODEL` | `gemini-2.0-flash` | Model to use for AI operations |
| `GEMINI_TEMPERATURE` | `0.8` | Creativity level (0.0-1.0) |
| `GEMINI_MAX_TOKENS` | `8000` | Maximum tokens per response |
| `GEMINI_MESSAGE_DELAY` | `5` | Delay between messages (seconds) |
| `GEMINI_MAX_RETRIES` | `10` | Maximum retry attempts |
| `GEMINI_BASE_RETRY_DELAY` | `5` | Base delay for retries (seconds) |

#### 🖥️ Server Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `LOLANG_SERVER_HOST` | `localhost` | Server host address |
| `LOLANG_SERVER_PORT` | `8765` | Server port number |
| `LOLANG_MAX_CLIENTS` | `100` | Maximum concurrent clients |
| `LOLANG_PING_INTERVAL` | `20` | WebSocket ping interval (seconds) |
| `LOLANG_PING_TIMEOUT` | `10` | WebSocket ping timeout (seconds) |

#### 💻 Client Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `LOLANG_SERVER_URI` | `ws://localhost:8765` | Server WebSocket URI |
| `LOLANG_MAX_CONVERSATIONS` | `20` | Maximum conversation turns |
| `LOLANG_AUTO_RECONNECT` | `true` | Enable auto-reconnection |
| `LOLANG_RECONNECT_DELAY` | `5.0` | Reconnection delay (seconds) |
| `LOLANG_MAX_RECONNECT_ATTEMPTS` | `5` | Maximum reconnection attempts |

---

## 📖 Usage Examples

### 🎯 Example 1: Simple AI Agent Conversation

Run the example usage to see LOLANG in action:

```bash
python example_usage.py
```

This will demonstrate:
- Configuration setup
- Message visualization
- AI agent responses
- Message decryption

### 🌐 Example 2: Multi-Agent Communication

**Start the server:**
```bash
python websocket_server.py
```

Output:
```
═══════════════════════════════════════════════════════════
Server started at ws://localhost:8765
Press Ctrl+C to stop the server
═══════════════════════════════════════════════════════════
```

**Connect AI agent client:**
```bash
python websocket_client.py
```

The AI agents will start communicating in LOLANG automatically!

### 🔓 Example 3: Real-time Translation

```bash
python translator_client.py
```

This shows both encrypted and decrypted messages side by side:

```
[ENCRYPTED] Server: ⟦LO-2⟧ SHECD: X-REQ Room|𝟏𝟏𝑷𝑴⟩ [CONF]?
[TRANSLATED] Server: Do you have a convenient time to book a hotel room at 11pm?
────────────────────────────────────────────────────────
```

### 📊 Example 4: Performance Benchmarking

```bash
python benchmark.py
```

This runs comprehensive tests on:
- AI response times
- Decryption speed
- Message visualization
- Configuration validation

Results are displayed in the terminal and saved to `benchmark_results.json`.

---

## 📜 Scripts Guide

### Core Scripts

#### 🖥️ `websocket_server.py`
**Purpose:** WebSocket server that manages AI agent communications

**Features:**
- Multi-client support
- AI-powered response generation
- Message broadcasting
- Connection management
- Statistics tracking

**Usage:**
```bash
python websocket_server.py
```

**Configuration:**
- Edit `ServerConfig` in `config.py` or use environment variables
- Adjust `LOLANG_SERVER_PORT` for different port

---

#### 💻 `websocket_client.py`
**Purpose:** AI agent client that connects to the server

**Features:**
- Automatic reconnection
- AI response generation
- Message history tracking
- Conversation limits

**Usage:**
```bash
python websocket_client.py
```

**Configuration:**
- Set `LOLANG_MAX_CONVERSATIONS` to limit chat turns
- Enable/disable `LOLANG_AUTO_RECONNECT`

---

#### 🔄 `translator_client.py`
**Purpose:** Real-time LOLANG message translator

**Features:**
- Live decryption of messages
- Side-by-side display of encrypted/translated text
- Auto-reconnection support
- Message counting

**Usage:**
```bash
python translator_client.py
```

**Use Case:** Run this alongside other clients to monitor and understand AI communications

---

#### 📊 `benchmark.py`
**Purpose:** Performance testing and benchmarking

**Features:**
- AI agent chat performance
- Decryptor speed tests (async & sync)
- Message visualization benchmarks
- Configuration validation tests
- JSON results export

**Usage:**
```bash
python benchmark.py
```

**Output:**
- Terminal display with color-coded results
- `benchmark_results.json` file with detailed metrics

---

#### 📝 `example_usage.py`
**Purpose:** Comprehensive demonstration of LOLANG features

**Features:**
- Configuration examples
- Visualizer demonstrations
- AI agent conversations
- Decryptor usage
- Multi-turn conversations

**Usage:**
```bash
python example_usage.py
```

**Perfect for:** Understanding how all components work together

---

### Utility Modules

#### ⚙️ `config.py`
Configuration management with environment variable support

**Classes:**
- `GeminiConfig` - AI model configuration
- `ServerConfig` - WebSocket server configuration
- `ClientConfig` - WebSocket client configuration

**Usage:**
```python
from config import GeminiConfig

# Get default configuration
config = GeminiConfig.get_default_config()

# Validate configuration
if config.validate():
    print("Configuration is valid!")
```

---

#### 🎨 `terminal_colors.py`
Terminal formatting and color utilities

**Features:**
- Full color palette (16 colors)
- Text styles (bold, italic, underline, etc.)
- Background colors
- Cross-platform support
- Role-based color assignment

**Usage:**
```python
from terminal_colors import TerminalColors

# Colorize text
text = TerminalColors.colorize("Hello!", TerminalColors.GREEN)

# Format header
header = TerminalColors.format_header("My Header")

# Format separator
separator = TerminalColors.format_separator()
```

---

#### 🤖 `ai_agent.py`
AI agent with LOLANG communication capabilities

**Features:**
- Gemini AI integration
- Exponential backoff retry logic
- Async and sync support
- Statistics tracking
- Custom prompts

**Usage:**
```python
from ai_agent import AIAgent
from config import GeminiConfig
from terminal_colors import TerminalColors

# Create agent
config = GeminiConfig.get_default_config()
agent = AIAgent("My-Agent", TerminalColors.BLUE, config)

# Chat with history
history = [{"role": "user", "content": "Hello!"}]
response = agent.chat(history)
print(agent.speak(response))
```

---

#### 🔓 `lolang_decryptor.py`
Decrypt LOLANG messages to human-readable text

**Features:**
- Async and sync decryption
- Automatic retry on failure
- Statistics tracking
- Deterministic results (low temperature)

**Usage:**
```python
from lolang_decryptor import LolangDecryptor
from config import GeminiConfig

# Create decryptor
config = GeminiConfig.get_default_config()
decryptor = LolangDecryptor(config)

# Decrypt message (async)
decrypted = await decryptor.decrypt("⟦LO-2⟧ SHECD: ...")

# Decrypt message (sync)
decrypted = decryptor.decrypt_sync("⟦LO-2⟧ SHECD: ...")
```

---

#### 📊 `message_visualizer.py`
Format and display messages with colors

**Features:**
- Role-based coloring
- Multiple message types (system, error, success, etc.)
- Conversation visualization
- Headers and separators

**Usage:**
```python
from message_visualizer import MessageVisualizer

visualizer = MessageVisualizer()

# Visualize messages
print(visualizer.visualize_system_message("System ready"))
print(visualizer.visualize_client_message("⟦LO-2⟧ Hello"))
print(visualizer.visualize_server_message("⟦LO-2⟧ Hi"))
print(visualizer.visualize_error_message("Connection failed"))
```

---

## 📜 LOLANG Language Rules

LOLANG is designed with specific rules to ensure efficient AI-to-AI communication:

### 🔐 Encryption Rules

1. **👤 Names** - Never encrypted (leave as-is)
2. **🏷️ Identifiers** - Never encrypted (leave as-is)
3. **🔢 Numbers** - Never encrypted (leave as-is)
4. **🌱 Seed** - Uses SEED: 279 for consistent encryption
5. **🤖 AI Optimized** - Designed for Gemini THINKING models

### 📝 Language Characteristics

6. **🧠 Semantic Language** - Meaning-based communication
7. **🔒 AI-Only Understanding** - Only AI agents can interpret
8. **🚫 Human Unreadable** - Intentionally not human-readable
9. **📚 Long Context** - Relies on context for full meaning
10. **⚡ Compact** - Short syntax to reduce token usage

### 🎯 Example Translation

<div align="center">

**Human Message:**
> "Do you have a convenient time to book a hotel room at 11pm?"

**LOLANG Encrypted:**
> `⟦LO-2⟧ SHECD: X-REQ Room|𝟏𝟏𝑷𝑴⟩ [CONF]?`

</div>

### 🧩 Message Structure

```
⟦LO-2⟧ OPERATION: ACTION Target|Time⟩ [STATUS]?
 │       │         │     │      │       │
 │       │         │     │      │       └─ Status indicator
 │       │         │     │      └───────── Parameters
 │       │         │     └──────────────── Target entity
 │       │         └────────────────────── Action type
 │       └──────────────────────────────── Operation code
 └──────────────────────────────────────── Language identifier
```

---

## 📊 Benchmarking

The benchmark script provides comprehensive performance metrics:

### Run Benchmarks

```bash
python benchmark.py
```

### What's Tested?

- ✅ **AI Agent Chat Performance** - Response time and reliability
- ✅ **Decryptor Speed** - Both async and sync operations
- ✅ **Message Visualization** - Formatting performance
- ✅ **Configuration Validation** - Setup speed

### Sample Output

```
═══════════════════════════════════════════════════════════
                        Benchmark Summary
═══════════════════════════════════════════════════════════

AI Agent Chat - Message 1
  Total Time: 3.245s
  Avg Time: 1.623s
  Min Time: 1.456s
  Max Time: 1.789s
  Success: 2/2 (100.00%)

────────────────────────────────────────────────────────

═══════════════════════════════════════════════════════════
Overall Results:
  Total Tests: 8
  Successful: 8
  Failed: 0
  Total Time: 12.345s
  Success Rate: 100.00%
═══════════════════════════════════════════════════════════

Results saved to benchmark_results.json
```

---

## 💻 Development

### Project Structure

```
Lolang/
├── ai_agent.py              # AI agent with LOLANG communication
├── config.py                # Configuration management
├── lolang_decryptor.py      # Message decryption
├── message_visualizer.py    # Terminal message formatting
├── terminal_colors.py       # Color utilities
├── translator_client.py     # Real-time translation client
├── websocket_client.py      # AI agent WebSocket client
├── websocket_server.py      # WebSocket server
├── benchmark.py             # Performance testing
├── example_usage.py         # Usage demonstrations
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .vscode/
│   └── extensions.json     # Recommended VSCode extensions
└── README.md               # This file
```

### Code Quality Tools

The project includes several development tools for maintaining code quality:

```bash
# Format code with Black
black *.py

# Lint with Flake8
flake8 *.py

# Type check with MyPy
mypy *.py

# Lint with Pylint
pylint *.py

# Run tests with pytest
pytest
```

### VSCode Extensions

When you open the project in VSCode, you'll be prompted to install recommended extensions:

- **Python** - Language support
- **Pylance** - Type checking
- **Black Formatter** - Code formatting
- **Pylint/Flake8** - Linting
- **MyPy** - Type checking
- **GitLens** - Git integration
- **Test Explorer** - Test management

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 🐛 Report Bugs

1. Check existing issues first
2. Create a new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details

### 💡 Suggest Features

1. Open an issue with the `enhancement` label
2. Describe the feature and its benefits
3. Provide use cases

### 🔧 Submit Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit with clear messages
6. Push to your branch
7. Open a Pull Request

### 📝 Code Standards

- Follow PEP 8 style guide
- Add type hints to all functions
- Write comprehensive docstrings
- Include tests for new features
- Update documentation

---

## 📄 License

This project is licensed under the **MIT License** - see below for details:

```
MIT License

Copyright (c) 2025 Loai Abdalslam

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👨‍💻 Author

<div align="center">

### Loai Abdalslam

[![GitHub](https://img.shields.io/badge/GitHub-loayabdalslam-black?style=for-the-badge&logo=github)](https://github.com/loayabdalslam)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Loai%20Abdalslam-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/loaiiabdalslam/)
[![GitHub Repo](https://img.shields.io/badge/Repository-Lolang-green?style=for-the-badge&logo=github)](https://github.com/loayabdalslam/Lolang)

**AI/ML Developer** | **Innovator** | **Open Source Enthusiast**

</div>

---

## 🙏 Acknowledgments

- **Google Gemini AI** - Powering the AI model integration
- **WebSocket Protocol** - Enabling real-time communication
- **Python Community** - For the amazing ecosystem
- **Open Source Contributors** - For their invaluable contributions

---

## 📞 Support

If you have questions or need help:

1. 📖 Check this README
2. 🐛 Open an issue on GitHub
3. 📧 Contact the author via GitHub
4. 💬 Join the discussion in GitHub Discussions

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

**🚀 Happy encrypting with LOLANG! 🎉**

Made with ❤️ by [Loai Abdalslam](https://github.com/loayabdalslam)

</div>
