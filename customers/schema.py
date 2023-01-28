import graphene
import time
from graphene_django import DjangoObjectType
from customers.models import Customer, Product

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = '__all__'
class ProductType(DjangoObjectType):
    class Meta:
        model= Product
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

class CreateProduct(graphene.Mutation):
    class Arguments:
        description = graphene.String()
        total = graphene.Int()
        customer = graphene.ID()

    product = graphene.Field(ProductType)

    def mutate(root, info, description, total, customer):
        product_id = Customer.objects.get(pk=customer)
        product = Product(description=description, total=total, customer=product_id).save()

        return CreateProduct(product=product)

class Query(graphene.ObjectType):
    customers = graphene.List(CustomerType)
    customer_name_first = graphene.Field(CustomerType, name=graphene.String(required=True))
    customer_name_multiple = graphene.List(CustomerType, name=graphene.String(required=True))
    products = graphene.List(ProductType)


    def resolve_customers(root, info):
        return Customer.objects.all()

    def resolve_customer_name_first(root, info, name):
        try:
            return Customer.objects.filter(name=name).first()
        except Customer.DoesNotExist:
            return None

    def resolve_products(root, info):
        return Customer.objects.select_related('customer').all()

    def resolve_customer_name_multiple(root, info, name):
        try:
            return Customer.objects.filter(name=name)
        except Customer.DoesNotExist:
            return None


class Mutations(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    create_product = CreateProduct.Field()

schema = graphene.Schema(query=Query, mutation=Mutations)