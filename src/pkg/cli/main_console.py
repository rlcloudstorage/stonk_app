"""src/pkg/cli/main_console.py"""

import argparse, logging, os

from pkg import DEBUG


logger = logging.getLogger(__name__)


def start_cli(ctx: dict):
    """"""
    if DEBUG:
        logger.debug(f"start_cli(ctx={ctx}, {type(ctx)})\n")

    # Create the ArgumentParser object
    parser = argparse.ArgumentParser(description="A simple script using argparse.")

    # Add arguments
    parser.add_argument("name", help="The name of the user.")
    parser.add_argument("--greet", action="store_true", help="Include a greeting.")

    # Parse the arguments
    args = parser.parse_args()

    # Access the arguments
    if args.greet:
        print(f"Hello, {args.name}!")
    else:
        print(f"{args.name}, no greeting for you.")

    if args.name == "bob":
        print(f"args._get_args: {args._get_args}")

# =======

    # cli = argparse.ArgumentParser()
    # subparsers = cli.add_subparsers(dest="subcommand")

    # def argument(*name_or_flags, **kwargs):
    #     return (list(name_or_flags), kwargs)

    # def subcommand(args=[], parent=subparsers):
    #     def decorator(func):
    #         parser = parent.add_parser(func.__name__, description=func.__doc__)
    #         for arg in args:
    #             parser.add_argument(*arg[0], **arg[1])
    #         parser.set_defaults(func=func)
    #     return decorator

    # @subcommand()
    # def nothing(args):
    #     print("Nothing special!")

    # @subcommand([argument("backtest", help="backtest trading strategies")])
    # def backtest(args):
    #     from pkg.cli import cmd_backtest
    #     cmd_backtest.cli(ctx=ctx, args=args)

    # @subcommand([argument("-d", help="Debug mode", action="store_true")])
    # def test(args):
    #     print(args)

    # @subcommand([argument("-f", "--filename", help="A thing with a filename")])
    # def filename(args):
    #     print(args.filename)

    # @subcommand([argument("name", help="Name")])
    # def name(args):
    #     print(args.name)

    # args = cli.parse_args()
    # if args.subcommand is None:
    #     cli.print_help()
    # else:
    #     args.func(args)

# =======

    # def parse_args(*args):
    #     """"""
    #     parser = argparse.ArgumentParser(
    #         prog="stonk_app",
    #         # usage="%(prog)s <command> [options]",
    #         description=" * Download stock charts, S&P heatmaps, OHLC price data\n * Backtest trading strategies",
    #         epilog=" '%(prog)s' copyright \N{COPYRIGHT SIGN} 2025, rueben lake. All rights reserved.",
    #         formatter_class=argparse.RawDescriptionHelpFormatter,
    #     )
    #     subparsers = parser.add_subparsers(title="commands", prog="stonk_app", metavar="")

    # #     # add_load_subparser(subparsers)
    # #     # add_write_subparser(subparsers)
    #     # add_save_subparser(subparsers)
    #     backtest_parser(subparsers=subparsers)
    #     data_parser(subparsers=subparsers)

    #     return parser.parse_args(*args)

    # def backtest_parser(subparsers):
    #     """"""
    #     # parser = subparsers.add_parser("backtest", help="backtest trading strategies")
    #     # parser.add_argument("-d", "--database", default="", help="set database used for backtesting", metavar="")
    #     # parser.add_argument("-s", "--strategy", help="strategy to use for backtesting", metavar="")
    #     # args = parser.parse_args(*args)
    #     # args = parser.parse_args()

    #     # from pkg.cli import cmd_backtest
    #     # cmd_backtest.cli(ctx=ctx, args=args)

    #     parser = subparsers.add_parser("backtest", help="backtest trading strategies")
    #     parser.add_argument("-d", "--database", default="", help="set database used for backtesting", metavar="")
    #     parser.add_argument("-s", "--strategy", help="strategy to use for backtesting", metavar="")

    # def data_parser(subparsers):
    #     """"""
    #     parser = subparsers.add_parser("data", help="fetch online OHLC price data")
    #     parser.add_argument("-d", "--database", default="", help="set database for OHLC data", metavar="")
    #     parser.add_argument("-p", "--provider", default="", help="select an online data provider", metavar="")
    #     parser.add_argument("-t", "--ticker", default="", help="list of ticker symbols to fetch", metavar="")

    # # def add_load_subparser(subparsers):
    # #     parser = subparsers.add_parser('load', help='Load something somewhere')
    # #     parser.add_argument('--config',
    # #                         help='Path to configuration file for special settings')
    # #     parser.add_argument('--dir', default=os.getcwd(),
    # #                         help='The directory to load')
    # #     parser.add_argument('book', help='The book to load into this big thing')
    # #     parser.add_argument('chapter', nargs='?', default='',
    # #                         help='Optionally specify a chapter')
    # #     parser.add_argument('verse', nargs='*',
    # #                         help='Optionally pick as many verses as you want to'
    # #                         ' load')
    # #     parser.set_defaults(command='load')

    # # def add_write_subparser(subparsers):
    # #     parser = subparsers.add_parser(
    # #         'write', help='Execute commands defined in a config file')
    # #     parser.add_argument('config', help='The path to the config file')
    # #     parser.set_defaults(command='write')

    # def add_save_subparser(subparsers):
    #     parser = subparsers.add_parser(
    #             'save',
    #             help='Save this big thing for use somewhere later')
    #     parser.add_argument('-n', '--name', default=None,
    #                         help='The name of the component to save')
    #     parser.add_argument('path', help="The way out of Plato's cave")
    #     parser.set_defaults(command='save')

    # args = parse_args()
    # print(f"args: {args}")

# =======

    # parser = argparse.ArgumentParser(
    #     prog="stonk_app",
    #     # usage="%(prog)s <command> [options]",
    #     description=" * Download stock charts, S&P heatmaps, OHLC price data\n * Backtest trading strategies",
    #     epilog="%(prog)s copyright \N{COPYRIGHT SIGN} 2025, rueben lake.  All rights reserved.",
    #     formatter_class=argparse.RawDescriptionHelpFormatter,
    # )

    # subparser = parser.add_subparsers(
    #     title="commands",
    #     prog="stonk_app",
    #     metavar=""
    # )

    # backtest_parser = subparser.add_parser(name="backtest", help="backtest stockmarket trading strategies")
    # # backtest_parser.set_defaults(func='')
    # print(f"*** backtest_parser.parse_args(): {backtest_parser.parse_args()}")

    # database_parser = subparser.add_parser(name="database", help="set database used for backtesting")
    # # data_parser.set_defaults(func='')

    # parser.add_argument(
    #     "--version", action="version", version="%(prog)s 0.1.0",
    #     help="display current version and exit"
    # )

    # print(f"parser.__dict__: {parser.__dict__}\n")
    # print(f"backtest_parser: {backtest_parser}\n")
    # print(f"database_parser: {database_parser}\n")

    # args = parser.parse_args()
    # print(f"args: {args}")
