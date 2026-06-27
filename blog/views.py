from django.shortcuts import render, render, get_object_or_404, redirect
from blog.models import Post, ReplayComment
from django.contrib import messages
from blog.form import CommentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.db.models import F

# Create your views here.
def blog_grid(request,  **kwargs):
    post = Post.objects.filter(status=True)
    if kwargs.get("ca_name") != None:
        post = post.filter(category__name=kwargs["ca_name"])
    if kwargs.get("au_name"):
        post = post.filter(author__username=kwargs["au_name"])
    if kwargs.get("ta_name"):
        post = post.filter(tag__name__iexact=kwargs["ta_name"]).distinct()
    paginator = Paginator(post, 3)
    try:
        page_number = request.GET.get("page")
        post = paginator.get_page(page_number)
    except PageNotAnInteger:
        post = paginator.get_page(1)
    except EmptyPage:
        post = paginator.get_page(paginator.num_pages)

    context={"post":post}
    return render(request, 'blog/blog-grid.html', context)

def blog_detail(request, slug, **kwargs):
    post = get_object_or_404(Post, slug=slug, status=True)
    post.views += 1
    post.save(update_fields=['views'])

    posts = Post.objects.filter(status = True)
    comments = post.comment.all()

    if request.method == 'POST':

        form_type = request.POST.get('form_type')

        if form_type == 'comment':
            form = CommentForm(request.POST)

            if form.is_valid():
                comment_obj = form.save(commit=False)
                comment_obj.author=request.user
                comment_obj.post = post
                comment_obj.save()

                messages.success(request, "کامنت شما ثبت شد")
                return redirect('blog:blog_detail', slug=slug)
            else:
                messages.error(request, "اطلاعات فرم صحیح نیست")
        elif form_type == 'reply':
            reply_text = request.POST.get('comment')
            parent_id = request.POST.get('parent_id')

            if reply_text and parent_id:
                ReplayComment.objects.create(
                    author=request.user,
                    comment=reply_text,
                    question_comment_id=int(parent_id)
                )
                messages.success(request, "کامنت شما ثبت شد")
                return redirect('blog:blog_detail', slug=slug)
            else:
                messages.error(request, "اطلاعات فرم صحیح نیست")

    context = {
        "post": post,
        "posts" : posts,
        "comments" : comments,
    }
    return render(request, 'blog/blog-detail.html', context)

def like_post(request, pk):
    post = Post.objects.get(pk=pk)

    liked = request.session.get(f"liked_{pk}", False)

    if liked:
        post.like = F('like') - 1
        request.session[f"liked_{pk}"] = False
        liked = False
    else:
        post.like = F('like') + 1
        request.session[f"liked_{pk}"] = True
        liked = True

    post.save()
    post.refresh_from_db()

    return JsonResponse({
        "likes": post.like,
        "liked": liked
    })