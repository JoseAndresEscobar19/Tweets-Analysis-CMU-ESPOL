# Analisis-tweets-CMU-ESPOL
Análisis de tweets en las revueltas ocurridas en Latinoamérica a finales del 2019.

## Requisitos
* Python: 3.7.3
* Django: 2.2.4
* Environ: pip install django-environ
* Agregar el .env en /analisistweets

## Perform backups
1. Connect to server
2. Backup :
```
cd CMU_backups
mysqldump -u [DB_USER] -p[DB_PASS] --no-tablespaces [DB_NAME] > [filename].sql
```

## Development workflow
1. Start python virtual environment.
2. Set environment variables :
```
SECRET_KEY=<secret>
DJANGO_SETTINGS_MODULE=analisistweets.settings_dev
```
3. Change directory and start app :
```
cd web_app
python manage.py runserver
```
