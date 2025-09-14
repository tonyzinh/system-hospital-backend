import os
from dotenv import load_dotenv

load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', "hospital_db"),
        'USER': os.getenv('POSTGRES_USER', "hospital_db"),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', "hospital_pass"),
        'HOST': os.getenv('POSTGRES_HOST', "localhost"),
        'PORT': os.getenv('POSTGRES_PORT', "5432"),
    }
}

