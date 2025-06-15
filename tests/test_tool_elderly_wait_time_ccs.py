import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_community_mcp_server import tool_elderly_wait_time_ccs

class TestElderlyWaitTimeCCS(unittest.TestCase):
    @patch('hkopenai.hk_community_mcp_server.tool_elderly_wait_time_ccs.requests.get')
    def test_fetch_elderly_wait_time_data(self, mock_get):
        # Setup mock response
        mock_response = Mock()
        mock_response.content = (
            "資助長者社區照顧服務\tSubsidised CCS for the elderly \t輪候人數\tNo. of applicants\t\"輪候時間（以月數為單位）\": \"\tWaiting time (in months) (Average from the past 3 months) \t因使用長者社區照顧服務券而被列為「非活躍」個案的長者人數\tNo. of elderly persons classified as “inactive” upon using the Community Care Service Voucher for the Elderly\t截至日期\tAs at date\r\n綜合家居照顧服務(體弱個案)/改善家居及社區照顧服務\tIntegrated Home Care Services (Frail Cases)/Enhanced Home and Community Care Services\t8836\t8836\t19\t19\t2330\t2330\t二零一九年五月三十一日\t31-May-21\r\n長者日間護理中心/單位\tDay Care Centres/Units for the Elderly\t4649\t4649\t12\t12\t2330\t2330\t二零一九年五月三十一日\t31-May-19\r\n綜合家居照顧服務(體弱個案)/改善家居及社區照顧服務\tIntegrated Home Care Services (Frail Cases)/Enhanced Home and Community Care Services\t8471\t8471\t19\t19\t2347\t2347\t二零一九年六月三十日\t30-Jun-19\r\n長者日間護理中心/單位\tDay Care Centres/Units for the Elderly\t4709\t4709\t13\t13\t2347\t2347\t二零一九年六月三十日\t30-Jun-19\r\n綜合家居照顧服務(體弱個案)/改善家居及社區照顧服務\tIntegrated Home Care Services (Frail Cases)/Enhanced Home and Community Care Services\t8650\t8650\t20\t20\t2393\t2393\t二零一九年七月三十一日\t31-Jul-20\r\n長者日間護理中心/單位\tDay Care Centres/Units for the Elderly\t4771\t4771\t12\t12\t2393\t2393\t二零一九年七月三十一日\t31-Jul-19\r\n綜合家居照顧服務(體弱個案)/改善家居及社區照顧服務\tIntegrated Home Care Services (Frail Cases)/Enhanced Home and Community Care Services\t8678\t8678\t21\t21\t2352\t2352\t二零一九年八月三十一日\t31-Aug-19\r\n長者日間護理中心/單位\tDay Care Centres/Units for the Elderly\t4870\t4870\t12\t12\t2352\t2352\t二零一九年八月三十一日\t31-Aug-19\r\n綜合家居照顧服務(體弱個案)/改善家居及社區照顧服務\tIntegrated Home Care Services (Frail Cases)/Enhanced Home and Community Care Services\t8264\t8264\t21\t21\t2548\t2548\t二零一九年九月三十日\t30-Sep-19\r\n長者日間護理中心/單位\tDay Care Centres/Units for the Elderly\t4718\t4718\t11\t11\t2548\t2548\t二零一九年九月三十日\t30-Sep-19\r\n綜合家居照顧服務(體弱個案)/改善家居及社區照顧服務\tIntegrated Home Care Services (Frail Cases)/Enhanced Home and Community Care Services\t7265\t7265\t18\t18\t2532\t2532\t二零一九年十月三十一日\t31-Oct-19\r\n長者日間護理中心/單位\tDay Care Centres/Units for the Elderly\t4744\t4744\t12\t12\t2532\t2532\t二零一九年十月三十一日\t31-Oct-19\r\n綜合家居照顧服務(體弱個案)/改善家居及社區照顧服務\tIntegrated Home Care Services (Frail Cases)/Enhanced Home and Community Care Services\t6410\t6410\t17\t17\t2640\t2640\t二零一九年十一月三十日\t30-Nov-19\r\n"
        ).encode('utf-16-le')
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Call the function under test
        result = tool_elderly_wait_time_ccs.fetch_elderly_wait_time_data(2019, 2020)

        # Assertions
        mock_get.assert_called_once_with("https://www.swd.gov.hk/datagovhk/elderly/statistics-on-waiting-list-and-waiting-time-for-ccs.csv")
        self.assertEqual(len(result), 12)

if __name__ == "__main__":
    unittest.main()
