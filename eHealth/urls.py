from django.conf.urls import patterns, include, url
from eHealth import views

urlpatterns = (#
               url(r'^$', views.index, name="index"),
               url(r'^searching/', views.searching, name='search'),
               url(r'^user', views.user, name="user"),
               url(r'^category', views.ajax_saved_pages, name="ajax_saved_pages"),
               url(r'^deleteCategory', views.ajax_delete_categories, name="ajax_delete_categories"),
               url(r'^deletePage', views.ajax_delete_pages, name="ajax_delete_pages"),
               url(r'^getUserInfo', views.ajax_get_user_info, name="ajax_get_user_info"),
               url(r'^changeUserInfo', views.ajax_change_user_info, name="ajax_change_user_info"),
               url(r'^Page', views.ajax_add_page, name="ajax_add_page"),
               url(r'^addCategory', views.ajax_add_category, name="ajax_add_category"),
               url(r'^pageClick', views.ajax_page_click, name="ajax_page_click"),
               url(r'^Privacy', views.ajax_page_status_change, name="ajax_page_status_change"),
               url(r'^gpages',views.ajax_get_all_page_statuses, name="ajax_get_all_page_statuses"),
               url(r'^about', views.about, name='about'),
              url(r'^health', views.about, name='h')
               )
