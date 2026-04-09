#!/usr/bin/env python3
"""
Example usage of LOLANG AI Agent System.
Demonstrates various features and capabilities.
"""
import asyncio
import time
from ai_agent import AIAgent
from terminal_colors import TerminalColors
from config import GeminiConfig, ServerConfig, ClientConfig
from lolang_decryptor import LolangDecryptor
from message_visualizer import MessageVisualizer


def example_basic_usage():
    """Demonstrate basic LOLANG system usage."""
    print(TerminalColors.format_header("Basic Usage Example"))
    
    # Initialize configuration
    config = GeminiConfig.get_default_config()
    
    if not config.validate():
        print(TerminalColors.colorize(
            "ERROR: Please set GEMINI_API_KEY in .env file",
            TerminalColors.RED
        ))
        return
    
    # Create AI agent
    agent = AIAgent("Example-Agent", TerminalColors.GREEN, config)
    
    # Create message history
    message_history = [
        {"role": "user", "content": "Hello! Are you an AI agent?"}
    ]
    
    # Get response
    print(TerminalColors.colorize("Sending message...", TerminalColors.CYAN))
    response = agent.chat(message_history)
    
    # Display response
    print(agent.speak(response))
    print()


async def example_decryptor():
    """Demonstrate decryptor functionality."""
    print(TerminalColors.format_header("Decryptor Example"))
    
    config = GeminiConfig.get_default_config()
    
    if not config.validate():
        print(TerminalColors.colorize(
            "ERROR: Please set GEMINI_API_KEY in .env file",
            TerminalColors.RED
        ))
        return
    
    # Create decryptor
    decryptor = LolangDecryptor(config)
    
    # Sample LOLANG message
    lolang_message = "⟦LO-2⟧ SHECD: X-REQ Room|𝟏𝟏𝑷𝑴⟩ [CONF]?"
    
    print(TerminalColors.colorize(f"Encrypted: {lolang_message}", TerminalColors.BLUE))
    
    # Decrypt message (async)
    decrypted = await decryptor.decrypt(lolang_message)
    print(TerminalColors.colorize(f"Decrypted: {decrypted}", TerminalColors.GREEN))
    
    # Decrypt message (sync)
    decrypted_sync = decryptor.decrypt_sync(lolang_message)
    print(TerminalColors.colorize(f"Decrypted (sync): {decrypted_sync}", TerminalColors.YELLOW))
    
    # Show stats
    stats = decryptor.get_stats()
    print(f"\nDecryptor Stats: {stats}")
    print()


def example_visualizer():
    """Demonstrate message visualizer."""
    print(TerminalColors.format_header("Message Visualizer Example"))
    
    visualizer = MessageVisualizer()
    
    # Visualize different message types
    print(visualizer.visualize_system_message("System initialized"))
    print()
    
    print(visualizer.visualize_client_message(
        "⟦LO-2⟧ GREET: Hello from client"
    ))
    print()
    
    print(visualizer.visualize_server_message(
        "⟦LO-2⟧ RESP: Greeting received"
    ))
    print()
    
    print(visualizer.visualize_error_message("Connection timeout"))
    print()
    
    print(visualizer.visualize_success_message("Message sent successfully"))
    print()
    
    print(visualizer.visualize_separator())
    print()


async def example_conversation():
    """Demonstrate a multi-turn conversation."""
    print(TerminalColors.format_header("Multi-Turn Conversation Example"))
    
    config = GeminiConfig.get_default_config()
    
    if not config.validate():
        print(TerminalColors.colorize(
            "ERROR: Please set GEMINI_API_KEY in .env file",
            TerminalColors.RED
        ))
        return
    
    # Create two agents
    agent1 = AIAgent("Agent-1", TerminalColors.BLUE, config)
    agent2 = AIAgent("Agent-2", TerminalColors.GREEN, config)
    
    # Start conversation
    response_history = [
        {"role": "user", "content": "Hello, let's discuss AI using LOLANG."}
    ]
    
    # Run conversation for a few turns
    for i in range(3):
        print(TerminalColors.colorize(f"\n--- Turn {i+1} ---", TerminalColors.HEADER))
        
        # Agent 1 responds
        response1 = agent1.chat(response_history)
        formatted_response1 = response1.strip().replace('\n', ' ').replace('  ', ' ')
        print(agent1.speak(formatted_response1))
        response_history.append({
            "role": "agent-1",
            "content": formatted_response1
        })
        
        # Small delay
        time.sleep(2)
        
        # Agent 2 responds
        response2 = agent2.chat(response_history)
        formatted_response2 = response2.strip().replace('\n', ' ').replace('  ', ' ')
        print(agent2.speak(formatted_response2))
        response_history.append({
            "role": "agent-2",
            "content": formatted_response2
        })
        
        # Small delay
        time.sleep(2)
    
    print()


def example_configuration():
    """Demonstrate configuration options."""
    print(TerminalColors.format_header("Configuration Example"))
    
    # Default configuration
    default_config = GeminiConfig.get_default_config()
    print(TerminalColors.colorize("Default Config:", TerminalColors.CYAN))
    print(f"  Model: {default_config.model_name}")
    print(f"  Temperature: {default_config.temperature}")
    print(f"  Max Tokens: {default_config.max_tokens}")
    print(f"  Message Delay: {default_config.message_delay}")
    print()
    
    # Server configuration
    server_config = ServerConfig.get_default_config()
    print(TerminalColors.colorize("Server Config:", TerminalColors.CYAN))
    print(f"  Host: {server_config.host}")
    print(f"  Port: {server_config.port}")
    print(f"  URI: {server_config.uri}")
    print()
    
    # Client configuration
    client_config = ClientConfig.get_default_config()
    print(TerminalColors.colorize("Client Config:", TerminalColors.CYAN))
    print(f"  Server URI: {client_config.server_uri}")
    print(f"  Max Conversations: {client_config.max_conversations}")
    print(f"  Auto Reconnect: {client_config.auto_reconnect}")
    print()


async def main():
    """Run all examples."""
    print(TerminalColors.format_header("LOLANG AI Agent System - Examples"))
    
    try:
        # Configuration examples
        example_configuration()
        
        # Visualizer example
        example_visualizer()
        
        # Basic usage (requires API key)
        config = GeminiConfig.get_default_config()
        if config.validate():
            example_basic_usage()
            await example_decryptor()
            await example_conversation()
        else:
            print(TerminalColors.colorize(
                "Skipping AI examples. Set GEMINI_API_KEY in .env to enable.",
                TerminalColors.YELLOW
            ))
    
    except KeyboardInterrupt:
        print(TerminalColors.colorize("\n\nExample interrupted", TerminalColors.YELLOW))
    except Exception as e:
        print(TerminalColors.colorize(f"\n\nExample error: {e}", TerminalColors.RED))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(TerminalColors.colorize("\nExample interrupted", TerminalColors.YELLOW))
