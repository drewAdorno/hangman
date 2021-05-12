from django.shortcuts import render, redirect
import random
from . import words
def index(request):
    if 'word' not in request.session:
        if 'difficulty' not in request.session or request.session['difficulty'] == 'easy':
            request.session['word']=words.easy[random.randint(0, len(words.easy)-1)]
        elif request.session['difficulty'] == 'med':
            request.session['word']=words.med[random.randint(0, len(words.med)-1)]
        else:
            request.session['word']=words.hard[random.randint(0, len(words.hard)-1)]
        request.session['word2']=request.session['word']
        request.session['masked_word']= "_" * len(request.session['word'])
        request.session['remainingGuesses']=10
        request.session['status']='ongoing'
        request.session['picture']=f'images/{request.session["remainingGuesses"]}.jpg'
        request.session['placeholder']={}
        request.session['lettersGuessed']=[]
    context={
        'numGuesses':request.session["remainingGuesses"]
    }

    return render(request, 'app1/index.html', context)

def letter(request):     
        #letter=letter.lower()
        letter=request.POST['letter'].lower()  #make letter lowercase
        result = request.session['word2'].find(letter)   #see if letter is in the word
        if result == -1:    #if its not in the word
            letter=letter.upper()   #make a n
            request.session['lettersGuessed'].append(letter)
            request.session['remainingGuesses'] -= 1
            request.session['picture']=f'images/{request.session["remainingGuesses"]}.jpg'
            result_check(request)
            return redirect('/')
        while(request.session['word2'].find(letter) != -1):
            result = request.session['word2'].find(letter)
            request.session['word2'] =request.session['word2'][0:result] + " " + request.session['word2'][result + 1:]
            temp = request.session['masked_word'][0:result] + letter + request.session['masked_word'][result + 1:]
            request.session['masked_word'] = temp
            print(request.session['masked_word'])
        result_check(request)
        return redirect('/')

def result_check(request):
    if request.session['word'] == request.session['masked_word']:
        request.session['status'] = 'win'
    if request.session['remainingGuesses'] == 1:
        request.session['status']='lose'
        for i in range(len(request.session['masked_word'])):
            if(request.session['masked_word'][i]=='_'):
                request.session['placeholder'][request.session['word'][i]]='text-danger'
            else:
                request.session['placeholder'][request.session['word'][i]]=''
        print(request.session['placeholder'])

def newGame(request, difficulty):
    request.session.clear()
    request.session['difficulty']=difficulty
    return redirect('/')

def leaderboard(request):
    return render(request, 'leaderboard.html')