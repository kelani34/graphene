import graphene
import time
from graphene_django import DjangoObjectType
from customers.models import Customer

class CustomerType(DjangoObjectType):
    class Meta:
        model =Customer
        fields = '__all__'

class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        industry = graphene.String()
    customer = graphene.Field(CustomerType)
    
    def mutate(root, info, name, industry): 
        time.sleep(3)
        customer = Customer(name=name, industry=industry)
        customer.save()
        return CreateCustomer(customer=customer)

class Query(graphene.ObjectType):
    customers = graphene.List(CustomerType)
    customer_name_first = graphene.Field(CustomerType, name=graphene.String(required=True))
    customer_name_multiple = graphene.List(CustomerType, name=graphene.String(required=True))


    def resolve_customers(root, info):
        return Customer.objects.all()

    def resolve_customer_name_first(root, info, name):
        try:
            return Customer.objects.filter(name=name).first()
        except Customer.DoesNotExist:
            return None

    def resolve_customer_name_multiple(root, info, name):
        try:
            return Customer.objects.filter(name=name)
        except Customer.DoesNotExist:
            return None


class Mutations(graphene.ObjectType):
    createCustomer = CreateCustomer.Field()

schema = graphene.Schema(query=Query, mutation=Mutations)