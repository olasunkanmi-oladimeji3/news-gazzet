from . import views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
app_name='zenithal'

urlpatterns = [
    path('',views.homeview,name='home'),
    path('about/',views.aboutview,name='about'),
    path('post/<int:pk>', views.postview, name='post_detail'),

    path('post/new/', views.CreatePostView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('drafts/', views.DraftListView.as_view(), name='post_draft_list'),
    path('post/<int:pk>/remove/', views.PostDeleteView.as_view(), name='post_remove'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),

    path('<slug:category_slug>/',views.homeview,name='category'),
]
if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
