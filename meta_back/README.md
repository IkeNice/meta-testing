# Project setup
The `requirements.txt` file list all Python libraries this project depends on, and they will be installed using:

```python
pip install -r requirements.txt
```

# Perform database migration:
```python
py manage.py check
py manage.py migrate
```

# Start Django server
Inside this folder run:

```python
py manage.py runserver
```

# Run `data_transfer.py` in Command Line:
First, you need to set up db_config.py file:
  - create db_config.py
  - open db_config.py.default and copy whole file
  - paste it in your db_config.py
  - set your own information

After that in Command Line:
```python
py data_transfer.py
```
