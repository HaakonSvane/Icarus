from src.alphavantage.alpha_vantage_api.alphavantage import AlphaVantage

class FundamentalData(AlphaVantage):
    def __init__(self, api_key=None, output_format='json'):
        super().__init__(api_key, output_format)

    @AlphaVantage._make_request
    def get_company_overview(self, symbol):
        return "OVERVIEW"

    @AlphaVantage._make_request
    def get_income_statement(self, symbol):
        return "INCOME_STATEMENT"

    @AlphaVantage._make_request
    def get_income_statement(self, symbol):
        return "BALANCE_SHEET"