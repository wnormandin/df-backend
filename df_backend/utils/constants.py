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


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
EMAIL_DATA_DIR = os.path.join(DATA_DIR, 'email')
LOG_DATA_DIR = os.path.join(DATA_DIR, 'logs')
LOG_LEVEL = int(os.environ.get('DF_LOG_LEVEL', 10))
GENDER_CHOICES = [('male', 'Male'), ('female', 'Female'), ('neutral', 'Neutral')]

DF_SYSTEM_USER = 'system'
DF_PLAYER_GROUP = 'players'

CORE_STATS = ['food', 'drink', 'stamina', 'toughness', 'agility', 'dexterity', 'intelligence',
              'wisdom', 'charm', 'persuasion', 'introversion', 'stability', 'friendliness',
              'elements', 'physical', 'magic', 'hunger', 'thirst', 'exhaustion']
