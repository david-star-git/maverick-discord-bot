import json
import unittest
from unittest.mock import patch, mock_open
from imports.permissions import has_permission  # Adjust the import as necessary

class TestPermissionUtil(unittest.TestCase):

    def setUp(self):
        # Define the permissions JSON data to be used in the tests
        self.perms_json = json.dumps({
            "users": {
                "everyone": {
                    "perms": ["help", "ticket", "location", "void_trader", "price"]
                },
                "377185902998323203": {
                    "nickname": "Lua",
                    "groups": ["dev", "mod", "tester"],
                    "perms": [""]
                },
                "620272143955001385": {
                    "nickname": "Doxter",
                    "groups": ["tester"],
                    "perms": [""]
                }
            },
            "groups": {
                "dev": ["api_call", "ping"],
                "mod": ["manage_ticket", "ping"],
                "tester": ["set_calc", "shopping", "ping"]
            }
        })

    @patch("builtins.open", new_callable=mock_open)
    def test_user_with_specific_permission(self, mock_file):
        mock_file.return_value.read.return_value = self.perms_json
        result = has_permission(377185902998323203, "api_call")
        self.assertTrue(result)

    @patch("builtins.open", new_callable=mock_open)
    def test_user_with_group_permissions(self, mock_file):
        mock_file.return_value.read.return_value = self.perms_json
        result = has_permission(620272143955001385, "shopping")
        self.assertTrue(result)

    @patch("builtins.open", new_callable=mock_open)
    def test_user_without_permission(self, mock_file):
        mock_file.return_value.read.return_value = self.perms_json
        result = has_permission(620272143955001385, "api_call")  # This user does not have api_call permission
        self.assertFalse(result)

    @patch("builtins.open", new_callable=mock_open)
    def test_user_with_everyone_permission(self, mock_file):
        mock_file.return_value.read.return_value = self.perms_json
        result = has_permission(0, "help")  # Assuming everyone has access to 'help'
        self.assertTrue(result)

    @patch("builtins.open", new_callable=mock_open)
    def test_user_not_found(self, mock_file):
        mock_file.return_value.read.return_value = self.perms_json
        result = has_permission(999999999999999999, "set_calc")  # This command is only available to certain groups
        self.assertFalse(result)

    @patch("builtins.open", new_callable=mock_open)
    def test_permission_not_found(self, mock_file):
        mock_file.return_value.read.return_value = self.perms_json
        result = has_permission(377185902998323203, "this_does_not_exist")  # Command that does not exist
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()