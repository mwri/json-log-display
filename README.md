# JSON log display (json-log-display)

A CLI tool for presenting JSON logging data nicely on the CLI. If there is additional non JSON
data it will attempt to ignore that and use the valid JSON that is there.

It also colours the output, can pre filter, post filter, pass through or ignore non JSON data
and supports an output format string.

## Installation

JSON log display requires Python 3.6 or higher.

Install the pip package as follows:

```
$ pip install json-log-display
```

## Use

Once installed a `jld` CLI util should be available, and all you have to do is pipe logging
which has embedded JSON to it. For example:

```
$ tail -f /some/log/file | jld
2022-10-29T16:56:11.646734D INFO some info
2022-10-29T16:56:11.693193D DEBUG some debug
2022-10-29T16:56:11.646734D INFO more info
2022-10-29T16:56:11.646734D INFO warning alert bad
2022-10-29T16:56:11.646734D ERROR really gone wrong now
```

The lines will be coloured according to the level.

To change the colour of a level you can either specify a CLI argument, for
example `--col info=green`, or set an environment variable, like `JLD_LEVEL_INFO_COL=green`.

To change the output format use `--out_format`, the default format string is
`${timestamp} ${level} ${message}"`. Each `${xxxx}` is a deference to a key in
the JSON objects logged.

To change the field which is used to determine the log colour use `--level_field`. For
example `--level_field loglevel`.

To hide non JSON data use `--no_passthrough`.

To pre filter the input (only include lines matching a given regular expression) use
`--pre_filter REGEX` and provide a regular expression.

To filter the output based on the JSON data use `--data_filter KEY=REGEX`.

By default JSON log display will attempt to skip junk to find valid JSON log data later
in the line. To disable this if this causes problems and your logging does not have a prefix
use `--no_json_search`.

## Development

A nox config is provided and Makefile. Install nox if necessary and run `nox` or
run `make`, which will use your default Python version and create a virtual
environment.

You can install development requirements in your current environment as follows:

```
$ pip install '.[dev]'
```
