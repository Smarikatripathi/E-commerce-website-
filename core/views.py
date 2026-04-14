from django.shortcuts import redirect, render, get_object_or_404
from core.models import Category, Order, Payment, Vendor, Product, ProductImage, Wishlist, ProductReview, Address, HeroSlide, OrderItem
from taggit.models import Tag
# Create your views here.
from django.shortcuts import render
from django.db.models import Q
import requests
import json
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from decimal import Decimal, InvalidOperation
import random
import uuid


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
def about(request):
    return render(request, "core/about.html")

def contact(request):
    return render(request, "core/contact.html")

def account(request):
    return render(request, "core/account.html")  # make sure template exists
def wishlist(request):
    return render(request, "core/wishlist.html")  

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

def orders(request):
    return render(request, "core/orders.html")

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
@login_required
def checkout(request):
    order = Order.objects.filter(user=request.user).last()
    cart = request.session.get('cart', {})

    products = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(pid=product_id)

        product.quantity = quantity
        product.total = product.price * quantity

        total_price += product.total
        products.append(product)

    # No temp order creation here

    return render(request, 'core/checkout.html', {
        'products': products,
        'total_price': total_price,
        'order': order,   # Remove this
    })

def place_order(request):
    cart = request.session.get('cart', {})

    if request.method == "POST":

        payment_method = request.POST.get("payment_method")

        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get("full_name"),
            address=request.POST.get("address"),
            phone=request.POST.get("phone"),
            total_price=0
        )

        total_price = 0

        for product_id, quantity in cart.items():
            product = Product.objects.get(pid=product_id)

            item_total = product.price * quantity
            total_price += item_total

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

        order.total_price = total_price
        order.save()

        request.session['cart'] = {}

        # 🔥 PAYMENT LOGIC
        if payment_method == "khalti":
            return redirect('core:khalti_payment', order.id)

        else:
            order.payment_status = "COD"
            order.save()
            return redirect('core:order_success', order.id)

    return redirect('core:checkout')



def khalti_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    try:
        amount_in_paisa = int(Decimal(order.total_price) * 100)
    except (InvalidOperation, TypeError, ValueError):
        request.session["payment_error"] = "Invalid order amount."
        return redirect("core:payment_failed")

    if amount_in_paisa < 1000:
        request.session["payment_error"] = "Khalti requires a minimum payment amount of Rs. 10."
        return redirect("core:payment_failed")

    if not settings.KHALTI_SECRET_KEY:
        request.session["payment_error"] = "Khalti secret key not configured."
        return redirect("core:payment_failed")

    payload = {
        "return_url": request.build_absolute_uri("/payment-success/"),
        "website_url": request.build_absolute_uri("/"),
        "amount": amount_in_paisa,
        "purchase_order_id": str(order_id),
        "purchase_order_name": f"Order {order_id}",
        "customer_info": {
            "name": order.full_name,
            "email": getattr(order.user, "email", "") or "customer@example.com",
            "phone": order.phone,
        },
    }

    headers = {
        "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    print("PAYLOAD:", payload)
    print("HEADERS:", {k: v if k != "Authorization" else "***" for k, v in headers.items()})

    try:
        response = requests.post(settings.KHALTI_INITIATE_URL, json=payload, headers=headers, timeout=30)
        data = response.json()
    except requests.RequestException as exc:
        request.session["payment_error"] = f"Unable to connect to Khalti: {exc}"
        return redirect("core:payment_failed")
    except ValueError:
        request.session["payment_error"] = "Khalti returned an invalid response."
        return redirect("core:payment_failed")

    print("STATUS:", response.status_code)
    print("RESPONSE:", data)

    # IMPORTANT CHECK
    if response.status_code == 200 and "payment_url" in data:
        return redirect(data["payment_url"])

    error_detail = data.get("detail") or data.get("message") or data
    request.session["payment_error"] = f"STATUS: {response.status_code} RESPONSE: {error_detail}"
    return redirect("core:payment_failed")


def payment_success(request):
    pidx = request.GET.get('pidx')
    status = request.GET.get('status')
    order_id = request.GET.get('purchase_order_id')

    print("RETURN STATUS:", status)

    if not pidx:
        return HttpResponse("Invalid request")

    # VERIFY PAYMENT WITH LOOKUP API
    headers = {
        "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        settings.KHALTI_LOOKUP_URL,
        json={"pidx": pidx},
        headers=headers
    )

    data = response.json()
    print(" LOOKUP RESPONSE:", data)

    if data['status'] == "Completed":
        if order_id:
            order = Order.objects.filter(id=order_id).first()
            if order:
                order.payment_status = "paid"
                order.paid_status = True
                order.save(update_fields=["payment_status", "paid_status"])
                return redirect("core:order_success", order.id)
        return HttpResponse("Payment Successful ")

    return redirect("core:payment_failed")

# @csrf_exempt
# def verify_khalti(request):
#     if request.method == "POST":
#         data = json.loads(request.body)

#         payload = {
#             'token': data['token'],
#             'amount': data['amount']
#         }

#         headers = {
#             'Authorization': f"Key {settings.KHALTI_SECRET_KEY}"
#         }

#         response = requests.post(settings.KHALTI_VERIFY_URL, payload, headers=headers)
#         response_data = response.json()

#         if response.status_code == 200:
#             return JsonResponse({'message': 'Payment Successful'})
#         else:
#             return JsonResponse({'message': 'Payment Failed'})
def payment_failed(request):
    return render(request, "core/payment_failed.html", {
        "payment_error": request.session.pop("payment_error", None)
    })

def order_success(request, order_id):
    order = Order.objects.get(id=order_id)

    return render(request, "core/order_success.html", {
        "order": order
    })

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, "core/my_orders.html", {
        "orders": orders
    })

@login_required
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    items = OrderItem.objects.filter(order=order)

    return render(request, "core/order_detail.html", {
        "order": order,
        "items": items
    })
# Generate PDF Invoice
@login_required
def download_invoice(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    items = OrderItem.objects.filter(order=order)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "INVOICE")

    p.setFont("Helvetica", 12)
    p.drawString(50, 760, f"Order ID: {order.id}")
    p.drawString(50, 740, f"Name: {order.full_name}")
    p.drawString(50, 720, f"Phone: {order.phone}")
    p.drawString(50, 700, f"Total: Rs. {order.total_price}")

    y = 660
    p.drawString(50, y, "Items:")
    y -= 20

    for item in items:
        p.drawString(50, y, f"{item.product.title} x {item.quantity} = Rs. {item.price}")
        y -= 20

    p.showPage()
    p.save()

    return response

def test_keys(request):
    return HttpResponse(
        f"PUBLIC: {getattr(settings, 'KHALTI_PUBLIC_KEY', 'Not set')}<br>"
        f"SECRET: {getattr(settings, 'KHALTI_SECRET_KEY', 'Not set')}"
    )


from django.shortcuts import render, redirect

def esewa_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    amount = float(order.total_price)

    context = {
        "amount": amount,
        "tax_amount": 0,
        "total_amount": amount,
        "transaction_uuid": str(uuid.uuid4()),
        "product_code": "EPAYTEST",
        "success_url": "http://127.0.0.1:8000/esewa-success/",
        "failure_url": "http://127.0.0.1:8000/esewa-failed/",
    }

    return render(request, "core/esewa_payment.html", context)


def esewa_success(request):
    return render(request, "core/esewa_success.html")


def esewa_failed(request):
    return render(request, "core/esewa_failed.html")