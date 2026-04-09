"""
WebSocket Server module for LOLANG AI Agent communication system.
Handles multi-client WebSocket server with AI agent integration.
"""
import asyncio
import json
import logging
import signal
import sys
from typing import Set, Dict, Any
from websockets.server import serve
from websockets.legacy.server import WebSocketServerProtocol

from ai_agent import AIAgent
from terminal_colors import TerminalColors
from config import GeminiConfig, ServerConfig
from lolang_decryptor import LolangDecryptor
from message_visualizer import MessageVisualizer

logger = logging.getLogger(__name__)


class AgentServer:
    """WebSocket server that manages AI agent communications."""
    
    def __init__(self, server_config: ServerConfig = None, 
                 gemini_config: GeminiConfig = None):
        """
        Initialize the agent server.
        
        Args:
            server_config: Server configuration
            gemini_config: Gemini AI configuration
        """
        self.server_config = server_config or ServerConfig.get_default_config()
        self.gemini_config = gemini_config or GeminiConfig.get_default_config()
        
        self.agent = AIAgent("Server-Agent", TerminalColors.BLUE, self.gemini_config)
        self.decryptor = LolangDecryptor(self.gemini_config)
        self.visualizer = MessageVisualizer()
        
        self.clients: Set[WebSocketServerProtocol] = set()
        self.response_history: list = []
        self.running = False
        self._server = None
        
        logger.info("AgentServer initialized")

    async def register(self, websocket: WebSocketServerProtocol):
        """
        Register a new client connection.
        
        Args:
            websocket: Client WebSocket connection
        """
        self.clients.add(websocket)
        client_count = len(self.clients)
        print(self.visualizer.visualize_info_message(
            f"Client connected. Total clients: {client_count}"
        ))
        logger.info(f"Client registered. Total: {client_count}")

    async def unregister(self, websocket: WebSocketServerProtocol):
        """
        Unregister a client connection.
        
        Args:
            websocket: Client WebSocket connection
        """
        if websocket in self.clients:
            self.clients.remove(websocket)
            client_count = len(self.clients)
            print(self.visualizer.visualize_info_message(
                f"Client disconnected. Total clients: {client_count}"
            ))
            logger.info(f"Client unregistered. Total: {client_count}")

    async def process_message(self, websocket: WebSocketServerProtocol, message: str):
        """
        Process an incoming message from a client.
        
        Args:
            websocket: Client WebSocket connection
            message: Raw message string
        """
        try:
            data = json.loads(message)
            content = data.get("content", "")
            role = data.get("role", "user")

            # Add message to history
            self.response_history.append({"role": role, "content": content})

            # Decrypt for internal processing
            decrypted_client_message = await self.decryptor.decrypt(content)
            logger.debug(f"Decrypted client message: {decrypted_client_message}")

            # Visualize client message
            print(self.visualizer.visualize_client_message(content))

            # Generate AI response
            response = self.agent.chat(self.response_history)
            formatted_response = response.strip().replace('\n', ' ').replace('  ', ' ')

            # Decrypt server response for internal processing
            decrypted_server_response = await self.decryptor.decrypt(formatted_response)
            logger.debug(f"Decrypted server response: {decrypted_server_response}")

            # Visualize server response
            print(self.visualizer.visualize_server_message(formatted_response))

            # Add response to history
            self.response_history.append({
                "role": "server-agent",
                "content": formatted_response
            })

            # Broadcast response to all clients
            await self.broadcast(json.dumps({
                "role": "server-agent",
                "content": formatted_response
            }))
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON message: {e}")
            print(self.visualizer.visualize_error_message(f"Invalid message format: {e}"))
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            print(self.visualizer.visualize_error_message(f"Message processing error: {e}"))

    async def broadcast(self, message: str):
        """
        Broadcast a message to all connected clients.
        
        Args:
            message: Message to broadcast
        """
        if self.clients:
            try:
                await asyncio.gather(
                    *[client.send(message) for client in self.clients],
                    return_exceptions=True
                )
            except Exception as e:
                logger.error(f"Broadcast error: {e}")

    async def handler(self, websocket: WebSocketServerProtocol, path: str = None):
        """
        WebSocket connection handler.
        
        Args:
            websocket: Client WebSocket connection
            path: Connection path (optional)
        """
        await self.register(websocket)
        try:
            async for message in websocket:
                if not self.running:
                    break
                await self.process_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            logger.info("Client connection closed")
        except Exception as e:
            logger.error(f"Handler error: {e}", exc_info=True)
            print(self.visualizer.visualize_error_message(f"Connection error: {e}"))
        finally:
            await self.unregister(websocket)

    async def start(self):
        """Start the WebSocket server."""
        self.running = True
        
        try:
            self._server = await serve(
                self.handler,
                self.server_config.host,
                self.server_config.port,
                ping_interval=self.server_config.ping_interval,
                ping_timeout=self.server_config.ping_timeout
            )
            
            print(self.visualizer.visualize_success_message(
                f"Server started at {self.server_config.uri}"
            ))
            print(self.visualizer.visualize_info_message(
                "Press Ctrl+C to stop the server"
            ))
            
            logger.info(f"Server listening on {self.server_config.uri}")
            
            # Keep server running
            while self.running:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"Server start error: {e}", exc_info=True)
            raise

    def stop(self):
        """Stop the WebSocket server."""
        self.running = False
        print(self.visualizer.visualize_warning_message("Server stopping..."))
        logger.info("Server stop requested")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get server statistics.
        
        Returns:
            Dictionary with server stats
        """
        return {
            "running": self.running,
            "connected_clients": len(self.clients),
            "message_history_count": len(self.response_history),
            "server_uri": self.server_config.uri,
            "agent_stats": self.agent.get_stats(),
            "decryptor_stats": self.decryptor.get_stats()
        }


# Handle Ctrl+C for Windows
def signal_handler():
    """Handle interrupt signal."""
    print(TerminalColors.colorize("\nStopping server...", TerminalColors.YELLOW))
    sys.exit(0)


async def main():
    """Main entry point for the server."""
    # Configure logging
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger.setLevel(logging.ERROR)
    
    agent_server = AgentServer()

    # Handle graceful shutdown based on platform
    if sys.platform != 'win32':
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, agent_server.stop)
    else:
        # Windows doesn't support add_signal_handler
        pass

    try:
        await agent_server.start()
    except KeyboardInterrupt:
        print(TerminalColors.colorize("\nStopping server...", TerminalColors.YELLOW))
    except Exception as e:
        print(TerminalColors.colorize(f"Server error: {e}", TerminalColors.RED))
        logger.error(f"Server error: {e}", exc_info=True)
    finally:
        agent_server.stop()
        if agent_server._server:
            agent_server._server.close()
            await agent_server._server.wait_closed()
        print(TerminalColors.colorize("Server closed", TerminalColors.YELLOW))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        signal_handler()


