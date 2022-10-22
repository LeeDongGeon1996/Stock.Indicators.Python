from typing import Iterable, Optional, TypeVar

from stock_indicators._cslib import CsIndicator
from stock_indicators.indicators.common.chain import chainable
from stock_indicators.indicators.common.helpers import RemoveWarmupMixin
from stock_indicators.indicators.common.results import IndicatorResults, ResultBase
from stock_indicators.indicators.common.quote import Quote


def _wrap_results(results):
    return RSIResults(results, RSIResult)

def _calculate(indicator_params, is_chaining):
    if is_chaining:
        return CsIndicator.GetRsi(*indicator_params)
    else:
        return CsIndicator.GetRsi[Quote](*indicator_params)

@chainable(is_chainable=True, calc_func=_calculate, wrap_func=_wrap_results)
def get_rsi(quotes: Iterable[Quote], lookback_periods: int = 14) -> "RSIResults[RSIResult]":
    """Get RSI calculated.

    Relative Strength Index (RSI) measures strength of the winning/losing streak over N lookback periods
    on a scale of 0 to 100, to depict overbought and oversold conditions.

    Parameters:
        `quotes` : Iterable[Quote]
            Historical price quotes.

        `lookback_periods` : int, defaults 14
            Number of periods in the lookback window.

    Returns:
        `RSIResults[RSIResult]`
            RSIResults is list of RSIResult with providing useful helper methods.

    See more:
         - [RSI Reference](https://daveskender.github.io/Stock.Indicators.Python/indicators/Rsi/#content)
         - [Helper Methods](https://daveskender.github.io/Stock.Indicators.Python/utilities/#content)
    """
    return (quotes, lookback_periods)


class RSIResult(ResultBase):
    """
    A wrapper class for a single unit of RSI results.
    """

    @property
    def rsi(self) -> Optional[float]:
        return self._csdata.Rsi

    @rsi.setter
    def rsi(self, value):
        self._csdata.Rsi = value


_T = TypeVar("_T", bound=RSIResult)
class RSIResults(RemoveWarmupMixin, IndicatorResults[_T]):
    """
    A wrapper class for the list of RSI(Relative Strength Index) results.
    It is exactly same with built-in `list` except for that it provides
    some useful helper methods written in CSharp implementation.
    """
