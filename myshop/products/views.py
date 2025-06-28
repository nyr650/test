from django.shortcuts import render, get_object_or_404
from products.models import Product
from cart.forms import CartAddProductForm
from .models import Category

def home(request):
    return render(request, 'products/home.html')

def about(request):
    return render(request, 'products/about.html')

def contact(request):
    return render(request, 'products/contact.html')

def shop(request):
    return render(request, 'products/shop.html')

def product_detail(request):
    return render(request, 'products/single-product.html')

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})

def search(request):
    query = request.GET.get('q')
    results = []



    if query:
        results = Product.objects.filter(name__icontains=query)

    return render(request, 'products/search_results.html', {
        'query': query,
        'results': results
    })

def products_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'products/products_by_category.html', {
        'category': category,
        'products': products,
    })
