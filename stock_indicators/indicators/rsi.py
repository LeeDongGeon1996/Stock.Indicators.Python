from typing import Iterable, Optional, Type
from stock_indicators._cslib import CsIndicator
from stock_indicators._cstypes import List as CsList
from stock_indicators._cstypes import Decimal as CsDecimal
from stock_indicators._cstypes import to_pydecimal
from stock_indicators.indicators.common.results import IndicatorResults, ResultBase
from stock_indicators.indicators.common.quote import Quote

def get_rsi(quotes: Iterable[Quote], lookback_periods: int = 14):
    rsi_list = CsIndicator.GetRsi[Quote](CsList(Quote, quotes), lookback_periods)
    return RSIResults(rsi_list, RSIResult)

class RSIResult(ResultBase):
    """
    A wrapper class for a single unit of RSI results.
    """

    def __init__(self, rsi_result):
        super().__init__(rsi_result)

    @property
    def rsi(self):
        return to_pydecimal(self._csdata.Rsi)

    @rsi.setter
    def rsi(self, value):
        self._csdata.Rsi = CsDecimal(value)


class RSIResults(IndicatorResults[RSIResult]):
    """
    A wrapper class for the list of RSI(Relative Strength Index) results.
    It is exactly same with built-in `list` except for that it provides
    some useful helper methods written in CSharp implementation.
    """

    def __init__(self, data: Iterable, wrapper_class: Type[RSIResult]):
        super().__init__(data, wrapper_class)

    @IndicatorResults._verify_data
    def remove_warmup_periods(self, remove_periods: Optional[int] = None):
        if remove_periods is not None:
            return super().remove_warmup_periods(remove_periods)
        
        removed_results = CsIndicator.RemoveWarmupPeriods(CsList(type(self._csdata[0]), self._csdata))

        return self.__class__(removed_results, self._wrapper_class)

    @IndicatorResults._verify_data
    def to_quotes(self) -> Iterable[Quote]:
        quotes = CsIndicator.ConvertToQuotes(CsList(type(self._csdata[0]), self._csdata))

        return quotes