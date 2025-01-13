from django import forms
from .models import CompanyInfo, SalesmanInfo,Products


class CompanyInfoForm(forms.ModelForm):
    class Meta:
        model = CompanyInfo
        fields = ['company_name', 'company_contact', 'company_email', 'company_address']




class SalesmanForm(forms.ModelForm):
    # Use a ModelChoiceField to select the company by name
    company = forms.ModelChoiceField(queryset=CompanyInfo.objects.all(), to_field_name='company_id', empty_label="Choose a Company")

    class Meta:
        model = SalesmanInfo
        fields = ['salesman_name', 'salesman_contact', 'company']  # Display the company field by name
        
        
class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['item_name', 'type_id', 'company_id', 'item_status']
        widgets = {
            'item_status': forms.Select(choices=Products.ITEM_STATUS_CHOICES),
        }

