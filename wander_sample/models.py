from django.db import models


class BasicOperation(models.Model):
    id = models.CharField(max_length=100, unique=True, primary_key=True)

    def __str__(self):
        return f'<BasicOperation: {self.id}>'

    def simple_str(self):
        return f'{self.id}'


class Operation(models.Model):
    name = models.CharField(default='unnamed', max_length=10000)
    operation_chain = models.ManyToManyField(BasicOperation)

    def __str__(self):
        Operation.objects.prefetch_related('operation_chain')
        if self.name != 'unnamed':
            return f'<Operation: {self.name}>'
        else:
            return f'<Operation: {" ".join([i.simple_str() for i in self.operation_chain.all()])}>'


class Attribute(models.Model):
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    result = models.BooleanField()

    class Meta:
        unique_together = ('operation', 'result')

    def __str__(self):
        return f'<Attribute: {self.operation}({self.result})>'


class InformationPack(models.Model):
    name = models.CharField(default='unnamed', max_length=10000)
    attribute_chain = models.ManyToManyField(Attribute)

    def __str__(self):
        InformationPack.objects.prefetch_related('attribute_chain')
        if self.name != 'unnamed':
            return f'<InformationPack: {self.name}>'
        else:
            return f'<InformationPack: {" ".join([str(i) for i in self.attribute_chain.all()])}>'
