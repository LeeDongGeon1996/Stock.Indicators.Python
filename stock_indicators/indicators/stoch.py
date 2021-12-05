from typing import Iterable, Optional, Type, TypeVar
from stock_indicators._cslib import CsIndicator
from stock_indicators._cstypes import List as CsList
from stock_indicators._cstypes import Decimal as CsDecimal
from stock_indicators._cstypes import to_pydecimal
from stock_indicators.indicators.common.results import IndicatorResults, ResultBase
from stock_indicators.indicators.common.quote import Quote

def get_stoch(quotes: Iterable[Quote], lookback_periods: int = 14, signal_periods: int = 3, smooth_periods: int = 3):
    """Get Stochastic Oscillator calculated, with KDJ indexes.
    
    Stochastic Oscillatoris a momentum indicator that looks back N periods to produce a scale of 0 to 100.
    %J is also included for the KDJ Index extension.
      
    Parameters:
        `quotes` : Iterable[Quotes]
            Historical price quotes.
        
        `lookback_periods` : int, defaults 14
            Number of periods for the Oscillator.
            
        `signal_periods` : int, defaults 3
            Smoothing period for the %D signal line.
            
        `smooth_periods` : int, defaults 3
            Smoothing period for the %K Oscillator.
            Use 3 for Slow or 1 for Fast.
    
    Returns:
        `StochResults[StochResult]`
            StochResults is list of StochResult with providing useful helper methods.
    
    See more:
         - [Stochastic Oscillator Reference](https://daveskender.github.io/Stock.Indicators.Python/indicators/Stoch/#content)
         - [Helper Methods](https://daveskender.github.io/Stock.Indicators.Python/utilities/#content)
    """
    stoch_results = CsIndicator.GetStoch[Quote](CsList(Quote, quotes), lookback_periods, signal_periods, smooth_periods)
    return StochResults(stoch_results, StochResult)

class StochResult(ResultBase):
    """
    A wrapper class for a single unit of Stochastic Oscillator(with KDJ Index) results.
    """

    @property
    def oscillator(self):
        return to_pydecimal(self._csdata.Oscillator)

    @oscillator.setter
    def oscillator(self, value):
        self._csdata.Oscillator = CsDecimal(value)

    @property
    def signal(self):
        return to_pydecimal(self._csdata.Signal)

    @signal.setter
    def signal(self, value):
        self._csdata.Signal = CsDecimal(value)

    @property
    def percent_j(self):
        return to_pydecimal(self._csdata.PercentJ)

    @percent_j.setter
    def percent_j(self, value):
        self._csdata.PercentJ = CsDecimal(value)

    k = oscillator
    d = signal
    j = percent_j

T = TypeVar("T", bound=StochResult)
class StochResults(IndicatorResults[T]):
    """
    A wrapper class for the list of Stochastic Oscillator(with KDJ Index) results.
    It is exactly same with built-in `list` except for that it provides
    some useful helper methods written in C# implementation.
    """

    def __init__(self, data: Iterable, wrapper_class: Type[T]):
        super().__init__(data, wrapper_class)

    @IndicatorResults._verify_data
    def remove_warmup_periods(self, remove_periods: Optional[int] = None):
        if remove_periods is not None:
            return super().remove_warmup_periods(remove_periods)

        removed_results = CsIndicator.RemoveWarmupPeriods(CsList(type(self._csdata[0]), self._csdata))

        return self.__class__(removed_results, self._wrapper_class)
        