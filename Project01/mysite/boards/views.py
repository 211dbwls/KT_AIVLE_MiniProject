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
    

# tts
import os
import azure.cognitiveservices.speech as speechsdk

speech_key, service_region = "c2d4ab5286b44c59a8917abe6d015d6b", "koreacentral"

def tts_test(request):
    result = ""
    
    if request.method == 'POST':
        text = request.POST.get('text')
        language = request.POST.get('languages')
        
        if text is not None:
            speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
            audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

            speech_config.speech_synthesis_voice_name = language  # 언어 설정
            # https://learn.microsoft.com/ko-kr/azure/cognitive-services/speech-service/language-support?tabs=tts (언어 설정 참고)

            speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

            speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()  # 오디오 출력
            
            # 결과 출력
            if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                print("Speech synthesized for text [{}]".format(text))
            elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = speech_synthesis_result.cancellation_details
                print("Speech synthesis canceled: {}".format(cancellation_details.reason))
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    if cancellation_details.error_details:
                        print("Error details: {}".format(cancellation_details.error_details))
                        print("Did you set the speech resource key and region values?") 
            
    return render(request, 'tts_test.html', {'resultText':result})

# translate
import requests, uuid, json

key = "929ada72d3f242df893e3bb5b3b8ccd1"
endpoint = "https://api.cognitive.microsofttranslator.com"
location = "koreacentral"

path = '/translate'
constructed_url = endpoint + path

headers = {
    'Ocp-Apim-Subscription-Key': key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

def translate(request):
    result = ""
    
    if request.method == 'POST':
        trans_from_language = request.POST.get('trans-from')
        trans_to_language = request.POST.get('trans-to')
        params = {
            'api-version': '3.0',
            'from': trans_from_language,
            'to': trans_to_language
            # https://learn.microsoft.com/ko-kr/azure/cognitive-services/translator/language-support (언어 지원)
        }
        
        trans_text = request.POST.get('text')
        
        if trans_text is not None:
            body = [{
                'text': trans_text
            }]

            req = requests.post(constructed_url, params=params, headers=headers, json=body)
            response = req.json()

            result = response[0]['translations'][0]['text']
    
    return render(request, 'tts_test.html', {'resultText':result})