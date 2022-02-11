echo "from django.contrib.auth.models import User; User.objects.create_superuser('$DJANGO_ADMIN','','$DJANGO_ADMIN_PASSWORD')" | python manage.py shell
