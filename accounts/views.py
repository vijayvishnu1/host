import time
from datetime import datetime
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db.models.functions import Concat
from django.db.models import Value
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import *
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from .token import account_activation_token
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.utils import timezone

User = settings.AUTH_USER_MODEL
User = get_user_model()


# Create your views here.

def home(request):
    return render(request, 'accounts/HOME.html')


def Regtype(request):
    return render(request, 'accounts/regtype.html')


def message(request):
    return render(request, 'accounts/Message.html')


def Features(request):
    return render(request, 'accounts/features.html')


def Testimonials(request):
    return render(request, 'accounts/TESTIMONALS.html')


def Clientfindanadvocate(request):
    return render(request, 'accounts/client find an advocate.html')


def advocate_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_advocate:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')

    return wrapper


def client_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_client:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')

    return wrapper


@login_required(login_url='login')
def Contactus(request):
    context = {}
    if request.method == "POST":
        form = ContactusForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            email = form.cleaned_data.get("email")
            message = form.cleaned_data.get("message")
            obj = contactus.objects.create(name=name, email=email, message=message)
            obj.save()
            messages.success(request, 'message submitted our team will contact you soon')
            return redirect('message')
    else:
        form = ContactusForm()
    context['form'] = form
    return render(request, 'accounts/contactus.html', context)


@login_required(login_url='login')
def clientheaderview(request):
    user = request.user
    obj = Clientprofiles.objects.filter(user=user)
    k = user.Clientprofiles.objects.get
    return render(request, 'accounts/clientheader.html', {'obj': obj})


@login_required(login_url='login')
@client_required
def cprofileview(request):
    user = request.user
    obj = Clientprofiles.objects.filter(user=user)
    con = Client.objects.filter(user=user)
    return render(request, 'accounts/clientprofile.html', {'obj': obj, 'con': con})


# --------------Client register----------------------------------------------------------------

def Client_register(request):
    if request.user.is_authenticated:
        return redirect('clienthome')
    else:
        form = ClientSignUpForm()
        if request.method == 'POST':
            form = ClientSignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.is_active = False
                user.save()
                username = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for client ' + username)

                current_site = get_current_site(request)
                mail_subject = 'Activation link has been sent to your email id..kindly confirm your email..'
                message = render_to_string('accounts/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return HttpResponse(
                    'Please confirm your email address to complete the registration..and activate your account')
        else:
            form = ClientSignUpForm()
        return render(request, 'accounts/clientreg.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'successfully confirmed your email..')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def Advocate_register(request):
    if request.user.is_authenticated:
        return redirect('advocatehome')
    else:
        form = AdvocateSignUpForm()
        if request.method == 'POST':
            form = AdvocateSignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.is_active = False
                user.save()
                username = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for advocate ' + username)
                current_site = get_current_site(request)
                mail_subject = 'Activation link has been sent to your email id..kindly confirm your email..'
                message = render_to_string('accounts/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return HttpResponse(
                    'Please confirm your email address to complete the registration..and activate your account')
        else:
            form = AdvocateSignUpForm()
        return render(request, 'accounts/advocatereg.html', {'form': form})


def loginuser(request):
    if request.user.is_authenticated and request.user.is_client == True:
        return redirect('clienthome')
    elif request.user.is_authenticated and request.user.is_advocate == True:
        return redirect('advocatehome')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)

            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                auth.login(request, user)
                if user.is_authenticated and user.is_client == True:
                    return redirect('clienthome')
                if user.is_authenticated and user.is_advocate == True:
                    return redirect('advocatehome')



                if user is not None:
                    login(request, user)
                    return redirect('/')
                else:

                    messages.error(request, "Invalid username or password")
            else:
                messages.error(request, "Invalid username or password")

        # context={'form':AuthenticationForm()}
        form = AuthenticationForm()
        # recaptcha = FormWithCaptcha() ,"recaptcha": recaptcha
        return render(request, 'accounts/login.html', {"form": form})


########################################-client-#####################################################################


# @@@@@@----client profile----@@@@@@@@@@
@login_required(login_url='login')
@client_required
def Clientprofile(request):
    context = {}
    if request.method == "POST":
        form = ClientprofileForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            house_name = form.cleaned_data.get("house_name")
            city = form.cleaned_data.get("city")
            district = form.cleaned_data.get("district")
            state = form.cleaned_data.get("state")
            postoffice = form.cleaned_data.get("postoffice")
            picode = form.cleaned_data.get("picode")
            pimage = form.cleaned_data.get("pimage")
            date_of_birth = form.cleaned_data.get("date_of_birth")
            obj = Clientprofiles.objects.create(house_name=house_name, city=city, district=district, user=user,
                                                state=state, postoffice=postoffice, picode=picode, pimage=pimage,
                                                date_of_birth=date_of_birth)
            obj.save()
            messages.success(request, 'successfully created your profile')
            return redirect('message')
    else:
        form = ClientprofileForm()
    context['form'] = form
    return render(request, 'accounts/clientprofileedit.html', context)


@login_required(login_url='login')
@client_required
def clientprofileupdate(request, pk):
    clientprofiles = Clientprofiles.objects.get(id=pk)
    form = ClientprofileForm(instance=clientprofiles)
    if request.method == 'POST':
        form = ClientprofileForm(request.POST, request.FILES, instance=clientprofiles)
        if form.is_valid():
            user = request.user
            obj = form.save(commit=False)
            obj.user = user
            obj.save()
            messages.success(request, 'successfully updated your profile')
            return redirect('message')
    context = {'form': form}
    return render(request, 'accounts/clientprofileedit.html', context)




@login_required(login_url='login')
def feedbackclientview(request):
    context = {}
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data.get("rating")
            description = form.cleaned_data.get("description")
            user = request.user
            obj = Clientfeedback.objects.create(rating=rating, description=description, user=user)
            obj.save()
            messages.success(request, 'thank you for your response')
            return redirect('message')
    else:
        form = FeedbackForm()
    context['form'] = form
    return render(request, 'accounts/clientfeedback.html', context)


###################################----client case  pdf--------##################################################################
@login_required(login_url='login')

def users_render_pdf_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    user = get_object_or_404(Clientcase, pk=pk)

    template_path = 'accounts/client_case_generate_pdf.html'
    context = {'user': user}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    # to directly download the pdf we need attachment
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # to view on browser we can remove attachment
    response['Content-Disposition'] = 'filename="report.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


# def logoutUser(request):
#     logout(request)
#     return redirect('login')

#
def logoutUser(request):
    if request.user.is_authenticated:
        user_status = UserStatus.objects.get(user=request.user)
        user_status.is_online = False
        user_status.last_seen = timezone.now()
        user_status.save()
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@client_required
def Clienthome(request):
    user = request.user
    user_status, created = UserStatus.objects.get_or_create(user=user)
    if request.user.is_authenticated:
        user_status.is_online = True
    else:
        user_status.is_online = False
        user_status.last_seen = timezone.now()
    user_status.save()
    case_count = Clientcase.objects.filter(user=user).count()
    assignned_count = CaseAssignment.objects.filter(requested_by=user).count()
    context = {'case_count': case_count, 'assignned_count': assignned_count}
    return render(request, 'accounts/clienthome.html', context)



# ----------------Forgot password----------------------------------------------------------------------

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        User = get_user_model()
        if User.objects.filter(email=email).exists():

            user = User.objects.get(email__exact=email)

            # Reset password email

            current_site = get_current_site(request)
            mail_subject = 'forgot password link has been send to your email id'
            message = render_to_string('accounts/ResetPassword_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            send_mail(
                'Please activate your account',
                message,
                'ajcejobportal@gmail.com',
                [email],
                fail_silently=False,
            )

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'accounts/Forgot_Password.html')


def resetpassword_validate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        # uid = urlsafe_base64_decode(uidb64).decode()
        # user = User._default_manager.get(pk=uid)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # if user is not None and default_token_generator.check_token(user, token):
    if user is not None and account_activation_token.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            User = get_user_model()
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/ResetPassword.html')


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! client advocate search box !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

@login_required(login_url='login')
@client_required
def search(request):
    advocates = Advocate.objects.all()
    specializations = list(set([advocate.specifications for advocate in advocates]))
    sort_by = request.GET.get('specifications')
    search_query = request.GET.get('q')
    if sort_by:
        advocates = advocates.filter(specifications=sort_by).order_by('user__first_name')
    else:
        advocates = advocates.order_by('user__first_name')

    if search_query:
        advocates = advocates.filter(
            Q(user__first_name__icontains=search_query) | Q(user__last_name__icontains=search_query))



    context = {'advocates': advocates, 'specializations': specializations}
    return render(request, 'accounts/c_search.html', context)

@login_required(login_url='login')
@client_required
def advocate_details(request, id):
    advocate = User.objects.select_related('advocate').get(pk=id)
    return render(request, 'accounts/adv_detailed_search_view.html', {'advocate': advocate})


    ##@@@@@@@@@@@@@----client case----@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@login_required(login_url='login')
@client_required
def Clientcaseregister(request):
    context = {}
    if request.method == "POST":
        form = ClientcaseForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.is_notrequested = True
            obj.save()
            messages.success(request, 'successfully registered your case')
            return redirect('message')
    else:
        form = ClientcaseForm()
    context['form'] = form
    return render(request, 'accounts/1.html', context)
@login_required(login_url='login')
@client_required
def clientcaseview(request):
    user = request.user
    obj = Clientcase.objects.filter(user=user)
    return render(request, 'accounts/clientcaseview.html', {'obj': obj})
@login_required(login_url='login')
@client_required
def clientcaseupdate(request, pk):
    clientcase = get_object_or_404(Clientcase, case_id=pk, user=request.user)
    form = ClientcaseForm(instance=clientcase)
    if request.method == 'POST':
        form = ClientcaseForm(request.POST, request.FILES, instance=clientcase)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Successfully updated your case')
            return redirect('message')
    context = {'form': form}
    return render(request, 'accounts/1.html', context)
@login_required(login_url='login')
@client_required
def deleteclientcase(request, pk):
    clientcase = Clientcase.objects.get(case_id=pk)
    if request.method == "POST":
        clientcase.delete()
        messages.success(request, 'successfully deleted your case')
        return redirect('message')
    context = {'item': clientcase}
    return render(request, 'accounts/clientcasedelete.html', context)


# ___@@@@@@@@@@@@@@@@@@@@@@@@____CLIENT CASE MANAGEMENT REQUEST ASSISTANCE_________@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@____
@login_required(login_url='login')
@client_required
def Client_case_management(request):
    return render(request, 'accounts/clientcasemanagement.html')
@login_required(login_url='login')
@client_required
def Client_case_option(request):
    return render(request, 'accounts/client_case_option.html')
@login_required(login_url='login')
@client_required
def Client_service_option(request):
    return render(request, 'accounts/client_service_option.html')


@login_required(login_url='login')
@client_required
def advocate_list(request):
    advocates = Advocate.objects.all()
    specializations = list(set([advocate.specifications for advocate in advocates]))
    sort_by = request.GET.get('specifications')
    search_query = request.GET.get('q')
    if sort_by:
        advocates = advocates.filter(specifications=sort_by).order_by('user__first_name')
    else:
        advocates = advocates.order_by('user__first_name')

    if search_query:
        advocates = advocates.filter(
            Q(user__first_name__icontains=search_query) | Q(user__last_name__icontains=search_query))

    context = {'advocates': advocates, 'specializations': specializations}
    return render(request, 'accounts/advocate_list.html', context)


@login_required(login_url='login')
@client_required
def chat(request, advocate_id=None):
    user = request.user
    client = Client.objects.get(user=user)
    advocates = Advocate.objects.filter(caseassignment__case__user=user).distinct()

    if advocate_id:
        advocate = Advocate.objects.get(pk=advocate_id)
        if request.method == 'POST':
            message = request.POST.get('message')
            receiver = advocate.user
            new_message = Message(sender=user, receiver=receiver, message=message)
            new_message.save()


        messages = Message.objects.filter(
            Q(sender=user, receiver=advocate.user) | Q(sender=advocate.user, receiver=user)).order_by('timestamp')

        # Get the UserStatus object of the advocate
        advocate_status = UserStatus.objects.get(user=advocate.user)
        if advocate_status.is_online:
            advocate_status_message = 'online'
        else:
            advocate_status_message = 'last seen ' + str(advocate_status.last_seen)

        return render(request, 'accounts/chat.html',
                      {'advocates': advocates, 'advocate': advocate, 'messages': messages,
                       'advocate_status_message': advocate_status_message})
    else:
        return render(request, 'accounts/chat.html', {'advocates': advocates})


from textblob import TextBlob
import json

def view_feedback(request, advocate_id):
    reviews = Review.objects.filter(advocate=advocate_id)
    data = {'positive': 0, 'neutral': 0, 'negative': 0}
    comments = []
    for review in reviews:
        comments.append(review.comment)
        analysis = TextBlob(review.comment)
        if analysis.sentiment.polarity > 0:
            data['positive'] += 1
        elif analysis.sentiment.polarity == 0:
            data['neutral'] += 1
        else:
            data['negative'] += 1
    data = json.dumps(data)
    context = {
        'reviews': reviews,
        'comments': comments,
        'data': data,
    }
    return render(request, 'accounts/viewfeedback.html', context)



@login_required(login_url='login')
@client_required
def assign_case(request, id):
    context = {}
    if request.method == "POST":
        form = CaseAssignmentForm(request.POST)
        if form.is_valid():
            advocate = Advocate.objects.get(user_id=id)
            requested_by = request.user
            case = form.cleaned_data['case']

            if CaseAssignment.objects.filter(case=case, advocate=advocate).exists():
                messages.warning(request, f'{advocate} is already assigned to this case.')
                return redirect('message')
            elif case.is_requested:
                messages.warning(request,
                                 'This case cannot be requested to this advocate because it has already been requested to another advocate and is in the pending stage. kindly wait for further updates.....')
                return redirect('message')
            else:
                obj = CaseAssignment.objects.create(advocate=advocate, requested_by=requested_by, case=case)
                obj.save()
                case.is_requested = True
                case.is_pending = True
                case.is_notrequested = False
                case.save()
                messages.success(request, 'Request sent successfully')
                return redirect('message')
    else:
        form = CaseAssignmentForm()
    context['form'] = form
    return render(request, 'accounts/clientassign_case.html', context)

def client_case_management_view(request):
    user = request.user.id
    assignments = CaseAssignment.objects.filter(requested_by=user)
    cases = []
    for assignment in assignments:
        case = assignment.case
        advocate = assignment.advocate
        if case.is_requested == True or case.is_pending == True:
            cases.append({
                'assignment': assignment,
                'advocate': advocate,
            })
    return render(request, 'accounts/clientcasemanagement.html', {'cases': cases})


@login_required(login_url='login')
@client_required
def client_request_cancel(request, pk):
    case_assignment = get_object_or_404(CaseAssignment, id=pk)
    case_assignment_history = get_object_or_404(CaseAssignment, id=pk)
    client_case = case_assignment.case
    client_case.is_rejected = False
    client_case.is_notrequested = True
    client_case.is_requested = False
    client_case.is_pending = False
    client_case.save()
    case_assignment_history.delete()
    messages.success(request, 'Assignment Request Canceled Successfully')
    return redirect('message')


def add_review(request, id):
    advocate = Advocate.objects.get(user_id=id)
    user = request.user

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            if CaseAssignment.objects.filter(requested_by=user, advocate=advocate).exists():
                # Create a Client object for the logged-in user
                client, created = Client.objects.get_or_create(user=user)

                review = form.save(commit=False)
                review.advocate = advocate
                review.client = client
                review.save()
                messages.success(request, 'Your review has been submitted.')
                return redirect('message')
            else:
                messages.warning(request, 'You cannot give a review to this advocate.')
                return redirect('message')

    else:
        form = ReviewForm()

    return render(request, 'accounts/add_review.html', {'form': form, 'advocate': advocate})







from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def advocate_recommendation_view(request, case_type):
    # Get all advocates with the given case type
    advocates = Advocate.objects.filter(specifications=case_type)

    # Get the current client
    client = request.user.client

    # Get all reviews for this client
    client_reviews = Review.objects.filter(client=client)

    # Create a dictionary to store the review ratings and comments for each advocate
    advocate_reviews = {}
    # Iterate over all reviews and store them in the dictionary for each advocate
    for review in client_reviews:
        advocate = review.advocate
        if advocate in advocate_reviews:
            advocate_reviews[advocate]['ratings'].append(review.rating)
            advocate_reviews[advocate]['comments'].append(review.comment)
        else:
            advocate_reviews[advocate] = {'ratings': [review.rating], 'comments': [review.comment]}

    # Create a dictionary to store the cosine similarity score for each advocate
    advocate_scores = {}
    for advocate in advocates:
        if advocate in advocate_reviews:
            ratings = advocate_reviews[advocate]['ratings']
            comments = advocate_reviews[advocate]['comments']
            if ratings and comments:  # Check if lists are non-empty
                # Convert the comments into a document-term matrix
                vectorizer = CountVectorizer(stop_words='english')
                dtm = vectorizer.fit_transform(comments)
                # Calculate the cosine similarity score between the document-term matrix and the case_type vector
                case_type_vector = vectorizer.transform([case_type])
                score = cosine_similarity(dtm, case_type_vector)[0][0]
                advocate_scores[advocate] = score

    # Sort the advocates based on their cosine similarity score
    sorted_advocates = sorted(advocate_scores.items(), key=lambda x: x[1], reverse=True)

    # Check if there are any advocates to recommend
    if sorted_advocates:
        recommendations = [{'advocate': advocate, 'score': score} for advocate, score in sorted_advocates]
    else:
        recommendations = []

    return render(request, 'accounts/client_advocate_recommendation.html', {'recommendations': recommendations})


#     @@@@@@@@@@@@@@@@@@@@@@@@@@!!!!!!!!!!!!   ADVOCATE AREA   !!!!!!!!!!!!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

@login_required(login_url='login')
@advocate_required
def advocatehome(request):
    user = request.user
    user_status, created = UserStatus.objects.get_or_create(user=user)
    if request.user.is_authenticated:
        user_status.is_online = True
    else:
        user_status.is_online = False
        user_status.last_seen = timezone.now()
    user_status.save()
    if request.user.is_authenticated and request.user.is_advocate:
        advocate = request.user.advocate  # Get the Advocate object related to the user
        context = {'advocate': advocate}
        return render(request, 'accounts/advocatehome.html', context)
    else:
        return redirect('login')
@login_required(login_url='login')
@advocate_required
def advocatemessage(request):
    return render(request, 'accounts/advocateMessage.html')
@login_required(login_url='login')
@advocate_required
def advocate_profile(request):
    user = request.user
    advocate = user.advocate
    return render(request, 'accounts/advocate_profile.html', {'user': user, 'advocate': advocate})
@login_required(login_url='login')
@advocate_required
def update_advocate(request, id):
    advocate = get_object_or_404(Advocate, pk=id)
    if request.method == 'POST':
        advocate.license_number = request.POST.get('license_number', advocate.license_number)
        advocate.office_address = request.POST.get('office_address', advocate.office_address)
        advocate.phone_number = request.POST.get('phone_number', advocate.phone_number)
        advocate.experience = request.POST.get('experience', advocate.experience)
        advocate.specifications = request.POST.get('specifications', advocate.specifications)
        advocate.languages = request.POST.get('languages', advocate.languages)
        advocate.description = request.POST.get('description', advocate.description)
        if request.FILES.get('pimage'):
            advocate.pimage = request.FILES['pimage']
        advocate.dob = request.POST.get('dob', advocate.dob)
        advocate.court = request.POST.get('court', advocate.court)
        advocate.save()
        messages.success(request, 'Successfully updated your profile..Redirecting....')
        redirect_url = reverse('Advocateprofile')
        return render(request, 'accounts/advocateMessage.html', {'redirect_url': redirect_url})
    return render(request, 'accounts/advocateprofileedit.html', {'advocate': advocate})



@login_required(login_url='login')
@advocate_required
def feedbackadvocateview(request):
    context = {}
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data.get("rating")
            description = form.cleaned_data.get("description")
            user = request.user
            obj = Clientfeedback.objects.create(rating=rating, description=description, user=user)
            obj.save()
            messages.success(request, 'thank you for your response')
            return redirect('advocatemessage')
    else:
        form = FeedbackForm()
    context['form'] = form
    return render(request, 'accounts/Advocatefeedback.html', context)


@login_required(login_url='login')
@advocate_required
def AdvocateContactus(request):
    context = {}
    if request.method == "POST":
        form = ContactusForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            email = form.cleaned_data.get("email")
            message = form.cleaned_data.get("message")
            obj = contactus.objects.create(name=name, email=email, message=message)
            obj.save()
            messages.success(request, 'message submitted our team will contact you soon')
            return redirect('advocatemessage')
    else:
        form = ContactusForm()
    context['form'] = form
    return render(request, 'accounts/Advocatecontactus.html', context)


@login_required(login_url='login')
@advocate_required
def schedule_view(request):
    schedules = Schedule.objects.filter(advocate=request.user)
    context = {'schedules': schedules}
    return render(request, 'accounts/schedule.html', context)


@login_required(login_url='login')
@advocate_required
def add_schedule(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.advocate = request.user
            schedule.save()
            return redirect('schedule_view')
    else:
        form = ScheduleForm()
    context = {'form': form}
    return render(request, 'accounts/add_schedule.html', context)


@login_required(login_url='login')
@advocate_required
def edit_schedule(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('schedule_view')
    else:
        form = ScheduleForm(instance=schedule)
    context = {'form': form}
    return render(request, 'accounts/edit_schedule.html', context)


@login_required(login_url='login')
@advocate_required
def delete_schedule(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    if request.method == 'POST':
        schedule.delete()
        return redirect('schedule_view')
    return render(request, 'accounts/delete_schedule.html', {'schedule': schedule})


@login_required(login_url='login')
@advocate_required
def advocate_caserequest_assignments_view(request):
    user = request.user.id
    assignments = CaseAssignment.objects.filter(advocate=user)
    cases = []
    for assignment in assignments:
        case = assignment.case
        case_proof = case.proof
        case_description = case.description
        if  case.is_accepted == False and case.is_rejected == False:
            cases.append({
                'assignment': assignment,
                'case_proof': case_proof,
                'case_description': case_description,
            })
    return render(request, 'accounts/adv_assignments_requestview.html', {'cases': cases})


@login_required(login_url='login')
@advocate_required
def accept_assignment(request, id):
    case_assignment = get_object_or_404(CaseAssignment, id=id)
    client_case = case_assignment.case
    client_case.is_accepted = True
    client_case.is_rejected = False
    client_case.is_notrequested = False
    a = client_case.user.first_name
    b = client_case.user.last_name
    d = case_assignment.advocate.user.first_name
    e = case_assignment.advocate.user.last_name
    client_case.save()

    subject = 'Your case request has been accepted'
    message = f'Dear {a} {b} this is to inform you that your case request has been accepted by advocate {d} {e} ' \
              f'kindly visit My Attorney protel and contact your advocate for more information...'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [client_case.user.email]
    send_mail(subject, message, from_email, recipient_list)

    messages.success(request, 'Assignment accepted successfully')
    return redirect('advocatemessage')


@login_required(login_url='login')
@advocate_required
def reject_assignment(request, id):
    case_assignment = get_object_or_404(CaseAssignment, id=id)
    client_case = case_assignment.case
    client_case.is_rejected = True
    client_case.is_notrequested = True
    client_case.is_requested = False

    a = client_case.user.first_name
    b = client_case.user.last_name
    d = case_assignment.advocate.user.first_name
    e = case_assignment.advocate.user.last_name

    client_case.save()
    subject = 'Your case request has been rejected'
    message = f'Dear {a} {b} this is to inform you that your case request has been rejected by advocate {d} {e} ' \
              f'kindly visit My Attorney protel  for more information...'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [client_case.user.email]
    send_mail(subject, message, from_email, recipient_list)

    messages.success(request, 'Assignment Rejected successfully...Redirecting')
    redirect_url = reverse('advocate_caserequest_assignments_view')
    return render(request, 'accounts/advocateMessage.html', {'redirect_url': redirect_url})


@login_required(login_url='login')
@advocate_required
def Advclient(request):
    user = request.user.id
    assignments = CaseAssignment.objects.filter(advocate=user, case__is_accepted=True)
    cases = []
    search_query = request.GET.get('q', '')
    if search_query:
        assignments = assignments.filter(Q(case__title__icontains=search_query) | Q(case__user__first_name__icontains=search_query) | Q(case__user__last_name__icontains=search_query))
    for assignment in assignments:
        case = assignment.case
        client = case.user
        client_profile = client.clientprofiles
        cases.append({
            'assignment': assignment,
            'case': case,
            'client': client,
            'client_profile': client_profile,
        })
    return render(request, 'accounts/avdvocateclients.html', {'cases': cases})

from django.utils import timezone
from datetime import timedelta

@login_required(login_url='login')
@advocate_required
def advocate_chat(request, client_id=None):
    user = request.user
    if user.is_advocate:
        advocate = user.advocate
        subquery = CaseAssignment.objects.filter(advocate=advocate).values_list('case__user__client', flat=True).distinct()
        clients = Client.objects.filter(user__client__in=subquery)
        client_profiles = Clientprofiles.objects.filter(user__client__in=subquery).select_related('user')
        client_images = {client_profile.user_id: client_profile.pimage.url if client_profile.pimage else None for client_profile in client_profiles}
        clients = [{'client': client, 'image': client_images.get(client.user_id)} for client in clients]



    if client_id:
        client = Client.objects.get(pk=client_id)
        client_profile = Clientprofiles.objects.select_related('user').filter(user__client=client).first()
        user_status = UserStatus.objects.filter(user=client.user).first()
        if request.method == 'POST':
            message = request.POST.get('message')
            receiver = client.user
            new_message = Message(sender=user, receiver=receiver, message=message)
            new_message.save()
        latest_message = Message.objects.filter(Q(sender=user, receiver=client.user) | Q(sender=client.user, receiver=user)).order_by('-timestamp').first()
        # latest_message = Message.objects.filter(sender=client.user, receiver=user).order_by('-timestamp').first()
        messages = Message.objects.filter(
            Q(sender=user, receiver=client.user) | Q(sender=client.user, receiver=user)).order_by('timestamp')
        context = {'clients': clients, 'client': client, 'messages': messages, 'latest_message': latest_message}
        if client_profile:
            context['client_image'] = client_profile.pimage.url
        if user_status and user_status.is_online:
            context['user_status'] = 'online'
        elif user_status and not user_status.is_online:
            last_seen = user_status.last_seen + timedelta(hours=5, minutes=30)  # Add timezone offset
            last_seen_str = last_seen.strftime('%b %d, %Y %I:%M %p')
            context['user_status'] = 'Last seen: ' + last_seen_str
        return render(request, 'accounts/advchat.html', context)
    else:
        return render(request, 'accounts/advchat.html', {'clients': clients})



@login_required(login_url='login')
@advocate_required
def client_case_details(request, assignment_id):
    assignment = get_object_or_404(CaseAssignment, pk=assignment_id, advocate=request.user.id)
    client_case =  assignment.case
    user = client_case.user
    client = Client.objects.get(user=user)
    client_profiles = Clientprofiles.objects.get(user=user)
    context = {'client_case': client_case, 'client': client, 'client_profiles': client_profiles}
    return render(request, 'accounts/client_case_details.html', context)


# @login_required(login_url='login')
# @advocate_required
# def create_case(request):
#     advocate = request.user.advocate
#     case_assignments = CaseAssignment.objects.filter(advocate=advocate)
#     clients = [case.requested_by for case in case_assignments]
#     cases = []
#     for client in clients:
#         client_cases = Clientcase.objects.filter(user=client)
#         for case in client_cases:
#             if CaseAssignment.objects.filter(case=case, advocate=advocate).exists():
#                 cases.append(case)
#
#     # Create a set of unique case titles
#     unique_case_titles = set(case.title for case in cases)
#
#     # Create a list of unique cases
#     unique_cases = []
#     for title in unique_case_titles:
#         case = next((case for case in cases if case.title == title), None)
#         unique_cases.append(case)
#
#     if request.method == 'POST':
#         client_id = request.POST.get('client')
#         case_id = request.POST.get('case')
#         client = Client.objects.get(pk=client_id)
#         case=Clientcase.objects.get(pk=case_id)
#         title = request.POST.get('title')
#         sub_title = request.POST.get('sub_title')
#         description = request.POST.get('description')
#         date_filed = request.POST.get('date_filed')
#         court = request.POST.get('court')
#         cnr = request.POST.get('cnr')
#         status = request.POST.get('status')
#         outcome = request.POST.get('outcome')
#         filed_lawsuit = filed_lawsuits.objects.create(
#             created_by=request.user,
#             client=client,
#             refference=case,
#             title=title,
#             sub_title=sub_title,
#             description=description,
#             date_filed=date_filed,
#             court=court,
#             cnr=cnr,
#             status=status,
#             outcome=outcome
#         )
#         # use set method to set the values of the many-to-many field
#         filed_lawsuit.save()
#         for key, value in request.POST.items():
#             if key.startswith('judge'):
#                 judge_name = value.strip()
#                 if judge_name:
#                     judge = Judge.objects.create(name=judge_name)
#                     filed_lawsuit.judges.add(judge)
#         messages.success(request, 'Case created successfully')
#         return redirect('advocatemessage')
#     context = {
#         'clients': clients,
#         'cases': unique_cases
#     }
#
#     return render(request, 'accounts/create_case.html', context)



@login_required(login_url='login')
@advocate_required
def create_case(request):
    advocate = request.user.advocate
    case_assignments = CaseAssignment.objects.filter(advocate=advocate)
    clients = [case.requested_by for case in case_assignments]
    cases = []
    for client in clients:
        client_cases = Clientcase.objects.filter(user=client)
        for case in client_cases:
            if CaseAssignment.objects.filter(case=case, advocate=advocate).exists():
                cases.append(case)

    # Create a set of unique case titles
    unique_case_titles = set(case.title for case in cases)

    # Create a list of unique cases
    unique_cases = []
    for title in unique_case_titles:
        case = next((case for case in cases if case.title == title), None)
        unique_cases.append(case)

    if request.method == 'POST':
        client_id = request.POST.get('client')
        case_id = request.POST.get('case')
        client = Client.objects.get(pk=client_id)
        case = Clientcase.objects.get(pk=case_id)
        title = request.POST.get('title')
        sub_title = request.POST.get('sub_title')
        description = request.POST.get('description')
        date_filed = request.POST.get('date_filed')
        court_name = request.POST.get('court_name')
        court_year = request.POST.get('court_year')
        cnr = request.POST.get('cnr')
        status = request.POST.get('status')
        outcome = request.POST.get('outcome')

        filed_lawsuit = filed_lawsuits.objects.create(
            created_by=request.user,
            client=client,
            refference=case,
            title=title,
            sub_title=sub_title,
            description=description,
            date_filed=date_filed,
            cnr=cnr,
            status=status,
            outcome=outcome
        )

        # Save multiple Defendant details
        for i in range(1, 4):
            defendant_name = request.POST.get(f'defendant_name_{i}')
            defendant_address = request.POST.get(f'defendant_address_{i}')
            defendant_phone_number = request.POST.get(f'defendant_phone_number_{i}')
            defendant_email = request.POST.get(f'defendant_email_{i}')
            if defendant_name:
                defendant = Defendant.objects.create(
                    name=defendant_name,
                    address=defendant_address,
                    phone_number=defendant_phone_number,
                    email=defendant_email
                )
                filed_lawsuit.defendants.add(defendant)

        # Save Court details
        court_name = request.POST.get('court_name')
        court_year = request.POST.get('court_year')
        if court_name and court_year:
            court = Court.objects.create(name=court_name, year=court_year)
            filed_lawsuit.courts.add(court)

        # Save multiple Judge details
        for key, value in request.POST.items():
            if key.startswith('judge'):
                judge_name = value.strip()
                if judge_name:
                    judge = Judge.objects.create(name=judge_name)
                    filed_lawsuit.judges.add(judge)

        messages.success(request, 'Case created successfully')
        return redirect('advocatemessage')
    context = {
        'clients': clients,
        'cases': unique_cases
    }

    return render(request, 'accounts/create_case.html', context)





from django.shortcuts import render
import os
import pickle
import PyPDF2
import textract
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from summa.summarizer import summarize


# Define the categories
categories = ['Agreements', 'Deeds', 'Human Resources', 'Taxes', 'Valuations']

# Load the trained model from the pickle file
with open('model.pickle', 'rb') as f:
    vectorizer, clf = pickle.load(f)

def predict_document_type(request):
    if request.method == 'POST':
        # Get the uploaded file from the form data
        uploaded_file = request.FILES['pdf_file']

        # Save the uploaded file to a temporary file
        with open('temp.pdf', 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        # Extract text from the uploaded PDF file
        pdf_file = open('temp.pdf', 'rb')
        #pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        pdf_file.close()

        summary = summarize(text, ratio=0.2)


        # Extract keywords from the text
        tokens = word_tokenize(text)
        keywords = [token.lower() for token in tokens if token.isalpha()]
        corpus = ' '.join(keywords)

        # Predict the type of the uploaded PDF file
        X = vectorizer.transform([corpus])
        predicted_category = clf.predict(X)[0]

        # Delete the temporary filep
        os.remove('temp.pdf')

        return render(request, 'accounts/predict_pdf_form.html', {'predicted_category': predicted_category,'summary': summary})
    else:
        return render(request, 'accounts/predict_pdf_form.html')



