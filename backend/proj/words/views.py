import random
from django.shortcuts import render
import rest_framework
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseNotFound

from .models import Words
# Create your views here.

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Words
        fields = ['pk', 'word', 'pinyin', 'translation']


class RandomWord(APIView):
    def get(self, *args, **kwargs):
        all_words = Words.objects.all()
        random_word = random.choice(all_words)
        serialized_random_word = WordSerializer(random_word, many=False)
        return Response(serialized_random_word.data)
    

class NextWord(APIView):
    def get(self, request, pk, format=None):
        word = Words.objects.filter(pk__gt=pk).first()
        if not word:
            return HttpResponseNotFound()
        return Response(WordSerializer(word, many=False).data)
    

class AddWord(APIView):
    def post(self, request):
        entry = Words.objects.create(
            word=request.data['word'],
            pinyin=request.data['pinyin'],
            translation=request.data['translation']
        )
        return Response(WordSerializer(entry, many=False).data)
    

class AllWords(APIView):
    def get(self, request, format=None):
        all_words = Words.objects.all()
        return Response(WordSerializer(all_words, many=True).data)