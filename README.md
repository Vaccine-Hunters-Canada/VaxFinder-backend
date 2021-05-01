<div align="center">
    <h1>VaxFinder - Backend</h1>
</div>

<div align="center">
    <strong>The backend for the Vaccine Hunters Finder tool.</strong>
</div>

<br/>

<div align="center">
    <a href="https://www.python.org/downloads/">
        <img src="https://img.shields.io/badge/python-3.8-blue.svg" alt="Python 3.8" />
    </a>
    <a href="https://github.com/psf/black">
        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black" />
    </a>
</div>

## Development

### Prerequisites

1. [Python ~3.8](https://www.python.org/downloads/)
2. [Poetry](https://python-poetry.org/): A tool for dependency management and packaging.
3. Access to VaxFinder's Microsoft SQL Server database hosted on [Azure](https://azure.microsoft.com/en-ca/services/sql-database/). Please message Patrick or Evan for access.

### Installation

1. Install the unixODBC library if you are on a linux environment as it's required for pyodbc (hence *aioodbc*). You can install it using your package manager, for example:

        $ sudo apt-get install unixodbc
        $ sudo apt-get install unixodbc-dev

2. Install Microsoft ODBC Driver 17 for SQL Server: [Windows](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15) | [Mac](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver15) | [Linux](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15)

3. Set up a VSCode MyPy Language Server (Optional)

    On macOS or Linux:

        $ python -m venv ~/.mypyls
        $ ~/.mypyls/bin/pip install "https://github.com/matangover/mypyls/archive/master.zip#egg=mypyls[default-mypy]"

    On Windows:

        $ python -m venv %USERPROFILE%\.mypyls
        $ %USERPROFILE%\.mypyls\Scripts\pip install "https://github.com/matangover/mypyls/archive/master.zip#egg=mypyls[default-mypy]"

    Install the mypy extension in VS Code (or reload the window if the extension is already installed).

4. Install all python dependencies with [Poetry](https://python-poetry.org/).

    ```
    $ poetry install
    ```

### Running the Server

1. Spawn a shell within a virtual environment.

    ```
    $ poetry shell
    ```

    All python dependencies should be installed within the virtual environment from the previous step.

2. Run the server on port `8007` from the root of the project within the shell.

    ```
    $ DB_URL={DATABASE_URL} python -m app.main
    ```

    - Swagger: [http://localhost:8007/swagger](http://localhost:8007/swagger)
    - ReDoc: [http://localhost:8007/redoc](http://localhost:8007/redoc)
    - OpenAPI Spec (JSON): [http://localhost:8007/openapi.json](http://localhost:8007/openapi.json)


## Production

TBA
