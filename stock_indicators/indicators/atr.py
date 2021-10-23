from typing import Iterable, List, Optional, Type
from stock_indicators._cslib import CsIndicator
from stock_indicators._cstypes import List as CsList
from stock_indicators._cstypes import Decimal as CsDecimal
from stock_indicators._cstypes import to_pydecimal
from stock_indicators.indicators.common.results import IndicatorResults, ResultBase
from stock_indicators.indicators.common.quote import Quote

def get_atr(quotes: Iterable[Quote], lookback_periods: int = 14):
    atr_results = CsIndicator.GetAtr[Quote](CsList(Quote, quotes), lookback_periods)
    return ATRResults(atr_results, ATRResult)

class ATRResult(ResultBase):
    def __init__(self, atr_result):
        super().__init__(atr_result)

    @property
    def tr(self):
        return to_pydecimal(self._csdata.Tr)
    
    @tr.setter
    def tr(self, value):
        self._csdata.Tr = CsDecimal(value)

    @property
    def atr(self):
        return to_pydecimal(self._csdata.Atr)
    
    @atr.setter
    def atr(self, value):
        self._csdata.Atr = CsDecimal(value)

    @property
    def atrp(self):
        return to_pydecimal(self._csdata.Atrp)

    @atrp.setter
    def atrp(self, value):
        self._csdata.Atrp = CsDecimal(value)
    
class ATRResults(IndicatorResults[ATRResult]):
    """
    A wrapper class for the list of ATR(Average True Range) results. 
    It is exactly same with built-in `list` except for that it provides
    some useful helper methods written in C# implementation.
    """

    def __init__(self, data, wrapper_class: Type[ATRResult]):
        super().__init__(data, wrapper_class)

    @IndicatorResults._verify_data
    def remove_warmup_periods(self, remove_periods: Optional[int] = None):
        if remove_periods is not None:
            return super().remove_warmup_periods(remove_periods)
        
        removed_results = CsIndicator.RemoveWarmupPeriods(CsList(type(self._csdata[0]), self._csdata))

        return self.__class__(removed_results, self._wrapper_class)
        