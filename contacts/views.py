from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Contact
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat


# Create your views here.
def index(request):
    contacts = Contact.objects.order_by('-id').filter(show=True)
    paginator = Paginator(contacts, 12)

    page = request.GET.get('p')
    contacts = paginator.get_page(page)

    return render(request, 'contacts/index.html', {
        'contacts': contacts
    })


def get_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    if not contact.show:
        raise Http404

    return render(request, 'contacts/get_contact.html', {
        'contact': contact
    })


def search(request):
    search = request.GET.get('search')

    if search is None:
        raise Http404

    fields = Concat('name', Value(' '), 'surname')

    contacts = Contact.objects.annotate(
        full_name=fields).order_by('-id').filter(
        Q(full_name__icontains=search) | Q(phone__icontains=search),
        show=True
    )

    paginator = Paginator(contacts, 12)

    page = request.GET.get('p')
    contacts = paginator.get_page(page)

    return render(request, 'contacts/search.html', {
        'contacts': contacts
    })
