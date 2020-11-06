import random

from django.contrib.auth.models import User

from app.models import Liber, Vlersim


def vlersim_automatik():
    liber_ids = list(Liber.objects.all().values_list('iid', flat=True))
    last_user_id = User.objects.values('id').last()['id']

    for index in range(1, 7000):
        print(f'User {index} po krijohet')
        user = User.objects.create(username=f'User-{index + last_user_id}', password=f'Password-{index + last_user_id}')

        random_books_to_read = random.randint(1, 300)
        BOOKS_READ = []
        vlerso_current_book = []

        for unit in range(1, random_books_to_read):
            temp_book = random.choice(liber_ids)
            if temp_book not in BOOKS_READ:
                BOOKS_READ.append(temp_book)

                print(f'Liber {unit} po shtohet per perdorues {index}')

                # Mirr librin e zgjedhur random
                libri_zgjedhur = Liber.objects.get(iid=temp_book)

                # Krijo nje vlersim random per librin e zgjedhur
                vlersimi = random.randint(0, 5)
                vlerso_current_book.append(Vlersim(perdorues=user, liber=libri_zgjedhur, vlersimi=vlersimi))

        Vlersim.objects.bulk_create(vlerso_current_book)
