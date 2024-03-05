from rest_framework import serializers
from courses.models import Subject


class SubjectCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subject
        fields = '__all__'
        #fields = ['id', 'title', 'slug', 'course_count', 'page_title', 'page_details', 'meta_title', 'meta_tags', 'meta_description', 'video_link']

    def create(self, validated_data):
      user = self.context['request'].user
      subject = Subject.objects.create(
         owner=user, 
         **validated_data
      )
      return subject