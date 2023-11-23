from django.shortcuts import render, get_object_or_404

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import Cadastro, Observacoes

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q


def render_main(request):

    return render(request, 'screens/main.html')

def edit_cadastro(request):
    if request.method == 'POST':
        edit_id = request.POST.get('editId')

        edit_cpf = request.POST.get('editCPF')
        edit_cnpj = request.POST.get('editCNPJ')

        if len(edit_cnpj) == 14:
            cnpj = '{}.{}.{}/{}-{}'.format(edit_cnpj[:2], edit_cnpj[2:5], edit_cnpj[5:8], edit_cnpj[8:12], edit_cnpj[12:])
        else:
            cnpj = edit_cnpj if edit_cnpj else ''

        if len(edit_cpf) == 11:
            cpf = '{}.{}.{}-{}'.format(edit_cpf[:3], edit_cpf[3:6], edit_cpf[6:9], edit_cpf[9:11])
        else:
            cpf = edit_cpf if edit_cpf else ''


        cadastro = get_object_or_404(Cadastro, pk=edit_id)
        cadastro.nome = request.POST.get('editNome')
        cadastro.cpf = cpf
        cadastro.cnpj = cnpj
        cadastro.ie = request.POST.get('editIE')
        cadastro.endereco = request.POST.get('editEndereco')
        cadastro.cidade = request.POST.get('editCidade')
        cadastro.bairro = request.POST.get('editBairro')
        cadastro.cep = request.POST.get('editCEP')
        cadastro.telefone = request.POST.get('editTelefone')
        cadastro.celular = request.POST.get('editCelular')
        cadastro.whatsapp = request.POST.get('editWhatsapp')
        cadastro.email = request.POST.get('editEmail')
        cadastro.save()


        # Editar observações
        edit_observacoes = request.POST.get('editObservacoes')
        observacoes = Observacoes.objects.filter(cadastro=cadastro)
        if observacoes.exists():
            observacao = observacoes.first()
            observacao.observacoes = edit_observacoes
            observacao.save()
        else:
            nova_observacao = Observacoes(cadastro=cadastro, observacoes=edit_observacoes)
            nova_observacao.save()

        return HttpResponseRedirect('/pesquisa/')



def save_cadastro(request):
    if request.method == 'POST':
        nome_fornecedor = request.POST.get('nome')
        endereco = request.POST.get('endereco')
        cidade = request.POST.get('cidade')
        bairro = request.POST.get('bairro')
        rua = request.POST.get('rua')
        cnpj = request.POST.get('cnpj')
        cpf = request.POST.get('cpf')
        cep = request.POST.get('cep')
        ie = request.POST.get('ie')
        telefone = request.POST.get('telefone')
        whatsapp = request.POST.get('whatsapp')
        email = request.POST.get('email')
        celular = request.POST.get('celular')
        observacoes = request.POST.get('observacoes')
        print(endereco)
        if cnpj != '':
            cnpj = '{}.{}.{}/{}-{}'.format(cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:])
        else:
            cnpj = ''
        if cpf != '':
            cpf = '{}.{}.{}-{}'.format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:11])
        else: 
            cpf = ''
    
   
        novo_cadastro = Cadastro.objects.create(
            nome=nome_fornecedor,
            endereco=endereco,
            cidade=cidade,
            bairro=bairro,
            cnpj=cnpj,
            cpf=cpf,
            ie=ie,
            cep=cep,
            telefone=telefone,
            whatsapp=whatsapp,
            email=email,
            celular=celular
        )
        nova_observacao = Observacoes.objects.create(
            cadastro=novo_cadastro,
            observacoes=observacoes
        )
        nova_observacao.save()

        return HttpResponseRedirect('/')
    return HttpResponse('Erro ao criar novo registro de fornecedor e produto')

def listar_cadastro(request):
    query_observacoes = request.GET.get('q_observacoes')
    query_informacoes = request.GET.get('q_informacoes')

    all_cadastros = Cadastro.objects.all()

    filters = Q()

    if query_observacoes:
        filters |= Q(observacoes__observacoes__icontains=query_observacoes)

    if query_informacoes:
        filters |= (
            Q(nome__icontains=query_informacoes) |
            Q(cnpj__icontains=query_informacoes) |
            Q(cpf__icontains=query_informacoes) |
            Q(ie__icontains=query_informacoes)
        )

    if filters:
        all_cadastros = all_cadastros.filter(filters).distinct()

    all_cadastros = all_cadastros.order_by('-data_criacao')

    cadastros_por_pagina = 10
    paginator = Paginator(all_cadastros, cadastros_por_pagina)
    
    page_number = request.GET.get('page')
    try:
        cadastros = paginator.page(page_number)
    except PageNotAnInteger:
        cadastros = paginator.page(1)
    except EmptyPage:
        cadastros = paginator.page(paginator.num_pages)

    context = {'cadastros': cadastros}
    return render(request, 'screens/lista.html', context)


def excluir_cadastro(request):
    if request.method == 'POST':
        cadastro_id = request.POST.get('cadastro_id')
        try:
            cadastro = Cadastro.objects.get(pk=cadastro_id)
            cadastro.delete()
            return HttpResponseRedirect('/pesquisa/')
        except Cadastro.DoesNotExist:
            return JsonResponse({'error': 'Cadastro não encontrado'}, status=404)