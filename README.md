[![CircleCI](https://circleci.com/gh/indyfree/tailor.svg?style=svg&circle-token=9ef56e6ccc4ae36b491f9cd438f6921d5b258727)](https://circleci.com/gh/indyfree/tailor)
# tailor - Tailored Data Solution
This repository keeps the progress and solution of Group 1 for the *Advanced Data Science in Practice* Seminar.
The seminar is hold by Prof. Grahl of [University of Cologne](http://www.digital.uni-koeln.de/de/team/prof-dr-joern-grahl/) in cooperation with [tailorit](https://www.tailorit.de).

## Requirements
- python 3.6
- GNU make

## Installation
This project is intended to run on Mac or Linux. On Windows it should also be runnable via the [Linux Subsystem](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

### Clone the repository
```bash
> git clone https://github.com/indyfree/tailor
```

### Install required packages
Installs dependencies with `pip`:
```bash
> make requirements
```

### Provide server information
Create a file `.env` in the project root:
```bash
> cd tailorit
> touch .env
```
Edit the file with an editor of your choice to provide credentials to the tailorit server. The file should look like this:
```bash
export TAILORIT_SERVER_ADDRESS=[address]
export TAILORIT_USER=[user]
export TAILORIT_PW=[password]
```
Where `[address]`, `[user]` and `[password]` have to be substituted with the respective values.

### Get the data
Download the provided data to `data/raw`.
```bash
> make data
```
## Run the project
This project is set up twofold:
1. Custom functions and algorithms live in the *tailor* python package in `src/tailor`.
2. A walkthrough through the data science process and visualizations are made with jupyter notebooks in `notebooks`. Required functions from *tailor* are imported.

Run the jupyter notebooks with:
```bash
> make jupyter
```

You can access the jupyter notebooks via your webbrowser at `http://localhost:8888/`.
