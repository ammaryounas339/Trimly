
from django.forms import URLField
from django.core.exceptions import ValidationError
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Url

import random

# This code is used to render the index page. If a form is submitted, it will save the url to the database and return the shortened url to the index page. If the form is not submitted, it will simply return the index page without a shortened url.

def index(response):
    # Define some default values.
    args = {'hidden': True, 'hidden_error': True, 'shortened': ""}

    # Check if the form was submitted.
    if response.method == "POST":
        
        if "trimly.info" in response.POST["url"]:
            id = response.POST["url"].split('/')[-1]
            if id.isdigit() and Url.objects.filter(id=id).exists():
                args['shortened'] = response.POST["url"]
                args['hidden'] = False
                return render(response, 'main/index.html', args)
            
        # Validate the URL.
        if validate_url(response.POST["url"]) == True:
            # Shorten the URL.
            link = add_https(response.POST["url"])
            if Url.objects.filter(link=link).exists():
               item = Url.objects.get(link=link)
               shortened = item.shortened
            else:
                shortened = shorten_url(response.POST["url"])
                # Save the URL to the database.
                Url(id=shortened.split('/')[-1], link=link, shortened=shortened).save()
            # Set the return values.
            args['hidden'] = False
            args['shortened'] = shortened
            return render(response, 'main/index.html', args)
        else:
            # Set the return values.
            args['hidden_error'] = False
            return render(response,'main/index.html',args)
        
    else:
        return render(response,'main/index.html',{'hidden' : True,'shortened':''})


def redirect_url(response,id):
    # Getting element from SQlite database
    try:
        item = Url.objects.get(id=id)
    # If element does not exist
    except:
        return HttpResponse("<h1>Invalid URL</h1>")
    
    
    return redirect(item.link)
    
def shorten_url(url, base_url="www.trimly.info/"):
    # Generate a random number
    while True:
        rand_num = random.randint(0, 1_000_000)
        # Ensure that the random number is not already in use
        if Url.objects.filter(id=rand_num).exists():
            continue
        break
    # Return the shortened URL
    return base_url+str(rand_num)

def add_https(url:str):
    """
    Adds https:// to the beginning of a URL if it is not already present.
    If the URL does not start with www., it adds that as well.
    """
    if url.startswith("https") or url.startswith("http"):
        # The URL already has https:// or http://, so we don't need to do anything.
        return url
    else:
        # The URL does not have https:// or http://, so we need to add it.
        if url.startswith("www."):
            # The URL starts with www., so we just need to add https://.
            return "https://"+url
        else:
            # The URL does not start with www., so we need to add https:// and www.
            return "https://www."+url
            
            
def validate_url(url):
    url_form_field = URLField()
    try:
        url = url_form_field.clean(url)
    except ValidationError:
        return False


    return True
