
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Post, Comment, VoteOption
from .forms import PostForm
from .forms import LoginForm

def index_view(request):
    popular = Post.objects.order_by('-created_at')[:5]
    return render(request, "index.html", {"popular": popular})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            for text in request.POST.getlist('options[]'):
                if text.strip():
                    VoteOption.objects.create(post=post, text=text.strip())
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm()
    return render(request, "create_post.html", {"form": form})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST' and 'comment' in request.POST:
        Comment.objects.create(post=post, user=request.user, text=request.POST['comment'])
    total_votes = sum(opt.vote_count for opt in post.options.all()) or 1
    return render(request, "post_detail.html", {"post": post, "total": total_votes})

@login_required
def profile_view(request):
    favorites = Post.objects.filter(author=request.user)[:3]
    history = Post.objects.order_by('-created_at')[:5]
    return render(request, "profile.html", {"favorites": favorites, "history": history})

def register_view(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('login_view')
    return render(request, "register.html", {"form": form})

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('index')
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('login_view')

def index_view(request):
    recommended_comics = [
        {
            "id": 1,
            "title": "AM&PM",
            "image_url": "/static/images/AM&PM.jpg",
            "likes": 3021,
        },
        {
            "id": 2,
            "title": "姊夫",
            "image_url": "/static/images/姊夫.jpg",
            "likes": 1422,
        },
        {
            "id": 3,
            "title": "膽大黨",
            "image_url": "/static/images/膽大黨.jpg",
            "likes": 980,
        },
        {
            "id": 4,
            "title": "我的Vtuber女友",
            "image_url": "/static/images/我的Vtuber女友.jpg",
            "likes": 801,
        },
        {
            "id": 5,
            "title": "和尚日常",
            "image_url": "/static/images/和尚日常｜竹筍日常｜.jpeg",
            "likes": 2087,
        },
        {
            "id": 6,
            "title": "Madder & Teal",
            "image_url": "/static/images/Madder & Teal.png",
            "likes": 1593,
        },
    ]
    return render(request, "index.html", {
        "recommended_comics": recommended_comics
    })

# 漫畫詳情 view
def comic_detail_view(request, comic_id):
    comic_map = {
        1: {
            "title": "AM&PM",
            "description": "這是 AM&PM 的詳細內容。",
            "image_url": "/static/images/am_pm.jpg"
        },
        2: {
            "title": "姊夫",
            "description": "這是姊夫的介紹頁面。",
            "image_url": "/static/images/姊夫.jpg"
        },
        # 其他可擴充
    }
    comic = comic_map.get(comic_id, {
        "title": "未知漫畫",
        "description": "沒有找到此作品。",
        "image_url": "/static/images/default.jpg"
    })
    return render(request, "comic_detail.html", {"comic": comic})

def comic_detail_view(request, comic_id):
    comics = {
        1: {
            "title": "AM&PM",
            "image_url": "/static/images/AM&PM.jpg",
            "chapter": "第110話",
            "updated": "2025-05-20",
            "author": "JEAL阿柩",
            "categories": "愛情,",
            "status": "在連載中",
            "description": "兩一名在超商值大夜班的大學生，經常在凌晨五點與晚上十一點遇見同一位男高中生，逐漸產生好奇並展開交集——直到某天，熟悉的臉孔同時出現在店門口。",
            "comments": [
                {"user": "小月", "time": "2025-05-21 21:00", "text": "我超愛這對CP！！"},
                {"user": "匿名讀者", "time": "2025-05-20 18:40", "text": "劇情意外的有深度"},
            ],
        },
        2: {
            "title": "姊夫",
            "image_url": "/static/images/姊夫.jpg",
            "chapter": "第110話",
            "updated": "2025-05-20",
            "author": "一滴馬克非",
            "categories": "愛情,",
            "status": "在連載中",
            "description": "姊夫與小舅子相愛相殺的激情故事～～～ 【這注意！這是肉漫！是肉漫！是肉漫！三觀不正，主角瘋癲，高道德標準者請慎入，別點入後還開罵，謝謝體諒(^ ^)＞】。",
            "comments": [
                {"user": "小月", "time": "2025-05-21 21:00", "text": "我超愛這對CP！！"},
                {"user": "匿名讀者", "time": "2025-05-20 18:40", "text": "劇情意外的有深度"},
            ],
        },
        3: {
            "title": "膽大黨",
            "image_url": "/static/images/膽大黨.jpg",
            "chapter": "第195話",
            "updated": "2025-05-20",
            "author": "龍年伸",
            "categories": "科幻, 愛情, 神鬼, 校園",
            "status": "在連載中",
            "description": "認為幽靈存在但不相信外星人存在，喜歡演員高倉健的綾瀨桃，班上有一個相信外星人存在但不相信幽靈存在的超自然宅·高倉健。兩人為了證明自己的是唯一正解，各自前往兩個靈異聖地，高倉健遇到高速婆婆，綾瀨桃被帶往飛碟，外星人要取走兩人的性器官，千鈞一發間，小桃的力量開竅，兩人擊敗外星人脫困。風波過去，高倉健的蛋蛋少了一顆？",
            "comments": [
                {"user": "ahrxoy", "time": "2025-05-21 22:07", "text": "宗一!! Guru又出現了啊！！不對！！！！！"},
                {"user": "979****45", "time": "2025-05-21 14:53", "text": "編輯是不是腦袋有洞？"},
                {"user": "木玄", "time": "2025-05-21 13:43", "text": "太猛了這劇情"},
            ]
        },
        4: {
            "title": "我的Vtuber女友",
            "image_url": "/static/images/我的Vtuber女友.jpg",
            "chapter": "第195話",
            "updated": "2025-05-20",
            "author": "甜椒工房 Paprika Factory",
            "categories": "愛情，劇情",
            "status": "在連載中",
            "description": "熱愛唱歌的社恐宅女妙妙到男友工作的媒體公司應徵Vtuber—成為閃閃發光的虛擬偶像！但…現實還是沒想像中容易呢><“！！妙妙能否渡過重重難關成為大家心中的偶像，並捍衛到自己的愛情呢:3？",
            "comments": [
                {"user": "ahrxoy", "time": "2025-05-21 22:07", "text": "宗一!! Guru又出現了啊！！不對！！！！！"},
                {"user": "979****45", "time": "2025-05-21 14:53", "text": "編輯是不是腦袋有洞？"},
                {"user": "木玄", "time": "2025-05-21 13:43", "text": "太猛了這劇情"},
            ]
        },
        5: {
            "title": "和尚日常｜竹筍日常｜",
            "image_url": "/static/images/和尚日常｜竹筍日常｜.jpeg",
            "chapter": "第195話",
            "updated": "2025-05-20",
            "author": "龍年伸",
            "categories": "搞笑，生活動作",
            "status": "在連載中",
            "description": "如果和尚主動去找妖魔鬼怪，會產生怎麼樣的火花呢！",
            "comments": [
                {"user": "ahrxoy", "time": "2025-05-21 22:07", "text": "宗一!! Guru又出現了啊！！不對！！！！！"},
                {"user": "979****45", "time": "2025-05-21 14:53", "text": "編輯是不是腦袋有洞？"},
                {"user": "木玄", "time": "2025-05-21 13:43", "text": "太猛了這劇情"},
            ]
        },
        6: {
            "title": "Madder & Teal",
            "image_url": "/static/images/Madder & Teal.png",
            "chapter": "第195話",
            "updated": "2025-05-20",
            "author": "海塩子",
            "categories": "劇情，愛情",
            "status": "在連載中",
            "description": "排球校隊隊長的徐雪與人氣獨立樂團主唱的夏月，兩個大學女生距離逐漸拉近的合租室友日常。",
            "comments": [
                {"user": "ahrxoy", "time": "2025-05-21 22:07", "text": "宗一!! Guru又出現了啊！！不對！！！！！"},
                {"user": "979****45", "time": "2025-05-21 14:53", "text": "編輯是不是腦袋有洞？"},
                {"user": "木玄", "time": "2025-05-21 13:43", "text": "太猛了這劇情"},
            ]
        },
        # 更多 comic 可擴充於此...
    }

    comic = comics.get(comic_id)
    if not comic:
        return render(request, "404.html", status=404)
    return render(request, "comic_detail.html", {"comic": comic})
