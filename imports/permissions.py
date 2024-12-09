import json

def has_permission(user_id: int, command: str) -> bool:
    """
    Checks if a user has permission to execute a specified command.
    
    Args:
        user_id (int): The unique ID of the user whose permissions are being checked.
        command (str): The command for which the permission is being checked.
    
    Returns:
        bool: True if the user has permission to execute the command, False otherwise.
    
    Example:
    >>> has_permission(377185902998323203, 'ping')
    True
    """
    with open('data/perms.json', 'r') as file:
        perms = json.load(file)

    # Check if user has specific permissions
    user_perms = perms.get('users', {}).get(str(user_id), {})
    user_groups = user_perms.get('groups', [])
    user_permissions = set(user_perms.get('perms', []))

    # Collect all permissions from the user's groups
    group_permissions = set()
    for group in user_groups:
        group_permissions.update(perms.get('groups', {}).get(group, []))

    # Get permissions available to everyone
    everyone_permissions = set(perms.get('users', {}).get('everyone', {}).get('perms', []))

    # Combine all permissions
    all_permissions = user_permissions | group_permissions | everyone_permissions

    return command in all_permissions
