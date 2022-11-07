import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.urls import reverse
from app_users.models import Customer


def upload_to(instance, filename):
    return f'media/products/{str(instance.shop.name)}/{filename}'


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name=_('name'))

    class Meta:
        verbose_name_plural = _('categories')
        verbose_name = _('category')

    def __str__(self):
        return self.name

    objects = models.Manager()


class Item(models.Model):
    category = models.ForeignKey(Category, default=1, on_delete=models.CASCADE, verbose_name=_('category'),
                                 related_name='category_item')
    name = models.CharField(max_length=30, verbose_name=_('name'))
    code = models.CharField(max_length=100, verbose_name=_('code'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('price'))
    stock = models.PositiveIntegerField(verbose_name=_('stock'))
    image = models.ImageField(upload_to=upload_to, default=f'media/products/default.jpeg', blank=True)

    class Meta:
        verbose_name_plural = _('goods')
        verbose_name = _('good')

    def __str__(self):
        return str(_(self.name))

    def get_absolute_url(self):
        return reverse('shop:item', kwargs={'item_id': self.pk})

    def get_price(self):
        return self.price


class Shop(models.Model):
    name = models.CharField(max_length=30, verbose_name=_('name'))
    items = models.ManyToManyField(Item, related_query_name='shops')

    class Meta:
        verbose_name_plural = _('shops')
        verbose_name = _('shop')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:shop', kwargs={'pk': self.pk})


class Cart(models.Model):
    customer = models.OneToOneField(Customer, related_name='cart', on_delete=models.CASCADE, verbose_name=_('cart'))

    def __str__(self):
        return f'{self.customer.id} {self.customer.user.username}'

    def customer_id(self):
        return f'{self.customer.id}'

    def customer_name(self):
        return f'{self.customer.user.username}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, default=None, on_delete=models.CASCADE, related_name='cart_items',
                             verbose_name=_('cart'))
    item = models.ForeignKey(Item, null=True, blank=True, related_name='cart_items', on_delete=models.CASCADE,
                             verbose_name=_('item'))
    count = models.IntegerField(validators=[MinValueValidator(1)], null=True, blank=True, verbose_name=_('count'))
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                verbose_name=_('price'))
    added_at = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=_('added_at'))
    paid_at = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name=_('paid_at'))
    status = models.CharField(max_length=30, default='in_the_cart', verbose_name=_('status'))

    def customer_id(self):
        return f'{self.cart.customer_id}'

    def item_name(self):
        return f'{self.item.name}'

    def item_count(self):
        return f'{self.item.count}'

    def add_item(self, item, count):

        if self.item == item:
            self.count += count
        else:
            self.count = count

        self.price = item.price
        self.added_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# class Order(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_('customer'),
#                                  related_name='order')
#     item = models.ManyToManyField(Item, default=1, on_delete=models.CASCADE, verbose_name=_('item'),
#                                   related_name='order')
#     price = models.DecimalField(max_digits=10, default=0.00, decimal_places=2, verbose_name=_('price'))
#     item_count = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name=_('item count'))
#     date = models.DateTimeField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
#
#     class Meta:
#         verbose_name_plural = _('purchases')
#         verbose_name = _('purchase')
#
#     def get_absolute_url(self):
#         return reverse('shop:purchase', kwargs={'pk': self.pk})
