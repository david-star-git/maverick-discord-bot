import json

def get_user_color(user_id: int) -> str:
    # Load colors.json
    with open('colors.json', 'r') as f:
        colors_data = json.load(f)

    # Fetch user-specific colors or default to purple
    user_colors = colors_data.get('user_colors', {})
    default_colors = colors_data.get('default_colors', {})

    # Get the color name for the user or use purple as default
    color_name = user_colors.get(str(user_id), 'purple')

    # Return the hex color code from default_colors
    return default_colors.get(color_name, default_colors.get('purple'))
