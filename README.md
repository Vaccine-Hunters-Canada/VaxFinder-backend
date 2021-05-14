<div align="center">
    <h1>:syringe: :mag: VaxFinder - Backend</h1>
</div>

<div align="center">
    <strong>The backend for the Vaccine Hunters Finder tool.</strong>
</div>

<br/>

<div align="center">
    <a href="https://www.python.org/downloads/release/python-380/">
        <img src="https://img.shields.io/badge/python-3.8-blue.svg" alt="Python 3.8" />
    </a>
    <a href="https://github.com/psf/black">
        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black" />
    </a>
    <a href="https://discord.com/channels/822486436837326908/832366009091358731">
        <img src="https://img.shields.io/badge/-%23vax--ui--backend-7389D8?logo=discord&logoColor=ffffff&labelColor=6A7EC2" alt="Discord: #vax-ui-backend" />
    </a>
</div>

## Development

### Prerequisites

1. [Python 3.8](https://www.python.org/downloads/release/python-380/)
2. [Poetry](https://python-poetry.org/): A tool for dependency management and packaging.
3. Access to VaxFinder's Microsoft SQL Server database hosted on [Azure](https://azure.microsoft.com/en-ca/services/sql-database/). Please message Patrick or Evan for access.
4. [Docker](https://www.docker.com/) (for testing): A container management tool which we use to package our application.
5. [Docker Compose](https://docs.docker.com/compose/install/) (for testing): Multi-container orchestration to give high-level control of containers during testing.

### Installation

1. Install the unixODBC library if you are on a linux environment as it's required for pyodbc (hence *aioodbc*). You can install it using your package manager, for example:

    ```bash
    $ sudo apt-get install unixodbc
    $ sudo apt-get install unixodbc-dev
    ```

2. Install Microsoft ODBC Driver 17 for SQL Server: [Windows](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15) | [Mac](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver15) | [Linux](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15)

3. Set up a VSCode MyPy Language Server (Optional)

    On macOS or Linux:

    ```bash
    $ python -m venv ~/.mypyls
    $ ~/.mypyls/bin/pip install "https://github.com/matangover/mypyls/archive/master.zip#egg=mypyls[default-mypy]"
    ```

    On Windows:

    ```powershell
    $ python -m venv %USERPROFILE%\.mypyls
    $ %USERPROFILE%\.mypyls\Scripts\pip install "https://github.com/matangover/mypyls/archive/master.zip#egg=mypyls[default-mypy]"
    ```
   
    Install the mypy extension in VS Code (or reload the window if the extension is already installed).

4. Install all python dependencies with [Poetry](https://python-poetry.org/).

    ```bash
    $ poetry install
    ```

### Running the Server

1. Spawn a shell within a virtual environment.

    ```bash
    $ poetry shell
    ```

    All python dependencies should be installed within the virtual environment from the previous step.

2. Run the server on port `8007` from the root of the project within the shell.

    ```bash
    $ DB_URL={DATABASE_URL} python -m app.main
    ```

    - Swagger: [http://localhost:8007/swagger](http://localhost:8007/swagger)
    - ReDoc: [http://localhost:8007/redoc](http://localhost:8007/redoc)
    - OpenAPI Spec (JSON): [http://localhost:8007/openapi.json](http://localhost:8007/openapi.json)

    A note on the `DB_URL`. Since we're using SQL Server with a `pyodbc`-type driver, we form the URL like so:
    ```
    pyodbc+mssql://<USERNAME>:<PASSWORD>@<HOSTNAME>/<DATABASE_NAME>?driver=ODBC+Driver+17+for+SQL+Server
    ```

### Pre-commit Hooks

Pre-commit hooks helps identify simple issues in code before it's committed into Git. At the moment, *isort* and *black* are the only hooks that are set up. 

#### Install the git hook scripts

```bash
$ pre-commit install
```

#### Temporarily Disabling hooks

It's possible to disable hooks temporarily, but it isn't recommended.

```bash
$ SKIP=isort,black git commit -m <message>
```

## Testing

### Integration and Unit Tests

To run the integration and unit tests, you will need to use Docker Compose to spin up a Microsoft SQL Server instance, and then run the tests with the `DB_URL` pointed to it.

```bash
$ docker-compose up
$ DB_URL=pyodbc+mssql://SA:Password0@localhost?driver=ODBC+Driver+17+for+SQL+Server poetry run pytest -vvs app/tests/
```

Once you're done running the tests, you will need to tear down the database instance, otherwise if you try running the tests again it will use the same instance.

```bash
$ docker-compose down
$ docker-compose rm -f
```

There are ideas in the works to possibly group this all into a simple shell script or something or further wrap it in a test harness so it's not cumbersome.


## Environments

### Production

**Please note that the production environment is currently not stable.** :warning:

The production environment, deployed after a staging build of the `main` branch is manually approved, can be accessed here: [https://vax-availability-api.azurewebsites.net](https://vax-availability-api.azurewebsites.net).

- Swagger: [https://vax-availability-api.azurewebsites.net/swagger](https://vax-availability-api.azurewebsites.net/swagger)
- ReDoc: [https://vax-availability-api.azurewebsites.net/redoc](https://vax-availability-api.azurewebsites.net/redoc)
- OpenAPI: [https://vax-availability-api.azurewebsites.net/openapi.json](https://vax-availability-api.azurewebsites.net/openapi.json)

### Staging

The staging environment, which is automatically deployed from the `main` branch, can be accessed here: [https://vax-availability-api-staging.azurewebsites.net](https://vax-availability-api-staging.azurewebsites.net).

- Swagger: [https://vax-availability-api-staging.azurewebsites.net/swagger](https://vax-availability-api-staging.azurewebsites.net/swagger)
- ReDoc: [https://vax-availability-api-staging.azurewebsites.net/redoc](https://vax-availability-api-staging.azurewebsites.net/redoc)
- OpenAPI: [https://vax-availability-api-staging.azurewebsites.net/openapi.json](https://vax-availability-api-staging.azurewebsites.net/openapi.json)

