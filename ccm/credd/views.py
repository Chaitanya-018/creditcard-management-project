from django.shortcuts import render
from .models import ccard_info
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password,check_password


@csrf_exempt
def signUp(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        hashed_password = make_password(password)

        cc_num = request.POST.get("cc_num")  # already masked by middleware
        limit = request.POST.get("limit")

        ccard_info.objects.create(
            username=username,
            password=hashed_password,
            cc_num=cc_num,
            limit=limit,
            outstanding=0
        )

        return JsonResponse({
            "status": "success",
            "message": "User registered successfully"
        })

    return JsonResponse({
        "status": "failed",
        "message": "Invalid request method"
    })
