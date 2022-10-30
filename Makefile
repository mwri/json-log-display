all: docs lint

venv: venv/bin/activate venv/lib/.deps

venv/bin/activate:
	python3 -m venv venv

.PHONY: deps
deps: venv/lib/.deps

venv/lib/.deps: venv/bin/activate json_log_display/pkg_meta.py
	. venv/bin/activate \
		&& pip install $$(python3 json_log_display/pkg_meta.py install_requires)
	touch venv/lib/.deps

.PHONY: dev_deps
dev_deps: venv/lib/.dev_deps

venv/lib/.dev_deps: venv/bin/activate json_log_display/pkg_meta.py
	. venv/bin/activate \
		&& pip install $$(python3 json_log_display/pkg_meta.py extras_require dev)
	touch venv/lib/.dev_deps

.PHONY: docs
docs: venv venv/lib/.dev_deps
	. venv/bin/activate \
		&& make -C docs clean html

.PHONY: lint
lint: venv venv/lib/.dev_deps
	. venv/bin/activate \
		&& black --check --line-length 120 json_log_display \
		&& isort --check json_log_display

.PHONY: format
format: venv venv/lib/.dev_deps
	. venv/bin/activate \
		&& black --line-length 120 json_log_display \
		&& isort json_log_display

.PHONY: clean
clean:
	rm -rf ./venv ./*.egg-info ./build ./pip_dist ./.nox \
		$$(find json_log_display -name __pycache__) $$(find json_log_display -name '*.pyc')
	make -C docs clean

.PHONY: dist
dist: venv
	. venv/bin/activate \
		&& pip install setuptools wheel \
		&& python3 setup.py sdist bdist_wheel
