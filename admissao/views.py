from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView
from .models import Contrato, Templates
from django.db.models import Q
from .forms import TemplateSelectForm, UploadFileForm
from django.http import HttpResponseRedirect


class ContratoSearchView(ListView):
    model = Contrato
    template_name = "admissao/busca_de_candidatos.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        context["order_by"] = self.request.GET.get("order_by", "-id")
        page_obj = context["page_obj"]

        # Obtém o número da página atual
        current_page = page_obj.number

        # Se há mais de 5 páginas
        if page_obj.paginator.num_pages > 5:
            if current_page - 2 < 1:
                start_page = 1
                end_page = 5
            elif current_page + 2 > page_obj.paginator.num_pages:
                start_page = page_obj.paginator.num_pages - 4
                end_page = page_obj.paginator.num_pages
            else:
                start_page = current_page - 2
                end_page = current_page + 2
        else:
            start_page = 1
            end_page = page_obj.paginator.num_pages

        context["page_range"] = range(start_page, end_page + 1)

        return context

    def get_queryset(self):
        query = self.request.GET.get("q")
        order_by = self.request.GET.get("order_by", "-id")
        if query:
            return Contrato.objects.filter(Q(cpf__icontains=query)).order_by(order_by)
        return Contrato.objects.all().order_by(order_by)


from django.contrib import messages  # Importar para enviar mensagens


def upload_template(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_template = Templates(
                name=form.cleaned_data["name"],
                file=request.FILES["file"],
                ano_vigencia=form.cleaned_data["ano_vigencia"],
            )
            new_template.save()
            return HttpResponseRedirect(
                "/upload_template"
            )  # Redirect to a page showing success.
    else:
        form = UploadFileForm()
    return render(request, "admissao/upload.html", {"form": form})
