from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Post, Reply
from boards.forms import PostingForm, PostingUpdateForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

# Create your views here.
def boards(request):
    posts_faq = Post.objects.filter(category="FAQ")
    posts_inquiry = Post.objects.filter(category="Inquiry")
        
    return render(request, 'boards.html', {'posts_faq':posts_faq, 'posts_inquiry':posts_inquiry})

@login_required
def posting(request):
    if request.method == 'POST':
        form = PostingForm(request.POST)
        for field in form:
            print("Field Error:", field.name, field.errors)
            
        if form.is_valid():
            post = Post()
            post.title = form.cleaned_data['title']
            post.detail = form.cleaned_data['detail']
            post.writer = request.user
            post.category = form.cleaned_data['category']
            post.save()
            return redirect('boards:boards')
        else:
            print('is not valid')
            return render(request, 'boards_posting.html', {'form':form})
    else:
        form = PostingForm()
        return render(request, 'boards_posting.html', {'form':form})
    
def faq_detail(request, bpk):
    url = 'faq_detail' + '/' + bpk
    post = Post.objects.get(id=bpk)
    reply = post.reply_set.all()
    return render(request, 'boards_detail.html', {'post':post, 'url':url, 'reply':reply})

def inquiry_detail(request, bpk):
    url = 'inquiry_detail' + '/' + bpk
    post = Post.objects.get(id=bpk)
    reply = post.reply_set.all()
    return render(request, 'boards_detail.html', {'post':post, 'url':url, 'reply':reply})

@login_required
@require_http_methods(['GET', 'POST'])
def update(request, bpk):
    post = Post.objects.get(id=bpk)
    
    if request.method == 'POST':
        form = PostingUpdateForm(request.POST)
        for field in form:
            print("Field Error:", field.name, field.errors)
        
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.detail = form.cleaned_data['detail']
            post.save()
            
            if post.category == 'FAQ':
                return redirect('boards:faq_detail', bpk)
            elif post.category == 'Inquiry':
                return redirect('boards:inquiry_detail', bpk)
                
        else:
            print("is not valid")
            return render(request, 'boards_update.html', {'form':form})
    else:
        form = PostingUpdateForm(instance=post)
        return render(request, 'boards_update.html', {'form':form, 'post':post})
    
@login_required
def delete(request, bpk):
    post = Post.objects.get(id=bpk)
    post.delete()
    return redirect('boards:boards')

def creply(request, bpk):
    post = Post.objects.get(id=bpk)
    
    if request.method == 'POST':
        comment = request.POST.get('comment')
        reply = Reply(post=post, commenter=request.user, comment=comment)
        reply.save()
    
    if post.category == 'FAQ':
        return redirect('boards:faq_detail', bpk)
    elif post.category == 'Inquiry':
        return redirect('boards:inquiry_detail', bpk)
    
def dreply(request, bpk, rpk):
    post = Post.objects.get(id=bpk)
    reply = Reply.objects.get(id=rpk)
    reply.delete()
    
    if post.category == 'FAQ':
        return redirect('boards:faq_detail', bpk)
    elif post.category == 'Inquiry':
        return redirect('boards:inquiry_detail', bpk)