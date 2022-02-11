echo "from django.contrib.auth.models import User; User.objects.create_superuser($DJANGO_ADMIN,'',$DJANGO_PASSWORD)" | python manage.py shell
