from django.shortcuts import render
from eHealth.models import Category
from eHealth.bing import run_query
from eHealth.medLine import med_query
from eHealth.myfunctions import text_analysis
from eHealth.healthFinder import health_query
from eHealth.models import *
from eHealth.bing import run_query
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
import simplejson
import json
from django.template.defaultfilters import slugify
import django
from models import Page,Category,Searcher



#did not finish Ajax suggestions
def ajax_suggestions(request):
    typedSoFar= request.POST.getlist('typedSoFar')[0]
    print typedSoFar

    return HttpResponse(ajax_suggestion)



def add_Page(titl, cat, vis, link, summ, flesch, polarity, subjectivity):
    p = Page.objects.get_or_create(category=cat,linkURL=link, title=titl, flesch_score=flesch, polarity_score=polarity, subjectivity_score=subjectivity  )[0]
    p.category=cat
    p.visits=vis
    p.summary=summ
    p.flesch_score=flesch
    p.subjectivity_score=subjectivity
    p.polarity_score=polarity
    p.save()
    return p

def ajax_add_page(request):
    used=request.user    
    searcher=Searcher.objects.all().get(searcher=used)
    link= request.POST.getlist('link')[0]
    titl=request.POST.getlist('titl')[0]
    categor=request.POST.getlist('categor')[0]
    
    print "link", link
    print "title", titl
    print "category", categor


    actualCategory,created = Category.objects.get_or_create(user=searcher, name=categor)
    actualCategory.slug = slugify(categor)
    df=slugify(categor)
    actualCategory.save()
    print "Category", actualCategory
    print "created,", created
    actualCategory = Category.objects.all().filter(user=searcher).filter(name=categor).get(slug=df)
    print "Category after,",actualCategory
    
    actualPage=None
    page_list=Page.objects.all().filter(category=actualCategory).filter(title=titl)
    if page_list:
        actualPage=page_list[0]
    else:
        actualPage=Page(category=actualCategory, title=titl, linkURL=link)
        print "in the else"
    #print "actual page", actualPage
    #pages=Page.objects.all()
    #print page_list
    #NOT THIS: #actualPage =  Page.objects.get_or_create(category=actualCategory, title=titl)[0]
    #print "Page", actualPage

    actualPage.linkURL=link
    actualPage.summary="this is a page"
    actualPage.flesch_score=6
    actualPage.polarity_score=8
    actualPage.subjectivity_score=9
    #add the flesch, polarity, subjectivity scores here
    #add the summary, visits score here
    actualPage.save()
    print "Page", actualPage
    category_slug=actualCategory.slug
    page_list=Page.objects.all().filter(category=actualCategory)
    json_obj={}
    json_object_list=[]
    for page in page_list:
        page_obj={}
        if created:
            page_obj['created']="true"
            page_obj['categorypk']=actualCategory.pk
            page_obj['categoryname']=actualCategory.name
        else:
            page_obj['created']="false"
        page_obj['category_slug']=category_slug
        page_obj['name']=page.title
        page_obj['linkurl']=page.linkURL
        page_obj['pagepk']=page.pk        
        page_obj['pagestatus']=page.is_public
        print page.linkURL
        json_object_list.append(page_obj)
    json_obj['meta']=json_object_list
    resp= simplejson.dumps(json_obj)

    return HttpResponse(resp)

def ajax_add_category(request):
    nam=request.POST['categoryName']
    used=request.user
    searcher=Searcher.objects.all().get(searcher=used)
    resp=slugify(nam)
    

    cate = Category.objects.get_or_create(user=searcher, slug=resp)[0]
    cate.name=nam
    cate.save()
    print cate
    resp=cate.name
    return HttpResponse(resp)

def random(request):
    context_dict={}
    response = render(request, 'eHealth/random.html', context_dict)
    return response

#def index(request):
#    print 'this is index'
#    context_dict={}

def index(request):
    context_dict = {}
    #public categories
    list_of_pages=Page.objects.all().filter(is_public=True)
    context_dict['popular_pages'] = list_of_pages.order_by('-visits')[:5]
    context_dict['shared_pages'] = list_of_pages.order_by('-visits')[5:10]

    #["www.mimis.com", "www.poyias.com"]

    response = render(request, 'eHealth/index.html', context_dict)

    return response

def ajax_page_click(request):
    primaryKey=request.POST['primarykey']

    page=Page.objects.all().get(pk=primaryKey)
    print "page", page
    page.visits = page.visits+1
    page.save()

    return HttpResponse('true')

def ajax_page_status_change(request):
    print "okay"
    primaryKey=request.POST.getlist('pk')[0]
    isPub=request.POST.getlist('status')[0]
    
    page=Page.objects.all().get(pk=int(primaryKey))
    print page
    
    if(int(isPub)==1):
        page.is_public=True
    else:
        page.is_public=False
    page.save()

    print primaryKey
    print isPub
    print "last thing, " , page.is_public
    return HttpResponse("true")

def ajax_delete_pages(request):
    information= request.POST['information']
    realInfo= information.split(',')
    counter=0
    cate=None
   # print information

    for categor in Category.objects.all():
      #  print "name:", categor.name
        print "slug:",categor.slug
        if(categor.slug ==realInfo[0]):
            cate=categor


    #searcher=Searcher.objects.all().get(searcher=request.user)
    # print "searcher", searcher
    for inf in realInfo:
        if(counter==0):
            counter=counter+1   
          #  print "inside lop"
        else:
            Page.objects.filter(category=cate).get(pk=int(inf)).delete()
    #print "cate", cate
   
    page_list=Page.objects.all().filter(category=cate)
    json_obj={}
    json_object_list=[]
    for page in page_list:
        page_obj={}
        page_obj['name']=page.title
        page_obj['linkurl']=page.linkURL
        page_obj['pagepk']=page.pk
        page_obj['pagestatus']=page.is_public
      #  print page.linkURL
        json_object_list.append(page_obj)
    json_obj['meta']=json_object_list
    resp= simplejson.dumps(json_obj)
    print resp
    
    return HttpResponse(resp)

def ajax_change_user_info(request):
    user=request.user
    search=Searcher.objects.all().get(searcher=user)
    user_info= request.POST['information']
    print user_info
    user_info_list=user_info.split(',')
    print "user_info_list[0]",user_info_list[0]
    

    search.age=int(user_info_list[0])
    search.name=user_info_list[1]
    search.surname=user_info_list[2]
    user.username= user_info_list[3]
    user.save()
    search.email=user_info_list[4]
    search.gender=user_info_list[5]
    search.save()
   
    print search.age
    print search.name
    print search.surname
    print search.searcher.username
    print search.email
    print search.gender


    json_obj={}
    userinfo={}
    json_object_list=[]
    userinfo['firstnameinp']=search.name
    userinfo['lastnameinp']=search.surname
    userinfo['ageinp']=str(search.age)
    userinfo['genderinp']=search.gender
    userinfo['emailinp']=str(search.email)
    userinfo['usernameinp']=request.user.username
    json_object_list.append(userinfo)
    json_obj['meta']=json_object_list
    resp=simplejson.dumps(json_obj)
    return HttpResponse(resp)

def ajax_get_user_info(request):
    searcher=Searcher.objects.all().get(searcher=request.user)
    json_obj={}
    userinfo={}
    json_object_list=[]
    userinfo['firstnameinp']=searcher.name
    userinfo['lastnameinp']=searcher.surname
    userinfo['ageinp']=str(searcher.age)
    userinfo['genderinp']=searcher.gender
    userinfo['emailinp']=str(searcher.email)
    userinfo['usernameinp']=request.user.username
    json_object_list.append(userinfo)
    json_obj['meta']=json_object_list
    resp=simplejson.dumps(json_obj)
    return HttpResponse(resp)

def ajax_delete_categories(request):
    categories_To_Delete = request.POST['cats_for_deletion']
    list_categories=categories_To_Delete.split(',')
    number=0
   # print "list_categories=",list_categories
    for categor in list_categories:
        number=int(categor)
        print "pk number: ",number
        cate=Category.objects.get(pk=number)
        # first delete the pages pertaining to the category
        Page.objects.filter(category=cate).delete()
        # second delete the category
        cate.delete()
    json_obj={}
    searcher_= Searcher.objects.all().get(searcher=request.user)
    list_categories2=Category.objects.all().filter(user=searcher_)
    json_object_list=[]
    for categ in list_categories2:
        categ_obj={}
        categ_obj['categpk']=categ.pk
        categ_obj['categslug']=categ.slug
        categ_obj['categname']=categ.name
        json_object_list.append(categ_obj)
    json_obj['meta']=json_object_list
    resp=simplejson.dumps(json_obj)
    return HttpResponse(resp)

def ajax_saved_pages(request):
    category_slug= request.POST['category_slug']
    searcher=Searcher.objects.all().get(searcher=request.user)

    category_retrieved=Category.objects.all().filter(user=searcher).get(slug=category_slug)
    page_list=Page.objects.all().filter(category=category_retrieved)
   # print "hello there"
                       # literally just copied code from stack overflow
    json_obj={}
    json_object_list=[]
    for page in page_list:
        page_obj={}
        page_obj['name']=page.title
        page_obj['linkurl']=page.linkURL
        page_obj['pagepk']=page.pk        
        page_obj['pagestatus']=page.is_public
        #print page.linkURL
        json_object_list.append(page_obj)
    json_obj['meta']=json_object_list
    resp= simplejson.dumps(json_obj)
    #print resp
    return HttpResponse(resp)


def ajax_get_all_page_statuses(request):
   
    searcher=Searcher.objects.all().get(searcher=request.user)

    category_list=Category.objects.all().filter(user=searcher)
    page_list=[]
    #page_list=Page.objects.all().filter(category=category_retrieved)
    #pages=None
   
    print "length of list",len(category_list)
    counter=1
    for categor in category_list:
        #print categor
        df=Page.objects.all().filter(category=categor)        
        #print df
        page_list.extend(df)
        #savedPages.extend(list(Page.objects.all().filter(category=categor)))
        #if not (counter>len(category_list)):
        #    page_list.extend(list(Page.objects.all().get(category=categor)))
        #counter=counter+1
        
    #print "OUOIEWRUWE"
    print page_list
    json_obj={}
    json_object_list=[]
    #print "printing the public"
    for page in page_list:
        page_obj={}
        #page_obj['name']=page.title
        #page_obj['linkurl']=page.linkURL
        page_obj['pagepk']=page.pk        
        #print page.is_public
        page_obj['pagestatus']=page.is_public
        #print page.linkURL
        json_object_list.append(page_obj)
    json_obj['meta']=json_object_list
    resp= simplejson.dumps(json_obj)
    return HttpResponse(resp)



@login_required
def user(request):
    if not request.user.is_authenticated():
        return HttpResponse("No log in. Please log in. ")
    context_dictionary={}
    searcher=Searcher.objects.get(searcher=request.user)
    context_dictionary['userInformation']=searcher
    categoryList=Category.objects.filter(user=searcher)
    context_dictionary['cateogoryList']=categoryList
    #so initially, all the saved links for this user are displayed, 
    # then by clicking on a Category, Ajax uses another function for population
    
    savedPages=[]
    for cat in categoryList:
        savedPages.extend(list(Page.objects.all().filter(category=cat)))
    
    #savedPages=Saved_Page.objects.filter(user=searcher)
    context_dictionary['savedPages']=savedPages
    #print "savedPages is," , savedPages
    response = render(request, 'eHealth/user.html', context_dictionary)
    return response


def category(request, slug_name):
    context_dict = {}

    try:
        category = Category.objects.get(slug=slug_name)

        context_dict['category_name'] = category.name

        context_dict['category'] = category

        context_dict['slug'] = slug_name

    except Category.DoesNotExists:
        pass

    return render(request, 'eHealth/category.html', context_dict)


def searching(request):
    all_results = []

    bing_list = []

    medLine_list = []

    healthFinder_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            bing_list = run_query(query)
            medLine_list = med_query(query)
            healthFinder_list = health_query(query)

    bing_list = text_analysis(bing_list)
    medLine_list = text_analysis(medLine_list)
    healthFinder_list = text_analysis(healthFinder_list)
    # implement HealthFinder when ready!

    context_dic = {'bing_list': bing_list,
                   'med': medLine_list,
                   'health': healthFinder_list,
                   'all_results': bing_list + medLine_list + healthFinder_list
                   }

    response = render(request, 'eHealth/searching.html', context_dic)



    return response


def about(request):
    return render(request, 'eHealth/about.html')
