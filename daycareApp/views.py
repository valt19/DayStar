from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseBadRequest
from .forms import *
from . filters import *
from .models import *
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, 'daycareApp/home.html')

def index(request):
    return render(request, 'daycareApp/base.html')

@login_required
def index(request):
    today_sitters = Sitter.objects.all().order_by('-id')
    today_babys = Baby.objects.all().order_by('-id')
    all_sitters = Sitter.objects.all()
    all_babys = Baby.objects.all()
    count_sitters = Sitter.objects.count()
    count_babys = Baby.objects.count()
    all_onduty = Sitter_on_duty.objects.count()

    # all_sale = Sale.objects.all()
    context = {
        'today_babys': today_babys,
        'today_sitters': today_sitters,
        'count_sitters': count_sitters,
        'count_babys': count_babys,
        'all_sitters': all_sitters,
        'all_babys': all_babys,
        'all_onduty': all_onduty,
    }
    template = loader.get_template('daycareApp/index.html')
    return HttpResponse(template.render(context))

# sitter views   
@login_required
def sitterReg(request):
    addSitterForm = Sitter_regForm(request.POST)  
    message = None
    if request.method == 'POST':
        if addSitterForm.is_valid():
            newSitter = addSitterForm.save(commit=False)  
            newSitter.save()
            message = "Sitter Added Successfully!"
            return redirect('sitters')
        else:
            message = "Sitter Registration Failed"
    else:
        addSitterForm = Sitter_regForm()  

    return render(request, 'daycareApp/sitter_reg.html', {'addSitterForm': addSitterForm, 'message': message})

@login_required
def sitters(request): 
    all_sitters = Sitter.objects.all()
    context = {
        'all_sitters': all_sitters
    }
    template = loader.get_template('daycareApp/sitters.html')
    return HttpResponse(template.render(context))

@login_required
def viewSitter(request, id): # sttier viewing page
    all_sitter = Sitter.objects.get(id=id)
    context = {
       'all_sitter': all_sitter
    }
    template = loader.get_template('daycareApp/view_sitter.html')
    return HttpResponse(template.render(context))

def edit_sitterdetails(request, id):
    item = get_object_or_404(Sitter, id=id)
    if request.method == 'POST':
        form = Sitter_regForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Redirect to a success page
    else:
        form = Sitter_regForm(instance=item)
    return render(request, 'daycareApp/edit_sitter.html', {'form': form})


@login_required
def babyReg(request):
    addBabyForm = Baby_regForm(request.POST)  
    message = None
    if request.method == 'POST':
        if addBabyForm.is_valid():
            newBaby = addBabyForm.save(commit=False) 
            newBaby.save()
            message = "Baby Added Successfully!"
            return redirect('babys')
        else:
            message = "Baby Registration Failed"
    else:
        addBabyForm = Baby_regForm()  

    return render(request, 'daycareApp/baby_reg.html', {'addBabyForm': addBabyForm, 'message': message})


@login_required
def babys(request):
    all_babys = Baby.objects.all().order_by('id')
    babysearch=BabyFilter(request.GET, queryset=all_babys)
    all_babys=babysearch.qs
    return render(request, 'daycareApp/babies.html', {'all_babys': all_babys, 'babysearch': babysearch})

def deleteBaby(request, id):
    Baby.objects.filter(id=id).delete()
    return redirect('/babies')


#sell item form
@login_required
def sale(request):
    itemform = Item_sellForm(request.POST)
    sell_message = None
    if request.method == 'POST':
        if itemform.is_valid():
            newItem = itemform.save(commit=False)
            newItem.save()
            sell_message = "Item Sold Successfully!"
            return redirect('sale')
        else:
            sell_message = "Item Sell failed!"
    else:
        itemform = Item_sellForm()
    item = AddItem.objects.all()
    return render(request, 'daycareApp/sale.html', {'itemform': itemform, 'item': item, 'sell_message': sell_message})

def selling(request, pk):
    sell = AddItem.objects.get(id=pk)
    form = Item_sellForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            newItem = form.save(commit=False)
            newItem.doll_name = sell
            newItem.amount_paid = sell.price
            newItem.save()
            sell_quantity = int(request.POST['quantity'])
            sell.quantity -= sell_quantity
            sell.save()
            # print(sell.doll_name) 
            # print(request.POST['quantity'])
            # print(sell.quantity)
            return redirect('sale')
    return render(request, 'daycareApp/selling.html', {'form': form})

def salesrecord(request):
    sales = ItemSelling.objects.all()
    total = sum([item.amount_paid for item in sales if item.amount_paid is not None])
    change = sum([item.get_change() for item in sales if item.get_change() is not None])
    net = total - change
    return render(request, 'daycarerApp/salerecord.html', {'total': total, 'sales': sales, 'total': total, 'net': net, 'change': change})

#adding stock to sale
@login_required
def addItem(request):
    add_item_form = Item_regForm(request.POST)
    add_message = None
    if request.method == 'POST':
        if add_item_form.is_valid():
            newItem = add_item_form.save(commit=False)
            newItem.save()
            add_message = "Item Added Successfully!"
            return redirect('sale')
        else:
            add_message = "Item Addition failed!"
    else:
        add_item_form = Item_regForm()

    return render(request, 'daycareApp/addStock.html', {'addItemForm': add_item_form, 'add_message': add_message})

def onduty(request):
    if request.method == 'POST':
        form = Sitter_dutyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('allonduty')
    else:
        form = Sitter_dutyForm()
    return render(request, 'daycareApp/onduty.html', {'form': form})


def allonduty(request):
    duty = Sitter_on_duty.objects.all()
    context ={
        'duty': duty,
    }
    template = loader.get_template('daycareApp/allOnduty.html')
    return HttpResponse(template.render(context))
    

def editOnduty(request, id):
    edited = get_object_or_404(Sitter_on_duty, id=id)
    if request.method == 'POST':
        form = Sitter_dutyForm(request.POST, instance=edited)
        if form.is_valid():
            form.save()
            return redirect('allonduty')
    else: 
        form = Sitter_dutyForm(instance=edited)
    return render(request, 'daycareApp/editOnduty.html', {'form': form, 'edited': edited})

def addmore(request, id):
    issue_doll = AddItem.objects.get(id=id)
    if request.method == 'POST':
        form = Addmore(request.POST)
        if form.is_valid():
            newDoll = request.POST.get('quantity')
            if newDoll:
                try:
                    added = int(newDoll)
                    issue_doll.quantity += added
                    issue_doll.save()
                    print(added)
                    print(issue_doll.quantity)
                    return redirect('sale')
                except ValueError:
                    return HttpResponseBadRequest('Invalid quantity')
    else:
        form = Addmore()
    return render(request, 'daycareApp/addmore.html', {'form': form })

#views for baby payments
def babyPay(request):
    baby = BabyPayment.objects.all()
    return render(request, 'daycareApp/babypay.html', {'baby': baby })

def babyadd(request):
    if request.method == 'POST':
        form = BabyPaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('babypay')
    else: 
        form = BabyPaymentForm()
    return render(request, 'daycareApp/babyadd.html', {'form': form})

def babyedit(request, id):
    edited = get_object_or_404(BabyPayment, id=id)
    if request.method == 'POST':
        form = BabyPaymentForm(request.POST, instance=edited)
        if form.is_valid():
            form.save()
            return redirect('babypay')
    else: 
        form = BabyPaymentForm(instance=edited)
    return render(request, 'daycareApp/babyedit.html', {'form': form, 'edited': edited})
    

#sitter payment views
def sitterpay(request):
    sitter = SitterPayment.objects.all()
    return render(request, 'daycareApp/sitterpay.html', {'sitter': sitter })

def sitteradd(request):
    if request.method == 'POST':
        form = SitterPaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sitterpay')
    else: 
        form = SitterPaymentForm()
    return render(request, 'daycareApp/sitteradd.html', {'form': form})

def sitteredit(request, id):
    edited = get_object_or_404(SitterPayment, id=id)
    if request.method == 'POST':
        form = SitterPaymentForm(request.POST, instance=edited)
        if form.is_valid():
            form.save()
            return redirect('sitterpay')
    else: 
        form = SitterPaymentForm(instance=edited)
    return render(request, 'daycareApp/sitteredit.html', {'form': form, 'edited': edited})


# authetications
@login_required
def deleteSitter(request, id):
    sitter = Sitter.objects.get(id=id)
    if request.method == 'POST':
        # If the confirmation form is submitted
        if 'confirm_delete' in request.POST:
            # Delete the sitter
            sitter.delete()
            return redirect('sitters')
        elif 'cancel_delete' in request.POST:
            return redirect('sitters')
    return render(request, 'daycareApp/sitters.html', {'sitter': sitter})

@login_required
def logout_view(request):
    logout(request)
    return redirect('/') # redirect user to the index page
