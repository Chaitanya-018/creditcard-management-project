from django.shortcuts import render
from .models import ccard_info
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password,check_password
from .models import ccard_info


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



@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = ccard_info.objects.get(username=username)

            if check_password(password, user.password):
                return JsonResponse({
                    "status": "success",
                    "message": "Login successful"
                })
            else:
                return JsonResponse({
                    "status": "failed",
                    "message": "Invalid credentials"
                })

        except ccard_info.DoesNotExist:
            return JsonResponse({
                "status": "failed",
                "message": "User does not exist"
            })

    return JsonResponse({
        "status": "failed",
        "message": "Invalid request method"
    })



@csrf_exempt
def spend_credit(request):
    if request.method == "POST":
        username = request.POST.get("username")
        amount = int(request.POST.get("amount"))

        try:
            user = ccard_info.objects.get(username=username)

            available_limit = user.limit - user.outstanding

            if amount <= 0:
                return JsonResponse({
                    "status": "failed",
                    "message": "Invalid amount"
                })

            if amount > available_limit:
                return JsonResponse({
                    "status": "failed",
                    "message": "Insufficient credit limit"
                })

            user.outstanding += amount
            user.save()

            return JsonResponse({
                "status": "success",
                "message": "Transaction successful",
                "outstanding": user.outstanding,
                "available_limit": user.limit - user.outstanding
            })

        except ccard_info.DoesNotExist:
            return JsonResponse({
                "status": "failed",
                "message": "User not found"
            })

    return JsonResponse({
        "status": "failed",
        "message": "Invalid request method"
    })



@csrf_exempt
def pay_bill(request):
    if request.method == "POST":
        username = request.POST.get("username")
        amount = int(request.POST.get("amount"))

        try:
            user = ccard_info.objects.get(username=username)

            if amount <= 0:
                return JsonResponse({
                    "status": "failed",
                    "message": "Invalid amount"
                })

            if amount > user.outstanding:
                return JsonResponse({
                    "status": "failed",
                    "message": "Amount exceeds outstanding balance"
                })

            user.outstanding -= amount
            user.save()

            return JsonResponse({
                "status": "success",
                "message": "Bill payment successful",
                "outstanding": user.outstanding,
                "available_limit": user.limit - user.outstanding
            })

        except ccard_info.DoesNotExist:
            return JsonResponse({
                "status": "failed",
                "message": "User not found"
            })

    return JsonResponse({
        "status": "failed",
        "message": "Invalid request method"
    })

