import os

# Database credentials and config
DB_USER = os.environ.get('DF_DB_USER', 'dunderfunk')
DB_PASS = os.environ.get('DF_DB_PASS', None)
DB_NAME = os.environ.get('DF_DB_NAME', 'df_backend')
DB_HOST = os.environ.get('DF_DB_HOST', '127.0.0.1')
DB_PORT = os.environ.get('DF_DB_PORT', '3306')

# Placeholders for outbound SMTP
SMTP_HOST = os.environ.get('DF_SMTP_HOST', None)
SMTP_USER = os.environ.get('DF_SMTP_USER', None)
SMTP_PASS = os.environ.get('DF_SMTP_PASS', None)
SMTP_PORT = os.environ.get('DF_SMTP_PORT', None)

# Email archive settings
EMAIL_ARCHIVE_PATH = os.environ.get('DF_EMAIL_ARCHIVE', os.path.expanduser('~/df_outbound_mail'))
