from django.conf.urls import url
from django.urls.conf import path
from django.urls.resolvers import URLPattern
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path

from .views import CreateBoostedItems, DetailProductView, DraftsListView, EditProductView, MyActiveProductsListView, MyClosedProductsListView, MyDraftProductsListView, MyProductsListView, ProductListView, CreateProductView, close_product, delete_product, post_image, delete_image, publish_product, ProductList1
from .home import *
app_name = "products"
urlpatterns = [
    re_path(r"^$", home_view, name="home"),
    re_path(r"^dashboard/$", dashboard_view, name="dashboard"),
    re_path(r"^$", ProductListView.as_view(), name="list"),
    re_path(r"^new-product/$", CreateProductView.as_view(), name="create_new"),
    re_path(r"^boost-item/$", CreateBoostedItems.as_view(), name="boost-item"),
    re_path(r"^post-image/$", post_image, name="post_image"),
    re_path(r"^delete-image/$", delete_image, name="delete_image"),
    re_path(r"^delete/(?P<id>\d+)/$", delete_product, name="delete_property"),
    re_path(r"^close/(?P<id>\d+)/$", close_product, name="close_property"),
    re_path(r"^publish/(?P<id>\d+)/$", publish_product, name="publish_property"),
    re_path(r"^my_listings/", MyProductsListView.as_view(), name="my_listings"),
    re_path(r"^my_active_listings/$", MyActiveProductsListView.as_view(), name="my_active_listings"),
    re_path(r"^my_draft_listings/$", MyDraftProductsListView.as_view(), name="my_draft_listings"),
    re_path(r"^my_closed_listings/$", MyClosedProductsListView.as_view(), name="my_closed_listings"),
    re_path(r"^my-drafts/$", DraftsListView.as_view(), name="drafts"),
    re_path(r"^edit/(?P<pk>\d+)/$", EditProductView.as_view(), name="edit_product"),
    re_path(r"^(?P<slug>[-\w]+)/$", DetailProductView.as_view(), name="listing"),


    path('', home_view, name="list"),
    path("^dashboard/$", dashboard_view, name="dashboard"),
    path('products', ProductListView.as_view(), name="list"),
    # path('new-product/', CreateProductView.as_view(), name="create_new"),
    path('post-image/', post_image, name="post_image" ),
    path('boost-item/', CreateBoostedItems.as_view(), name="boost_item"),
    path('delete-image/', delete_image, name = "delete_image"),
    path('delete/(?P<id>\d+', delete_product, name="delete_property"),
    path('close/(?P<id>\d+)/$',close_product, name="close_property"),
    path('publish/(?P<id>\d+)/$', publish_product, name="publish_product"),
    path('my_listings/', MyProductsListView, name="my_listings"),
    path('my_active_listings/$', MyActiveProductsListView, name="my_active_listings"),
    path('my_draft_listings/$', MyDraftProductsListView, name="my_draft_listings"),
    path('my_closed_listings/$', MyClosedProductsListView, name= "my_closed_listings"),
    path('my-drafts/$', DraftsListView, name="drafts"),
    path('edit/(?P<pk>\d+)/$', EditProductView, name="edit_product"),
    path('(?P<slug>[-\w]+)/$', DetailProductView, name="Product"),
    path('category/<category_slug>/', ProductList1.as_view(), name = "product_list_by_category")
]+ static(settings.STATIC_URL, document_root=settings.STATIC_URL)
