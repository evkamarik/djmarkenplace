from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('user'), related_name='customer')
    first_name = models.CharField(max_length=30, null=True, blank=True, verbose_name=_('name'))
    last_name = models.CharField(max_length=30, null=True, blank=True, verbose_name=_('last name'))
    email = models.EmailField()
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone_number = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True,
                                    verbose_name=_('phone number'))
    address = models.CharField(max_length=250, verbose_name=_('address'))
    balance = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name=_('balance'))
    status = models.CharField(max_length=30, default='Initial', verbose_name=_('status'))

    class Meta:
        verbose_name_plural = _('customers')
        verbose_name = _('customer')

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('users:account', kwargs={'customer_id': self.pk})

    objects = models.Manager()
