from django.db import models
from enum import Enum, IntEnum
from django.urls import reverse
from slugify import slugify
from django.conf import settings
from taggit.managers import TaggableManager

# Create your models here.


class Status(Enum):
    DRAFT = "DRAFT"
    OPEN = "OPEN"
    CLOSED = "CLOSED"



class Category(Enum):
    VEHICLE = "VEHICLE"
    PROPERTY = "PROPERTY"
    MOBILE_PHONES_AND_TABLETS ="MOBILE PHONES AND TABLETS"
    ELECTRONICS = "ELECTRONICS"
    HOME_AND_FURNITURE_APPLIANCES = "HOME_AND_FURNITURE_APPLIANCES"
    HEALTH_AND_BEAUTY = "HEALTH_AND_BEAUTY"
    FASHION = "FASHION"
    SPORTS_ARTS_AND_OUTDOOR = "SPORTS_ARTS_AND_OUTDOOR"
    SEEKING_WORK = "SEEKING_WORK"
    SERVICES = "SERVICES"
    JOBS = "JOBS"
    BABIES_AND_KIDS = "BABIES_AND_KIDS"
    ANIMALS_AND_PETS = "ANIMALS_AND_PETS"
    AGRICULTURE_AND_FOOD = "AGRICULTURE_AND_FOOD"
    COMMERCIAL_EQUIPMENT_AND_TOOLS = "COMMERCIAL_EQUIPMENT_AND_TOOLS"
    REPAIR_AND_CONSTRUCTION = "REPAIR_AND_CONSTRUCTION"



class product(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,related_name="seller",on_delete=models.SET_NULL,)
    title = models.CharField(max_length=50)
    Description = models.TextField(blank=True, null=True)
    category = models.CharField(choices=[(tag.name, tag.value) for tag in Category], max_length=30)
    county = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    slug = models.SlugField(max_length=80, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=1)
    status = models.CharField(choices=[(tag.name, tag.value) for tag in Status], max_length=10, default=Status.OPEN)
    views= models.IntegerField(default=0)
    tags = TaggableManager(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.user.username}-{self.title}",lowecase=True,max_length=80
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})

    
class image(models.Model):
    product = models.ForeignKey(product, null=True, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', verbose_name="image",)
    index = models.IntegerField(null=True)
    

    class Meta:
        verbose_name = "image"
        verbose_name_plural = "images"


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
