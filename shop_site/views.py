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
        cartProduct.quantity += 1
        cartProduct.save()
    else:
        ShoppingCart.objects.create(productObject = row, author = user, quantity = quantity)
    return HttpResponse("Продукт добавлен", status = 200)

def shoppingCart(request):
    if not(request.user.is_authenticated):
        return HttpResponseBadRequest('Пользователь не авторизован')
    
    user = request.user
    rows = ShoppingCart.objects.filter(author=user)
    totalPrice = 0
    for row in rows:
        totalPrice += row.quantity * row.productObject.price

    context = {
        'rows':rows,
        'totalPrice':totalPrice
    }
    return render(request, 'cart.html', context)

