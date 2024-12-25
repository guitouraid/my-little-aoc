# either relative to project dir or absolute
DEFAULT_DATA_DIR = 'data/{year}'

# relative to `DEFAULT_DATA_DIR` or absolute
DEFAULT_DATA_FILE = '{year}_{day}.txt'

# relative to settings directory
DEFAULT_SETTINGS_DIR = '{year}'

# relative to `SETTINGS_DIR` or absolute
DEFAULT_SETTINGS_FILE = 'settings_{year}_{day}.py'

# the template file name, to be placed in templates dir if changed
DEFAULT_TEMPLATE = 'settings.py.j2'

# read mode to apply for template
DEFAULT_READ_MODE = 'lines'
