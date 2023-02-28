from django.shortcuts import render, redirect

from companies.models import CompanyProfile, Follows, Likes, Reviews
from .models import Catalog, CatalogItem, CatalogCategory
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from advertisements.models import Ad





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

def manageCatalog(request, catalog_id):
    catalog_id = str(catalog_id)
    catalog = Catalog.objects.get(id=catalog_id)
    company_id = catalog.company.id
    company = CompanyProfile.objects.get(id=company_id)
    categories = CatalogCategory.objects.filter(catalog=catalog_id)
    catalogItems = CatalogItem.objects.filter(catalog=catalog_id)
    context = {
        "company": company,
        "catalog": catalog,
        "categories":categories,
        "catalogItems":catalogItems,

    }
    return render(request, 'catalog/manageCatalog.html', context)

def createCatalogCategory(request, catalog_id):
    catalog_id = str(catalog_id)
    catalog = Catalog.objects.get(id=catalog_id)
    company_id = catalog.company.id
    company = CompanyProfile.objects.get(id=company_id)
    if request.method == 'POST':
        category = CatalogCategory()
        category.catalog = catalog
        category.name = request.POST['name']
        category.description = request.POST['description']
        category.save()
        messages.success(request, 'Category created successfully')
        return redirect(reverse('manageCatalog', kwargs={'catalog_id':catalog_id}))
        
    context = {
        "company": company,
        "catalog": catalog,

    }
    return render(request, 'catalog/createCatalogCategory.html', context)

def deleteCatalogCategory(request, category_id):
    category_id = str(category_id)
    category = CatalogCategory.objects.get(id=category_id)
    catalog_id = category.catalog.id
    category.delete()
    messages.success(request, 'Category deleted successfully')
    return redirect(reverse('manageCatalog', kwargs={'catalog_id':catalog_id}))

def createCatalogItem(request, catalog_id, category_id):
    catalog_id = str(catalog_id)
    category_id = str(category_id)
    catalog = Catalog.objects.get(id=catalog_id)
    company_id = catalog.company.id
    company = CompanyProfile.objects.get(id=company_id)
    category = CatalogCategory.objects.get(id=category_id)
    if request.method == 'POST':
        item = CatalogItem()
        item.catalog = catalog
        item.category = category
        item.name = request.POST['name']
        item.description = request.POST['description']
        item.price = request.POST['price']
        item.image = request.FILES['image']
        item.save()
        messages.success(request, 'Item created successfully')
        return redirect(reverse('manageCatalog', kwargs={'catalog_id':catalog_id}))
        
    context = {
        "company": company,
        "catalog": catalog,
        "category": category,
    }
    return render(request, 'catalog/createCatalogItem.html', context)

def deleteCatalogItem(request, item_id):
    item_id = str(item_id)
    item = CatalogItem.objects.get(id=item_id)
    catalog_id = item.catalog.id
    item.delete()
    messages.success(request, 'Item deleted successfully')
    return redirect(reverse('manageCatalog', kwargs={'catalog_id':catalog_id}))

def viewCompanyCatalog(request, company_id):
    company_id = str(company_id)
    ads = Ad.objects.filter(adStatus='Active')
    company = CompanyProfile.objects.get(id=company_id)
    context ={
        "company": company,
        "ads": ads,
    }
    if Catalog.objects.filter(company=company_id).exists():
        catalog = Catalog.objects.get(company=company_id)
        categories = CatalogCategory.objects.filter(catalog=catalog.id)
        catalogItems = CatalogItem.objects.filter(catalog=catalog.id)
        context = {
            "company": company,
            "catalog": catalog,
            "categories":categories,
            "catalogItems":catalogItems,
            "ads": ads,

        }
    
    return render(request, 'catalog/viewCompanyCatalog.html', context)