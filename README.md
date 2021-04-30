# VaxFinder-backend
Backend for the Vaccine Hunters Finder tool.

## Development
### Dependency Installation
------------
1. AIOODBC

    In a linux environment pyodbc_ (hence *aioodbc*) requires the unixODBC_ library.
    You can install it using your package manager, for example:

        $ sudo apt-get install unixodbc
        $ sudo apt-get install unixodbc-dev
    
    In a windows environment, you can skip this step.

2. Microsoft ODBC 17

    [Linux Installation](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15)
    
    [Windows Installation](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15)

3. VSCode MyPy Language Server (Optional)

    On macOS or Linux:

        $ python -m venv ~/.mypyls
        $ ~/.mypyls/bin/pip install "https://github.com/matangover/mypyls/archive/master.zip#egg=mypyls[default-mypy]"

    On Windows:

        $ python -m venv %USERPROFILE%\.mypyls
        $ %USERPROFILE%\.mypyls\Scripts\pip install "https://github.com/matangover/mypyls/archive/master.zip#egg=mypyls[default-mypy]"

    Install the mypy extension in VS Code (or reload the window if the extension is already installed).

4. Run

        pip install -r requirements.txt

    in the root of the repo

### Running the Server
------------

Run

    python -m api.main --database_url='{DATABASE_URL}'

in the root of the repo. The backend will be served on [`localhost:8007`](http://localhost:8007)

## Production
------------
TBA