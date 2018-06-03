
"""""
@csrf_exempt
def index_person(request,Model,search_field):
    model = Model.objects.all()

    if not request.method == 'POST':
        if 'name' in request.session:
            request.POST = request.session['name']
            request.method = 'POST'
    if request.method == 'POST':

        request.POST = QueryDict('').copy()
        print('To')
        print(request.session['name'])
        request.POST.update(request.session['name'])
        f = request.POST.getlist('name')
        print(f)
        form = FindForm(request.POST)
        request.session['name'] = request.POST
        if form.is_valid():
            name = form.cleaned_data['name']
            if(name):
                if search_field=='name':
                    print(search_field)
                    model = model.filter(name__contains = name)
                elif search_field=='title':
                    print(search_field)
                    model = model.filter(title__contains=name)
                elif search_field == 'username':
                    print(search_field)
                    model = model.filter(username__contains=name)
            model = model.distinct()
    else:
        form = FindForm()
    paginator = Paginator(model, 12)
    page = request.GET.get('page')

    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    dict = {
        'message': results,
        'form': form,
    }
    url=''

    dict.update(debug(request))
    if Model==Post:
        url='Atom/search_post.html'
    elif Model==Person:
        url='Atom/search_user.html'
    elif Model==Wall:
        url='Atom/search_wall.html'
    print(url)
    return render_to_response(url, dict)
#, RequestContext(request,csrf(request))


"""""