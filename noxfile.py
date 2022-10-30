"""NOX config."""

import glob
import importlib

import nox

pkg_meta_spec = importlib.util.spec_from_file_location(
    "pkg_meta",
    "json_log_display/pkg_meta.py",
)
pkg_meta = importlib.util.module_from_spec(pkg_meta_spec)
pkg_meta_spec.loader.exec_module(pkg_meta)

default_pyvsn = "3"


@nox.session(python=[default_pyvsn])
def build(session):
    session.install(*pkg_meta.install_requires)
    session.install("setuptools", "wheel")
    session.run("python3", "setup.py", "sdist", "bdist_wheel")


@nox.session(python=[default_pyvsn])
def docs(session):
    session.install(*pkg_meta.install_requires)
    session.install("sphinx", "sphinx-rtd-theme")
    session.cd("docs")
    session.run("sphinx-build", "-M", "clean", "source", "build")
    session.run("sphinx-build", "-M", "html", "source", "build")


@nox.session(python=[default_pyvsn])
def lint(session):
    session.install("black", "isort")
    session.run("black", "--check", "--line-length", "120", "json_log_display")
    session.run("isort", "--check", "json_log_display")
