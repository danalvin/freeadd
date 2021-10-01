from django.db import models
from enum import Enum, IntEnum
from django.urls import reverse
from slugify import slugify
from django.conf import settings
from taggit.managers import TaggableManager
from autoslug import AutoSlugField

# Create your models here.


class Status(Enum):
    DRAFT = "DRAFT"
    OPEN = "OPEN"
    CLOSED = "CLOSED"

# for me to call that kwa frontend, lazma zikuwe populated na vitu, wacha nikuhow exaple kwa site

class Category(models.Model):
    name=models.CharField( max_length=50)
    slug = AutoSlugField(populate_from='name')
    image = models.ImageField(upload_to='images/categries', verbose_name="category image", null=True)
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name

    def get_product_count(self):
        """ Returns amount of posts of this category """
        post_count = product.objects.filter(category = self).count()
        return(post_count)

    def get_absolute_url(self):
        return reverse('products:product_list_by_category', args=[self.slug,])



class Subcategory(models.Model):
    name=models.CharField( max_length=50)
    Category=models.ForeignKey("Category", verbose_name="category", on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='name')
    class Meta:
        verbose_name = "Sub Category"
        verbose_name_plural = "Sub Categories"

    def __str__(self):
        return self.name

    def get_product_count(self):
        """ Returns amount of posts of this category """
        post_count = product.objects.filter(Subcategory = self).count()
        return(post_count)

    def get_absolute_url(self):
        return reverse('products:product_list_by_category', args=[self.slug,])



class Brand(models.Model):
    name=models.CharField( max_length=50)
    SubCategory=models.ForeignKey("Subcategory", verbose_name="brand", on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='name')
    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name

    def get_product_count(self):
        """ Returns amount of posts of this category """
        post_count = product.objects.filter(Brand = self).count()
        return(post_count)

    def get_absolute_url(self):
        return reverse('products:product_list_by_category', args=[self.slug,])


class County(models.Model):
    name=models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='name')
    class Meta:
        verbose_name = "County"
        verbose_name_plural = "Counties"
    def __str__(self):
        return self.name



class area(models.Model):
    name=models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='name')
    County=models.ForeignKey("County", verbose_name="County", on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Area"
        verbose_name_plural = "Area"
    def __str__(self):
        return self.name



class BoostedItem(models.Model):
    BoostChoices = (
        ('None', ('None')),
        ('Regular', ('Regular')),
        ('Premium', ('Premium')),
        ('Platinum', ('Platinum')),
    )
    product= models.ForeignKey("product", on_delete=models.CASCADE)
    type=models.ForeignKey("BoostedType", verbose_name="type", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class BoostedType(models.Model):
    name=models.CharField( max_length=50)
    price=models.PositiveIntegerField(blank=False)
    duration = models.CharField(max_length=50, default=30)

    def __str__(self):
        return self.name


class product(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,related_name="seller",on_delete=models.SET_NULL,)
    title = models.CharField(max_length=50)
    Description = models.TextField(blank=True, null=True)
    category = models.ForeignKey("Category", verbose_name="Category", on_delete=models.CASCADE)
    Subcategory=models.ForeignKey("Subcategory", on_delete=models.CASCADE)
    Brand=models.ForeignKey("Brand", on_delete=models.CASCADE)
    county = models.ForeignKey("County", verbose_name="County", on_delete=models.CASCADE)
    location=models.ForeignKey('area', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=100, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=1)
    status = models.CharField(choices=[(tag.name, tag.value) for tag in Status], max_length=10, default=Status.OPEN)
    views= models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', verbose_name="image",)
    image2 = models.ImageField(upload_to='images/', verbose_name="image2",null=True)
    image3 = models.ImageField(upload_to='images/', verbose_name="image3",null=True)

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    
class image(models.Model):
    image = models.ImageField(upload_to='images/', verbose_name="image",)
    index = models.IntegerField(null=True)




class ProductQuerySet(models.query.QuerySet):
    """Personalized queryset created to improve model usability"""

    def get_open(self):
        """Returns only the open items in the current queryset."""
        return self.filter(status="OPEN")

    def get_drafts(self):
        """Returns only the items marked as DRAFT in the current queryset."""
        return self.filter(status="DRAFT")

    def get_closed(self):
        """Returns only the items marked as closed in the current queryset."""
        return self.filter(status="CLOSED")

    def get_counted_tags(self):
        tag_dict = {}
        query = (
            self.filter(status="P").annotate(tagged=Count("tags")).filter(tags__gt=0)
        )
        for obj in query:
            for tag in obj.tags.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1

                else:  # pragma: no cover
                    tag_dict[tag] += 1

        return tag_dict.items()
