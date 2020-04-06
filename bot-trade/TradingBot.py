from .TradingModel import TradingModel
from .backtesting.StrategyEvaluator import StrategyEvaluator
from .exchanges.Binance import Binance
from .stratergies.Strategies import Strategies
from loguru import logger


# Now, We will put everything together. Continuing with our command line interface, we will allow ourselves
# to backtest strategies, evaluate them (see what coins have those strategies fulfilled right now), and if
# any coins are eligible, we will plot & backtest that strategy on that particular coin, and if we are 
# happy with the results, we can place an order. 

def back_test_strategies(symbols=None, interval='1h', plot=False, strategy_evaluators=None,
                         options=None):
    if symbols is None:
        symbols = []

    if strategy_evaluators is None:
        strategy_evaluators = []

    if options is None:
        options = dict(starting_balance=100, initial_profits=1.01, initial_stop_loss=0.9,
                       incremental_profits=1.005, incremental_stop_loss=0.995)

    coins_tested = 0
    trade_value = options['starting_balance']

    for symbol in symbols:
        logger.debug('Back testing begin for {}'.format(symbol))
        model = TradingModel(symbol=symbol, time_frame=interval)
        for evaluator in strategy_evaluators:
            resulting_balance = evaluator.back_test(
                model,
                starting_balance=options['starting_balance'],
                initial_profits=options['initial_profits'],
                initial_stop_loss=options['initial_stop_loss'],
                incremental_profits=options['incremental_profits'],
                incremental_stop_loss=options['incremental_stop_loss'],
            )

            if resulting_balance != trade_value:
                logger.debug(evaluator.strategy.__name__
                             + ": starting balance: " + str(trade_value)
                             + ": resulting balance: " + str(round(resulting_balance, 2)))
                if plot:
                    model.plot_data(
                        buy_signals=evaluator.results[model.symbol]['buy_times'],
                        sell_signals=evaluator.results[model.symbol]['sell_times'],
                        plot_title=evaluator.strategy.__name__ + " on " + model.symbol)

                evaluator.profits_list.append(resulting_balance - trade_value)
                evaluator.update_result(trade_value, resulting_balance)

            coins_tested = coins_tested + 1

    for evaluator in strategy_evaluators:
        print("")
        evaluator.print_results()


# Now, We will write the function that checks the current market conditions 
# & allows us to place orders if the conditions are good

strategy_matched_symbol = "\nStragey Matched Symbol! \
    \nType 'b' then ENTER to backtest the strategy on this symbol & see the plot \
    \nType 'p' then ENTER if you want to Place an Order \
    \nTyping anything else or pressing ENTER directly will skip placing an order this time.\n"

ask_place_order = "\nType 'p' then ENTER if you want to Place an Order \
    \nTyping anything else or pressing ENTER directly will skip placing an order this time.\n"


def evaluate_strategies(symbols=None, strategy_evaluators=None, interval='1h',
                        options=None):
    if symbols is None:
        symbols = []

    if strategy_evaluators is None:
        strategy_evaluators = []

    if options is None:
        options = dict(starting_balance=100, initial_profits=1.01, initial_stop_loss=0.9,
                       incremental_profits=1.005, incremental_stop_loss=0.995)

    for symbol in symbols:
        logger.debug(symbol)
        model = TradingModel(symbol=symbol, time_frame=interval)
        for evaluator in strategy_evaluators:
            if evaluator.evaluate(model):
                logger.info("\n" + evaluator.strategy.__name__ + " matched on " + symbol)
                logger.info(strategy_matched_symbol)
                answer = input()

                if answer == 'b':
                    resulting_balance = evaluator.back_test(
                        model,
                        starting_balance=options['starting_balance'],
                        initial_profits=options['initial_profits'],
                        initial_stop_loss=options['initial_stop_loss'],
                        incremental_profits=options['incremental_profits'],
                        incremental_stop_loss=options['incremental_stop_loss'],
                    )
                    model.plot_data(
                        buy_signals=evaluator.results[model.symbol]['buy_times'],
                        sell_signals=evaluator.results[model.symbol]['sell_times'],
                        plot_title=evaluator.strategy.__name__ + " matched on " + symbol
                    )
                    logger.info(evaluator.results[model.symbol])
                    logger.info(ask_place_order)
                    answer = input()
                if answer == 'p':
                    logger.info("\nPlacing Buy Order. ")

                    # We need to update the PlaceOrder function - we don't know what symbol we will be buying
                    # beforehand, but let's say that we have received a symbol on coin ABCETH, where 1 ABC = 0.0034
                    # ETH. Binance only allows us to make orders ABOVE 0.01 ETH, so we need to buy at least 3 ABC.
                    # However, if we received a symbol on XYZETH, and say 1 XYZ = 3 ETH, maybe we only want to buy
                    # 0.05 XYZ. Therfore, we need to specify the amount we need to buy in terms of QUOTE ASSET (ETH),
                    # not base asset. # We are changing the PlaceOrder function to reflect that.

                    order_result = model.exchange.place_order(model.symbol, "BUY", "MARKET", quantity=0.02, test=False)
                    if "code" in order_result:
                        logger.debug("\nERROR.")
                        logger.debug(order_result)
                    else:
                        logger.debug("\nSUCCESS.")
                        logger.debug(order_result)


# Now, we're almost ready to start the bot.

opening_text = "\nWelcome to Crypto Trading Bot. \n \
    Press 'b' (ENTER) to backtest all strategies \n \
    Press 'e' (ENTER) to execute the strategies on all coins \n \
    Press 'q' (ENTER) to quit. "


def main():
    exchange = Binance()
    symbols = exchange.get_trading_symbols(quote_assets=["ETH"])

    strategy_evaluators = [
        StrategyEvaluator(strategy_function=Strategies.boll_strategy),
        StrategyEvaluator(strategy_function=Strategies.ma_strategy),
        StrategyEvaluator(strategy_function=Strategies.ichimoku_bullish)
    ]

    print(opening_text)

    answer = input()
    while answer not in ['b', 'e', 'q']:
        print(opening_text)
        answer = input()

    if answer == 'e':
        evaluate_strategies(symbols=symbols, interval='5m', strategy_evaluators=strategy_evaluators)
    if answer == 'b':
        back_test_strategies(symbols=symbols, interval='5m', plot=True, strategy_evaluators=strategy_evaluators)
    if answer == 'q':
        print("\nBYE!\n")
