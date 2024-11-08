from datetime import datetime as dt

# Examples
# console.log("This is an informational message.")
# console.error("This is an error message.")
# console.warning("This is a warning message.")
# console.success("This is a success message.")
# console.wtf("This should never happen!")

class Console:
    """A simple logging class with different levels of logging."""
    
    # ANSI escape sequences for colors
    COLORS = {
        "INFO": "\033[0;34m",      # Blue
        "ERROR": "\033[0;31m",     # Red
        "WARNING": "\033[0;33m",   # Yellow
        "SUCCESS": "\033[0;32m",   # Green
        "WTF": "\033[1;35m",       # Bright Magenta
        "GRAY": "\033[0;37m",      # Light Gray for timestamp
        "RESET": "\033[0m"         # Reset to default
    }

    def log(self, message: str):
        """Logs an informational message to the console with a timestamp."""
        self._write_log("INFO", message)

    def error(self, message: str):
        """Logs an error message to the console with a timestamp."""
        self._write_log("ERROR", message)

    def warning(self, message: str):
        """Logs a warning message to the console with a timestamp."""
        self._write_log("WARNING", message)
    
    def success(self, message: str):
        """Logs a success message to the console with a timestamp."""
        self._write_log("SUCCESS", message)
    
    def wtf(self, message: str):
        """Logs a critical error message to the console, indicating
        a serious issue that should never occur. with a timestamp."""
        self._write_log("WTF", message)

    def _write_log(self, level: str, message: str):
        """Internal method to write a log message with a specified level."""
        current_time = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp_color = self.COLORS["GRAY"]
        color = self.COLORS.get(level, self.COLORS["RESET"])
        
        # Set message color based on log level
        if level == "INFO":
            message_color = self.COLORS["RESET"]
        else:
            message_color = self.COLORS.get(level, self.COLORS[level])

        print(f"{timestamp_color}[{current_time}]{self.COLORS['RESET']} {color}[{level}]{self.COLORS['RESET']} {message_color}{message}{self.COLORS['RESET']}")

# Create an instance of the Console class
console = Console()
