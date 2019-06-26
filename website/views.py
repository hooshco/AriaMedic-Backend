from django.shortcuts import render , redirect
from django.http import  HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate , login , logout
from . import models
import json
import os
import jdatetime

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


    products_arr = []


    for product in products:
        video = product.videos.all().exists()
        sound = product.sounds.all().exists()
        quize = product.quizes.all().exists()
        book = product.books.all().exists()
        type_txt = ""
        if book:
            type_txt = "کتاب/"
        if quize:
            type_txt += "آزمون/"
        if sound:
            type_txt += "صوت/"
        if video:
            type_txt += "ویدئو/"
        if type_txt == "":
            type_txt = "-"





        categorys_arr = []
        category = product.category.all()

        for cat in category:
            j = {
                "CatName":cat.category.title
            }
            categorys_arr.append(j)
        p = {
            "id":product.id,
            "product_name": product.product_name,
            "system_code": product.system_code,
            "categorys":categorys_arr,
            "price": product.price,
            "sell_type":product.sell_type,
            "publisher": product.publisher.title,
            "is_active":product.is_active,
            "discount": product.discount_percent if product.discount_percent else 0,
            "type_txt":type_txt
        }
        products_arr.append(p)
    return render(request,"products/all.html",context={"products":products_arr})

@require_http_methods(["GET"])
def delete_product(request,id):
    models.Product.objects.get(id=id).delete()
    return redirect("product")

@require_http_methods(["GET","POST"])
def update_product(request,id):
    if request.method == "GET":
        categorys = models.Category.objects.all()
        publisher = models.Publisher.objects.all()
        product = models.Product.objects.get(id=id)
        images = product.images.all()

        video = product.videos.all()
        sound = product.sounds.all()
        quize = product.quizes.all()
        book = product.books.all()
        type_txt = None
        if book:
            type_txt = "کتاب/"
        if quize:
            type_txt += "آزمون/"
        if sound:
            type_txt += "صوت/"
        if video:
            type_txt += "ویدئو/"
        if type_txt == None:
            type_txt = "-"

        categorys_arr = []
        category = product.category.all()
        images_arr = []

        for img in images:
            i = {
                "url":"http://127.0.0.1:8000"+img.image.url
            }
            images_arr.append(i)
        for cat in category:
            j = {
                "CatName": cat.category.title
            }
            categorys_arr.append(j)
        p = {
            "id": product.id,
            "product_name": product.product_name,
            "system_code": product.system_code,
            "categorys": categorys_arr,
            "price": product.price,
            "sell_type": product.sell_type,
            "publisher": product.publisher.title,
            "is_active": product.is_active,
            "discount": product.discount_percent if product.discount_percent else 0,
            "type_txt": type_txt,
            "description": product.description,
            "images":images_arr
        }


        return render(request, "products/edit.html",context={"categorys":categorys,"publishers":publisher,"product":p,"sounds":sound,"quizes":quize,"videos":video,"books":book })
    else:
        title = request.POST.get("title")
        description = request.POST.get("description")
        cats = request.POST.getlist("category")
        pid = request.POST.get("publisher")
        system_code = request.POST.get("system_code")
        price = request.POST.get("price")
        sell_type = request.POST.get("sell_type")
        discount_percent = request.POST.get("discount_percent")
        discount_time = request.POST.get("discount_time")
        is_active = request.POST.get("is_active")

        date = None
        if int(sell_type) == 2:
            jal = discount_time.split("/")
            jdate = jdatetime.datetime(int(jal[0]), int(jal[1]), int(jal[2]))
            date = jdatetime.datetime.togregorian(jdate)

        product = models.Product.objects.get(id=id)
        product.product_name = title
        product.description = description
        publisher = models.Publisher.objects.get(id=pid)
        product.publisher = publisher
        product.system_code = system_code
        product.price = price
        product.sell_type = int(sell_type)
        product.discount_percent = int(discount_percent) if discount_percent else None
        product.discount_time = date
        product.is_active = True if int(is_active) == 1 else False
        product.save()
        if "images" in request.FILES:
            for img in request.FILES.getlist('images'):
                product.images.all().delete()
                image = models.ProductImage()
                image.product = product
                image.image = img
                image.save()
        for id in cats:
            category = models.Category(id=id)
            product.category.all().delete()
            pcat = models.ProductCategory()
            pcat.product = product
            pcat.category = category
            pcat.save()
        return redirect("product")

@require_http_methods(["POST", "GET"])
def insert_products(request):

    if request.method == "GET":
        categorys = models.Category.objects.all()
        publisher = models.Publisher.objects.all()


        return render(request, "products/create.html",context={"categorys":categorys,"publishers":publisher })
    else:
        title = request.POST.get("title")
        description = request.POST.get("description")
        cats = request.POST.getlist("category")
        pid = request.POST.get("publisher")
        system_code = request.POST.get("system_code")
        price = request.POST.get("price")
        sell_type = request.POST.get("sell_type")
        discount_percent = request.POST.get("discount_percent")
        discount_time = request.POST.get("discount_time")
        is_active = request.POST.get("is_active")
        # images = request.FILES("images")
        date = None
        if int(sell_type) == 2:
            jal = discount_time.split("/")
            jdate = jdatetime.datetime(int(jal[0]),int( jal[1]), int(jal[2]))
            date = jdatetime.datetime.togregorian(jdate)

        product = models.Product()
        product.product_name = title
        product.description = description
        publisher = models.Publisher.objects.get(id=pid)
        product.publisher = publisher
        product.system_code = system_code
        product.price = price
        product.sell_type = int(sell_type)
        product.discount_percent = int(discount_percent) if discount_percent else None
        product.discount_time = date
        product.is_active = True if int(is_active) == 1 else False
        product.save()
        for img in request.FILES.getlist('images'):
            image = models.ProductImage()
            image.product = product
            image.image = img
            image.save()
        for id in cats:
            category = models.Category(id=id)
            pcat = models.ProductCategory()
            pcat.product = product
            pcat.category = category
            pcat.save()
        return redirect("insert_product")

@require_http_methods(["POST", "GET"])
def video(request):
    if request.method == "GET":
        products = models.Product.objects.all()

        videos = models.Video.objects.all()
        vid_arr = []
        for video in videos:
            jdata = {
                "id": video.id,
                "title": video.title,
                "teacher": video.teacher,
                "publish_date": jdatetime.datetime.fromgregorian(datetime=video.publish_date).strftime("%Y/%m/%d"),
                "time_duration": video.time_duration,
                "language": video.language,
                "size": "10 مگابایت"
            }
            vid_arr.append(jdata)

        return render(request,"videos/all.html",context={"videos":vid_arr,"products":products})
    else:
        title = request.POST.get("title")
        teacher = request.POST.get("teacher")
        pid = request.POST.get("product")
        time_duration = request.POST.get("time_duration")
        publish_date = request.POST.get("publish_date")
        v_file = request.FILES.get("video_file")
        language = request.POST.get("language")
        product = models.Product.objects.get(id=pid)
        jal = publish_date.split("/")
        jdate = jdatetime.datetime(int(jal[0]), int(jal[1]), int(jal[2]))
        date = jdatetime.datetime.togregorian(jdate)

        v = models.Video()
        v.title = title
        v.teacher = teacher
        v.product = product
        v.file = v_file
        v.publish_date = date
        v.time_duration = time_duration
        v.language = language
        v.save()
        return redirect("video")

@require_http_methods(["POST", "GET"])
def update_video(request,id):
    if request.method == "GET":
        video = models.Video.objects.get(id=id)
        products = models.Product.objects.all()
        jdata = {
            "id": video.id,
            "title": video.title,
            "teacher": video.teacher,
            "publish_date": jdatetime.datetime.fromgregorian(datetime=video.publish_date).strftime("%Y/%m/%d"),
            "time_duration": video.time_duration,
            "language": video.language,
            "size": "10 مگابایت",
            "productId":video.product.id
        }
        return render(request,"videos/edit.html",context={"video":jdata,"products":products})
    else:
        title = request.POST.get("title")
        teacher = request.POST.get("teacher")
        pid = request.POST.get("product")
        time_duration = request.POST.get("time_duration")
        publish_date = request.POST.get("publish_date")
        v_file = request.FILES.get("video_file")
        language = request.POST.get("language")
        product = models.Product.objects.get(id=pid)
        jal = publish_date.split("/")
        jdate = jdatetime.datetime(int(jal[0]), int(jal[1]), int(jal[2]))
        date = jdatetime.datetime.togregorian(jdate)

        v = models.Video.objects.get(id=id)
        v.title = title
        v.teacher = teacher
        v.product = product
        if v_file:
            v.file = v_file
        v.publish_date = date
        v.time_duration = time_duration
        v.language = language
        v.save()
        return redirect("video")

@require_http_methods(["GET"])
def delete_video(request,id):
        models.Video.objects.get(id=id).delete()
        return redirect("video")



@require_http_methods(["POST", "GET"])
def sound(request):
    if request.method == "GET":
        products = models.Product.objects.all()

        sounds = models.Sound.objects.all()
        sound_arr = []
        for sound in sounds :
            jdata = {
                "id": sound.id,
                "title": sound.title,
                "teacher": sound.teacher,
                "publish_date": jdatetime.datetime.fromgregorian(datetime=sound.publish_date).strftime("%Y/%m/%d"),
                "time_duration": sound.time_duration,
                "language": sound.language,
                "size": "10 مگابایت"
            }
            sound_arr.append(jdata)

        return render(request,"sounds/all.html",context={"sounds":sound_arr,"products":products})
    else:
        title = request.POST.get("title")
        teacher = request.POST.get("teacher")
        pid = request.POST.get("product")
        time_duration = request.POST.get("time_duration")
        publish_date = request.POST.get("publish_date")
        s_file = request.FILES.get("sound_file")
        language = request.POST.get("language")
        product = models.Product.objects.get(id=pid)
        jal = publish_date.split("/")
        jdate = jdatetime.datetime(int(jal[0]), int(jal[1]), int(jal[2]))
        date = jdatetime.datetime.togregorian(jdate)

        v = models.Sound()
        v.title = title
        v.teacher = teacher
        v.product = product
        v.file = s_file
        v.publish_date = date
        v.time_duration = time_duration
        v.language = language
        v.save()
        return redirect("sound")

@require_http_methods(["POST", "GET"])
def update_sound(request,id):
    if request.method == "GET":
        sound = models.Sound.objects.get(id=id)
        products = models.Product.objects.all()
        jdata = {
            "id": sound.id,
            "title": sound.title,
            "teacher": sound.teacher,
            "publish_date": jdatetime.datetime.fromgregorian(datetime=sound.publish_date).strftime("%Y/%m/%d"),
            "time_duration": sound.time_duration,
            "language": sound.language,
            "size": "10 مگابایت",
            "productId":sound.product.id
        }
        return render(request,"sounds/edit.html",context={"sound":jdata,"products":products})
    else:
        title = request.POST.get("title")
        teacher = request.POST.get("teacher")
        pid = request.POST.get("product")
        time_duration = request.POST.get("time_duration")
        publish_date = request.POST.get("publish_date")
        s_file = request.FILES.get("sound_file")
        language = request.POST.get("language")
        product = models.Product.objects.get(id=pid)
        jal = publish_date.split("/")
        jdate = jdatetime.datetime(int(jal[0]), int(jal[1]), int(jal[2]))
        date = jdatetime.datetime.togregorian(jdate)

        v = models.Sound.objects.get(id=id)
        v.title = title
        v.teacher = teacher
        v.product = product
        if s_file:
            v.file = s_file
        v.publish_date = date
        v.time_duration = time_duration
        v.language = language
        v.save()
        return redirect("sound")

@require_http_methods(["GET"])
def delete_sound(request,id):
        models.Sound.objects.get(id=id).delete()
        return redirect("sound")


@require_http_methods(["POST", "GET"])
def book(request):
    if request.method == "GET":
        products = models.Product.objects.all()

        books = models.Book.objects.all()
        books_arr = []
        for book in books :
            jdata = {
                "id": book.id,
                "title": book.title,
                "teacher": book.teacher,
                "publish_date": jdatetime.datetime.fromgregorian(datetime=book.publish_date).strftime("%Y/%m/%d"),
                "page_count": book.page_count,
                "language": book.language,
                "size": "10 مگابایت"
            }
            books_arr.append(jdata)

        return render(request,"books/all.html",context={"books":books_arr,"products":products})
    else:
        title = request.POST.get("title")
        teacher = request.POST.get("teacher")
        pid = request.POST.get("product")
        page_count = request.POST.get("page_count")
        publish_date = request.POST.get("publish_date")
        b_file = request.FILES.get("book_file")
        language = request.POST.get("language")
        product = models.Product.objects.get(id=pid)
        jal = publish_date.split("/")
        jdate = jdatetime.datetime(int(jal[0]), int(jal[1]), int(jal[2]))
        date = jdatetime.datetime.togregorian(jdate)

        v = models.Book()
        v.title = title
        v.teacher = teacher
        v.product = product
        v.file = b_file
        v.publish_date = date
        v.page_count = page_count
        v.language = language
        v.save()
        return redirect("book")

@require_http_methods(["POST", "GET"])
def update_book(request,id):
    if request.method == "GET":
        book = models.Book.objects.get(id=id)
        products = models.Product.objects.all()
        jdata = {
            "id": book.id,
            "title": book.title,
            "teacher": book.teacher,
            "publish_date": jdatetime.datetime.fromgregorian(datetime=book.publish_date).strftime("%Y/%m/%d"),
            "page_count": book.page_count,
            "language": book.language,
            "size": "10 مگابایت",
            "productId": book.product.id
        }
        return render(request,"books/edit.html",context={"book":jdata,"products":products})
    else:
        title = request.POST.get("title")
        teacher = request.POST.get("teacher")
        pid = request.POST.get("product")
        page_count = request.POST.get("page_count")
        publish_date = request.POST.get("publish_date")
        b_file = request.FILES.get("book_file")
        language = request.POST.get("language")
        product = models.Product.objects.get(id=pid)
        jal = publish_date.split("/")
        jdate = jdatetime.datetime(int(jal[0]), int(jal[1]), int(jal[2]))
        date = jdatetime.datetime.togregorian(jdate)

        v = models.Book.objects.get(id=id)
        v.title = title
        v.teacher = teacher
        v.product = product
        if b_file:
            v.file = b_file
        v.publish_date = date
        v.page_count = page_count
        v.language = language
        v.save()
        return redirect("book")

@require_http_methods(["GET"])
def delete_book(request,id):
        models.Book.objects.get(id=id).delete()
        return redirect("book")





@require_http_methods(["POST", "GET"])
def quize(request):
    if request.method == "GET":
        products = models.Product.objects.all()

        quizes = models.Quize.objects.all()
        quizes_arr = []
        for quize in quizes :
            jdata = {
                "id": quize.id,
                "title": quize.title,
                "teacher": quize.teacher,
                "publish_date": jdatetime.datetime.fromgregorian(datetime=quize.publish_date).strftime("%Y/%m/%d"),
                "question_count": quize.question_count,
                "language": quize.language,
                "size": "10 مگابایت"
            }
            quizes_arr.append(jdata)

        return render(request,"quizes/all.html",context={"quizes":quizes_arr,"products":products})
    else:
        title = request.POST.get("title")
        teacher = request.POST.get("teacher")
        pid = request.POST.get("product")
        question_count = request.POST.get("quize_count")
        publish_date = request.POST.get("publish_date")
        q_file = request.FILES.get("quize_file")
        language = request.POST.get("language")
        product = models.Product.objects.get(id=pid)
        jal = publish_date.split("/")
        jdate = jdatetime.datetime(int(jal[0]), int(jal[1]), int(jal[2]))
        date = jdatetime.datetime.togregorian(jdate)

        v = models.Quize()
        v.title = title
        v.teacher = teacher
        v.product = product
        v.file = q_file
        v.publish_date = date
        v.question_count = question_count
        v.language = language
        v.save()
        return redirect("quize")

@require_http_methods(["POST", "GET"])
def update_quize(request,id):
    if request.method == "GET":
        quize = models.Quize.objects.get(id=id)
        products = models.Product.objects.all()
        jdata = {
            "id": quize.id,
            "title": quize.title,
            "teacher": quize.teacher,
            "publish_date": jdatetime.datetime.fromgregorian(datetime=quize.publish_date).strftime("%Y/%m/%d"),
            "question_count": quize.question_count,
            "language": quize.language,
            "size": "10 مگابایت",
            "productId": quize.product.id
        }
        return render(request,"quizes/edit.html",context={"quize":jdata,"products":products})
    else:
        title = request.POST.get("title")
        teacher = request.POST.get("teacher")
        pid = request.POST.get("product")
        quize_count = request.POST.get("quize_count")
        publish_date = request.POST.get("publish_date")
        b_file = request.FILES.get("quize_file")
        language = request.POST.get("language")
        product = models.Product.objects.get(id=pid)
        jal = publish_date.split("/")
        jdate = jdatetime.datetime(int(jal[0]), int(jal[1]), int(jal[2]))
        date = jdatetime.datetime.togregorian(jdate)
        v = models.Quize.objects.get(id=id)
        v.title = title
        v.teacher = teacher
        v.product = product
        if b_file:
            v.file = b_file
        v.publish_date = date
        v.question_count = quize_count
        v.language = language
        v.save()
        return redirect("quize")

@require_http_methods(["GET"])
def delete_quize(request,id):
        models.Quize.objects.get(id=id).delete()
        return redirect("quize")