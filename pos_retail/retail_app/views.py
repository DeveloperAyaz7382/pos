
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item_Type ,CompanyInfo,SalesmanInfo,Products , Stock,StockTracking, StockExpiry,Order,OrderItem,Wastage
from .forms import CompanyInfoForm
from django.contrib import messages


def home(request):
    return render(request, 'home.html')
# List view
# def item_type_list(request):
#     item_types = Item_Type.objects.all()
#     return render(request, 'item_type_list.html', {'item_types': item_types})

# # Create view
# def item_type_create(request):
#     if request.method == 'POST':
#         # type_id = request.POST['type_id']
#         type_name = request.POST['type_name']
#         type_description = request.POST['type_description']
#         Item_Type.objects.create(type_name=type_name, type_description=type_description)
#         return redirect('item_type_list')
#     return render(request, 'item_type_form.html')

# # Update view
# def item_type_update(request, id):
#     item_type = get_object_or_404(Item_Type, type_id=id)
#     if request.method == 'POST':
#         item_type.type_name = request.POST['type_name']
#         item_type.type_description = request.POST['type_description']
#         item_type.save()
#         return redirect('item_type_list')
#     return render(request, 'item_type_form.html', {'item_type': item_type})

# # Delete view
# def item_type_delete(request, id):
#     item_type = get_object_or_404(Item_Type, type_id=id)
#     if request.method == 'POST':
#         item_type.delete()
#         return redirect('item_type_list')
#     return render(request, 'item_type_confirm_delete.html', {'item_type': item_type})





# List all item types
def item_type_list(request):
    item_types = Item_Type.objects.all()
    return render(request, 'item_type_list.html', {'item_types': item_types})

# Create a new item type
def item_type_create(request):
    if request.method == 'POST':
        type_name = request.POST.get('type_name')
        type_description = request.POST.get('type_description')

        if type_name:  # Ensure type_name is provided
            Item_Type.objects.create(type_name=type_name, type_description=type_description)
            return redirect('item_type_list')
        
    return render(request, 'item_type_form.html', {'action': 'Create'})

# Update an item type
def item_type_update(request, pk):
    item_type = get_object_or_404(Item_Type, pk=pk)

    if request.method == 'POST':
        item_type.type_name = request.POST.get('type_name', item_type.type_name)
        item_type.type_description = request.POST.get('type_description', item_type.type_description)
        item_type.save()
        return redirect('item_type_list')

    return render(request, 'item_type_form.html', {'item_type': item_type, 'action': 'Update'})

# Delete an item type
def item_type_delete(request, pk):
    item_type = get_object_or_404(Item_Type, pk=pk)

    if request.method == 'POST':
        item_type.delete()
        return redirect('item_type_list')

    return render(request, 'item_type_confirm_delete.html', {'item_type': item_type})

# CREATE: Add a new company
def companyinfo_create(request):
    if request.method == 'POST':
        form = CompanyInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('companyinfo_list')  # Redirect to the company list page
    else:
        form = CompanyInfoForm()
    return render(request, 'companyinfo_form.html', {'form': form})

# READ: List all companies
def companyinfo_list(request):
    companies = CompanyInfo.objects.all()  # Get all companies
    return render(request, 'companyinfo_list.html', {'companies': companies})

# UPDATE: Edit a company
def companyinfo_update(request, id):
    company = get_object_or_404(CompanyInfo, company_id=id)
    if request.method == 'POST':
        form = CompanyInfoForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('companyinfo_list')  # Redirect to the company list page
    else:
        form = CompanyInfoForm(instance=company)
    return render(request, 'companyinfo_form.html', {'form': form, 'company': company})

# DELETE: Delete a company
def companyinfo_delete(request, id):
    company = get_object_or_404(CompanyInfo, company_id=id)
    if request.method == 'POST':
        company.delete()
        return redirect('companyinfo_list')  # Redirect to the company list page
    return render(request, 'companyinfo_confirm_delete.html', {'company': company})


def salesman_list(request):
       # Fetch all salesmen
    salesmen = SalesmanInfo.objects.all()
    
    # Loop through salesmen to manually fetch their related company
    for salesman in salesmen:
        salesman.company = CompanyInfo.objects.get(company_id=salesman.company_id)

    return render(request, 'salesman_list.html', {'salesmen': salesmen})

def create_salesman(request, company_id):
    company = get_object_or_404(CompanyInfo, company_id=company_id)
    salesmen = SalesmanInfo.objects.select_related('company').all()

    if request.method == 'POST':
        salesman_name = request.POST.get('salesman_name')
        salesman_contact = request.POST.get('salesman_contact')

        if salesman_name and salesman_contact:
            SalesmanInfo.objects.create(
                salesman_name=salesman_name,
                salesman_contact=salesman_contact,
                company=company
            )
            messages.success(request, f"Salesman added successfully to {company.company_name}.")
            return redirect('salesman_list')

        messages.error(request, "All fields are required.")

    return render(request, 'create_salesman.html', {'company': company, 'salesmen': salesmen})


# def create_salesman(request, company_id):
#        # Fetch all salesmen
#     salesmen = Salesman.objects.all()
    
#     # Loop through salesmen to manually fetch their related company
#     for salesman in salesmen:
#         salesman.company = CompanyInfo.objects.get(company_id=salesman.company_id)
#     company = get_object_or_404(CompanyInfo, company_id=company_id)

#     if request.method == 'POST':
#         salesman_name = request.POST.get('salesman_name')
#         salesman_contact = request.POST.get('salesman_contact')

#         if salesman_name and salesman_contact:
#             Salesman.objects.create(
#                 salesman_name=salesman_name,
#                 salesman_contact=salesman_contact,
#                 company_id=company.company_id
#             )
#             # messages.success(request, f"{company.company_name}.")
#             return redirect('salesman_list')  # Replace with the actual list view URL

#         messages.error(request, "All fields are required.")

#     return render(request, 'create_salesman.html', {'company': company , 'salesmen': salesmen})



def edit_salesman(request, salesman_id):
    salesman = get_object_or_404(SalesmanInfo, salesman_id=salesman_id)

    if request.method == 'POST':
        salesman_name = request.POST.get('salesman_name')
        salesman_contact = request.POST.get('salesman_contact')

        if salesman_name and salesman_contact:
            salesman.salesman_name = salesman_name
            salesman.salesman_contact = salesman_contact
            salesman.save()
            messages.success(request)
            return redirect('salesman_list')  # Replace with your actual list view URL name

        messages.error(request, "All fields are required.")

    return render(request, 'edit_salesman.html', {'salesman': salesman})


def delete_salesman(request, salesman_id):
    salesman = get_object_or_404(SalesmanInfo, salesman_id=salesman_id)

    if request.method == 'POST':
        salesman.delete()
        messages.success(request, "Salesman deleted successfully.")
        return redirect('salesman_list')  # Replace with your actual list view URL name

    return render(request, 'delete_salesman.html', {'salesman': salesman})


def inventory_list(request):
    items = Products.objects.all()
    return render(request, 'inventory_list.html', {'items': items})

def inventory_form_view(request, inventory_id=None):
    # If editing, fetch the existing inventory; otherwise, set inventory to None
    inventory = None
    if inventory_id:
        inventory = get_object_or_404(Products, item_id=inventory_id)

    if request.method == 'POST':
        # Retrieve form data
        item_name = request.POST.get('item_name')
        type_id = request.POST.get('type_id')
        company_id = request.POST.get('company_id')
        # item_status = request.POST.get('item_status')

        # Validation: Ensure all required fields are filled
        if not item_name or not type_id or not company_id not in []:
            messages.error(request, 'All fields are required and must be valid.')
            return render(request, 'inventory_form.html', {
                'inventory': inventory,
                'types': Item_Type.objects.all(),
                'companies': CompanyInfo.objects.all(),
            })

        if inventory:
            # Update existing inventory
            inventory.item_name = item_name
            inventory.type_id_id = type_id
            inventory.company_id_id = company_id
            # inventory.item_status = item_status
            inventory.save()
            messages.success(request, 'Inventory item updated successfully.')
        else:
            # Create a new inventory
            Products.objects.create(
                item_name=item_name,
                type_id_id=type_id,
                company_id_id=company_id,
                # item_status=item_status,
            )
            # messages.success(request, 'Inventory item created successfully.')
            
            

        return redirect('inventory_list')
    

    # Fetch data for dropdowns
    items = Products.objects.all()  # Fetch all inventory items for the list
    types = Item_Type.objects.all()
    companies = CompanyInfo.objects.all()

    return render(request, 'inventory_form.html', {
        'inventory': inventory,
        'items': items,
        'types': types,
        'companies': companies,
    })

    
def delete_inventory(request, item_id):
    item = get_object_or_404(Products, pk=item_id)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Inventory item successfully deleted.')
        return redirect('inventory_list')  # Redirect to your inventory list view
    return render(request, 'delete_inventory.html', {'item': item})



def stock_form_view(request):
    inventory_items = Products.objects.all()
    salesmen = SalesmanInfo.objects.all()

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        salesman_id = request.POST.get('salesman_id')
        stock_quantity = int(request.POST.get('stock_quantity'))
        stock_unitprice = float(request.POST.get('stock_unitprice'))

        # Create a new Stock entry
        item = Products.objects.get(item_id=item_id)
        salesman = SalesmanInfo.objects.get(salesman_id=salesman_id)
        Stock.objects.create(
            item=item,
            salesman=salesman,
            stock_quantity=stock_quantity,
            stock_unitprice=stock_unitprice
        )
        return redirect('stock_list')

    context = {
        'inventory_items': inventory_items,
        'salesmen': salesmen,
    }
    return render(request, 'stock_form.html', context)


def stock_list_view(request):
    stocks = Stock.objects.all()
    context = {'stocks': stocks}
    return render(request, 'stock_list.html', context)



# Edit View
def stock_edit_view(request, stock_id):
    stock = get_object_or_404(Stock, stock_id=stock_id)
    inventory_items = Products.objects.all()
    salesmen = SalesmanInfo.objects.all()

    if request.method == 'POST':
        stock.item = Products.objects.get(item_id=request.POST.get('item_id'))
        stock.salesman = SalesmanInfo.objects.get(salesman_id=request.POST.get('salesman_id'))
        stock.stock_quantity = int(request.POST.get('stock_quantity'))
        stock.stock_unitprice = float(request.POST.get('stock_unitprice'))
        stock.save()
        return redirect('stock_list')

    context = {
        'stock': stock,
        'inventory_items': inventory_items,
        'salesmen': salesmen,
    }
    return render(request, 'stock_edit.html', context)

# Delete View
def stock_delete_view(request, stock_id):
    stock = get_object_or_404(Stock, stock_id=stock_id)
    if request.method == 'POST':
        stock.delete()
        return redirect('stock_list')
    return render(request, 'stock_delete.html', {'stock': stock})


def stock_tracking_list_view(request):
    trackings = StockTracking.objects.all()
    context = {'trackings': trackings}
    return render(request, 'stock_tracking_list.html', context)

def stock_tracking_form_view(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        stock_in = int(request.POST.get('tracking_stock_in', 0))
        stock_out = int(request.POST.get('tracking_stock_out', 0))
        current_stock = int(request.POST.get('tracking_current_stock'))
        remarks = request.POST.get('tracking_remarks', '')

        StockTracking.objects.create(
            item_id=item_id,
            tracking_stock_in=stock_in,
            tracking_stock_out=stock_out,
            tracking_current_stock=current_stock,
            tracking_remarks=remarks
        )
        return redirect('stock_tracking_list')

    items = Products.objects.all()
    return render(request, 'stock_tracking_form.html', {'items': items})

def stock_tracking_edit_view(request, tracking_id):
    tracking = get_object_or_404(StockTracking, tracking_id=tracking_id)

    if request.method == 'POST':
        tracking.item_id = request.POST.get('item_id')
        tracking.tracking_stock_in = int(request.POST.get('tracking_stock_in', 0))
        tracking.tracking_stock_out = int(request.POST.get('tracking_stock_out', 0))
        tracking.tracking_current_stock = int(request.POST.get('tracking_current_stock'))
        tracking.tracking_remarks = request.POST.get('tracking_remarks', '')
        tracking.save()
        return redirect('stock_tracking_list')

    items = Products.objects.all()
    return render(request, 'stock_tracking_edit.html', {'tracking': tracking, 'items': items})

def stock_tracking_delete_view(request, tracking_id):
    tracking = get_object_or_404(StockTracking, tracking_id=tracking_id)
    if request.method == 'POST':
        tracking.delete()
        return redirect('stock_tracking_list')
    return render(request, 'stock_tracking_delete.html', {'tracking': tracking})



# List all stock expiry records
def stock_expiry_list_view(request):
    expiries = StockExpiry.objects.all()
    context = {'expiries': expiries}
    return render(request, 'stock_expiry_list.html', context)

# Create a new stock expiry record
def stock_expiry_form_view(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        manufacture_date = request.POST.get('manufacture_date')
        expiry_date = request.POST.get('expiry_date')
        quantity_expiry = request.POST.get('quantity_expiry')
        expiry_status = request.POST.get('expiry_status', 1)

        # Create a new StockExpiry record
        StockExpiry.objects.create(
            item_id=item_id,
            manufacture_date=manufacture_date,
            expiry_date=expiry_date,
            quantity_expiry=quantity_expiry,
            expiry_status=expiry_status
        )
        return redirect('stock_expiry_list')

    items = Products.objects.all()
    return render(request, 'stock_expiry_form.html', {'items': items})

# Edit an existing stock expiry record
def stock_expiry_edit_view(request, expiry_id):
    expiry = get_object_or_404(StockExpiry, expiry_id=expiry_id)
    
    if request.method == 'POST':
        expiry.item_id = request.POST.get('item_id')
        expiry.manufacture_date = request.POST.get('manufacture_date')
        expiry.expiry_date = request.POST.get('expiry_date')
        expiry.quantity_expiry = request.POST.get('quantity_expiry')
        expiry.expiry_status = request.POST.get('expiry_status', 1)
        expiry.save()
        return redirect('stock_expiry_list')

    items = Products.objects.all()
    return render(request, 'stock_expiry_form.html', {'expiry': expiry, 'items': items})

# Delete a stock expiry record
def stock_expiry_delete_view(request, expiry_id):
    expiry = get_object_or_404(StockExpiry, expiry_id=expiry_id)
    if request.method == 'POST':
        expiry.delete()
        return redirect('stock_expiry_list')
    return render(request, 'stock_expiry_delete.html', {'expiry': expiry})



# List all orders
def order_list_view(request):
    orders = Order.objects.all()  # Fetch all orders
    context = {'orders': orders}
    return render(request, 'order_list.html', context)


# Create a new order
def order_form(request):
    items = Products.objects.all()  # Get all items to populate the item dropdown
    if request.method == 'POST':
        customer_name = request.POST.get('order_customer_name')  # Retrieve the customer name
        order_date = request.POST.get('order_date')
        total_amount = request.POST.get('total_amount')
        payment_status = request.POST.get('order_payment_status')
        order_status = request.POST.get('order_status')
        order_remarks = request.POST.get('order_remarks')

        if not customer_name:
            # Handle the case where customer_name is empty
            return render(request, 'order_form.html', {'items': items, 'error': 'Customer name is required'})

        # Create a new Order record
        Order.objects.create(
            order_customer_name=customer_name,
            order_date=order_date,
            total_amount=total_amount,
            order_payment_status=payment_status,
            order_status=order_status,
            order_remarks=order_remarks
        )
        return redirect('order_list')  # Redirect to the order list

    return render(request, 'order_form.html', {'items': items})

# Edit an existing order
def order_edit_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    items = Products.objects.all()  # Get all items for the dropdown
    if request.method == 'POST':
        order.order_customer_name = request.POST.get('order_customer_name')
        order.order_date = request.POST.get('order_date')
        order.total_amount = request.POST.get('total_amount')
        order.order_payment_status = request.POST.get('order_payment_status')
        order.order_status = request.POST.get('order_status')
        order.order_remarks = request.POST.get('order_remarks')
        order.save()
        return redirect('order_list')

    return render(request, 'order_form.html', {'order': order, 'items': items})

# Delete an order
def order_delete_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')  # Redirect to the order list
    return render(request, 'order_delete.html', {'order': order})


# List all order items
def order_item_list(request):
    order_items = OrderItem.objects.all()
    return render(request, 'order_item_list.html', {'order_items': order_items})

# # Add a new order item or edit an existing one
# def order_item_form(request, pk=None):
#     """
#     Handles both adding a new order item and editing an existing one.
#     If `pk` is provided, it edits the corresponding OrderItem; otherwise, it creates a new one.
#     """
#     if pk:
#         # Edit mode: fetch the existing OrderItem
#         order_item = get_object_or_404(OrderItem, pk=pk)
#     else:
#         # Add mode: no OrderItem exists
#         order_item = None

#     if request.method == 'POST':
#         # Fetch form data
#         order_id = request.POST.get('order_id')
#         item_id = request.POST.get('item_id')
#         order_item_quantity = request.POST.get('order_item_quantity')
#         order_item_unitprice = request.POST.get('order_item_unitprice')

#         # Fetch related model instances
#         order = get_object_or_404(Order, pk=order_id)
#         item = get_object_or_404(Inventory, pk=item_id)

#         if order_item:
#             # Update the existing OrderItem
#             order_item.order = order
#             order_item.item = item
#             order_item.order_item_quantity = order_item_quantity
#             order_item.order_item_unitprice = order_item_unitprice
#             order_item.save()
#         else:
#             # Create a new OrderItem
#             OrderItem.objects.create(
#                 order=order,
#                 item=item,
#                 order_item_quantity=order_item_quantity,
#                 order_item_unitprice=order_item_unitprice
#             )

#         return redirect('order_item_list')  # Redirect to the order item list view

#     # Fetch orders and items for the form
#     orders = Order.objects.all()
#     items = Inventory.objects.all()

#     # Render the form template
#     return render(request, 'order_item_form.html', {
#         'order_item': order_item,
#         'orders': orders,
#         'items': items,
#     })


def order_item_form(request, pk=None):
    if pk:
        # Edit mode: fetch the existing OrderItem
        order_item = get_object_or_404(OrderItem, pk=pk)
    else:
        # Add mode: no OrderItem exists
        order_item = None

    if request.method == 'POST':
        # Fetch form data
        order_id = request.POST.get('order_id')
        item_id = request.POST.get('item_id')
        order_item_quantity = request.POST.get('order_item_quantity')
        order_item_unitprice = request.POST.get('order_item_unitprice')

        # Fetch related model instances
        order = get_object_or_404(Order, pk=order_id)
        item = get_object_or_404(Products, pk=item_id)

        if order_item:
            # Update the existing OrderItem
            order_item.order = order
            order_item.item = item
            order_item.order_item_quantity = order_item_quantity
            order_item.order_item_unitprice = order_item_unitprice
            order_item.save()
        else:
            # Create a new OrderItem
            OrderItem.objects.create(
                order=order,
                item=item,
                order_item_quantity=order_item_quantity,
                order_item_unitprice=order_item_unitprice
            )

        return redirect('order_item_list')  # Redirect to the order item list view

    # Fetch orders and items for the form
    orders = Order.objects.all()
    items = Products.objects.all()

    return render(request, 'order_item_form.html', {
        'order_item': order_item,
        'orders': orders,
        'items': items,
    })
    
    
# Edit an existing order item
def order_item_edit(request, pk):
    order_item = get_object_or_404(OrderItem, pk=pk)

    if request.method == 'POST':
        # Manually update the order item with data from POST request
        order_item.order_item_quantity = request.POST.get('order_item_quantity', order_item.order_item_quantity)
        order_item.order_item_unitprice = request.POST.get('order_item_unitprice', order_item.order_item_unitprice)
        order_item.save()

        # Redirect to order item list page after saving the changes
        return redirect('order_item_list')

    return render(request, 'order_item_edit.html', {'order_item': order_item})

def order_item_delete(request, order_item_id):
    # Use `order_item_id` instead of `id`
    order_item = get_object_or_404(OrderItem, order_item_id=order_item_id)

    if request.method == 'POST':
        # Delete the order item after confirmation
        order_item.delete()
        return redirect('order_item_list')  # Redirect to the order item list after deletion

    return render(request, 'order_item_delete_confirm.html', {'order_item': order_item})

def wastage_list(request):
    # Retrieve all wastage records from the database
    wastages = Wastage.objects.all()
    
    # Render the template and pass the wastages to the context
    return render(request, 'wastage_list.html', {'wastages': wastages})


# def wastage_report(request, wastage_id):
#     # Retrieve the wastage object based on the wastage_id
#     wastage = get_object_or_404(Wastage, wastage_id=wastage_id)
    
#     if request.method == 'POST':
#         # Retrieve data from POST
#         item_id = request.POST.get('item_id')  # Ensure you are getting the item_id field
#         if not item_id:
#             # If item_id is missing or empty, you can handle the error appropriately
#             return render(request, 'error.html', {'error_message': 'Item ID is required.'})
        
#         # Retrieve other fields as needed
#         quantity_ordered = request.POST.get('quantity_ordered')
#         quantity_received = request.POST.get('quantity_received')
#         quantity_wasted = request.POST.get('quantity_wasted')
#         reason_for_wastage = request.POST.get('reason_for_wastage')
#         return_status = request.POST.get('return_status')
#         remarks = request.POST.get('remarks')

#         # Fetch the Inventory object by item_id
#         item = Inventory.objects.get(item_id=item_id)

#         # Create or update Wastage record
#         Wastage.objects.create(
#             item=item,
#             quantity_ordered=quantity_ordered,
#             quantity_received=quantity_received,
#             quantity_wasted=quantity_wasted,
#             reason_for_wastage=reason_for_wastage,
#             return_status=return_status,
#             remarks=remarks
#         )

#         return redirect('wastage_list')  # Redirect after saving
#     else:
#         # GET request: pass context data, like the available items
#         items = Inventory.objects.all()
#         return render(request, 'wastage_report.html', {'items': items} , {'wastage': wastage})
def wastage_report(request, wastage_id=None):
    if request.method == 'POST':
        # Handling POST request to create or update a wastage record
        item_id = request.POST.get('item_id')
        quantity_ordered = request.POST.get('quantity_ordered')
        quantity_received = request.POST.get('quantity_received')
        quantity_wasted = request.POST.get('quantity_wasted')
        reason_for_wastage = request.POST.get('reason_for_wastage')
        return_status = request.POST.get('return_status')
        remarks = request.POST.get('remarks')

        # Validate the required fields
        if not all([item_id, quantity_ordered, quantity_received, quantity_wasted, reason_for_wastage, return_status]):
            return render(request, 'wastage_report.html', {
                'error': 'All fields are required.',
                'items': Products.objects.all(),
            })

        # If we have a `wastage_id`, we are editing an existing record
        if wastage_id:
            wastage = get_object_or_404(Wastage, pk=wastage_id)
            wastage.item_id = item_id
            wastage.quantity_ordered = quantity_ordered
            wastage.quantity_received = quantity_received
            wastage.quantity_wasted = quantity_wasted
            wastage.reason_for_wastage = reason_for_wastage
            wastage.return_status = return_status
            wastage.remarks = remarks
            wastage.save()
        else:
            # If `wastage_id` is None, we are creating a new record
            Wastage.objects.create(
                item_id=item_id,
                quantity_ordered=quantity_ordered,
                quantity_received=quantity_received,
                quantity_wasted=quantity_wasted,
                reason_for_wastage=reason_for_wastage,
                return_status=return_status,
                remarks=remarks,
            )

        return redirect('wastage_list')  # Redirect to the wastage list after saving the data

    # If it's a GET request, render the form with the existing data if `wastage_id` is provided
    if wastage_id:
        wastage = get_object_or_404(Wastage, pk=wastage_id)
        context = {
            'wastage': wastage,
            'items': Products.objects.all(),
        }
    else:
        context = {
            'items': Products.objects.all(),
        }

    return render(request, 'wastage_report.html', context)

def delete_wastage(request, wastage_id):
    wastage = get_object_or_404(Wastage, wastage_id=wastage_id)

    if request.method == 'POST':
        wastage.delete()
        return redirect('wastage_list')  # Redirect to the success page after deletion

    return render(request, 'delete_wastage.html', {'wastage': wastage})