"""CLI entry points."""


import argparse
import json
import os
import re
import sys

import colors


def jld():
    def parse_args():
        parser = argparse.ArgumentParser(
            description=(
                "Look for JSON logging in STDIN and display a human readable alternative.\n"
                "\n"
                "Colours may also be specified by environment variables, for example setting\n"
                "JLD_LEVEL_DEBUG_COL=red will have the same effect as --col debug=red.\n"
                "\n"
                "The default colour may be set wirth eithrer --col default=xxxx or by setting\n"
                "the JLD_LEVEL_DEFAULT_COL environment variable.\n"
                "\n"
                "Use --out_format to specify an alternative output format, the default is\n"
                '"${timestamp} ${level} ${message}". Or set the JLD_OUT_FORMAT environment\n'
                "variable.\n"
                "\n"
                "Use --pre_filter to specify a regex which will be used to filter the raw input.\n"
                "Use --data_filter to specify a key and regex which will be used to filter the\n"
                "JSON data before display. The filter will pass if any part of the line matches\n"
                "the regex, but you can specify ^ and $ to require an exact match, as usual."
            )
        )

        parser.add_argument(
            "--col",
            help="set/change the colour used for a level",
            action="append",
            default=[],
        )
        parser.add_argument(
            "--level_field",
            help="set/change the key/field which has the log level (default is 'level')",
            action="append",
            default="level",
        )
        parser.add_argument(
            "--out_format",
            help="set/change the output format (default is '${timestamp} ${level} ${message}')",
            default=os.environ.get("JLD_OUT_FORMAT") or "${timestamp} ${level} ${message}",
        )
        parser.add_argument(
            "--no_passthrough",
            help="pass through non JSON",
            action="store_true",
            default=False,
        )
        parser.add_argument(
            "--no_json_search",
            help="do not search through the input lines looking for valid JSON",
            action="store_true",
            default=False,
        )
        parser.add_argument(
            "--pre_filter",
            help="if given, only include lines matching this regular expression (like an inbuilt grep)",
            default=None,
        )
        parser.add_argument(
            "--data_filter",
            help="if given, only include JSON data matches (for example --data_filter level='(INFO|ERROR)')",
            default=None,
        )

        return parser.parse_args()

    def output(line):
        print(line)

    def format_output(data, format):
        return re.sub(r"\${([^}]+)}", lambda m: data.get(m.group(1), f"NONE({m.group(1)})"), format)

    def handle_json(args, level_cols, data):
        level = data.get(args.level_field, "default")
        col_f = level_cols.get(level.lower(), level_cols["default"])
        output(col_f(format_output(data, args.out_format)))

    def handle_non_json(args, line):
        if not args.no_passthrough:
            output(colors.blue(line.rstrip()))

    def parse_data_filter(data_filter_arg):
        (k, v) = data_filter_arg.split("=", 1)
        return (k, re.compile(v))

    def find_json(line):
        start_pos = line.find("{")
        end_pos = line.rfind("}")

        if start_pos == -1 or end_pos == -1:
            return None

        while end_pos != -1:
            try:
                return json.loads(line[start_pos : end_pos + 1])
            except json.decoder.JSONDecodeError:
                pass

            end_pos = line.rfind("}", start_pos, end_pos)

        return find_json(line[start_pos + 1 :])

    level_cols = {
        "level_cols": {
            k[10:-4].lower(): getattr(colors, v)
            for k, v in os.environ.items()
            if k.startswith("JLD_LEVEL_") and k.endswith("_COL")
        },
    }

    level_cols.setdefault(None, colors.white)
    level_cols.setdefault("info", colors.cyan)
    level_cols.setdefault("warning", colors.yellow)
    level_cols.setdefault("error", colors.red)
    level_cols.setdefault("debug", colors.magenta)
    level_cols.setdefault("default", colors.white)

    args = parse_args()

    for col_arg in args.col:
        (level, col) = col_arg.split("=")
        level_cols[level] = getattr(colors, col)

    pre_filter = None if args.pre_filter is None else re.compile(args.pre_filter)
    (filter_key, filter_cre) = (None, None) if args.data_filter is None else parse_data_filter(args.data_filter)

    for line in sys.stdin:
        if pre_filter is not None and not pre_filter.search(line):
            continue

        data = None
        if args.no_json_search:
            try:
                data = json.loads(line)
            except json.decoder.JSONDecodeError:
                pass
        else:
            data = find_json(line)

        if data is None:
            handle_non_json(args, line)
        else:
            if filter_key is None or (filter_key in data and filter_cre.match(data[filter_key])):
                handle_json(args, level_cols, data)
