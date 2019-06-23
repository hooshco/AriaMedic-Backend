from django.shortcuts import render , redirect
from django.http import  HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate , login , logout
from . import models
import json
import os

@require_http_methods(["POST"])
def Register(request):
    phoneNumber = request.POST.get("phoneNumber")
    password = request.POST.get("password")
    fullName = request.POST.get("fullName")
    # TODO Will add City , University and Major For user
    user = models.User.objects._create_user(phoneNumber=phoneNumber,password=password,full_name=fullName)
    return HttpResponse("OK")

@csrf_exempt
@require_http_methods(["POST"])
def Login(request):
    phoneNumber = request.POST.get("phoneNumber")
    password = request.POST.get("password")
    user = authenticate(username=phoneNumber, password=password)
    if user != None:
        print("Succesfull")
        login(request,user)
    else:
        print("Faild")
    return HttpResponse("OK")

@require_http_methods(["POST"])
def LogOut(request):
    logout(request)
    return HttpResponse("OK")

@require_http_methods(["POST","GET"])
def dashboard(request):
    return render(request,"index.html")

@require_http_methods(["POST","GET"])
def state(request):
    if request.method == "POST":
        name = request.POST.get("name")
        state = models.State()
        state.name = name
        state.save()

        return HttpResponse(json.dumps({"status":"ok"}))
    else:
        states = models.State.objects.all()
        state_arr = []
        for state in states:

            state_arr.append(state.as_json())
        return render(request,"parent.html",context={"states":state_arr})

@require_http_methods(["POST"])
def update_state(request,id):
    name = request.POST.get("name")
    state = models.State.objects.get(id=id)
    if state:
        state.name = name
        state.save()
    return HttpResponse("OK")

@require_http_methods(["POST"])
def delete_state(request,id):
    models.State.objects.get(id=id).delete()
    return HttpResponse("OK")


@require_http_methods(["POST","GET"])
def major(request):
    if request.method == "POST":
        name = request.POST.get("name")
        m_type = request.POST.get("type")
        major = models.Major()
        major.name = name
        major.m_type = m_type
        major.save()

        return HttpResponse(json.dumps({"status":"ok"}))
    else:
        majors = models.Major.objects.all()
        major_arr = []
        for major in majors:
            major_arr.append(major.as_json())
        return HttpResponse({"data":major_arr})

@require_http_methods(["POST"])
def update_major(request,id):
    name = request.POST.get("name")
    major = models.Major.objects.get(id=id)
    if major:
        major.name = name
        major.save()
    return HttpResponse("OK")

@require_http_methods(["POST"])
def delete_major(request,id):
    models.Major.objects.get(id=id).delete()
    return HttpResponse("OK")


@require_http_methods(["POST","GET"])
def tag(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        tag = models.Tag()
        tag.name = name
        tag.description = description
        tag.save()
        return redirect("tag")
    else:
        tags = models.Tag.objects.filter()
        tag_arr = []
        for tag in tags:
            tag_arr.append(tag.as_json())
        return render(request,"tags/all.html",context={"tags":tag_arr})

@require_http_methods(["POST","GET"])
def update_tag(request,id):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        tag = models.Tag.objects.get(id=id)
        if tag:
            tag.name = name
            tag.description = description
            tag.save()
        return redirect("tag")
    else:
        tag = models.Tag.objects.get(id=id)

        return render(request, "tags/edit.html", context={"tag": tag.as_json()})

@require_http_methods(["GET"])
def delete_tag(request,id):
    models.Tag.objects.get(id=id).delete()
    return redirect("tag")


@require_http_methods(["POST","GET"])
def category(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        parentId = request.POST.get("parentId") if "parentId" in request.POST else None
        parent = None
        if parentId:
            parent = models.Category.objects.get(id=parentId)
        category = models.Category()
        category.title = title
        category.parent = parent
        category.description = description
        category.save()

        return redirect("category")
    else:
        categorys = models.Category.objects.all()
        category_arr = []
        for category in categorys:
            category_arr.append(category.as_json())
        return render(request,"categories/all.html",context={"categorys":category_arr})

@require_http_methods(["POST","GET"])
def update_category(request,id):
    if request.method == "POST":
        category = models.Category.objects.get(id=id)
        title = request.POST.get("title")
        description = request.POST.get("description")
        parentId = request.POST.get("parentId") if "parentId" in request.POST else None
        parent = None
        if parentId:
            parent = models.Category.objects.get(id=parentId)
        if category:
            category.title = title
            category.description = description
            category.parent = parent
            category.save()
        return redirect("category")
    else:
        cat = models.Category.objects.get(id=id)
        categorys = models.Category.objects.all()
        category_arr = []
        for category in categorys:
            category_arr.append(category.as_json())
        return render(request, "categories/edit.html", context={"categorys": category_arr,"cat":cat.as_json()})

@require_http_methods(["GET"])
def delete_category(request,id):
    models.Category.objects.get(id=id).delete()
    return redirect("category")

@require_http_methods(["POST","GET"])
def publisher(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        link = request.POST.get("link")

        publisher = models.Publisher()
        publisher.profile_image = request.FILES['profile_image']
        publisher.backgrount_image = request.FILES["background"]
        publisher.title = title
        publisher.description = description
        publisher.link = link
        # TODO Will add ImageFiled For Upload

        publisher.save()


        return redirect("publisher")
    else:
        publishers = models.Publisher.objects.all()
        publisher_arr = []
        for publisher in publishers:
            publisher_arr.append(publisher.as_json())
        return render(request,"publishers/all.html",context={"publishers":publisher_arr})

@require_http_methods(["POST","GET"])
def update_publisher(request,id):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        link = request.POST.get("link")

        publisher = models.Publisher.objects.get(id=id)
        if publisher:
            if "background" in request.FILES:
                os.remove(publisher.backgrount_image.path)
                publisher.backgrount_image = request.FILES["background"]
            if "profile_image" in request.FILES:
                os.remove(publisher.profile_image.path)
                publisher.profile_image = request.FILES["profile_image"]
            publisher.title = title
            publisher.description = description
            publisher.link = link
            publisher.save()
        return redirect("publisher")
    else:
        publisher = models.Publisher.objects.get(id=id)

        return render(request, "publishers/edit.html", context={"publisher": publisher.as_json()})



@require_http_methods(["POST","GET"])
def delete_publisher(request,id):
    models.Publisher.objects.get(id=id).delete()
    return redirect("publisher")

@require_http_methods(["POST","GET"])
def discount(request):
    if request.method == "POST":
        code = request.POST.get("code")
        percent = request.POST.get("percent")
        expire_date = request.POST.get("expire_date")
        try_count = request.POST.get("try_count")
        description = request.POST.get("description")

        discount = models.Discount()
        discount.code = code
        discount.percent = percent
        # TODO Will Convert TimeStamp to DateTimeField
        discount.expire_date = expire_date
        discount.try_count = try_count
        discount.description = description
        discount.save()

        return HttpResponse(json.dumps({"status":"ok"}))
    else:
        discounts = models.Discount.objects.all()
        discount_arr = []
        for discount in discounts:
            discount_arr.append(discount.as_json())
        return HttpResponse({"data":discount_arr})

@require_http_methods(["POST"])
def update_discount(request,id):
    code = request.POST.get("code")
    percent = request.POST.get("percent")
    expire_date = request.POST.get("expire_date")
    try_count = request.POST.get("try_count")
    description = request.POST.get("description")

    discount = models.Discount.objects.get(id=id)
    if discount:
        discount.code = code
        discount.percent = percent
        discount.expire_date = expire_date
        discount.try_count = try_count
        discount.description = description
        discount.save()
    return HttpResponse("OK")

@require_http_methods(["POST"])
def delete_discount(request,id):
    models.Discount.objects.get(id=id).delete()

    return HttpResponse("OK")

@require_http_methods(["POST","GET"])
def products(request):
    products = models.Product.objects.all()



    return render(request,"products/all.html")


@require_http_methods(["POST", "GET"])
def insert_products(request):

    if request.method == "GET":
        categorys = models.Category.objects.all()
        publisher = models.Publisher.objects.all()


        return render(request, "products/create.html",context={"categorys":categorys,"publishers":publisher })
    else:
        title = request.POST.get("title")
        description = request.POST.get("description")
        catid = request.POST.get("category")
        pid = request.POST.get("publisher")
        system_code = request.POST.get("system_code")
        description = request.POST.get("description")
        price = request.POST.get("price")
        sell_type = request.POST.get("sell_type")
        discount_percent = request.POST.get("discount_percent")
        discount_time = request.POST.get("discount_time")
        is_active = request.POST.get("is_active")
        images = request.FILES("images")
