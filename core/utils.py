from rich.console import Console

console = Console()

class Colors:
    HEADER = 'magenta'
    BLUE = 'blue'
    GREEN = 'green'
    YELLOW = 'yellow'
    RED = 'red'
    ENDC = ''
    BOLD = 'bold'
    UNDERLINE = 'underline'

def print_color(message, color=Colors.BLUE):
    """Print colored message."""
    if color in [Colors.BOLD, Colors.UNDERLINE]:
        console.print(f"[{color}]{message}[/{color}]")
    else:
        # We can just pass the color style to rich print
        # Some colors defined above are standard ansi names, rich supports them
        console.print(f"[{color}]{message}[/{color}]")

def to_snake_case(text: str) -> str:
    """Convert text to snake_case."""
    import re
    str1 = re.sub('(.)([A-Z][a-z]+)', r'\\1_\\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\\1_\\2', str1).lower()

def to_pascal_case(text: str) -> str:
    """Convert text to PascalCase."""
    return ''.join(word.capitalize() for word in to_snake_case(text).split('_'))
