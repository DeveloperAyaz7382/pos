import datetime
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item_Type ,CompanyInfo,SalesmanInfo,Products , Stock,StockTracking, StockExpiry,Order,OrderItem 
from .forms import CompanyInfoForm
from django.contrib import messages
from .models import OrderReturn
from datetime import datetime



def home(request):
    return render(request, 'home.html')

# List all item types
def itemtypelist(request):
    item_types = Item_Type.objects.all()
    return render(request, 'itemtypelist.html', {'item_types': item_types})

# Create a new item type
def item_type_create(request):
    if request.method == 'POST':
        type_name = request.POST.get('type_name')
        type_description = request.POST.get('type_description')

        if type_name:  # Ensure type_name is provided
            Item_Type.objects.create(type_name=type_name, type_description=type_description)
            return redirect('itemtypelist')
        
    return render(request, 'item_type_form.html', {'action': 'Create'})

# Update an item type
def edit_itemtype(request, pk):
    # Retrieve the item type or return a 404 if not found
    item_type = get_object_or_404(Item_Type, pk=pk)

    if request.method == 'POST':
        # Get data from the request
        type_name = request.POST.get('type_name')
        type_description = request.POST.get('type_description')

        # Validate inputs
        if not type_name or not type_description:
            messages.error(request, "Type name and description are required.")
            return render(request, 'edititemtype.html', {'item_type': item_type, 'action': 'Update'})

        # Update the fields and save
        item_type.type_name = type_name
        item_type.type_description = type_description
        item_type.save()

        # Provide success feedback
        messages.success(request, "Item type updated successfully.")
        return redirect('itemtypelist')  # Redirect to the item type list page

    # Render the form with the current data for GET request
    return render(request, 'edit_itemtype.html', {'item_type': item_type, 'action': 'Update'})

def delete_itemtype(request, pk=None):
    if pk is None:
        return JsonResponse({'error': 'Invalid ID provided'}, status=400)
    
    item_type = get_object_or_404(Item_Type, pk=pk)

    if request.method == 'POST':
        item_type.delete()
        return redirect('itemtypelist')  # Redirect to the list page after deletion

    return render(request, 'delete_itemtype.html', {'item_type': item_type})

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
        item_formula = request.POST.get('item_formula')
        item_price= float(request.POST.get('item_price'))
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
            inventory.item_formula = item_formula
            inventory.item_price = item_price
            inventory.type_id_id = type_id
            inventory.company_id_id = company_id
            # inventory.item_status = item_status
            inventory.save()
            messages.success(request, 'Inventory item updated successfully.')
        else:
            # Create a new inventory
            Products.objects.create(
                item_name=item_name,
                item_formula=item_formula,
                item_price=item_price,
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
    stocks = Stock.objects.all()

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
        return redirect('stock_form')

    context = {
        'inventory_items': inventory_items,
        'salesmen': salesmen,
        'stocks':stocks,
        
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
        return redirect('stock_tracking_form')

    items = Products.objects.all()
    trackings = StockTracking.objects.all()
    return render(request, 'stock_tracking_form.html', {'items': items,'trackings': trackings})

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
        return redirect('stock_expiry_form')
    

    items = Products.objects.all()
    expiries = StockExpiry.objects.all()
    return render(request, 'stock_expiry_form.html', {'items': items,'expiries': expiries})

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
        return redirect('stock_expiry_form')

    items = Products.objects.all()
    return render(request, 'stock_expiry_form.html', {'expiry': expiry, 'items': items})

# Delete a stock expiry record
def stock_expiry_delete_view(request, expiry_id):
    expiry = get_object_or_404(StockExpiry, expiry_id=expiry_id)
    if request.method == 'POST':
        expiry.delete()
        return redirect('stock_expiry_form')
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



def order_item_form(request, pk=None):
    if pk:
        # Edit mode: fetch the existing OrderItem
        order_item = get_object_or_404(OrderItem, pk=pk)
    else:
        # Add mode: no OrderItem exists
        order_item = None

    if request.method == 'POST':
        # Fetch form data
        order_customer_name = request.POST.get('order_customer_name')
        order_date = request.POST.get('order_date')
        order_payment_status = request.POST.get('order_payment_status')
        item_id = request.POST.get('item_id')
        order_item_quantity = request.POST.get('order_item_quantity')
        order_item_unitprice = request.POST.get('order_item_unitprice')
        order_item_discount = request.POST.get('order_item_discount')
        order_item_description = request.POST.get('order_item_description')

        # Fetch related model instances
        item = get_object_or_404(Products, pk=item_id)

        if order_item:
            # Update the existing OrderItem
            order_item.order_customer_name = order_customer_name
            order_item.order_date = order_date
            order_item.order_payment_status = order_payment_status
            order_item.item = item
            order_item.order_item_quantity = order_item_quantity
            order_item.order_item_unitprice = order_item_unitprice
            order_item.order_item_discount = order_item_discount
            order_item.order_item_description = order_item_description
            order_item.save()
        else:
            # Create a new OrderItem
            OrderItem.objects.create(
                order_customer_name=order_customer_name,
                order_date=order_date,
                order_payment_status=order_payment_status,
                item=item,
                order_item_quantity=order_item_quantity,
                order_item_unitprice=order_item_unitprice,
                order_item_discount=order_item_discount,
                order_item_description=order_item_description
            )

        return redirect('order_item_list')  # Redirect to the order item list view

    # Fetch items for the form
    items = Products.objects.all()

    return render(request, 'order_item_form.html', {
        'order_item': order_item,
        'items': items,
    })


def add_order(request, pk=None):
    # Fetch the existing order item if pk is provided
    order_item = get_object_or_404(OrderItem, pk=pk) if pk else None

    if request.method == 'POST':
        try:
            # Extract data from the request
            order_customer_name = request.POST['order_customer_name']
            order_date = request.POST['order_date']
            order_payment_status = request.POST['order_payment_status']
            item_id = int(request.POST['item_id'])
            order_item_quantity = int(request.POST['order_item_quantity'])
            order_item_unitprice = float(request.POST['order_item_unitprice'])
            order_item_discount = float(request.POST['order_item_discount'])
            order_item_description = request.POST['order_item_description']

            # Fetch related product
            item = get_object_or_404(Products, pk=item_id)

            # Update or create the OrderItem
            if order_item:
                order_item.order_customer_name = order_customer_name
                order_item.order_date = order_date
                order_item.order_payment_status = order_payment_status
                order_item.item = item
                order_item.order_item_quantity = order_item_quantity
                order_item.order_item_unitprice = order_item_unitprice
                order_item.order_item_discount = order_item_discount
                order_item.order_item_description = order_item_description
                order_item.save()
            else:
                OrderItem.objects.create(
                    order_customer_name=order_customer_name,
                    order_date=order_date,
                    order_payment_status=order_payment_status,
                    item=item,
                    order_item_quantity=order_item_quantity,
                    order_item_unitprice=order_item_unitprice,
                    order_item_discount=order_item_discount,
                    order_item_description=order_item_description
                )
            return redirect('add_order')
        except Exception as e:
            return render(request, 'add_order.html', {
                'order_item': order_item,
                'items': Products.objects.all(),
                'error': str(e)
            })

    # Render the form
    items = Products.objects.all()
    order_items = OrderItem.objects.all()
    return render(request, 'add_order.html', {'order_item': order_item, 'items': items ,'order_items': order_items })

    

def edit_order(request, pk):
    order_item = get_object_or_404(OrderItem, pk=pk)

    if request.method == 'POST':
        # Retrieve and safely update each field from POST data
        order_item.order_customer_name = request.POST.get('order_customer_name', order_item.order_customer_name)
        
        # Make sure the date is correctly formatted (assuming the input is in YYYY-MM-DD format)
        order_date = request.POST.get('order_date', order_item.order_date)
        if order_date:
            try:
                order_item.order_date = datetime.strptime(order_date, '%Y-%m-%d')
            except ValueError:
                pass  # Keep the original value if date is invalid
        
        try:
            order_item.order_item_quantity = int(request.POST.get('order_item_quantity', order_item.order_item_quantity))
        except (ValueError, TypeError):
            pass  # Keep the original value if conversion fails

        try:
            order_item.order_item_unitprice = float(request.POST.get('order_item_unitprice', order_item.order_item_unitprice))
        except (ValueError, TypeError):
            pass  # Keep the original value if conversion fails
        
        try:
            order_item.order_item_discount = float(request.POST.get('order_item_discount', order_item.order_item_discount))
        except (ValueError, TypeError):
            pass  # Keep the original value if conversion fails

        order_item.order_item_description = request.POST.get('order_item_description', order_item.order_item_description)
        order_item.order_payment_status = request.POST.get('order_payment_status', order_item.order_payment_status)

        # Save the updated order item
        order_item.save()

        # Redirect to order item list page after saving the changes
        return redirect('add_order')

    # Fetch all items for dropdowns or related fields if needed
    items = Products.objects.all()

    return render(request, 'edit_order.html', {
        'order_item': order_item,
        'items': items,
    })
    
    
def delete_order_item(request, order_item_id):
    order_item = get_object_or_404(OrderItem, pk=order_item_id)

    if request.method == 'POST':  # Ensure the method is POST
        order_item.delete()  # Perform the deletion
        return redirect('add_order')  # Redirect after successful deletion

    # If the request method is GET, display the confirmation page
    return render(request, 'order_item_delete_confirm.html', {'order_item': order_item})

# OrderReturn Views
def order_return_list(request):
    order_returns = OrderReturn.objects.all()
    return render(request, 'order_return_list.html', {'order_returns': order_returns})


def add_order_return(request):
    if request.method == 'POST':
        order_id = request.POST.get('order')
        return_reason = request.POST.get('return_reason')
        return_date = request.POST.get('return_date')
        order = get_object_or_404(Order, id=order_id)
        OrderReturn.objects.create(order=order, return_reason=return_reason, return_date=return_date)
        return redirect('order_return_list')
    orders = Order.objects.all()
   
    
    return render(request, 'add_order_return.html', {'orders': orders})


def edit_order_return(request, pk):
    order_return = get_object_or_404(OrderReturn, pk=pk)
    if request.method == 'POST':
        order_return.return_reason = request.POST.get('return_reason')
        order_return.return_date = request.POST.get('return_date')
        order_return.save()
        return redirect('order_return_list')
    return render(request, 'edit_order_return.html', {'order_return': order_return})


def delete_order_return(request, pk):
    order_return = get_object_or_404(OrderReturn, pk=pk)
    if request.method == 'POST':
        order_return.delete()
        return redirect('order_return_list')
    return render(request, 'delete_order_return.html', {'order_return': order_return})


# # CompanyReturn Views
# def company_return_list(request):
#     company_returns = CompanyReturn.objects.all()
#     return render(request, 'company_return_list.html', {'company_returns': company_returns})


# def add_company_return(request):
#     if request.method == 'POST':
#         company_id = request.POST.get('company')
#         return_reason = request.POST.get('return_reason')
#         return_date = request.POST.get('return_date')
#         company = get_object_or_404(CompanyInfo, id=company_id)
#         CompanyReturn.objects.create(company=company, return_reason=return_reason, return_date=return_date)
#         return redirect('company_return_list')
#     companies = CompanyInfo.objects.all()
#     return render(request, 'add_company_return.html', {'companies': companies})


# def edit_company_return(request, pk):
#     company_return = get_object_or_404(CompanyReturn, pk=pk)
#     if request.method == 'POST':
#         company_return.return_reason = request.POST.get('return_reason')
#         company_return.return_date = request.POST.get('return_date')
#         company_return.save()
#         return redirect('company_return_list')
#     return render(request, 'edit_company_return.html', {'company_return': company_return})


# def delete_company_return(request, pk):
#     company_return = get_object_or_404(CompanyReturn, pk=pk)
#     if request.method == 'POST':
#         company_return.delete()
#         return redirect('company_return_list')
#     return render(request, 'delete_company_return.html', {'company_return': company_return})
