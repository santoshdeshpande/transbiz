from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import transaction
from transbiz.apiserver.models import *


@transaction.non_atomic_requests
def create_vertical(v=5, c=10, s=20):
    last_id = 0
    iv = IndustryVertical.objects.all().order_by('-id').first()
    if iv:
        last_id = iv.id
    for i in range(last_id + 1, last_id + v + 1):
        iv = IndustryVertical(name="Vertical " + str(i))
        iv.save()
        create_categories(iv, c, s)


def create_categories(vertical, c, s):
    last_id = 0
    iv = Category.objects.all().order_by('-id').first()
    if iv:
        last_id = iv.id
    for i in range(last_id + 1, last_id + c + 1):
        c = Category(name="Category " + str(i), vertical=vertical)
        c.save()
        create_brands(c)
        create_sale(c, s)


def create_brands(category):
    Brand(name="Brand " + str(category.id), category=category).save()


def create_sale(category, s):
    last_id = 0
    iv = Category.objects.all().order_by('-id').first()
    if iv:
        last_id = iv.id
    user = User.objects.first()
    print user
    for i in range(last_id + 1, last_id + s + 1):
        brand = category.brand_set.first()
        new = (i % 3 == 0)
        start = datetime.now() + timedelta(hours=i)
        end = datetime.now() + timedelta(days=i)
        s = Sale(company_id=1, category=category, brand=brand, min_quantity=i, unit_of_measure=0,
                 model='model ' + str(i), price_in_inr=i * 1000, new=new, refurbished=not new, warranty=i,
                 start_date=start, end_date=end, active=True, created_by=user)
        s.save()


def delete_all():
    Category.objects.all().delete()
    Sale.objects.all().delete()
    IndustryVertical.objects.all().delete()
    Brand.objects.all().delete()


if __name__ == '__main__':
    print "Inserting dummy data"
    create_vertical()
