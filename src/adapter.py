class DataAdapter:
    def __init__(self) -> None:
        # Sample data from the Global Beverage Corporation Exchange
        self._stocks = {
            "TEA": {
                "Type": "Common",
                "Last Dividend": 0,
                "Fixed Dividend": 0,
                "Par Value": 100,
            },
            "POP": {
                "Type": "Common",
                "Last Dividend": 8,
                "Fixed Dividend": 0,
                "Par Value": 100,
            },
            "ALE": {
                "Type": "Common",
                "Last Dividend": 23,
                "Fixed Dividend": 0,
                "Par Value": 60,
            },
            "GIN": {
                "Type": "Preferred",
                "Last Dividend": 8,
                "Fixed Dividend": "2%",
                "Par Value": 100,
            },
            "JOE": {
                "Type": "Common",
                "Last Dividend": 13,
                "Fixed Dividend": 0,
                "Par Value": 250,
            },
        }

    def get_stocks(self) -> dict:
        return self._stocks
