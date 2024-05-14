run:
	@python manage.py runserver 0.0.0.0:8001
migrate:
	@python manage.py migrate
makemigrations:
	@python manage.py makemigrations
shell:
	@python manage.py shell_plus

