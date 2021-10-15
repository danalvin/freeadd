from django.conf.urls import url
from django.urls.conf import path
from django.urls.resolvers import URLPattern
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


from .views import CreateBoostedItems, CreateProductView2, DetailProductView, DraftsListView, EditProductView, Jobapplicationview, MyActiveProductsListView, MyClosedProductsListView, MyDraftProductsListView, MyProductsListView, ProductListView, CreateProductView, close_product, delete_product, post_image, delete_image, publish_product, ProductList1
from .home import *
app_name = "products"
urlpatterns = [
    path("", home_view, name="home"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("", ProductListView.as_view(), name="list"),
    path("new-product/", CreateProductView.as_view(), name="create_new"),
    path("new-product/", CreateProductView2.as_view(), name="createview2"),
    path("boost-item/", CreateBoostedItems.as_view(), name="boost-item"),
    path("job/", Jobapplicationview.as_view(), name="Job"),
    path("post-image/", post_image, name="post_image"),
    path("delete-image/", delete_image, name="delete_image"),
    path("delete/(?<id>\d+)/", delete_product, name="delete_property"),
    path("close/(?<id>\d+)/", close_product, name="close_property"),
    path("publish/(?<id>\d+)/", publish_product, name="publish_property"),
    path("my_listings/", MyProductsListView.as_view(), name="my_listings"),
    path("my_active_listings/", MyActiveProductsListView.as_view(), name="my_active_listings"),
    path("my_draft_listings/", MyDraftProductsListView.as_view(), name="my_draft_listings"),
    path("my_closed_listings/", MyClosedProductsListView.as_view(), name="my_closed_listings"),
    path("my-drafts/", DraftsListView.as_view(), name="drafts"),
    path("edit/(?<pk>\d+)/", EditProductView.as_view(), name="edit_product"),
    path("(?<slug>[-\w]+)/", DetailProductView.as_view(), name="listing"),


    path('', home_view, name="list"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path('products', ProductListView.as_view(), name="list"),
    # path('new-product/', CreateProductView.as_view(), name="create_new"),
    path('post-image/', post_image, name="post_image" ),
    path('boost-item/', CreateBoostedItems.as_view(), name="boost_item"),
    path('delete-image/', delete_image, name = "delete_image"),
    path('delete/(?<id>\d+', delete_product, name="delete_property"),
    path('close/(?<id>\d+)/',close_product, name="close_property"),
    path('publish/(?<id>\d+)/', publish_product, name="publish_product"),
    path('my_listings/', MyProductsListView, name="my_listings"),
    path('my_active_listings/', MyActiveProductsListView, name="my_active_listings"),
    path('my_draft_listings/', MyDraftProductsListView, name="my_draft_listings"),
    path('my_closed_listings/', MyClosedProductsListView, name= "my_closed_listings"),
    path('my-drafts/', DraftsListView, name="drafts"),
    path('edit/(?<pk>\d+)/', EditProductView, name="edit_product"),
    path('(?<slug>[-\w]+)/', DetailProductView, name="Product"),
    path('category/<category_slug>/', ProductList1.as_view(), name = "product_list_by_category")
]+ static(settings.STATIC_URL, document_root=settings.STATIC_URL)
