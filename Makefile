.PHONY: clean data lint requirements venv

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
VENV_DIR =  $(PROJECT_DIR)/env
NOTEBOOK_DIR =  $(PROJECT_DIR)/notebooks
DATA_RAW_DIR = $(PROJECT_DIR)/data/raw
PYTHON_INTERPRETER = $(VENV_DIR)/bin/python3
PIP = $(VENV_DIR)/bin/pip

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python Dependencies
requirements: venv
	$(PIP) install -U pip setuptools wheel
	$(PIP) install -r requirements.txt

## Make Dataset
data:
ifeq ($(wildcard $(DATA_RAW_DIR)/.),)
	@echo "Creating directory $(DATA_RAW_DIR)"
	@mkdir -p $(DATA_RAW_DIR)
endif
	$(PYTHON_INTERPRETER) src/data/make_dataset.py $(DATA_RAW_DIR)

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8
lint:
	$(PYTHON_INTERPRETER) -m flake8 src

jupyter:
	@echo "Running jupyter notebook in background..."
	@$(PYTHON_INTERPRETER) -m jupyter notebook --notebook-dir=$(NOTEBOOK_DIR) &> /dev/null &

## Install virtual environment
venv:
ifneq ($(wildcard $(VENV_DIR)/*),)
	@echo "Found $(VENV_DIR)"
else
	@echo "Did not find $(VENV_DIR), creating..."
	mkdir -p $(VENV_DIR)
	python3 -m venv $(VENV_DIR)
endif

