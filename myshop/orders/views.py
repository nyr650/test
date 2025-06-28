from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from django.contrib import messages

def cart_view(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price * quantity
        products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
        total += subtotal

    return render(request, 'orders/cart.html', {
        'cart_items': products,
        'total': total
    })


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart
    messages.success(request, 'Товар добавлен в корзину!')
    return redirect('cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
        messages.info(request, 'Товар удалён из корзины.')

    return redirect('cart')


def checkout(request):
    request.session['cart'] = {}
    messages.success(request, 'Заказ оформлен! (на будущее — тут будет запись в БД)')
    return redirect('cart')

from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Корзина пуста.')
        return redirect('cart')

    order = Order.objects.create(user=request.user)

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity
        )

    request.session['cart'] = {}  # очищаем корзину
    messages.success(request, 'Заказ оформлен!')
    return redirect('my_orders')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})

from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return render(request, 'orders/order_created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order_create.html', {'form': form})
