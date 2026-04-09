"""
Message Visualizer module for LOLANG communication system.
Provides formatted output for encrypted and decrypted messages.
"""
import logging
from terminal_colors import TerminalColors
from typing import Optional

logger = logging.getLogger(__name__)


class MessageVisualizer:
    """
    A module for visualizing LOLANG messages and their decrypted versions.
    Provides formatted output for better readability.
    """

    def __init__(self, separator_width: int = 80):
        """
        Initialize the message visualizer.
        
        Args:
            separator_width: Width of separator lines
        """
        self.logger = logger
        self.separator_width = separator_width

    def visualize_message(self, role: str, encrypted_message: str, 
                         decrypted_message: Optional[str] = None,
                         show_encrypted: bool = True,
                         show_decrypted: bool = True) -> str:
        """
        Visualize a message with its encrypted and optionally decrypted forms.

        Args:
            role: The role of the message sender (e.g., "Server-Agent", "Client-Agent")
            encrypted_message: The original LOLANG encrypted message
            decrypted_message: The decrypted human-readable message
            show_encrypted: Whether to show encrypted version
            show_decrypted: Whether to show decrypted version

        Returns:
            The formatted message for display
        """
        parts = []
        
        # Format the encrypted message
        if show_encrypted:
            encrypted_color = TerminalColors.get_role_color(role)
            formatted_encrypted = TerminalColors.colorize(
                f"[ENCRYPTED] {role}: {encrypted_message}",
                encrypted_color
            )
            parts.append(formatted_encrypted)

        # If decrypted message is provided, format it
        if decrypted_message and show_decrypted:
            formatted_decrypted = TerminalColors.colorize(
                f"[DECRYPTED] {role}: {decrypted_message}",
                TerminalColors.YELLOW
            )
            parts.append(formatted_decrypted)

        return "\n".join(parts)

    def visualize_client_message(self, encrypted_message: str, 
                                decrypted_message: Optional[str] = None,
                                **kwargs) -> str:
        """
        Visualize a client message.

        Args:
            encrypted_message: The original LOLANG encrypted message
            decrypted_message: The decrypted human-readable message
            **kwargs: Additional arguments passed to visualize_message

        Returns:
            The formatted client message for display
        """
        return self.visualize_message("Client-Agent", encrypted_message, 
                                     decrypted_message, **kwargs)

    def visualize_server_message(self, encrypted_message: str, 
                                decrypted_message: Optional[str] = None,
                                **kwargs) -> str:
        """
        Visualize a server message.

        Args:
            encrypted_message: The original LOLANG encrypted message
            decrypted_message: The decrypted human-readable message
            **kwargs: Additional arguments passed to visualize_message

        Returns:
            The formatted server message for display
        """
        return self.visualize_message("Server-Agent", encrypted_message, 
                                     decrypted_message, **kwargs)

    def visualize_system_message(self, message: str) -> str:
        """
        Visualize a system message.

        Args:
            message: The system message to display

        Returns:
            The formatted system message for display
        """
        return TerminalColors.colorize(f"System: {message}", TerminalColors.HEADER)

    def visualize_error_message(self, message: str) -> str:
        """
        Visualize an error message.

        Args:
            message: The error message to display

        Returns:
            The formatted error message for display
        """
        return TerminalColors.colorize(f"Error: {message}", TerminalColors.RED)

    def visualize_warning_message(self, message: str) -> str:
        """
        Visualize a warning message.

        Args:
            message: The warning message to display

        Returns:
            The formatted warning message for display
        """
        return TerminalColors.colorize(f"Warning: {message}", TerminalColors.YELLOW)

    def visualize_success_message(self, message: str) -> str:
        """
        Visualize a success message.

        Args:
            message: The success message to display

        Returns:
            The formatted success message for display
        """
        return TerminalColors.colorize(f"Success: {message}", TerminalColors.GREEN)

    def visualize_info_message(self, message: str) -> str:
        """
        Visualize an info message.

        Args:
            message: The info message to display

        Returns:
            The formatted info message for display
        """
        return TerminalColors.colorize(f"Info: {message}", TerminalColors.CYAN)

    def visualize_header(self, text: str) -> str:
        """
        Visualize a header.

        Args:
            text: The header text

        Returns:
            The formatted header
        """
        return TerminalColors.format_header(text)

    def visualize_separator(self) -> str:
        """
        Create a separator line.

        Returns:
            Formatted separator
        """
        return TerminalColors.format_separator('-', self.separator_width)

    def visualize_conversation(self, messages: list) -> str:
        """
        Visualize a complete conversation with multiple messages.

        Args:
            messages: List of message dicts with keys: 'role', 'encrypted', 'decrypted' (optional)

        Returns:
            Formatted conversation string
        """
        parts = []
        parts.append(self.visualize_header("Conversation"))
        parts.append(self.visualize_separator())
        
        for msg in messages:
            role = msg.get('role', 'Unknown')
            encrypted = msg.get('encrypted', '')
            decrypted = msg.get('decrypted')
            
            parts.append(self.visualize_message(role, encrypted, decrypted))
            parts.append(self.visualize_separator())
        
        return "\n".join(parts)

    def print_message(self, message: str, clear_screen: bool = False):
        """
        Print a formatted message to console.

        Args:
            message: Message to print
            clear_screen: Whether to clear screen before printing
        """
        if clear_screen:
            import os
            os.system('cls' if os.name == 'nt' else 'clear')
        print(message)
