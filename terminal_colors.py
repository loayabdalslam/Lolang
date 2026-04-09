"""
Terminal color and formatting utilities for LOLANG AI Agent System.
Provides cross-platform color support and enhanced formatting options.
"""
import sys
import os


class TerminalColors:
    """Terminal color codes and formatting utilities."""
    
    # Standard colors
    BLACK = '\033[30m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[31m'
    BRIGHT_GREEN = '\033[32m'
    BRIGHT_YELLOW = '\033[33m'
    BRIGHT_BLUE = '\033[34m'
    BRIGHT_MAGENTA = '\033[35m'
    BRIGHT_CYAN = '\033[36m'
    BRIGHT_WHITE = '\033[37m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # Text formatting
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKETHROUGH = '\033[9m'
    
    # Convenience aliases
    HEADER = MAGENTA
    ENDC = RESET
    
    # Check if terminal supports colors
    _supports_color = None
    
    @classmethod
    def supports_color(cls) -> bool:
        """Check if the current terminal supports colors."""
        if cls._supports_color is None:
            # Check environment variables
            if os.environ.get('TERM') == 'dumb':
                cls._supports_color = False
            elif os.environ.get('NO_COLOR'):
                cls._supports_color = False
            # Windows console
            elif sys.platform == 'win32':
                cls._supports_color = True
            # Check if stdout is a TTY
            elif hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
                cls._supports_color = True
            else:
                cls._supports_color = False
        return cls._supports_color
    
    @classmethod
    def colorize(cls, text: str, color: str, styles: list = None) -> str:
        """
        Apply color and styles to text.
        
        Args:
            text: Text to colorize
            color: Color code to apply
            styles: List of style codes to apply
            
        Returns:
            Colorized text string
        """
        if not cls.supports_color():
            return text
            
        style_codes = ''
        if styles:
            for style in styles:
                style_codes += style
                
        return f"{style_codes}{color}{text}{cls.RESET}"
    
    @classmethod
    def format_text(cls, text: str, styles: list) -> str:
        """
        Apply multiple styles to text without color.
        
        Args:
            text: Text to style
            styles: List of style codes to apply
            
        Returns:
            Styled text string
        """
        if not cls.supports_color():
            return text
            
        style_codes = ''.join(styles)
        return f"{style_codes}{text}{cls.RESET}"
    
    @classmethod
    def disable_colors(cls):
        """Manually disable color output."""
        cls._supports_color = False
    
    @classmethod
    def enable_colors(cls):
        """Manually enable color output."""
        cls._supports_color = True
    
    @classmethod
    def get_role_color(cls, role: str) -> str:
        """
        Get appropriate color for a given role.
        
        Args:
            role: Role name (e.g., 'server', 'client', 'system')
            
        Returns:
            Color code for the role
        """
        role_colors = {
            'server': cls.BLUE,
            'client': cls.GREEN,
            'system': cls.HEADER,
            'error': cls.RED,
            'warning': cls.YELLOW,
            'success': cls.GREEN,
            'info': cls.CYAN,
            'debug': cls.BRIGHT_BLACK,
        }
        
        role_lower = role.lower()
        for key, color in role_colors.items():
            if key in role_lower:
                return color
        
        return cls.WHITE
    
    @classmethod
    def format_message(cls, role: str, message: str, show_role: bool = True) -> str:
        """
        Format a complete message with role and color.
        
        Args:
            role: Role name
            message: Message content
            show_role: Whether to show the role prefix
            
        Returns:
            Formatted message string
        """
        color = cls.get_role_color(role)
        prefix = f"{role}: " if show_role else ""
        return cls.colorize(f"{prefix}{message}", color)
    
    @classmethod
    def format_header(cls, text: str, char: str = '=', width: int = 80) -> str:
        """
        Format a header with decorative characters.
        
        Args:
            text: Header text
            char: Character to use for decoration
            width: Total width of the header
            
        Returns:
            Formatted header string
        """
        if not cls.supports_color():
            return f"\n{char * width}\n{text}\n{char * width}\n"
            
        border = char * width
        return f"\n{cls.colorize(border, cls.CYAN)}\n{cls.colorize(text, cls.HEADER, [cls.BOLD])}\n{cls.colorize(border, cls.CYAN)}\n"
    
    @classmethod
    def format_separator(cls, char: str = '-', width: int = 80) -> str:
        """
        Format a separator line.
        
        Args:
            char: Character to use for separator
            width: Width of the separator
            
        Returns:
            Formatted separator string
        """
        if not cls.supports_color():
            return char * width
            
        return cls.colorize(char * width, cls.BRIGHT_BLACK)
