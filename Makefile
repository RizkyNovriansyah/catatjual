run:
	@python manage.py runserver 0.0.0.0:8000
runworker:
	@celery -A coofis worker -l debug
rungunicorn:
	@gunicorn --log-level=DEBUG -k eventlet t coofis.wsgi --bind 0.0.0.0:8000
runportal:
	@python manage.py runserver 127.0.0.1:9000 --settings=coofis.portal_settings
initial:
	@python manage.py initial
resetmigrations:
    ifdef app
		@python manage.py runscript resetmigrations --script-args=$$app --settings=coofis.portal_settings
    else
		@echo "please specified 'app'"
    endif
initdev:
	@python manage.py initdev --settings=coofis.portal_settings
initportal:
	@python manage.py initportal --settings=coofis.portal_settings
cleanmigrations:
	@python manage.py cleanmigrations
migrate:
	@python manage.py migrate
makemigrations:
	@python manage.py makemigrations
shell:
	@python manage.py shell_plus
