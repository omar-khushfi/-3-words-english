from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import *
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from .forms import *
import random
from django.http import JsonResponse
from django.views.decorators.http import require_GET

#@method_decorator(login_required,name='dispatch')
class enter_words(View):
    def post(self,request):
        word = wordform(request.POST, request.FILES)
        if word.is_valid():
            word = word.save(commit=False)
            word.user = request.user  # Assign the logged-in user
            word.save()  # Now s
        return redirect(reverse('enter-words'))
    def get(self,request):
        form=wordform()
        unwords=Unknown_word.objects.filter(user=request.user)
       
        context={
            'unwords':unwords,
            'form':form,
        }
        return render(request,'enter_words.html',context)


def delete_word(requset,pk):
    word=Word.objects.get(pk=pk)

    user=requset.user
    unword=Unknown_word.objects.get(user=user,word=word)
    # print(user)
    unword.delete()
    return redirect(reverse('enter-words'))



#@method_decorator(login_required,name='dispatch')
class exam(View):
    def post(self,request):
        selected_translation = request.POST.get('translation')
        word_id = request.POST.get('word_id')
        translations = request.POST.get('translations')
        translations=str(translations).split("'")
       
        x={}
        for i in translations:
            if i != ', ' and i!= '[' and i!=']' and i != "'":
                x[i]=[i];
        translations=x   
        word = Word.objects.get(id=word_id)
        ok=0
        result = f" الترجمة الصحيحة هي: {word.arabic}"
       
        if selected_translation == word.english:
            result = "إجابة صحيحة!"
            ok=1
        else:
            user=request.user
            unword=Unknown_word(user=user,word=word)
            if Unknown_word.objects.filter(user=user,word=word).exists():
                pass
            else:
                unword.save()
            
        context={
            'ok':ok,
            'translations':translations,
            'selected_translation':selected_translation,
            'result':result
        }
        return render(request, 'exam.html', context)
    
    def get(self,request):
        random_word = Word.objects.filter(user=request.user).order_by('?')[:3]
        main_word = random.choice(random_word)
        translations=[main_word.english] + [word.english for word in random_word if word != main_word]
        unwords=Unknown_word.objects.filter(user=request.user)
        random.shuffle(translations)
        context={
             'unwords':unwords,
            'main_word': main_word,
            'translations':translations
        }
        return render(request,'exam.html',context)



class WordListView(View):
    def get(self, request):
        query = request.GET.get('q')  
        if query:
            words = Word.objects.filter(user=request.user, english__icontains=query)
        else:
            words = Word.objects.filter(user=request.user)
        
        paginator = Paginator(words, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'page_obj': page_obj,
            'query': query,  # إرسال استعلام البحث الحالي (إذا وُجد) للعرض
        }
        return render(request, 'word_list.html', context)


     
class Register(CreateView):
    template_name='registration/signin.html'
    model=User
    form_class=UserCreationForm
    success_url= reverse_lazy('login') 

    def form_valid(self, form):
        # يتم الحفظ قبل تسجيل الدخول حتى نكون لدينا كائن المستخدم
        response = super().form_valid(form)
        # تسجيل الدخول تلقائيًا للمستخدم
        user = self.object
        login(self.request, user)
        # تحويل إلى صفحة البروفايل (الملف الشخصي)
        return redirect(reverse('enter-words'))
