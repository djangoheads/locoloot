# Install 
    
    pip install poetry
    poetry install

## Init Project

    python manage.py migrate 
    python manage.py loaddata languages_data.json.gz
    python manage.py update_countries_plus


## Associate Countries and languages 

    python manage.py shell
    >>> from languages_plus.utils import associate_countries_and_languages
    >>> associate_countries_and_languages()
