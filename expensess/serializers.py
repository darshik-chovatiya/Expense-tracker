import re
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from .models import Users , Category , Expense

class UserRegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'username', 'email', 'gender', 'password']

    password = serializers.CharField(write_only=True, required=True)
    
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Users.objects.all(), message="Username already exists.")]
    )

    email = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Users.objects.all(), message="Email already exists.")]
    )
 
    gender = serializers.ChoiceField(
        choices=Users.GENDER_CHOICES,
        error_messages={
            'invalid_choice': 'Please choose a valid gender: Male, Female, or Other.'
        }
    )

    def validate_email(self, value):
        errors = []
    
        if '@' not in value:
            errors.append("contain '@'")
        if '.' not in value:
            errors.append("contain '.'")
        if not value.endswith('.com'):
            errors.append("end with '.com'")
    
        if errors:
            raise serializers.ValidationError(
                f"Email must {', '.join(errors)}."
            )
    
        return value

    def validate_password(self, value):
        errors = []

        if len(value) < 8:
            errors.append("at least 8 characters")
        if not re.search(r'[A-Z]', value):
            errors.append("one uppercase letter")
        if not re.search(r'[a-z]', value):
            errors.append("one lowercase letter")
        if not re.search(r'\d', value):
            errors.append("one number")
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', value):
            errors.append("one special character")

        if errors:
            raise serializers.ValidationError(
                f"Password must contain {', '.join(errors)}."
            )
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Users(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class UserLoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()  
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username_or_email = data.get('username_or_email')
        password = data.get('password')

        print('username.....................' , username_or_email)

        print('password................................' , password)

        user = Users.objects.filter(username=username_or_email).first()
        if not user:
            user = Users.objects.filter(email=username_or_email).first()

        if not user:
            raise serializers.ValidationError({
                "errors": ["No account found with the provided username or email."]
            })

        user = authenticate(username=user.username, password=password)

        if user is None:
            raise serializers.ValidationError({
                "errors": ["Incorrect password."]
            })

        data['user'] = user
        return data

class UserCategoryserializers(serializers.ModelSerializer):
    
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        
        model = Category
        fields = ['id' , 'name' , 'user']

    def validate_name(self , value):
        user = self.context['request'].user
        
        if Category.objects.filter(user=user , name__iexact=value).exists():
            raise serializers.ValidationError("This category alerady exists ")
        
        return value
    
class UserExpenseserializers(serializers.ModelSerializer):

    class Meta:

        model = Expense
        fields = ['id' , 'user' , 'category' , 'title' , 'other' , 'description' ]

    title = serializers.CharField(required=True,
                                  validators=[UniqueValidator(queryset=Expense.objects.all(),
                                 message="Title already exists.")])

    def validate_category(self , value):
        user = self.context['request'].user

        if value.user != user:
            raise serializers.ValidationError("This category does not you")
        
        return value