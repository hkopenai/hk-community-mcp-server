import unittest
from unittest import mock
from unittest.mock import patch, Mock
from hkopenai.hk_community_mcp_server.app import create_mcp_server

class TestApp(unittest.TestCase):
    @patch('hkopenai.hk_community_mcp_server.app.FastMCP')
    @patch('hkopenai.hk_community_mcp_server.tool_elderly_wait_time_ccs.fetch_elderly_wait_time_data')
    def test_create_mcp_server(self, mock_tool_elderly, mock_fastmcp):
        # Setup mocks
        mock_server = Mock()
        
        # Track decorator calls and capture decorated functions
        decorator_calls = []
        decorated_funcs = []
        
        def tool_decorator(description=None):
            # First call: @tool(description=...)
            decorator_calls.append(((), {'description': description}))
            
            def decorator(f):
                # Second call: decorator(function)
                nonlocal decorated_funcs
                decorated_funcs.append(f)
                return f
                
            return decorator
            
        mock_server.tool = tool_decorator
        mock_fastmcp.return_value = mock_server
        mock_tool_elderly.return_value = [{'Service': 'Integrated Home Care Services', 'No. of applicants': 8836, 'Waiting time (months)': 19, 'Inactive cases due to voucher': 2330, 'As at date': '31-May-19'}]

        # Test server creation
        server = create_mcp_server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        self.assertEqual(server, mock_server)

        # Verify tools were decorated
        self.assertTrue(len(decorated_funcs) > 0)
        
        # Test the actual decorated functions
        for func in decorated_funcs:
            if func.__name__ == 'get_elderly_wait_time_ccs':
                result = func(2019, 2020)
                mock_tool_elderly.assert_called_once_with(2019, 2020)
                self.assertEqual(result, [{'Service': 'Integrated Home Care Services', 'No. of applicants': 8836, 'Waiting time (months)': 19, 'Inactive cases due to voucher': 2330, 'As at date': '31-May-19'}])

if __name__ == "__main__":
    unittest.main()
