from django.shortcuts import render
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime

# Create your views here.

def index(request):
    return render(request, 'store/index.html')

def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    b=Book.objects.get(id=bid)
    c=BookCopy.objects.filter(book=b,status=False).count()
    context = {
        'book': b, # set this to an instance of the required book
        'num_available': c, # set this to the number of copies of the book available, or 0 if the book isn't available
    }
    # START YOUR CODE HERE
    
    
    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    get_data = request.GET
    b=Book.objects.filter(title=get_data.get('title',' '),author=get_data.get('author',' '),genre=get_data.get('genre',' '))
    context = {
        'books': b, # set this to the list of required books upon filtering using the GET parameters
                       # (i.e. the book search feature will also be implemented in this view)
    }
    
    
    
    
    return render(request, template_name, context=context)

@login_required
def viewLoanedBooks(request):
    username = None
    if request.user.is_authenticated:
        username = request.user
    template_name = 'store/loaned_books.html'
    loan=BookCopy.objects.filter(status=True,borrower=username)
    context = {
        'books': loan,
    }
    '''
    The above key 'books' in the context dictionary should contain a list of instances of the 
    BookCopy model. Only those book copies should be included which have been loaned by the user.
    '''
    
    


    return render(request, template_name, context=context)

@csrf_exempt
@login_required
def loanBookView(request):
    if request.method=="POST":
        response_data = {
            'message': 'failure',
        }
        id=request.POST.get('bid',' ')
        b=Book.objects.get(id=id)
        copy=BookCopy.objects.filter(book=b)
        username = None
        if request.user.is_authenticated:
            username = request.user
        for x in copy:
            if x.status==False:
                x.status=True
                x.borrower=username
                
                now=datetime.datetime.now()
                x.borrow_date=now.strftime("%Y-%m-%d")
                x.save()
                response_data={
                    'message':'success'
                }
                return JsonResponse(response_data)
        return JsonResponse(response_data)        
    
    '''
    Check if an instance of the asked book is available.
    If yes, then set the message to 'success', otherwise 'failure'
    '''
    # START YOUR CODE HERE
    # book_id = None # get the book id from post data


    

'''
FILL IN THE BELOW VIEW BY YOURSELF.
This view will return the issued book.
You need to accept the book id as argument from a post request.
You additionally need to complete the returnBook function in the loaned_books.html file
to make this feature complete
''' 
@csrf_exempt
@login_required
def returnBookView(request):
    if request.method=="POST":
        response_data = {
            'message': 'failure',
        }
        id=request.POST.get('bid',' ')
        b=Book.objects.get(id=id)
        copy=BookCopy.objects.filter(book=b)
        for x in copy:
            if x.status==True:
                x.status=False
                x.borrow_date=None
                x.save()
                response_data={
                    'message':'success'
                }
                return JsonResponse(response_data)
        return JsonResponse(response_data)

@csrf_exempt
@login_required
def rateBookView(request):
    if request.method=="POST":
        response_data = {
            'message': 'failure',
        }
        id=request.POST.get('bid',' ')
        rating=request.POST.get('rating',' ')
        
        b=Book.objects.get(id=id)
        currentRatedbook=Rate.objects.filter(book=b)
        flag=0
        for x in currentRatedbook:
            if x.user==request.user.username:
                print(x.rating)
                flag=1
                x.rating=rating
                x.save()
                x.refresh_from_db()
                response_data={
                    'message':'success'
                }
        if flag==0:
            r=Rate(book=b,user=request.user,rating=rating)
            r.save()
            r.refresh_from_db()
            response_data={
                'message':'success'
            }
        totalRating=0
        totalRatingdone=len(currentRatedbook)    
        for x in currentRatedbook:
            totalRating=totalRating+float(x.rating)
        avgRating=totalRating/totalRatingdone
        b.rating=avgRating
        b.save()

        return JsonResponse(response_data)    
   
