from django.shortcuts import render, redirect
from .models import *
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.db.models import Avg
from django.http import JsonResponse

class Index(TemplateView):
    template_name = 'index.html'  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['category'] = Category.objects.all()

        category = Category.objects.all()[:6]

        for index, value in enumerate(category):
            products = Products.objects.filter(categoryObject=value)[:10]
            category[index].products = products

        context['category'] = category
        context['reviews'] = Reviews.objects.all()
        context['slider'] = SliderProducts.objects.all()
        context['randomImages'] = Products.objects.order_by('?')[:10]
        context['lastBlogs'] = Blogs.objects.order_by('-created_at')[:3]
        context['video'] = MainVideo.objects.all().order_by('?')[0]
        # context[video] = MainVideo.objects.all()[:1]

        return context


class ContactViews(CreateView):
    model = Contacts
    template_name = 'contact.html'
    fields = ['firstname', 'lastname', 'number', 'email', 'message']

def about(request):
    workers = Workers.objects.all()
    reviews = Reviews.objects.all()[:8]

    context = {
        'workers':workers,
        'reviews':reviews,
    }
    return render(request, "about.html", context)

# еще один способ передача контексту
# def about(request):
#     context = {}
#     context['workers'] = Workers.objects.all()
#     context['reviews'] = Reviews.objects.all()[:8]

#     return render(request, 'about.html', context)

def blogs(request):
    rows = Blogs.objects.all()
    context = {
        'rows':rows
    }
    return render(request, 'blog.html', context)

def productDetails(request, id):
    row = Products.objects.get(id=id)

    images = ProductsImages.objects.filter(productObject = row)
    likesCount = ProductsLikes.objects.filter(productObject = row).count()
    points = ProductsRaitings.objects.filter(productObject = row).aggregate(Avg('points'))['points__avg']

    context = {
        "row":row, 
        'images':images,
        "likesCount" : likesCount,
        "points" : points,
    }
    return render(request, "product-details.html", context)


def blogDetails(request, id):
    row = Blogs.objects.get(id=id)
    context = {
        "row":row
    }
    return render(request, "blog-details.html", context)

def shopPage(request):

    begin_price = 0
    end_price = 1000000

    if request.GET.get('begin_price'):
        begin_price = request.GET.get('begin_price')
    if request.GET.get('end_price'):
        end_price = request.GET.get('end_price')


    search = ""
    if request.GET.get('search'):
        search = request.GET.get('search')

    page = 1
    if request.GET.get('page'):
        page = int(request.GET.get('page'))

    rows = Products.objects.all().filter(name__contains=search, price__range=(begin_price, end_price))
    paginator = Paginator(rows, 15)

    next_page = page + 1 if (page + 1) <= len(paginator.page_range) else page
    previous_page = page - 1 if (page - 1) != 0 else page


    brands = Brands.objects.all()

    context = {
        "brands":brands,
        'result_count': f"Показано {15} из {len(rows)}",
        'products': paginator.page(page),
        'pages': paginator.page_range,
        'current_page':page,
        'next_page':next_page,
        'previous_page':previous_page,
    }
    return render(request, "shop.html", context)



def pressLike(request, id):

    if not (request.method == 'POST'):
        return HttpResponseBadRequest("Такой страницы нет")


    if not(request.user.is_authenticated):
        return HttpResponseBadRequest("Пользователь не авторизован")

    product = Products.objects.get(id=id)
    user = request.user

    isLiked = ProductsLikes.objects.filter(productObject = product, author = user).exists()

    if isLiked:
        row = ProductsLikes.objects.get(productObject = product, author = user)
        row.delete()
        return HttpResponseBadRequest("Вы уже нажимали кнопку лайк, status = 400") 

    ProductsLikes.objects.create(productObject = product, author = user)
    return HttpResponse("Лайк принят")

# сохранение рейтингов в базе
# def setRating(request):

#     # if not (request.method == 'POST'):
#     #     return HttpResponseBadRequest('Такой страницы нет')
    
#     if not(request.user.is_authenticated):
#         return HttpResponseBadRequest('Пользователь не авторизован')
    
#     user = request.user
    
#     points = int(request.GET.get('points'))
#     id = int(request.GET.get('id'))
#     print(id, points)

#     product = Products.objects.get(id=id)

#     isLiked = ProductsRaitings.objects.filter(productObject = product, author = user).exists()
        
#     if isLiked:
#         return HttpResponseBadRequest('Вы уже поставили оценку')
    
#     ProductsRaitings.objects.create(productObject = product, author = user, points=points)
#     return HttpResponse("Оценка принята", status = 200)

# перезапись рейтингов
def setRating(request):

    # if not (request.method == 'POST'):
    #     return HttpResponseBadRequest('Такой страницы нет')
    
    if not(request.user.is_authenticated):
        return HttpResponseBadRequest('Пользователь не авторизован')
    
    user = request.user
    
    points = int(request.GET.get('points'))
    id = int(request.GET.get('id'))
    print(id, points)

    product = Products.objects.get(id=id)

    isLiked = ProductsRaitings.objects.filter(productObject = product, author = user).exists()
        
    if isLiked:
        row = ProductsRaitings.objects.get(productObject = product, author = user)
        row.points = points
        row.save()
        return HttpResponse("Оценка принята", status = 200)
        
    
    ProductsRaitings.objects.create(productObject = product, author = user, points=points)
    return HttpResponse("Оценка принята", status = 200)


def saveMail(request):
    mail = request.POST.get('mail')
    Subscriptions.objects.create(mail = mail)
    return redirect('index')

def getRating(request, id):
    row = Products.objects.get(id=id)
    points = ProductsRaitings.objects.filter(productObject = row).aggregate(Avg('points'))['points__avg']

    return JsonResponse({'points':points})

def cart(request):
    return render(request, 'cart.html')

def setShoppingCart(request, id):
    if not(request.user.is_authenticated):
        return HttpResponseBadRequest('Пользователь не авторизован')
    user = request.user
    row = Products.objects.get(id=id)

    quantity = 1
    if request.GET.get('quantity'):
        quantity = int(request.GET.get('quantity'))

    


    isAdded = ShoppingCart.objects.filter(productObject = row, author = user).exists()
    if isAdded:
        cartProduct = ShoppingCart.objects.get(productObject = row, author = user)
        if request.GET.get('isMinus'):
            cartProduct.quantity -= 1
        else:
            cartProduct.quantity += 1

        if cartProduct.quantity <= 0:
            cartProduct.delete()
        else:
            cartProduct.save()
    else:
        ShoppingCart.objects.create(productObject = row, author = user, quantity = quantity)
    
    user = request.user
    rows = ShoppingCart.objects.filter(author=user)
    totalPrice = 0
    for row in rows:
        totalPrice += row.quantity * row.productObject.price

    return JsonResponse({'totalPrice':totalPrice})


def shoppingCart(request):
    if not(request.user.is_authenticated):
        return HttpResponseBadRequest('Пользователь не авторизован')
    
    user = request.user
    rows = ShoppingCart.objects.filter(author=user)
    totalPrice = 0
    for row in rows:
        totalPrice += row.quantity * row.productObject.price

    newProducts = Products.objects.all().order_by('-created_at')[:5]

    context = {
        'rows':rows,
        'totalPrice':totalPrice,
        'newProducts':newProducts
    }
    return render(request, 'cart.html', context)


def deleteShoppingCart(request, id):
    row = ShoppingCart.objects.get(id = id)
    row.delete()
    return HttpResponse("Продукт удален из корзины", status = 200)  



def video(request):
    rows = MainVideo.objects.all()
    context = {
        'rows' : rows,
    }
    return render(request, 'video.html', context)


import requests

def video(request):
    rows = MainVideo.objects.all()

    # pip install requests
    city = 'Osh'  # Или другой город
    api_key = 'a745c6cdd20fa1e6f3226942e1120168'
    api_url = f'http://api.weatherstack.com/current?access_key={api_key}&query={city}'

    response = requests.get(api_url) # получение данных из api 
    weather_data = response.json() 


    context = {
        'rows':rows, # видео

        # для погоды
        'city': city,
        'temperature': weather_data['current']['temperature'],
        'description': weather_data['current']['weather_descriptions'][0],
    }
    return render(request, 'video.html', context)

