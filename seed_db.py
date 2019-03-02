import datetime
import os
import random
import sys

import django
import faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_framework_crud.settings')
django.setup()

from todos.models import Todo

if len(sys.argv) > 1:
    if sys.argv[1] == 'drop':
        Todo.objects.all().delete()
fake = faker.Faker()
todos_count = Todo.objects.count()
todos_to_seed = 43
todos_to_seed -= todos_count
if todos_to_seed > 0:
    sys.stdout.write('[+] Seeding %d todos\n' % (todos_to_seed))
    start_date = datetime.date(year=2014, month=1, day=1)
    for i in range(0, todos_to_seed):
        title = ' '.join(fake.words(nb=random.randint(2, 5)))
        description = ' '.join(fake.sentences(nb=random.randint(2, 10)))
        created_at = fake.date_between(start_date=start_date, end_date=start_date.replace(2019))
        updated_at = fake.date_between(start_date=created_at, end_date='now')
        completed = fake.boolean(chance_of_getting_true=40)
        Todo.objects.create(title=title, description=description, completed=completed, created_at=created_at,
                            updated_at=updated_at)
