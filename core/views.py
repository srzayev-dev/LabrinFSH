from logging import error
from django.http import HttpResponseRedirect
from django.http.response import FileResponse, Http404, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.contrib.auth import get_user_model
from django.core.paginator import EmptyPage, Paginator
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post,SharePost
from core.forms import UploadFilesForm, ShareFilesForm

class SafePaginator(Paginator):
    def validate_number(self, number):
        try:
            return super(SafePaginator, self).validate_number(number)
        except EmptyPage:
            if number > 1:
                return self.num_pages
            else:
                raise

User = get_user_model()

def home_view(request):
    if request.method == "POST" and 'uploadFile' in request.POST:
        form = UploadFilesForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post(
                user = request.user,
                title = request.POST.get('title'),
                desc = request.POST.get('desc'),
                file_field=request.FILES['file_field']
            )
            post.save()
    else:
        form = UploadFilesForm()

    context = {
        'title' : 'Home',
        'form' : UploadFilesForm(),
    }

    return render(request, 'index.html', context=context)



class FileListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "myfiles.html"
    paginator_class = SafePaginator
    paginate_by = 4
    def get_queryset(self):
        queryset = Post.objects.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class FileDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "file_detail.html"

    def get(self, request, *args, **kwargs):
        my_file = self.get_object()
        if Post.objects.filter(pk=my_file.pk, user=self.request.user).exists() or SharePost.objects.filter(file=my_file, sharedUser=self.request.user).exists():
            file_detail =  Post.objects.get(pk=self.kwargs.get('pk'))
            context = {
                'file_detail' : file_detail,
                'form' : ShareFilesForm(),
            }
            return render(request, 'file_detail.html', context=context)
        return HttpResponse("You are not allowed to view this file")

    
    def post(self, request, *args, **kwargs):
        file_detail =  Post.objects.get(pk=self.kwargs.get('pk'))
        form = ShareFilesForm(request.POST)
        if form.is_valid():
            if file_detail.user == request.user:
                error = ''
                if SharePost.objects.filter(file=file_detail, sharedUser=form.cleaned_data.get('sharedUser'), can_comment=form.cleaned_data.get('can_comment')).exists() == False:
                    try:
                        sharepost = SharePost(
                        file = Post.objects.get(pk=self.kwargs['pk']),
                        user = request.user,
                        sharedUser = User.objects.get(id=form.cleaned_data.get('sharedUser').id),
                        can_comment = form.cleaned_data.get('can_comment')
                    )
                        sharepost.save()
                    except:
                        if form.cleaned_data.get('sharedUser') != request.user:
                            sharepost = SharePost.objects.get(file=file_detail, sharedUser=form.cleaned_data.get('sharedUser'))
                            sharepost.can_comment = form.cleaned_data.get('can_comment')
                            sharepost.save()
                            self.object = self.get_object()
                            context = super().get_context_data(**kwargs)
                            return HttpResponseRedirect(self.request.path_info)
                        else:
                            error = "You can't share your own file with yourself"
                else:
                    error = "User already shared this file"
                    
            else:
                error = "You are not allowed to share this file"
            context = {
                'file_detail' : file_detail,
                'form' : ShareFilesForm(),
                'error' : error,
            }
            return render(request, 'file_detail.html', context=context)
        else:
            form = ShareFilesForm()
            self.object = self.get_object()
            context = super().get_context_data(**kwargs)
            return self.render_to_response(context=context)



class sharedFileListView(ListView):
    model = SharePost
    template_name = "sharedfiles.html"
    paginator_class = SafePaginator
    paginate_by = 4
    def get_queryset(self):
        queryset = SharePost.objects.filter(sharedUser=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class OpenFileView(View):
    def get(self, *args, **kwargs):
        try:
            pdf = Post.objects.get(pk=self.kwargs.get('pk'))
        except Post.DoesNotExist:
            raise Http404("File does not exist")
        response = FileResponse(open(pdf.file_field.path, 'rb'))
        response['Content-Disposition'] = 'inline; filename="{}"'.format(
                pdf.title)
        return response


def room(request, room_name):
    return render(request, "room.html", {
        'room_name': room_name
    })