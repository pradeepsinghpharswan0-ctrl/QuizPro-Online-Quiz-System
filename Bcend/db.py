import sqlite3

DB_NAME = "quiz.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()

    with open("schema.sql", "r") as file:
        conn.executescript(file.read())

    conn.commit()
    conn.close()


def seed_questions():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM questions")
    count = cur.fetchone()[0]

    if count == 0:
        questions = [
            ("c", "easy", "Who is the father of C language?",
             "Steve Jobs", "James Gosling", "Dennis Ritchie", "Rasmus Lerdorf",
             "C", "Dennis Ritchie is the father of C Programming Language."),

            ("c", "easy", "Which of the following is not a valid C variable name?",
             "int number;", "float rate;", "int variable_count;", "int $main;",
             "D", "Only underscore is allowed as a special character in C variable names."),

            ("c", "easy", "All keywords in C are in ____________",
             "LowerCase letters", "UpperCase letters", "CamelCase letters", "None of the mentioned",
             "A", "All C keywords are written in lowercase letters."),

            ("c", "easy", "Which of the following is true for variable names in C?",
             "They can contain alphanumeric characters as well as special characters",
             "It is not an error to declare a variable to be one of the keywords",
             "Variable names cannot start with a digit",
             "Variable can be of any length",
             "C", "A C variable name cannot start with a digit."),

            ("c", "easy", "Which is valid C expression?",
             "int my_num = 100,000;", "int my_num = 100000;", "int my num = 1000;", "int $my_num = 10000;",
             "B", "Spaces, commas, and dollar signs cannot be used in a standard C variable name."),

            ("c", "easy", "Which of the following cannot be a variable name in C?",
             "volatile", "true", "friend", "export",
             "A", "volatile is a keyword in C, so it cannot be used as a variable name."),

            ("c", "easy", "What is short int in C programming?",
             "The basic data type of C", "Qualifier", "Short is the qualifier and int is the basic data type", "All of the mentioned",
             "C", "short is a qualifier and int is the basic data type."),

            ("c", "easy", "Which of the following declaration is not supported by C language?",
             "String str;", "char *str;", "float str = 3e2;", "Both “String str;” and “float str = 3e2;”",
             "A", "String is not a built-in data type in C language."),

            ("c", "easy", "Which keyword is used to prevent any changes in the variable within a C program?",
             "immutable", "mutable", "const", "volatile",
             "C", "const is used to make a variable constant in C."),

            ("c", "easy", "What is the result of logical or relational expression in C?",
             "True or False", "0 or 1", "0 if false and any positive number if true", "None of the mentioned",
             "B", "Logical and relational expressions in C return 0 or 1."),

            ("c", "easy", "Which of the following typecasting is accepted by C language?",
             "Widening conversions", "Narrowing conversions", "Widening & Narrowing conversions", "None of the mentioned",
             "C", "C supports both widening and narrowing type conversions."),

            ("c", "easy", "Where in C the order of precedence of operators do not exist?",
             "Within conditional statements, if, else", "Within while, do-while", "Within a macro definition", "None of the mentioned",
             "D", "Operator precedence exists in C expressions."),

            ("c", "easy", "Which of the following is NOT possible with any 2 operators in C?",
             "Different precedence, same associativity", "Different precedence, different associativity", "Same precedence, different associativity", "All of the mentioned",
             "C", "Operators with the same precedence generally follow the same associativity."),

            ("c", "easy", "What is an example of iteration in C?",
             "for", "while", "do-while", "all of the mentioned",
             "D", "for, while, and do-while are all examples of iteration in C."),

            ("c", "easy", "Functions can return enumeration constants in C?",
             "true", "false", "depends on the compiler", "depends on the standard",
             "A", "Functions can return enumeration constants in C."),

            ("c", "easy", "Functions in C Language are always _________",
             "Internal", "External", "Both Internal and External", "External and Internal are not valid terms for functions",
             "B", "By default, functions in C have external linkage."),

            ("c", "easy", "Which of following is not accepted in C?",
             "static a = 10;", "static int func (int);", "static static int a;", "all of the mentioned",
             "C", "Using static twice in the same declaration is not valid."),

            ("c", "easy", "Property which allows to produce different executable for different platforms in C is called?",
             "File inclusion", "Selective inclusion", "Conditional compilation", "Recursive macros",
             "C", "Conditional compilation allows different executable code for different platforms."),

            ("c", "easy", "What is #include <stdio.h>?",
             "Preprocessor directive", "Inclusion directive", "File inclusion directive", "None of the mentioned",
             "A", "#include <stdio.h> is a preprocessor directive."),

            ("c", "easy", "C preprocessors can have compiler specific features.",
             "True", "False", "Depends on the standard", "Depends on the platform",
             "A", "#pragma is an example of a compiler-specific preprocessor feature."),

            ("python", "easy", "Which keyword is used to define a function in Python?",
             "func", "define", "def", "function",
             "C", "In Python, functions are defined using the def keyword."),

            ("python", "easy", "Who developed Python programming language?", "Dennis Ritchie", "Guido van Rossum", "James Gosling", "Bjarne Stroustrup", "B", "Python was developed by Guido van Rossum."),

("python", "easy", "Which keyword is used to define a function in Python?", "func", "define", "def", "function", "C", "Python uses the def keyword to define a function."),

("python", "easy", "Which symbol is used for comments in Python?", "//", "/* */", "#", "<!-- -->", "C", "Python uses # for single-line comments."),

("python", "easy", "Which data type is used to store True or False values?", "int", "str", "bool", "float", "C", "Boolean values are stored using bool data type."),

("python", "easy", "Which function is used to display output in Python?", "echo()", "print()", "display()", "show()", "B", "print() is used to display output in Python."),

("python", "easy", "Which of the following is a Python list?", "{1,2,3}", "(1,2,3)", "[1,2,3]", "<1,2,3>", "C", "Lists in Python are written using square brackets."),

("python", "easy", "Which operator is used for exponentiation in Python?", "^", "**", "//", "%", "B", "** is used for exponentiation in Python."),

("python", "easy", "What is the output of len('Python')?", "5", "6", "7", "Error", "B", "Python has 6 characters."),

("python", "easy", "Which keyword is used for loop in Python?", "repeat", "loop", "for", "iterate", "C", "for is used to create loops in Python."),

("python", "easy", "Which function is used to take input from user?", "scan()", "input()", "read()", "get()", "B", "input() is used to take user input in Python."),

("python", "easy", "Which of these is immutable in Python?", "List", "Dictionary", "Tuple", "Set", "C", "Tuples are immutable in Python."),

("python", "easy", "Which file extension is used for Python files?", ".java", ".py", ".c", ".html", "B", "Python files use .py extension."),

("python", "easy", "Which keyword is used for decision making in Python?", "if", "check", "switch", "decide", "A", "if is used for decision making in Python."),

("python", "easy", "Which method adds an item to a list?", "add()", "insert()", "append()", "push()", "C", "append() adds an item at the end of a list."),

("python", "easy", "Which data type stores key-value pairs?", "List", "Tuple", "Dictionary", "String", "C", "Dictionary stores data in key-value pairs."),

("python", "easy", "What is the correct way to create a variable in Python?", "int x = 5", "x = 5", "var x = 5", "let x = 5", "B", "Python variables are created by assigning a value directly."),

("python", "easy", "Which keyword is used to import a module?", "include", "import", "using", "require", "B", "import is used to import modules in Python."),

("python", "easy", "Which method converts string to lowercase?", "lower()", "small()", "tolower()", "case()", "A", "lower() converts a string to lowercase."),

("python", "easy", "Which loop runs while a condition is true?", "for", "while", "do", "repeat", "B", "while loop runs as long as condition is true."),

("python", "easy", "What is Python mainly known for?", "Complex syntax", "Readability", "Only web design", "Only hardware control", "B", "Python is popular for its simple and readable syntax."),

("dbms", "easy", "What does DBMS stand for?", "Database Management System", "Data Backup Management System", "Digital Base Management Software", "Database Main Server", "A", "DBMS stands for Database Management System."),

("dbms", "easy", "Which language is used to manage databases?", "HTML", "SQL", "CSS", "C++", "B", "SQL is used to manage and query databases."),

("dbms", "easy", "What does SQL stand for?", "Structured Query Language", "Simple Query Language", "System Query Logic", "Standard Question Language", "A", "SQL stands for Structured Query Language."),

("dbms", "easy", "Which command is used to retrieve data from a database?", "GET", "SELECT", "FETCH", "OPEN", "B", "SELECT command is used to retrieve data."),

("dbms", "easy", "Which command is used to add new data into a table?", "ADD", "INSERT", "UPDATE", "CREATE", "B", "INSERT is used to add new records."),

("dbms", "easy", "Which command is used to remove records from a table?", "DELETE", "REMOVE", "DROP", "CLEAR", "A", "DELETE removes records from a table."),

("dbms", "easy", "Which key uniquely identifies each record in a table?", "Foreign Key", "Primary Key", "Candidate Key", "Super Key", "B", "Primary key uniquely identifies each record."),

("dbms", "easy", "Rows in a table are also called?", "Fields", "Attributes", "Records", "Columns", "C", "Rows are called records or tuples."),

("dbms", "easy", "Columns in a table are also called?", "Records", "Attributes", "Tuples", "Rows", "B", "Columns are called attributes or fields."),

("dbms", "easy", "Which command is used to create a table?", "MAKE TABLE", "CREATE TABLE", "NEW TABLE", "ADD TABLE", "B", "CREATE TABLE is used to create a new table."),

("dbms", "easy", "Which command is used to modify existing data?", "CHANGE", "MODIFY", "UPDATE", "ALTER", "C", "UPDATE is used to modify existing records."),

("dbms", "easy", "Which command removes a table completely?", "DELETE", "DROP", "REMOVE", "CLEAR", "B", "DROP removes the complete table structure and data."),

("dbms", "easy", "What is a foreign key?", "A key used to open database", "A key that links two tables", "A duplicate key", "A password", "B", "Foreign key links one table with another table."),

("dbms", "easy", "Which clause is used to filter records?", "ORDER BY", "WHERE", "GROUP BY", "HAVING", "B", "WHERE clause filters records."),

("dbms", "easy", "Which clause is used to sort records?", "WHERE", "SORT", "ORDER BY", "GROUP BY", "C", "ORDER BY is used to sort records."),

("dbms", "easy", "Which SQL function counts rows?", "SUM()", "COUNT()", "TOTAL()", "NUMBER()", "B", "COUNT() counts the number of rows."),

("dbms", "easy", "Which constraint prevents duplicate values?", "NOT NULL", "UNIQUE", "DEFAULT", "CHECK", "B", "UNIQUE prevents duplicate values."),

("dbms", "easy", "Which constraint prevents empty values?", "UNIQUE", "CHECK", "NOT NULL", "DEFAULT", "C", "NOT NULL prevents empty values."),

("dbms", "easy", "Which command is used to delete all rows but keep table structure?", "DROP", "TRUNCATE", "REMOVE", "CLEAR", "B", "TRUNCATE deletes all rows but keeps table structure."),

("dbms", "easy", "Which database model stores data in tables?", "Network model", "Hierarchical model", "Relational model", "Object model", "C", "Relational model stores data in tables."),
]

        cur.executemany(
            """
            INSERT INTO questions
            (category, difficulty, question, optA, optB, optC, optD, correct, explanation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            questions
        )

        conn.commit()

    conn.close()