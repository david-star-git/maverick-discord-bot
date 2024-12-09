import json

def get_user_color(user_id: int) -> int:
    # Load colors.json
    with open('data/colors.json', 'r') as f:
        colors_data = json.load(f)

    # Fetch user-specific colors or default to pingwin
    user_colors = colors_data.get('user_colors', {})
    default_colors = colors_data.get('default_colors', {})

    # Get the color name for the user or use pingwin as default
    color_name = user_colors.get(str(user_id), 'pingwin')

    # Get the hex color code from default_colors
    hex_color = default_colors.get(color_name, default_colors.get('pingwin'))

    # Remove the '#' and convert the hex color code to an integer
    return int(hex_color.replace('#', ''), 16)
