from django.shortcuts import render

# Create your views here.
def home_page_view(request):
    return render(request,'testapp/home.html')

def movie_news_view(request):
    news1='india china boarder tensions'
    news2='corna  deadtoll acrossed 15000 in India'
    news3='Assam floods'
    news4='Hyderabad corona cases raising'
    news5='Chennai corona active cases 1.5L'
    my_dict={'news1':news1,'news2':news2,'news3':news3,'news4':news4,'news5':news5}
    return(render(request,'testapp/movie_news.html',my_dict))

def sports_news_view(request):
    news1='india enters into olympics'
    news2='india defeats china in wrestling'
    news3='PV Sindu wins grandslam title'
    news4='sena nehawal enters into semis'
    news5='Anand viswanath '
    my_dict={'news1':news1,'news2':news2,'news3':news3,'news4':news4,'news5':news5}
    return(render(request,'testapp/sports_news.html',my_dict))

def politics_news_view(request):
    news1='Rahul Gandhi became chineese'
    news2='Soniya Gandhi secrete MOU with China 2006'
    news3='Manmohan singh is a puppet in congress party'
    news4='Galwan volley clashes dead toll 23 for india'
    news5='Chinas blame game with India continues'
    my_dict={'news1':news1,'news2':news2,'news3':news3,'news4':news4,'news5':news5}
    return(render(request,'testapp/politics_news.html',my_dict))
