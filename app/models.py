from django.contrib.auth.models import User
from django.db import models
# auth_models.User -> klase nga vete Django per menaxhimin e Users
from django.db.models import QuerySet
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Liber(models.Model):
    titulli = models.CharField(max_length=255)
    autori = models.CharField(max_length=255)
    cmimi = models.CharField(max_length=255)
    img_src = models.CharField(max_length=255)
    iid = models.IntegerField(primary_key=True)
    vlersimi_avg = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    def as_dict(self):
        return {
            "titulli": self.titulli,
            "autori": self.autori,
            "cmimi": self.cmimi,
            "img_src": self.img_src,
            "iid": self.iid,
            "vlersimi_mesatar": self.vlersimi_avg
        }


class Autor(models.Model):
    emri = models.CharField(max_length=255)
    iid = models.IntegerField(primary_key=True)

    # <grumbull me libra qe i ka shkruajtur ky/kjo autor/e>
    librat = models.ManyToManyField(Liber)

    def as_dict(self):
        return {
            "emri": self.emri,
            "iid": self.iid
        }


VLERSIMET = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)]


class Vlersim(models.Model):
    perdorues = models.ForeignKey(to=User, related_name='vlersimet', on_delete=models.CASCADE)
    liber = models.ForeignKey(to=Liber, related_name='vlersimet', on_delete=models.CASCADE)
    vlersimi = models.IntegerField(choices=VLERSIMET, default=0)


class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    librat = models.ManyToManyField(Liber)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profil.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profil.save()


class Cache(models.Model):
    librat_to_string = models.CharField(max_length=5000)
    perdorues = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
