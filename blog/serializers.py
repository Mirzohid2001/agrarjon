from rest_framework import serializers
from .models import *

class Legal_DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Legal_Documents
        fields = ('id','title', 'description', 'image')

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id','title', 'content', 'image')

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id','image', 'text')


from .models import Area, Seed, Worker, Tractor, Fertiliser, WorkType

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'

class SeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seed
        fields = '__all__'

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'

class TractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tractor
        fields = '__all__'

class FertiliserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fertiliser
        fields = '__all__'

class WorkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkType
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class MemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mems
        fields = '__all__'