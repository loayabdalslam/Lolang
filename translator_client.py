"""
Translator Client module for LOLANG communication system.
Connects to WebSocket server and translates all LOLANG messages in real-time.
"""
import asyncio
import json
import logging
import signal
import sys
from typing import Optional
from websockets.client import connect
from websockets.exceptions import ConnectionClosed, WebSocketException

from terminal_colors import TerminalColors
from config import GeminiConfig, ClientConfig
from lolang_decryptor import LolangDecryptor
from message_visualizer import MessageVisualizer

logger = logging.getLogger(__name__)


class TranslatorClient:
    """WebSocket client that translates LOLANG messages in real-time."""
    
    def __init__(self, client_config: ClientConfig = None, 
                 gemini_config: GeminiConfig = None):
        """
        Initialize the translator client.
        
        Args:
            client_config: Client configuration
            gemini_config: Gemini AI configuration
        """
        self.client_config = client_config or ClientConfig.get_default_config()
        self.gemini_config = gemini_config or GeminiConfig.get_default_config()
        
        self.decryptor = LolangDecryptor(self.gemini_config)
        self.visualizer = MessageVisualizer()
        
        self.websocket = None
        self.running = False
        self.message_count = 0
        self._reconnect_attempts = 0
        
        logger.info("TranslatorClient initialized")

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

    async def receive_messages(self):
        """Receive and translate messages from the server."""
        if not self.websocket:
            print(self.visualizer.visualize_error_message("Not connected to server"))
            return

        print(self.visualizer.visualize_system_message(
            "Translator client connected. Translating all LOLANG messages in real-time."
        ))
        print(self.visualizer.visualize_system_message(
            "Press Ctrl+C to stop the translator."
        ))
        print(self.visualizer.visualize_system_message(
            "Waiting for messages..."
        ))
        print(self.visualizer.visualize_separator())

        try:
            async for message in self.websocket:
                if not self.running:
                    break

                try:
                    data = json.loads(message)
                    content = data.get("content", "")
                    role = data.get("role", "server-agent")

                    # Determine colors based on role
                    if "server" in role.lower():
                        encrypted_color = TerminalColors.BLUE
                        translated_color = TerminalColors.YELLOW
                    else:
                        encrypted_color = TerminalColors.GREEN
                        translated_color = TerminalColors.HEADER

                    # Format role name for display
                    display_role = role.replace("-agent", "").title()

                    # Decrypt the message
                    decrypted_content = await self.decryptor.decrypt(content)

                    # Display both encrypted and decrypted messages
                    print(TerminalColors.colorize(
                        f"[ENCRYPTED] {display_role}: {content}", 
                        encrypted_color
                    ))
                    print(TerminalColors.colorize(
                        f"[TRANSLATED] {display_role}: {decrypted_content}", 
                        translated_color
                    ))
                    print(self.visualizer.visualize_separator())

                    # Increment message count
                    self.message_count += 1
                    
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
        """Stop the translator client."""
        self.running = False
        print(self.visualizer.visualize_warning_message("Translator client stopping..."))
        logger.info("Translator client stop requested")
    
    def get_stats(self) -> dict:
        """
        Get translator client statistics.
        
        Returns:
            Dictionary with client stats
        """
        return {
            "running": self.running,
            "message_count": self.message_count,
            "reconnect_attempts": self._reconnect_attempts,
            "decryptor_stats": self.decryptor.get_stats()
        }


# Handle Ctrl+C for Windows
def signal_handler():
    """Handle interrupt signal."""
    print(TerminalColors.colorize("\nStopping translator client...", TerminalColors.YELLOW))
    sys.exit(0)


async def main():
    """Main entry point for the translator client."""
    # Configure logging
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger.setLevel(logging.ERROR)
    
    translator = TranslatorClient()
    uri = "ws://localhost:8765"

    # Handle graceful shutdown based on platform
    if sys.platform != 'win32':
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, translator.stop)
    else:
        # Windows doesn't support add_signal_handler
        pass

    try:
        translator.running = True
        
        # Connect to server
        if not await translator.connect(uri):
            print(translator.visualizer.visualize_error_message(
                "Failed to connect to server"
            ))
            return

        # Start receiving and translating messages
        await translator.receive_messages()

    except KeyboardInterrupt:
        print(TerminalColors.colorize("\nStopping translator client...", TerminalColors.YELLOW))
    except Exception as e:
        print(TerminalColors.colorize(f"Translator error: {e}", TerminalColors.RED))
        logger.error(f"Translator error: {e}", exc_info=True)
    finally:
        translator.running = False
        await translator.close()
        print(TerminalColors.colorize("Connection closed", TerminalColors.YELLOW))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        signal_handler()
