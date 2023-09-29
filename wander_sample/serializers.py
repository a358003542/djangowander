from rest_framework import serializers


class ContactFormSerializer(serializers.Serializer):
    name = serializers.CharField(label='your name', max_length=100)

    def validate_name(self, value):
        if value == 'chimera':
            raise serializers.ValidationError('What did I tell you about chimeras?!')
        return value


from .models import Attribute, Operation, BasicOperation, InformationPack


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'
        depth = 1


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = '__all__'
        depth = 1


class BasicOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicOperation
        fields = '__all__'
        depth = 1


class InformationPackSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationPack
        fields = '__all__'
        depth = 1
