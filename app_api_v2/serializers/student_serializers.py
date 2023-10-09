from rest_framework import serializers

from courses.models import StudentCertificate


class CertificateVerficationSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='full_name'
    )

    user_image = serializers.CharField(
        source='user.image', read_only=True, max_length=50, allow_blank=True, allow_null=True)

    course = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='title'
    )

    completed_date = serializers.DateTimeField(
        source='enrollment.completed_date', read_only=True, allow_null=True, format="%d %b %Y")



    class Meta:
        model = StudentCertificate
        fields = ('ref_number', 'user', 'user_image', 'course', 'completed_date')
        # fields = '__all__'
