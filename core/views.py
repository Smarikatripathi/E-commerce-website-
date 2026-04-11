from django.shortcuts import HttpResponse, redirect, render, get_object_or_404
from core.models import Category, Vendor, Product, ProductImage, CartOrderItem, CartOrderItems, Tags, Wishlist, ProductReview, Address, HeroSlide
from taggit.models import Tag
# Create your views here.
from django.shortcuts import render
from django.db.models import Q

def about(request):
    return render(request, "core/about.html")

def account(request):
    return render(request, "core/account.html")  # make sure template exists
def wishlist(request):
    return render(request, "core/wishlist.html")  

def orders(request):
    return render(request, "core/orders.html")

def index(request):
    products = Product.objects.all()[:5]
    categories = Category.objects.all()
    deals = Product.objects.filter(featured=True)[:4]
    slides = HeroSlide.objects.all()
    
    context = { 
        'categories': categories,
        'products': products,
        'deals': deals,
        'slides': slides,}
    return render(request, 'core/index.html',context)

def product_list_view(request):
    products = Product.objects.filter(product_status='published')

    category = request.GET.get('category')
    vendor = request.GET.get('vendor')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # CATEGORY FILTER
    if category:
        products = products.filter(category__id=category)

    # VENDOR FILTER
    if vendor:
        products = products.filter(vendor__id=vendor)

    # PRICE FILTER
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    context = {
        'products': products,
        'categories': Category.objects.all(),
        'vendors': Vendor.objects.all(),

    }

    return render(request, 'core/product_list.html', context)

def category_list_view(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'core/category_list.html', context)

def category_product_list_view(request, category_id):
    products = Product.objects.filter(category_id=category_id, product_status='published')
    context = {
        'products': products
    }
    return render(request, 'core/category_product_list.html', context)

def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        'vendors': vendors
    }
    return render(request, 'core/vendor_list.html', context)

def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor)

    context = {
        "vendor": vendor,
        "products": products,
        
        
    }
    return render(request, "core/vendor_detail.html", context)

def contact(request):
    return render(request, "core/contact.html")

def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    product_images = ProductImage.objects.filter(product=product)
    reviews = ProductReview.objects.filter(product=product)
    deals = Product.objects.all()

    context = {
        "product": product,
        "product_images": product_images,
        "reviews": reviews,
    }
    return render(request, "core/product_detail.html", context)
def all_products(request):
    products = Product.objects.all()

    context = {
        'products': products
    }
    return render(request, 'core/all_products.html', context)
def hot_deals(request):
    return render(request, "core/hot_deals.html")

def mega_menu(request):
    return render(request, "core/mega_menu.html")

def blog_list(request):
    return render(request, "core/blog.html")

def pages(request):
    return render(request, "core/pages.html")

def shop(request):
    return render(request, "core/shop.html")

def tag_list_view(request, tag_slug=None):
    products = Product.objects.filter( product_status='published').order_by("-id")
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])

    context = {
        'tag': tag,
        'products': products
    }
    return render(request, 'core/tag.html', context)

def search(request):
    query = request.GET.get('q')

    category = request.GET.get('category')

    products = Product.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query),
        product_status='published'
    ).order_by("-date")

    context = {
        'products': products,
        'query': query
    }
    return render(request, 'core/search.html', context)

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    quantity = int(request.POST.get('quantity', 1)) if request.method == "POST" else 1

    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('core:cart')
def cart_view(request):
    cart = request.session.get('cart', {})

    products = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pid=product_id)

        product.quantity = quantity
        product.total = product.price * quantity

        total_price += product.total
        products.append(product)

    return render(request, 'core/cart.html', {
        'products': products,
        'total_price': total_price
    })

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]   # remove item completely

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('core:cart')

def checkout_view(request):
    cart = request.session.get('cart', {})

    products = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(pid=product_id)

        product.quantity = quantity
        product.total = product.price * quantity

        total_price += product.total
        products.append(product)

    return render(request, 'core/checkout.html', {
        'products': products,
        'total_price': total_price
    })

def checkout_view(request):
    cart = request.session.get('cart', {})

    products = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(pid=product_id)

        product.quantity = quantity
        product.total = product.price * quantity

        total_price += product.total
        products.append(product)

    return render(request, 'core/checkout.html', {
        'products': products,
        'total_price': total_price
    })