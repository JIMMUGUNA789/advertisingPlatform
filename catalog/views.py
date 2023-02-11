from django.shortcuts import render, redirect

from companies.models import CompanyProfile, Follows, Likes, Reviews
from .models import Catalog, CatalogItem, CatalogCategory
from django.contrib import messages
from django.urls import reverse, reverse_lazy





def createCatalog(request, company_id):
    company_id = str(company_id)
    company = CompanyProfile.objects.get(id=company_id)
    if request.method == 'POST':
        catalog = Catalog()
        catalog.company = company
        catalog.name = request.POST['name']
        catalog.description = request.POST['description']
        catalog.save()
        messages.success(request, 'Catalog created successfully')
        return redirect(reverse('businessDetailDashboard', kwargs={'company_id':company_id}))
        
    context = {
        "company": company,

    }
    return render(request, 'catalog/createCatalog.html', context)

def deleteCatalog(request, catalog_id):
    catalog_id = str(catalog_id)
    catalog = Catalog.objects.get(id=catalog_id)
    company_id = catalog.company.id
    catalog.delete()
    messages.success(request, 'Catalog deleted successfully')
    return redirect(reverse('businessDetailDashboard', kwargs={'company_id':company_id}))