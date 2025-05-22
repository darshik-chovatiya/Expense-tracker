from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import Category , Expense
from .serializers import UserRegistrationSerializer , UserLoginSerializer , UserCategoryserializers , UserExpenseserializers

class UserRegistrationView(APIView):

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({"status": True,
                             "message": "User registered successfully",
                             "refresh": str(refresh),
                             "access": access_token,
                            }, status=status.HTTP_201_CREATED)

        return Response({"satuas":False} , serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({"status": True,
                             "message": "User Login successfully",
                             "refresh": str(refresh),
                             "access": str(refresh.access_token)
                            }, status=status.HTTP_200_OK)

        return Response({"satuas":False},serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CategoryView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self , request):

        user = request.user
        categories = Category.objects.filter(user=user , is_deleted=False)
        serializer = UserCategoryserializers(categories , many=True)
        return Response({"status": True,
                         "message": "Category list fetched successfully",
                         "data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self , request):

        serializer = UserCategoryserializers(data=request.data , context={'request' : request})

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"status": True,
                             "message": "Category added successfully",
                             "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response({"status": False,
                         "message": "Category not added ",
                         "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  

    def put(self , request , category_id):

        if not category_id:
            return Response({"status":False,
                             "message":"category-id is required for update"},status=status.HTTP_400_BAD_REQUEST)   
        try:
            category = Category.objects.get(id=category_id , user=request.user , is_deleted=False)

        except Category.DoesNotExist:
            return Response({"status":False,
                             "message":"Category not found"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserCategoryserializers(category , data=request.data , partial=True , context={'request':request})

        if serializer.is_valid():
            serializer.save()
            return Response({"status":True,
                             "message":"Category updated successfully",
                             "data":serializer.data},status=status.HTTP_200_OK)
        
        return Response({"status":False,
                         "message":"Category update failed",
                         "error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            
    
    def delete(self , request , category_id):
        try:
            category = Category.objects.get(id=category_id , user=request.user)
            category.is_deleted = True
            category.save()

            return Response({"status":True,
                             "message" : "Category deleted successfully"}, status=status.HTTP_200_OK)
        
        except Category.DoesNotExist:
            return Response({"status":False,
                             "message":"Category not found"}, status=status.HTTP_404_NOT_FOUND)

   
        
class ExpenseView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self , request):
        user = request.user
        expense = Expense.objects.filter(user=user)
        serializer = UserExpenseserializers(expense , many=True)
        return Response({"status":True,
                         "message":"Expenses fetched successfully",
                         "data":serializer.data},status=status.HTTP_200_OK)
    
    def post(self , request):
        serializer = UserExpenseserializers(data=request.data , context={'request':request})

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"status":True,
                             "message":"Expense added successfully",
                             "data":serializer.data},status=status.HTTP_201_CREATED)
        
        return Response({"status":False,
                         "message":"Expense not added",
                         "data":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def put(self , request , expense_id):
         
        if not expense_id:
            return Response({"status":False,
                             "message":"Expense-id is required for update"},status=status.HTTP_400_BAD_REQUEST)   
        try:
            expense = Expense.objects.get(id=expense_id , user=request.user , is_deleted=False)

        except Expense.DoesNotExist:
            return Response({"status":False,
                             "message":"Expenses not found"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserExpenseserializers(expense , data=request.data , partial=True , context={'request':request})

        if serializer.is_valid():
            serializer.save()
            return Response({"status":True,
                             "message":"Expenses updated successfully",
                             "data":serializer.data},status=status.HTTP_200_OK)
        
        return Response({"status":False,
                         "message":"Expenses update failed",
                         "error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self , request , expense_id):
        try:
            expense = Expense.objects.get(id=expense_id , user=request.user)
            expense.is_deleted = True
            expense.save()

            return Response({"status":True,
                             "message" : "Expnese deleted successfully"}, status=status.HTTP_200_OK)
        
        except Expense.DoesNotExist:
            return Response({"status":False,
                             "message":"Expense not found"}, status=status.HTTP_404_NOT_FOUND)
         
    
class SingleExpenseView(APIView):

    def get(self , request , expense_id):
        try:
            expense = Expense.objects.get(id=expense_id)
            serializer = UserExpenseserializers(expense)

            return Response({"status":True,
                            "message":"Expenses fetched successfully",
                            "data":serializer.data},status=status.HTTP_200_OK)
        
        except Expense.DoesNotExist:
            return Response({"status":False,
                             "message":"Expense not found"}, status=status.HTTP_404_NOT_FOUND)