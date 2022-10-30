.. include:: <s5defs.txt>

JSON log display
================

A CLI tool for presenting JSON logging data nicely on the CLI. If there is additional non JSON
data it will attempt to ignore that and use the valid JSON that is there.

Installation
------------

JSON log display requires Python 3.6 or higher.

Install the pip package as follows:

::

   $ pip install json-log-display

Use
---

Once installed a `jld` CLI util should be available, and all you have to do is pipe logging
which has embedded JSON to it. For example:

| $ tail -f /some/log/file | jld
| :cyan:`2022-10-29T16:56:11.646734D INFO some info`
| :magenta:`2022-10-29T16:56:11.693193D DEBUG some debug`
| :cyan:`2022-10-29T16:56:11.646734D INFO more info`
| :yellow:`2022-10-29T16:56:11.646734D INFO warning alert bad`
| :red:`2022-10-29T16:56:11.646734D ERROR really gone wrong now`

To change the colour of a level you can either specify a CLI argument, for
example :code:`--col info=green`, or set an environment variable, like
:code:`JLD_LEVEL_INFO_COL=green`.

To change the output format use :code:`--out_format`, the default format string is
:code:`${timestamp} ${level} ${message}"`. Each :code:`${xxxx}` is a deference to a key in
the JSON objects logged.

To change the field which is used to determine the log colour use :code:`--level_field`.
For example :code:`--level_field loglevel`.

To hide non JSON data use :code:`--no_passthrough`.

To pre filter the input (only include lines matching a given regular expression) use
:code:`--pre_filter REGEX` and provide a regular expression.

To filter the output based on the JSON data use :code:`--data_filter KEY=REGEX`.

By default JSON log display will attempt to skip junk to find valid JSON log data later
in the line. To disable this if this causes problems and your logging does not have a prefix
use :code:`--no_json_search`.

Development
-----------

A nox config is provided and Makefile. Install nox if necessary and run :code:`nox` or
run :code:`make`, which will use your default Python version and create a virtual
environment.

You can install development requirements in your current environment as follows:

::

   $ pip install '.[dev]'
