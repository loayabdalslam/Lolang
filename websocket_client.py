"""
WebSocket Client module for LOLANG AI Agent communication system.
Handles WebSocket connection with automatic reconnection and AI agent integration.
"""
import asyncio
import json
import logging
import signal
import sys
from typing import List, Dict, Optional
from websockets.client import connect
from websockets.exceptions import ConnectionClosed, WebSocketException

from ai_agent import AIAgent
from terminal_colors import TerminalColors
from config import GeminiConfig, ClientConfig
from lolang_decryptor import LolangDecryptor
from message_visualizer import MessageVisualizer

logger = logging.getLogger(__name__)


class AgentClient:
    """WebSocket client that communicates with AI agents using LOLANG."""
    
    def __init__(self, client_config: ClientConfig = None, 
                 gemini_config: GeminiConfig = None):
        """
        Initialize the agent client.
        
        Args:
            client_config: Client configuration
            gemini_config: Gemini AI configuration
        """
        self.client_config = client_config or ClientConfig.get_default_config()
        self.gemini_config = gemini_config or GeminiConfig.get_default_config()
        
        self.agent = AIAgent("Client-Agent", TerminalColors.GREEN, self.gemini_config)
        self.decryptor = LolangDecryptor(self.gemini_config)
        self.visualizer = MessageVisualizer()
        
        self.response_history: List[Dict[str, str]] = []
        self.websocket = None
        self.running = False
        self.conversation_count = 0
        self._reconnect_attempts = 0
        
        logger.info("AgentClient initialized")

    async def connect(self, uri: str = None) -> bool:
        """
        Establish WebSocket connection.
        
        Args:
            uri: Server URI (uses config value if None)
            
        Returns:
            True if connection successful, False otherwise
        """
        target_uri = uri or self.client_config.server_uri
        
        try:
            self.websocket = await connect(target_uri)
            self._reconnect_attempts = 0
            logger.info(f"Connected to {target_uri}")
            print(TerminalColors.colorize(
                f"Connected to {target_uri}", 
                TerminalColors.GREEN
            ))
            return True
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            print(self.visualizer.visualize_error_message(f"Connection failed: {e}"))
            return False

    async def reconnect(self) -> bool:
        """
        Attempt to reconnect to the server.
        
        Returns:
            True if reconnection successful, False otherwise
        """
        if not self.client_config.auto_reconnect:
            return False
            
        if self._reconnect_attempts >= self.client_config.max_reconnect_attempts:
            logger.error("Max reconnection attempts reached")
            print(self.visualizer.visualize_error_message(
                "Max reconnection attempts reached"
            ))
            return False
        
        self._reconnect_attempts += 1
        delay = self.client_config.reconnect_delay * (2 ** (self._reconnect_attempts - 1))
        
        print(self.visualizer.visualize_warning_message(
            f"Reconnecting in {delay:.1f}s (attempt {self._reconnect_attempts}/{self.client_config.max_reconnect_attempts})"
        ))
        logger.info(f"Reconnect attempt {self._reconnect_attempts} in {delay}s")
        
        await asyncio.sleep(delay)
        return await self.connect()

    async def send_message(self, content: str) -> bool:
        """
        Send a message to the server.
        
        Args:
            content: Message content
            
        Returns:
            True if message sent successfully, False otherwise
        """
        if not self.websocket:
            print(self.visualizer.visualize_error_message("Not connected to server"))
            return False

        # Add to history
        self.response_history.append({"role": "client-agent", "content": content})

        # Display initial human message without decryption
        if len(self.response_history) == 1:
            print(self.visualizer.visualize_message("You", content))

        try:
            # Send to server
            await self.websocket.send(json.dumps({
                "role": "client-agent",
                "content": content
            }))
            return True
        except Exception as e:
            logger.error(f"Send message failed: {e}")
            print(self.visualizer.visualize_error_message(f"Send failed: {e}"))
            return False

    async def receive_messages(self):
        """Receive and process messages from the server."""
        if not self.websocket:
            print(self.visualizer.visualize_error_message("Not connected to server"))
            return

        try:
            async for message in self.websocket:
                if not self.running:
                    break

                try:
                    data = json.loads(message)
                    content = data.get("content", "")
                    role = data.get("role", "server-agent")

                    # Add to history
                    self.response_history.append({"role": role, "content": content})

                    # Visualize server message
                    print(self.visualizer.visualize_message(role, content))

                    # Increment conversation count
                    self.conversation_count += 1

                    # Check if we've reached the maximum conversations
                    if self.conversation_count >= self.client_config.max_conversations:
                        print(self.visualizer.visualize_system_message(
                            "Maximum conversation turns reached. Ending conversation."
                        ))
                        self.running = False
                        break

                    # Generate response with delay
                    await asyncio.sleep(2)
                    response = await self.agent.chat_async(self.response_history)
                    formatted_response = response.strip().replace('\n', ' ').replace('  ', ' ')

                    # Visualize client response
                    print(self.visualizer.visualize_client_message(formatted_response))

                    # Send response
                    await self.send_message(formatted_response)
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON received: {e}")
                    print(self.visualizer.visualize_error_message(f"Invalid message format: {e}"))
                except Exception as e:
                    logger.error(f"Error processing message: {e}", exc_info=True)
                    print(self.visualizer.visualize_error_message(f"Message error: {e}"))

        except ConnectionClosed:
            logger.warning("Connection closed by server")
            print(self.visualizer.visualize_warning_message("Connection closed by server"))
            
            # Attempt reconnection if enabled
            if self.client_config.auto_reconnect and self.running:
                if await self.reconnect():
                    await self.receive_messages()
        except WebSocketException as e:
            logger.error(f"WebSocket error: {e}")
            print(self.visualizer.visualize_error_message(f"WebSocket error: {e}"))
        except Exception as e:
            logger.error(f"Receive error: {e}", exc_info=True)
            print(self.visualizer.visualize_error_message(f"Receive error: {e}"))
        finally:
            await self.close()

    async def close(self):
        """Close the WebSocket connection."""
        if self.websocket:
            try:
                await self.websocket.close()
                logger.info("WebSocket connection closed")
            except Exception as e:
                logger.error(f"Error closing connection: {e}")
            finally:
                self.websocket = None

    def stop(self):
        """Stop the client."""
        self.running = False
        print(self.visualizer.visualize_warning_message("Client stopping..."))
        logger.info("Client stop requested")
    
    def get_stats(self) -> dict:
        """
        Get client statistics.
        
        Returns:
            Dictionary with client stats
        """
        return {
            "running": self.running,
            "conversation_count": self.conversation_count,
            "message_history_count": len(self.response_history),
            "reconnect_attempts": self._reconnect_attempts,
            "agent_stats": self.agent.get_stats(),
            "decryptor_stats": self.decryptor.get_stats()
        }


# Handle Ctrl+C for Windows
def signal_handler():
    """Handle interrupt signal."""
    print(TerminalColors.colorize("\nStopping client...", TerminalColors.YELLOW))
    sys.exit(0)


async def main():
    """Main entry point for the client."""
    # Configure logging
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger.setLevel(logging.ERROR)
    
    client = AgentClient()
    uri = "ws://localhost:8765"

    # Handle graceful shutdown based on platform
    if sys.platform != 'win32':
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, client.stop)
    else:
        # Windows doesn't support add_signal_handler
        pass

    try:
        client.running = True
        
        # Connect to server
        if not await client.connect(uri):
            print(client.visualizer.visualize_error_message("Failed to connect to server"))
            return

        # Send initial message
        initial_message = "Hello, are you an AI agent? Let's discuss artificial intelligence using LOLANG."
        await client.send_message(initial_message)

        # Start receiving messages
        await client.receive_messages()

    except KeyboardInterrupt:
        print(TerminalColors.colorize("\nStopping client...", TerminalColors.YELLOW))
    except Exception as e:
        print(TerminalColors.colorize(f"Client error: {e}", TerminalColors.RED))
        logger.error(f"Client error: {e}", exc_info=True)
    finally:
        client.running = False
        await client.close()
        print(TerminalColors.colorize("Connection closed", TerminalColors.YELLOW))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        signal_handler()
