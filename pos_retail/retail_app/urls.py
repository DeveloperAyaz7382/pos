from django.urls import path
from . import views

urlpatterns = [


    path('', views.home, name='home'),
    
    path('item-types/', views.item_type_list, name='item_type_list'),
    path('item-types/create/', views.item_type_create, name='item_type_create'),
    path('item-types/update/<int:pk>/', views.item_type_update, name='item_type_update'),
    path('item-types/delete/<int:pk>/', views.item_type_delete, name='item_type_delete'),
   
    path('companyinfo/', views.companyinfo_list, name='companyinfo_list'),
    path('companyinfo/create/', views.companyinfo_create, name='companyinfo_create'),
    path('companyinfo/update/<int:id>/', views.companyinfo_update, name='companyinfo_update'),
    path('companyinfo/delete/<int:id>/', views.companyinfo_delete, name='companyinfo_delete'),
    
    path('salesmen/', views.salesman_list, name='salesman_list'),
    path('salesman/create/<int:company_id>/', views.create_salesman, name='create_salesman'),
    path('salesman/<int:salesman_id>/edit/', views.edit_salesman, name='salesman_edit'),
    path('salesman/<int:salesman_id>/delete/', views.delete_salesman, name='salesman_delete'),
     

    path('inventory/', views.inventory_form_view, name='inventory_list'),  # Add a new item
    path('inventory/edit/<int:inventory_id>/', views.inventory_form_view, name='edit_inventory'),  # Edit an existing item
    path('inventory/delete/<int:item_id>/', views.delete_inventory, name='delete_inventory'),  # Delete an item
    

    path('stock-form/', views.stock_form_view, name='stock_form'),  # Define this pattern
    path('stock-list/', views.stock_list_view, name='stock_list'),
    path('stock-edit/<int:stock_id>/', views.stock_edit_view, name='stock_edit'),
    path('stock-delete/<int:stock_id>/', views.stock_delete_view, name='stock_delete'),
    
    
    path('stock-tracking-list/', views.stock_tracking_list_view, name='stock_tracking_list'),
    path('stock-tracking-form/', views.stock_tracking_form_view, name='stock_tracking_form'),
    path('stock-tracking-edit/<int:tracking_id>/', views.stock_tracking_edit_view, name='stock_tracking_edit'),
    path('stock-tracking-delete/<int:tracking_id>/', views.stock_tracking_delete_view, name='stock_tracking_delete'),
    
    
    path('stock-expiry-list/', views.stock_expiry_list_view, name='stock_expiry_list'),
    path('stock-expiry-form/', views.stock_expiry_form_view, name='stock_expiry_form'),
    path('stock-expiry-edit/<int:expiry_id>/', views.stock_expiry_edit_view, name='stock_expiry_edit'),
    path('stock-expiry-delete/<int:expiry_id>/', views.stock_expiry_delete_view, name='stock_expiry_delete'),
    
    path('order-list/', views.order_list_view, name='order_list'),
    path('order-form/', views.order_form, name='order-form'),  # This is the pattern we need
    path('order-edit/<int:order_id>/', views.order_edit_view, name='order_edit'),
    path('order-delete/<int:order_id>/', views.order_delete_view, name='order_delete'),
    
    
    path('order-item-list/', views.order_item_list, name='order_item_list'),
    path('order-item-form/', views.order_item_form, name='order_item_add'),  # URL for adding an order item
    path('order-item-form/<int:pk>/', views.order_item_edit, name='order_item_edit'),  # URL for editing an order item
    path('order-item-delete/<int:order_item_id>/', views.order_item_delete, name='order_item_delete'),

    
    path('wastage-list/', views.wastage_list, name='wastage_list'),
    path('wastage-report/', views.wastage_report, name='wastage_report'),  # For creating wastage
    path('wastage-report/<str:wastage_id>/', views.wastage_report, name='edit_wastage'),  # For editing wastage
    path('delete-wastage/<str:wastage_id>/', views.delete_wastage, name='delete_wastage'),  # For deleting wastage
]