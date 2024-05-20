from django.shortcuts import render , redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from authentification.models import Profile
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Post,Event,EventClub,EventSocial,Transport,Recommandation,Stage,Logement

from .models import Follow , Reservation
from .models import Comment
from .models import Notification
from itertools import chain
from django.utils.timesince import timesince
from django.utils import timezone

from datetime import datetime, timedelta

# Create your views here.


def profile(request , pk):
    #user = request.user
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    posts = Post.objects.filter(user=user_object)
    user_post_length = len(posts)
    reservations = Reservation.objects.filter(userPost=request.user)

        # Check if the current user follows the user whose profile is being viewed
    if request.user.is_authenticated:
        follower = request.user
        #print(follower) user current log in
        #print(user_object) visit user
        if Follow.objects.filter(follower=follower, followed_user=user_object).exists():
            button_text = 'Unfollow'
        else:
            button_text = 'Follow'
    else:
        button_text = None
    #print('button_text', button_text)
    # Get the count of followers and following
    user_followers = Follow.objects.filter(followed_user=user_object).count()
    user_following = Follow.objects.filter(follower=user_object).count()

    posts_all =[]
    img_url_like = []
    for post in posts :
        liked_posts = post.likes.all()[:3]
        fan_profile = [Profile.objects.get(user=fan) for fan in liked_posts]

        comments = Comment.objects.filter(post=post)
        post_comments = []
        num_comments = comments.count()
        for comment in comments:
            comment_user = comment.user
            comment_profile = Profile.objects.get(user=comment_user)
            comment_text = comment.text

            post_comments.append({'text': comment_text, 'profile': comment_profile})

        POST = {
            'post':post ,
            'fan_profile' : fan_profile ,
            'comments': post_comments,
            'num_comments': num_comments
        }
        posts_all.append({'post':POST , 'profile_img': user_profile.profileimg.url })
    return render(request, './account/profile.html' , {'user_profile' : user_profile ,
                       'reservations' : reservations , 'user' : follower ,    'user_object':user_object,   'user_followers': user_followers,
        'user_following': user_following, 'button_text': button_text, 'posts_all' : posts_all , 'user_post_length' : user_post_length})





def index(request):
    #! if age of post more than  1 month deleted

    now = timezone.now()
    posts = Post.objects.all()
    for post in posts:
        if post.created_at + timedelta(days=30) <= now:
            post.delete()

    #! method filter
    if request.method == 'POST':
        selected_events = request.POST.getlist('events')
        posts = []
        if 'allPosts' in selected_events:
            posts.extend(Post.objects.all())
        if 'All_events' in selected_events:
            posts.extend(Event.objects.all())
        if 'EventSocial' in selected_events:
            posts.extend(EventSocial.objects.all())
        if 'EventClub' in selected_events:
            posts.extend(EventClub.objects.all())
        if 'Transport' in selected_events:
            posts.extend(Transport.objects.all())
        if 'Logement' in selected_events:
            posts.extend(Logement.objects.all())
        if 'Recommandation' in selected_events:
            posts.extend(Recommandation.objects.all())
        if 'Stage' in selected_events:
            posts.extend(Stage.objects.all())
        if not posts:
            posts = Post.objects.all()
    else:
        posts = Post.objects.all()
    
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    posts_all = []
    profiles = Profile.objects.all()
    
    img_url_like = []

    Users_You_Can_Follow = []

    # Get the list of users the current user follows
    following_users = Follow.objects.filter(follower=request.user)
    unread_notifications_count = Notification.objects.exclude(user_notification=request.user, is_read=False).count()
    notifications = Notification.objects.filter(user_post=request.user).order_by('-timestamp')
    
    for profile in profiles:
        user_p = profile.user
        if user_p != request.user:
            # Check if the user is not in the following_users list
            if not following_users.filter(followed_user=user_p).exists():
                num_followers = Follow.objects.filter(followed_user=user_p).count()
                Users_You_Can_Follow.append({'profile': profile, 'num_followers': num_followers})


    notification_details = []
    for notification in notifications:
        user_profile = Profile.objects.get(user=notification.user_notification)
        timestamp = timesince(notification.timestamp, timezone.now())

        notification_detail = {
            'user_profile': user_profile,
            'notification_type': notification.notification_type,
            'timestamp': timestamp,
            'is_read': notification.is_read
        }
        notification_details.append(notification_detail)
    
    for post in posts :
        liked_posts = post.likes.all()[:3]
        fan_profile = [Profile.objects.get(user=fan) for fan in liked_posts]
        profile_img = Profile.objects.get(user=post.user).profileimg
        comments = Comment.objects.filter(post=post)
        post_comments = []
        num_comments = comments.count()
        for comment in comments:
            comment_user = comment.user
            comment_profile = Profile.objects.get(user=comment_user)
            comment_text = comment.text

            post_comments.append({'text': comment_text, 'profile': comment_profile})

        POST = {
            'post': post,
            'fan_profile': fan_profile,
            'comments': post_comments,
            'num_comments': num_comments
        }

        posts_all.append({'post':POST , 'profile_img': profile_img })
    return render(request, './account/index.html' , {'user_profile': user_profile , 'notification_details' : notification_details ,
                  'unread_notifications_count' : unread_notifications_count ,  'Users_You_Can_Follow' : Users_You_Can_Follow ,'posts_all' :posts_all})


@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return render(request, './account/search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def Follow_user(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        follower = User.objects.get(username=follower)
        #print('follower',follower) # user log in
        user = request.POST['user'] 
        user = User.objects.get(username=user)
        #print('user',user) # visiteur

        if Follow.objects.filter(follower=follower, followed_user=user).exists():
            delete_follower = Follow.objects.get(follower=follower, followed_user=user)
            delete_follower.delete()
            return redirect('/account/profile/'+user.username)
        else:
            new_follower = Follow.objects.create(follower=follower, followed_user=user)
            new_follower.save()
            notification = Notification.objects.create(
                user=new_follower.follower,
                notification_type='follow',
                follow=new_follower
            )
            notification.save()
            return redirect('/account/profile/'+user.username)
    else:
        return redirect('/')
    

@login_required(login_url='signin')
def edit_photo_profile(request):
    user = request.user
    
    user_profile = Profile.objects.get(user=user)
    if request.FILES.get('image_profile') != None:
        image = request.FILES.get('image_profile')
        #print("image " , image)
        user_profile.profileimg =image
        user_profile.save()
    return redirect('profile/'+user.username)


@login_required(login_url='signin')
def addComment(request):
    if request.method == 'POST':
        
        user_comment = request.POST['user_comment']
        user_comment = User.objects.get(username=user_comment)
        print('user_comment ', user_comment)
        post_comment = request.POST['post_comment']
        post_comment = Post.objects.get(id=post_comment)
        print('post_comment ', post_comment)
        comment = request.POST['comment']
        if user_comment and post_comment and comment:
            comment = Comment.objects.create(
                user=user_comment,
                post=post_comment,
                text=comment,
            )
            comment.save()
            notification = Notification.objects.create(
                user_post=post_comment.user,
                user_notification=post_comment.user,
                notification_type='comment',
                comment=comment
            )
            notification.save()


    return redirect('/')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required(login_url='signin')
def like_post(request):
    user_object = request.user
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    
    if user_object in post.likes.all():
        post.likes.remove(user_object)
        post.no_of_likes -= 1
    else:
        post.likes.add(user_object)
        post.no_of_likes += 1
        
    post.save()
    """ notification = Notification.objects.create(
                user_notification=user_of_reser ,
                user_post=user_of_post,
                notification_type='Reservation',
            ) 
    notification.save() """
    
    return redirect('/')


@login_required(login_url='signin')
def addPost( request ):
    return render(request, './account/addPost.html' )


@login_required(login_url='signin')
def add_post(request):
    if request.method == 'POST':
        post_type = request.POST.get('postType')
        user = request.user
        image = request.FILES.get('image_upload')
        caption = request.POST.get('caption')

        if post_type == 'post':
            post = Post.objects.create(user=user, image=image, caption=caption , type="post")

        elif post_type in ['Event', 'EventClub', 'EventSocial']:
            intitule = request.POST.get('intitule')
            description = request.POST.get('description')
            lieu = request.POST.get('lieu')
            contact_info = request.POST.get('contactInfo')

            if post_type == 'Event':
                post = Event.objects.create(user=user, image=image, caption=caption,
                                            intitule=intitule, description=description,
                                            lieu=lieu, contactInfo=contact_info, type="event")
            elif post_type == 'EventClub':
                club = request.POST.get('club')
                post = EventClub.objects.create(user=user, image=image, caption=caption,
                                                intitule=intitule, description=description,
                                                lieu=lieu, contactInfo=contact_info, club=club, type="eventClub")
            elif post_type == 'EventSocial':
                prix = float(request.POST.get('prix'))
                post = EventSocial.objects.create(user=user, image=image, caption=caption,
                                                  intitule=intitule, description=description,
                                                  lieu=lieu, contactInfo=contact_info, prix=prix, type="eventSocial")

        elif post_type == 'Stage':
            type_stg = int(request.POST.get('typestg'))
            societe = request.POST.get('societe')
            duree = int(request.POST.get('duree'))
            sujet = request.POST.get('sujet')
            contact_info = request.POST.get('contactInfo')
            specialite = request.POST.get('specialite')

            post = Stage.objects.create(user=user, image=image, caption=caption,
                                        typeStg=type_stg, societe=societe, duree=duree,
                                        specialite=specialite, sujet=sujet, contactInfo=contact_info, type="stage")

        elif post_type == 'Logement':
            local = request.POST.get('localisation')
            description = request.POST.get('description')
            contact_info = request.POST.get('contactInfo')

            post = Logement.objects.create(user=user, image=image, caption=caption,
                                            localisation=local, description=description, contactInfo=contact_info, type="logement")

        elif post_type == 'Transport':
            dep = request.POST.get('depart')
            dest = request.POST.get('destination')
            datedepart = request.POST.get('datedepart')
            hdep = request.POST.get('heureDepart')
            nbr_sieges = request.POST.get('nbrSieges')
            contact_info = request.POST.get('contactInfo')

            post = Transport.objects.create(user=user, image=image, caption=caption,
                                            depart=dep, destination=dest, heureDep=hdep, datedepart=datedepart,
                                            contactInfo=contact_info, nbrSieges=nbr_sieges, type="transport")

        elif post_type == 'Recommandation':
            text = request.POST.get('text')
            post = Recommandation.objects.create(user=user, image=image, caption=caption, text=text, type="recommandation")

        post.save()
        return redirect('/')

    return redirect('/')


@login_required(login_url='signin')
def PostDelete(request):
    if request.method == 'POST':
        id = request.POST.get('idPostDelete')
        post = Post.objects.filter(id=id)
        post.delete()
        return redirect('/account')  
    return redirect('/account')


@login_required(login_url='signin')
def PostDetails(request):
    if request.method == 'POST':
        post_id = request.POST.get('idPostDetails')
        
        post = Post.objects.get(id=post_id)
        print(post)
        if post.type == 'stage':
            post_details = Stage.objects.get( id=post_id)
        elif post.type == 'logement':
            post_details = Logement.objects.get(id=post_id)
        elif post.type == 'transport':
            post_details = Transport.objects.get(id=post_id)
        elif post.type == 'recommandation':
            post_details = Recommandation.objects.get(id=post_id)
        elif post.type == 'eventClub':
            post_details = EventClub.objects.get(id=post_id)
        elif post.type == 'eventSocial':
            post_details = EventSocial.objects.get(id=post_id)
        else:
            post_details = post
            pass
        #print(post_details.type)
        user_profile = Profile.objects.get(user=post_details.user)
        img_url_like = []

        liked_posts = post_details.likes.all()[:3]
        fan_profile = [Profile.objects.get(user=fan) for fan in liked_posts]
        profile_img = user_profile.profileimg
        comments = Comment.objects.filter(post=post_details)
        post_comments = []
        num_comments = comments.count()
        for comment in comments:
            comment_user = comment.user
            comment_profile = Profile.objects.get(user=comment_user)
            comment_text = comment.text

            post_comments.append({'text': comment_text, 'profile': comment_profile})

        POST = {
            'post': post_details,
            'fan_profile': fan_profile,
            'comments': post_comments,
            'num_comments': num_comments,
            'profile_img': profile_img
        }



        context = {'post': POST}
        return render(request, 'postDetails.html', context)
    else:
        return redirect('/')


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    user = request.user
   
    if request.method == 'POST':
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        email = request.POST['email']
        bio = request.POST['bio']
        location = request.POST['location']
        phoneNumber = request.POST['phoneNumber']
        utilisateur = request.POST['utilisateur']
        
        print(user_profile.user.first_name)
        print(firstName)
        user.first_name = firstName
        user.last_name = lastName
        user.email = email

        user_profile.bio = bio
        user_profile.location = location
        user_profile.phoneNumber = phoneNumber
        user_profile.utilisateur = utilisateur
        user_profile.save()
        user.save()
        return redirect('settings')
    #return render(request, 'setting.html' , {'user_profile': user_profile})
    #user_profile = get_object_or_404(Profile, user=request.user)
    return render(request, './account/setting.html' , {'user_profile': user_profile } )


@login_required(login_url='signin')
def reservation (request):
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    user_of_post= post.user
    user_of_reser = request.user
    reservation = Reservation.objects.create(
        post=post ,
        userPost = post.user ,
        user = user_of_reser ,
    )
    reservation.save()

    notification = Notification.objects.create(
                user_notification=user_of_reser ,
                user_post=user_of_post,
                notification_type='Reservation',
                ) 
    notification.save()
    return redirect('/')
    
def confirm_reservation(request):
    reservation_id = request.POST.get('reservation_id')
    print(reservation_id)
    reservation = Reservation.objects.get(id=reservation_id)
    reservation.confirmed = True
    reservation.save()
    return redirect('/')