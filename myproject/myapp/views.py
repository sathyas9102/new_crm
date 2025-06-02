from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import Customer, CallRecord, Activity, STAGES

@login_required
def dashboard(request):
    stages = [s[0] for s in STAGES]
    stage_customers = {stage: Customer.objects.filter(stage=stage, assigned_to=request.user) for stage in stages}
    return render(request, "dashboard.html", {"stage_customers": stage_customers})



# Move customer between stages
@login_required
def move_customer(request):
    if request.method == "POST":
        cust = get_object_or_404(Customer, id=request.POST.get('id'), assigned_to=request.user)
        new_stage = request.POST.get('new_stage')

        valid_stages = [s[0] for s in STAGES]
        if new_stage not in valid_stages:
            return JsonResponse({"status": "denied", "error": "Invalid stage"}, status=400)

        old_index = valid_stages.index(cust.stage)
        new_index = valid_stages.index(new_stage)

        if new_index > old_index or new_stage in ["Not Interested", "Won"]:
            cust.stage = new_stage
            cust.system_moved = False
            cust.save()
            Activity.objects.create(user=request.user, activity_type="move", detail=f"Moved {cust.name} to {new_stage}")
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "denied", "error": "Backward move not allowed"}, status=403)

    return JsonResponse({"status": "denied", "error": "Invalid request method"}, status=405)

# Add customer
@login_required
def add_customer(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email', '')

        if not name or not phone:
            return render(request, "add_customer.html", {"error": "Name and phone are required"})

        customer = Customer.objects.create(
            name=name,
            phone=phone,
            email=email,
            assigned_to=request.user
        )

        Activity.objects.create(
            user=request.user,
            activity_type="add",
            detail=f"Added {name} (Phone: {phone})"
        )

        return redirect('dashboard')

    return render(request, "add_customer.html")

# Record a call
@login_required
def record_call(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id, assigned_to=request.user)
    if request.method == "POST":
        notes = request.POST.get("notes", "")
        CallRecord.objects.create(customer=customer, notes=notes)
        Activity.objects.create(user=request.user, activity_type="call", detail=f"Called {customer.name}")
        return redirect('dashboard')
    return render(request, "record_call.html", {"customer": customer})

# View call history
@login_required
def call_history(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id, assigned_to=request.user)
    calls = CallRecord.objects.filter(customer=customer).order_by("-timestamp")
    return render(request, "call_history.html", {"customer": customer, "calls": calls})

# Daily Activity Report on logout
@login_required
def logout_view(request):
    from datetime import date
    today = date.today()
    activities = Activity.objects.filter(user=request.user, timestamp__date=today).order_by("-timestamp")
    return render(request, "dar.html", {"activities": activities})

# Bulk mail view
@login_required
def bulk_mail_view(request):
    return render(request, 'bulk_mail.html')

# Bulk WhatsApp view
@login_required
def bulk_whatsapp_view(request):
    return render(request, 'bulk_whatsapp.html')
