from user.models import CustomUser, Customer
from django.utils import timezone
from django.db.models import Q
from django.db.models.expressions import OrderBy, Value
from django.http.response import JsonResponse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from Sales.models import  Order, OrderProduct
from Products.models import Inventory, Product
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from user.decorators import (admin_required, inventory_manager_required,
                             manager_required, staff_required)
# Create your views here.
@method_decorator([login_required, staff_required], name="dispatch")
class OrdersList(ListView):
    model = Order
    context_object_name = "orders"
    template_name = "Sales/orders_list.html"
    

    def get_context_data(self, **kwargs):
        context = super(OrdersList, self).get_context_data(**kwargs)
        context["title"] = "Orders"
        context["orders"] = self.model.objects.all()
        context["order_open"] = True
        return context


@method_decorator([login_required, staff_required], name="dispatch")
class AddOrderView(CreateView):
    model = Order
    template_name = "Sales/new_order.html"
    context_object_name = "invoice"
    success_url = reverse_lazy("order_list")

    order_subtotal = 0
    order_total_bill = 0
    order_total_discount = 0
    order_total_cost = 0
    order_products = []

    def get(self, *args, **kwargs):
        if self.request.is_ajax():
            term = self.request.GET.get('term')
            query = self.request.GET.get('q')
            print (query)
            inventory = Inventory.objects.exclude(
                Q(product_quantity__lte=0, product__in=Product.objects.filter(allow_pre_order=False))
            ).filter(product__in=Product.objects.exclude(is_active=False).filter(
                Q(product_name__icontains=query) | Q(product_code__icontains=query))
                ).values()

            product = []
            for inv in inventory:
                prod = Product.objects.filter(id__icontains=inv['product_id']).all()
                print("-------PROD---------")
                print(inv['product_quantity'])
                p = prod.values()[0]
                p["inventory_quantity"] = inv['product_quantity']
                print(type(p))
                product.append(p)
                
            response_content = list(product)
            print("------------response product--------")
            print(response_content)
            return JsonResponse(response_content, safe= False)
        context = {}
        context["title"] = "Add Orders"
        context["pos_open"] = True
        return render(self.request, "Sales/new_order.html", context)
    

    def post(self, *args, **kwargs):
        print("------------POST add order---------")
        customer_name = self.request.POST.get("customer_to_add_id")
        gst_amount = self.request.POST.get("gst_amount")
        menu_products = self.request.POST.getlist("product_to_add_id")
        p_quantity = self.request.POST.getlist("p_quantity")
        p_sold_price = self.request.POST.getlist("sold_price")
        p_discount = self.request.POST.getlist("p_discount")

        if menu_products:
            print("---------order products------")
            print(menu_products)
            order = Order()
            invoice_date = str(timezone.now().date()).split('-')
            invoice_time = str(timezone.now().time()).split(':')
            invoice_num = str(invoice_date[1] + invoice_date[2] + invoice_time[2].split('.')[1])
            
            for i, o_product in enumerate(menu_products): 
                if p_discount[i] == "":
                    p_discount[i] = 0
                if gst_amount == "":
                    gst_amount = 0
                inventory = Inventory.objects.filter(product_id=o_product)
                product = Product.objects.filter(id=o_product)
                print(inventory)
                if inventory.filter(Q(product__in=Product.objects.filter(allow_pre_order=True)) , Q(product_quantity__lte=p_quantity[i])):
                    updated_qty = int(inventory.get().product_quantity) - int(p_quantity[i])
                    inventory.update(product_quantity=updated_qty)
                    print("product has pre-order allow but qty is less")
                    if product.get().is_never_sold:
                        product.update(is_never_sold=False)
                        print("Product was never Sold")
                    else:
                        print("Product has already Sold")

                elif inventory.filter(Q(product__in=Product.objects.filter(allow_pre_order=False)) , Q(product_quantity__gte=p_quantity[i])):
                    updated_qty = int(inventory.get().product_quantity) - int(p_quantity[i])
                    inventory.update(product_quantity=updated_qty)
                else:
                    inventory.update(product_quantity=0)
                    if product.get().is_never_sold:
                        product.update(is_never_sold=False)
                        print("Product was never Sold")
                    else:
                        print("Product has already Sold")

                self.order_total_bill += (int(p_sold_price[i])-int(p_discount[i])) * int(p_quantity[i])
                self.order_subtotal += (int(p_sold_price[i]) - int(p_discount[i]))* int(p_quantity[i])
                if int(p_sold_price[i]) > int(inventory.get().product.sale_price):
                    
                    self.order_total_discount += 0 + (int(p_discount[i]) * int(p_quantity[i]))
                else:
                    self.order_total_discount += (int(inventory.get().product.sale_price)-
                      int(p_sold_price[i])+ int(p_discount[i])) * int(p_quantity[i])
                order.invoice_num = invoice_num
                order.customer = Customer.objects.filter(id=customer_name).get()
                order.subtotal = self.order_subtotal
                order.total_bill = self.order_total_bill + int(gst_amount)
                order.total_discount = self.order_total_discount
                order.gst_amount = int(gst_amount)
                order.paid_amount = 0
                order.payment_type = 'Unpaid'
                self.order_total_cost += (int(inventory.get().product.purchase_price) * int(p_quantity[i]))
                order.order_cost = self.order_total_cost
                order.created_at = timezone.now()
                order.save()

                   
                order_pro = OrderProduct()
                order_pro.purchased_product = inventory.get()
                order_pro.invoice_item = order
                order_pro.purchased_quantity = int(p_quantity[i])
                order_pro.sold_at_price = int(p_sold_price[i])
                if int(p_sold_price[i]) >= int(inventory.get().product.sale_price):
                    order_pro.product_discount = 0 + int(p_discount[i])
                else:
                    order_pro.product_discount = int(inventory.get().product.sale_price) - int(p_sold_price[i]) + int(p_discount[i])

                self.order_products.append(order_pro)
                for order_product in self.order_products:
                    order_product.order = order
                    order_product.save()                   
                
        else:
            print("no Item selected")
            return redirect(reverse_lazy("order_add"))
        return redirect(reverse_lazy("orders_list"))



    def get_context_data(self, **kwargs):
        context = super(AddOrderView, self).get_context_data(**kwargs)
        context["title"] = "Add Orders"
        context["pos_open"] = True
        return context


@method_decorator([login_required, staff_required], name="dispatch")
class OrderDetail(DetailView):
    model = Order
    template_name='Sales/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super(OrderDetail, self).get_context_data(**kwargs)
        print(self.kwargs)
        invoice = kwargs['object']
        print(invoice.gst_amount)
        context["invoice"] = invoice

        context["title"] = "Orders"
        context["order_open"] = True
        return context

    def post(self, *args, **kwargs):
        viewname = "orders_list"
        print("detail view post request")
        print(kwargs)
        received_amount = int(self.request.POST.get("received_price"))
        order = Order.objects.filter(id=kwargs["pk"])
        new_received_amount = received_amount + int(order.get().paid_amount)
        
        if order.get().total_bill > new_received_amount:
            Order.objects.filter(id=kwargs["pk"]).update(paid_amount=new_received_amount, 
            payment_type="Installment",
            updated_at=timezone.now(),
            )
        if order.get().total_bill == new_received_amount:
            Order.objects.filter(id=kwargs["pk"]).update(paid_amount=new_received_amount, 
            payment_type="Full Paid",
            updated_at=timezone.now(),
            )
        return redirect(reverse_lazy(viewname))

@login_required
def order_add_customer(request, *args, **kwargs):
    if request.is_ajax():
        query = request.GET.get('q')
        print (query)
        if not query :
            customer = ''
            print("Query is empty...")
        else:
            customer = Customer.objects.filter(Q(person_name__icontains=query) | Q(phone__icontains=query)).values()
        response_content = list(customer)
        print("------------response customer--------")
        print(response_content)
    return JsonResponse(response_content, safe= False)


def print_invoice(request, *args, **kwargs):
    context = {}
    print(kwargs)
    template_name = "Sales/partials/invoice_print.html"
    context['invoice'] = Order.objects.filter(id=kwargs['pk']).get()
    return render(request, template_name, context)