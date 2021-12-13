from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World'

""" 
This is a simple Flask project, however, as project scales
in complexity and size, maintaining everything on a single 
file can be overwhelming. For this reason, Python projects
use package organization to split the code in various modules
to import them as needed. 
The goal file structure will be:
├── flaskr/
│   ├── __init__.py
│   ├── db.py
│   ├── schema.sql
│   ├── auth.py
│   ├── blog.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── blog/
│   │       ├── create.html
│   │       ├── index.html
│   │       └── update.html
│   └── static/
│       └── style.css
├── tests/
│   ├── conftest.py
│   ├── data.sql
│   ├── test_factory.py
│   ├── test_db.py
│   ├── test_auth.py
│   └── test_blog.py
├── venv/
├── setup.py
└── MANIFEST.in
flaskr/, a Python package containing your application code and files.
tests/, a directory containing test modules.
venv/, a Python virtual environment where Flask and other dependencies are installed.
Installation files telling Python how to install your project.
Version control config, such as git. You should make a habit of using some type of version control for all your projects, no matter the size.
Any other project files you might add in the future.
In our case, the venv folder is global to the repo, and for that matter we will have a slightly different folder structure.
Some files we should add to the .gitignore file are:
venv/
*.pyc
__pycache__/
instance/
.pytest_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/
"""
