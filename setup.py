from distutils.core import setup
setup(
    name = 'nautilus',
    packages = ['nautilus'],
    version = '0.0',
    description = 'A library for creating microservice applications.',
    author = 'Alec Aivazis',
    author_email = 'alec@aivazis.com',
    url = 'https://github.com/aaivazis/nautilus',
    download_url = 'https://github.com/aaivazis/nautilus/tarball/0.0',
    keywords = ['microservice', 'flask', 'graphql'],
    classifiers = [],
    install_requires = [
        'bcrypt',
        'flask',
        'flask_admin',
        'flask_graphql',
        'flask_jsontools',
        'flask_login',
        'flask_script',
        'flask_sqlalchemy',
        'graphene',
        'sqlalchemy',
    ]
)
