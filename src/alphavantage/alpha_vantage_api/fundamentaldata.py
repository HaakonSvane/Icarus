from src.alphavantage.alpha_vantage_api.alphavantage import AlphaVantage
import re
import pathlib


# TODO: Mostly only returns json format. Convert to user format.
class FundamentalData(AlphaVantage):
    def __init__(self, api_key=None, output_format='json',
                 error_log_dir=pathlib.Path(__file__).parent.parent.absolute(), log_errors=True):
        super().__init__(api_key, output_format, error_log_dir, log_errors)

    @AlphaVantage._shape_request
    def get_company_overview(self, symbol):
        return "OVERVIEW"

    @AlphaVantage._shape_request
    def get_income_statement(self, symbol):
        return "INCOME_STATEMENT"

    @AlphaVantage._shape_request
    def get_balance_sheet(self, symbol):
        return "BALANCE_SHEET"

    @AlphaVantage._shape_request
    def get_cash_flow(self, symbol):
        return "CASH_FLOW"

    # TODO: This returns csv no matter what
    @AlphaVantage._shape_request
    def get_listing_status(self, date=None, state='active'):
        if date and not re.match(r'\d{4}-\d{2}-\d{2}', date):
            raise ValueError("Date must have format YYYY-MM-DD")
        if not (state == 'active' or state == 'delisted'):
            raise ValueError('"state" must be either "active" or "delisted"')
        return "LISTING_STATUS"
