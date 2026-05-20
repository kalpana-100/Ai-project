from django.shortcuts import render
from django.http  import HttpResponse

from .forms import CreateProductForm, UpdateProductForm
from .models import Product
from django.contrib.auth.decorators import login_required

# Create your views here.
def homepage(request):
	p= Product.objects.all()
	data ={
		"products":p
    }
	return render(request,"home/products.html",data)

def get_item(request,id):
	try:
		product=Product.objects.get(id=id)
	except:
		return HttpResponse("Product Not Found")
	data={
		'product':product
	}
	return render(request,"home/product.html",data)
from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

# def create_product(request):
#     if request.method == "POST":
#         name = request.POST.get('name')
#         price = request.POST.get('price')
#         description = request.POST.get('description')

#         p = Product(name=name, price=price, description=description)
#         p.save()

#         return HttpResponse("Product Created Successfully")

#     return render(request, "home/create.html")

#create
@login_required()
def create_product(request):
	form=CreateProductForm()
	if request.method=="POST":
		user=request.user
		form=CreateProductForm(request.POST)
		if form.is_valid():
			product = form.save(commit=False)
			product.owner = request.user
			form.save()
   
		return HttpResponse("Product Created Successfully")
	return render(request,"home/create.html",{"form":form})

#update
@login_required()
def update_product(request,id):
	try:
		product=Product.objects.get(id=id)
		if request.user != product.owner:
			return HttpResponse("You are not the owner of this product")
	except:
		return HttpResponse("Product Not Found")
	form=UpdateProductForm(instance=product)
	if request.method=="POST":
		form=UpdateProductForm(request.POST,instance=product)
		if form.is_valid():
			form.save()
		return HttpResponse("Product Updated Successfully")
	return render(request,"home/update.html",{"form":form})

#delete
@login_required()
def delete_product(request,id):
	try:
		product=Product.objects.get(id=id)
		if request.user != product.owner:
			return HttpResponse("You are not the owner of this product")
	except:
		return HttpResponse("Product Not Found")
	form=UpdateProductForm(instance=product)
	if request.method=="POST":
		form=UpdateProductForm(request.POST,instance=product)
		if form.is_valid():
			form.save()
	product.delete()
	return HttpResponse("Product Deleted Successfully")

def aboutus(request):
	return HttpResponse("i am anuja")

def contactus(request):
	return HttpResponse("9844000000")
def base(request):
	return render(request,'base.html')
def about(request):
    data = {
        'Name': 'Anuja',
        'Age': 21,
        'fav_fruits': ['Apple', 'Mango', 'Banana']
    }
    return render(request, 'home/about.html',data)

