import re
from Logging import log as Log
# CẢM ƠN GITHUB https://github.com/the-robot cho source code này

"""
 module này để tìm các lỗi phát sinh ra trong html có thể là thông báo lỗi từ data base hay không
"""

## các thong báo lỗi của sql
sql_errors = {
    "MySQL": (r"SQLi syntax.*MySQL", r"Warning.*mysql_.*", r"MySQL Query fail.*", r"SQLi syntax.*MariaDB server",r"Warning",
              r"mysqli_num_rows()",r"mysql_fetch_array",r"Error at line near"),
    "PostgreSQL": (r"PostgreSQL.*ERROR", r"Warning.*\Wpg_.*", r"Warning.*PostgreSQL"),
    "Microsoft SQLi Server": (
        r"OLE DB.* SQLi Server", r"(\W|\A)SQLi Server.*Driver", r"Warning.*odbc_.*", r"Warning.*mssql_",
        r"Msg \d+, Level \d+, State \d+", r"Unclosed quotation mark after the character string",
        r"Microsoft OLE DB Provider for ODBC Drivers"),
    "Microsoft Access": (r"Microsoft Access Driver", r"Access Database Engine", r"Microsoft JET Database Engine",
                         r".*Syntax error.*query expression"),
    "Oracle": (
        r"\bORA-[0-9][0-9][0-9][0-9]", r"Oracle error", r"Warning.*oci_.*", "Microsoft OLE DB Provider for Oracle"),
    "IBM DB2": (r"CLI Driver.*DB2", r"DB2 SQLi error"),
    "SQLite": (r"SQLite/JDBCDriver", r"System.Data.SQLite.SQLiteException"),
    "Informix": (r"Warning.*ibase_.*", r"com.informix.jdbc"),
    "Sybase": (r"Warning.*sybase.*", r"Sybase message")
}


def check(html):
    # print(type(html))
    if type(html) is bytes:
        html = html.decode('utf-8')

    for db, errors in sql_errors.items():
        for error in errors:
            if re.compile(error).search(html):
                Log.info('error  ' + error)
                return True, db
        return False, None
