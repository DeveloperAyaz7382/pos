from django.urls import path
from . import views

urlpatterns = [


    path('', views.home, name='home'),
    
    path('item_types/', views.itemtypelist, name='itemtypelist'),
    path('item-types/create/', views.item_type_create, name='item_type_create'),
    path('item-types/edit/<int:pk>/', views.edit_itemtype, name='edit_itemtype'),
    path('item_type/delete/<int:pk>/', views.delete_itemtype, name='delete_itemtype'),
   
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
    # path('order-item-form/', views.order_item_form, name='order_item_add'),  # URL for adding an order item
    path('add_order/', views.add_order, name='add_order'),  # URL for adding an order item
    path('edit_order/<int:pk>/', views.edit_order, name='edit_order'),
   path('order-item/delete/<int:order_item_id>/', views.delete_order_item, name='delete_order_item'),
   # OrderReturn URLs
    path('order-returns/', views.order_return_list, name='order_return_list'),
    path('order-returns/add/', views.add_order_return, name='add_order_return'),
    path('order-returns/<int:pk>/edit/', views.edit_order_return, name='edit_order_return'),
    path('order-returns/<int:pk>/delete/', views.delete_order_return, name='delete_order_return'),

    # CompanyReturn URLs
    # path('company-returns/', views.company_return_list, name='company_return_list'),
    # path('company-returns/add/', views.add_company_return, name='add_company_return'),
    # path('company-returns/<int:pk>/edit/', views.edit_company_return, name='edit_company_return'),
    # path('company-returns/<int:pk>/delete/', views.delete_company_return, name='delete_company_return'),
]