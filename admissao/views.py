from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from .models import Contrato, Templates
from django.db.models import Q
from .forms import UploadFileForm, AdmissaoForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy


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


# class FormCandidatoCreateView(CreateView):
#     model = Contrato
#     form_class = AdmissaoForm
#     template_name = "admissao/formulario_candidato.html"
#     success_url = reverse_lazy("form_candidato")

#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         for field, errors in form.errors.items():
#             for error in errors:
#                 messages.error(
#                     self.request, f"Erro no campo '{form.fields[field].label}': {error}"
#                 )
#         return super().form_invalid(form)


class FormCandidatoCreateView(CreateView):
    model = Contrato
    form_class = AdmissaoForm
    template_name = "admissao/formulario_candidato.html"  # substitua com o seu template
    success_url = reverse_lazy(
        "form_candidato"
    )  # substitua com a URL que você quer redirecionar após o sucesso

    def form_valid(self, form):
        cpf = form.cleaned_data.get("cpf")
        collaborator = Contrato.objects.filter(cpf=cpf).first()

        if collaborator:
            # Atualizar o objeto existente
            for field, value in form.cleaned_data.items():
                if (
                    value is not None
                    and hasattr(collaborator, field)
                    and field != "created_by"
                ):
                    setattr(collaborator, field, value)
            collaborator.save()
            self.object = collaborator
        else:
            # Criar um novo objeto
            if self.request.user.is_authenticated:
                form.instance.created_by = self.request.user
            self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def validate_cpf(value):
        if len(value) != 11 or not value.isdigit():
            return False
        cpf = [int(char) for char in value]
        if cpf == cpf[::-1]:
            return False
        for i in range(9):
            val = sum((cpf[num] * ((10 - i) % 11)) for num in range(0, 10))
            digit = ((val * 10) % 11) % 10
            if digit != cpf[9]:
                return False
        val = sum((cpf[num] * ((11 - i) % 11)) for num in range(0, 11))
        digit = ((val * 10) % 11) % 10
        if digit != cpf[10]:
            return False
        return True
