from rest_framework.serializers import ModelSerializer
from component.models.account import Tag, Category, Attribute


class AttributeSerializer(ModelSerializer):
    class Meta:
        model = Attribute
        exclude = ('id','desc')

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id','desc')

class TagSerializer(ModelSerializer):
    attributes = AttributeSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Tag
        exclude = ('id',)