from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import Contact

# Create your views here.
def contact(requset):
    if requset.method == 'POST':
        listing_id = requset.POST['listing_id']
        listing = requset.POST['listing']
        name = requset.POST['name']
        email = requset.POST['email']
        phone = requset.POST['phone']
        message = requset.POST['message']
        user_id = requset.POST['user_id']
        realtor_email = requset.POST['realtor_email']

        if requset.user.is_authenticated():
            user_id = requset.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id,user_id=user_id)
            if has_contacted:
                messages.error(requset,'You have already made an inquiry for this listing')
                return redirect('/listings/' + listing_id)


    contact = Contact(listing=listing,listing_id=listing_id,name=name,email=email,phone=phone,
                      message=message,user_id=user_id)
    contact.save()
    
    send_mail(
        'Property Listing Inquiry',
        'There has been an inquiry for '+listing+' . Sign into the admin panel for more info',
        'mohamed.azoz20010@gmail.com',
        [realtor_email,'mohamed.azoz20010@gmail.com'],
        fail_silently=False
    )

    messages.success(requset,'Your request has been submitted, a realtor will get back to you soon')
    return redirect('/listings/'+listing_id)