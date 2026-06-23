from django.shortcuts import render
from blog.models import Post, ReplayComment
from django.contrib import messages
from django.shortcuts import redirect
from blog.form import CommentForm
from django.shortcuts import render, get_object_or_404

# Create your views here.
def blog_grid(request):
    posts = Post.objects.filter(status = True)

    context={"posts":posts}
    return render(request, 'blog/blog-grid.html', context)

def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=True)

    posts = Post.objects.filter(status = True)
    comments = post.comment.all()

    if request.method == 'POST':

        form_type = request.POST.get('form_type')

        if form_type == 'comment':
            form = CommentForm(request.POST)

            if form.is_valid():
                comment_obj = form.save(commit=False)
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