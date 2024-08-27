# HOME ASSIGNMENT - BitBucket Automation


**[Environment Configuration](#environment-configuration)**

   * **[Virtual environment and dependency manager](#virtual-environment-and-dependency-manager)**</br>
   * **[Pre-Commits code formating](#pre-commits-code-formating)**
   * **[Installation](#installation)**
   * **[Configuration](#configuration)**
   * **[Execution](#execution)**
   * **[Parameters](#parameters)**
   * **[Analyzing failure with the playwright trace file](#analyzing-failure-with-the-playwright-trace-file)**

**[Project Structure](#project-structure)**
   - **[artefacts](#artefacts-directory)**
   - **[src](#src)**
     - **[fixtures](#fixtures)**
     - **[helpers](#helpers)**
     - **[pages](#pages)**
     - **[tests](#tests)**
   - **[.flake8](#flake8)**
   - **[.pre-commit-config.yaml](#pre-commit-configyaml)**
   - **[conftest.py](#conftestpy)**
   - **[poetry.lock](#poetrylock)**
   - **[pyproject.toml](#pyprojecttoml)**
   - **[pytest.ini](#pytestini)**
   - **[README.md](#readmemd)**

**[Contact](#contact)**


# Environment Configuration

## Virtual environment and dependency manager
Poetry is a tool for Python packaging and dependency management. It allows you to declare libraries needed for your
project and manage them.

### Poetry installation

> **WARNING:** Before installing poetry in the project, create `.venv` folder first. This way poetry environment will be
installed locally in the project folder.

To install poetry run 

`python3 -m pip install poetry`

### Poetry virual environment usage

To just execute a command using the virtual environment (for example by a CI) run:

`poetry run command_to_be_executted`

Above command will execute command in the virtual environment.
If we want to enter the virtual environment, we need to execute:

`poetry shell`

To exit the poetry you can execute command: `poetry exit` but it won't deactivate the environmnet. to deactivate it, you need to execute `deactivate` command while in the virtual environment.

## Pre-Commits code formating
To keep the code clean we'll use a few tools that will make sure everything in the code is looking the proper (pythonic) way. Those tools are:
 - flake8 - which includes: Pyflakes, McCabe and pycodestyle
 - isort - which sorts all the imports the right way
 - black - code formatter.

## Installation

1. Install poetry:

   `python3 -m pip install --upgrade pip`

   `python3 -m pip install poetry`

   `pre-commit install`

2. Run poetry to install dependecies and setup virtual environment:
    To execute tests from outside of the environment (for example on CI):
    
    `poetry run python3 -m pytest <params>`
    
    To enter virtual environment execute:
    
    `poetry shell`

## Configuration

1. Install playwright nodes
   Below command will download multiple playwright browser nodes, they are required to execute tests.
   
   `poetry run playwright install`

2. Set Logging
   Logging can be set in the `./conftest.py` :
   
   LOGGERS = "TEST,PAGE,FIXTURE,API,GENERATOR" - enabling loggers
   LOG_LEVEL = "debug" - setting level

3. Set Testing suite
   Suite configuration can be set in `pytest.ini` file in the `-m` parameter.
   Just logicaly connect marks that needs to be used:
      -m="UI or API" - will execute all tests that have `UI` or `API` mark

4. Account Settings:
   To setup account for tests use `.env` file:

   ```
   USERNAME=
   PASSWORD=

   API_URL=https://api.bitbucket.org/2.0/repositories/<WORKSPACE>
   APP_URL=https://bitbucket.org/<WORKSPACE>

   API_USER=
   API_PASS=
   ```

## Execution

   To execute tests run:
      - `pytest` - for series execution
      - `pytest -n auto` - for parallel execution

## Parameters
All available parameters are noted in below table:

| Parameter     | Required | Description                                                                    |
|---------------|----------|--------------------------------------------------------------------------------|
| -m            | Yes      | Specify markers to select suite of tests. Check pytest.ini for available marks |
| --screenshots | No       | Path for the screenshots. Default: artefacts/screenshots                       |
| --html        | No       | Path for the reports: default: artefacts/reports                               |
| --headed      | No       | headless or headed mode                                                        |
| --junitxml    | No       | JUnit XML report                                                               |
| --traceing    | No       | Playwright traceing options                                                    |

## Analyzing failure with the playwright trace file
When the `--traceing` option is used, playwright will create a test-results folder with the `trace.zip` file for each
test in the `../tests/tests-results/` directory.

There are to options to open the _trace_ file:
1. Open the trace.playwright.dev site and load the file there.
2. Execute `playwright show-trace <path to trace file>`

This will open the UI mode where you can inspect each step and verify why test has failed.

# Project Structure

### Artefacts directory
This folder includes all the artefacts mainly screenshots and reports

### SRC
All the main functionality: helpers, fixtures, PO and tests

### fixtures
Overall fixtures not related to a specific functionality.

### helpers
A helper methods not related directly to pages or endpoints

### pages
Pages are representations of the pages in the tested project. 
In most cases each page will be divided into 2 or more files:
1. **page file** - This is a browser tab representation. It will include the page url, name and basic methods like visit. It will include Page Objects too.
2. **page object file** - Elements on the page are grouped into page objects. Page object file will include:
   - Locators of the elements
   - Texts used in the tests for each page
   - Statics - emails, logins, any static data
   - simple methods that use the locators
   - advanced methods that will use simple methods.

This way we'll make sure those files won't be too big and everything will be organized.
Folder includes 2 base files:
- base_page.py - it includes basic actions that are valid for all pages
- base_po.py - it includes model classes for page object file.


### tests
This folder includes all the test modules. Each module name has to start with the *test_* word.
It's required by the pytest to automatically discover tests modules. The same goes for the 
Class and method names.

In the tests folder there is one additional file called `conftest.py`. It is automatically loaded
by pytest and here it's used to change pages and endpoints into fixtures.

### .flake8
Flake8 is a wrapper around these tools:

 - PyFlakes - A simple program which checks Python source files for errors. Pyflakes analyzes programs and detects
   various errors
 - pycodestyle - pycodestyle is a tool to check your Python code against some of the style conventions in PEP 8.
 - Ned Batchelder's McCabe script - Ned's script to check McCabe complexity.

### .pre-commit-config.yaml
It's a configuration file for pre-commit hooks. Whenever a git commit command is used, pre-commit hook is triggered
and executes: black, flake8 and isort. This way code will always be properly formatted on the remote repository.

### conftest.py
Pytest configuration file that is triggered on the framework start. It includes basic configuration
like add-options, make_report or pytest_configure.

### poetry.lock
> INFO: This file is autogenerated by poetry.

List of user external modules in the project with strict versions.

### pyproject.toml
Pytest project configuration file for external tools, which includes:
 - poetry config
 - poetry dependencies list
 - black configuration
 - isort configuration

### pytest.ini
Pytest configuration file that include:
 - list of pytest marks
 - default input parameters - if setup here then they don't need to be sent during project execution.

### README.md
This file.

## Contact
For more information contact:
 - [Przemysław Łukasik](mailto:plukasik.projectq@gmail.com)