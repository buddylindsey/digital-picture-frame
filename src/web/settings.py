import os

DEBUG = True

django_settings = {
    'DEBUG': DEBUG,
    'SECRET_KEY': os.urandom(32),
    'ALLOWED_HOSTS': ['*'],
    'ROOT_URLCONF': 'src.web.urls',
    'MIDDLEWARE_CLASSES': (
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
    'TEMPLATES': [{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['{}'.format(os.path.dirname(os.path.abspath(__file__)))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },]
}