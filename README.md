# Kanban Project

Um quadro Kanban no estilo Trello, feito com Django, para estudar desenvolvimento web.

O usuário faz login, cria quadros, organiza as tarefas em listas ("A fazer", "Fazendo", "Feito") e arrasta os cartões entre as listas.

> Projeto de estudo: o código é escrito por mim, seguindo o roteiro abaixo.
> Guia completo: [Projeto Kanban estilo Trello — Guia de Estudo](https://claude.ai/code/artifact/6b828e8a-e3a1-45e1-8ba5-98b18ced18a0)

---

## Tecnologias

| Tecnologia | Uso | Situação |
| --- | --- | --- |
| Python + Django 6.1 | Backend | ✅ Instalado |
| SQLite | Banco de dados em desenvolvimento | ✅ Configurado |
| PostgreSQL | Banco de dados principal | ⏳ Planejado |
| Docker + Docker Compose | Ambiente | ⏳ Planejado |
| HTML + CSS (Flexbox) | Interface | ⏳ Planejado |
| JavaScript + SortableJS | Arrastar e soltar | ⏳ Planejado |

---

## Estrutura

```
Kanban-project/
├── graphic/        # app principal (quadros, listas, cartões)
├── project/
│   ├── manage.py
│   └── project/    # settings, urls, wsgi, asgi
└── venv/           # ambiente virtual (não versionar)
```

---

## Como rodar

```bash
# ativar o ambiente virtual
source venv/bin/activate

# entrar na pasta do manage.py
cd project

# aplicar as migrations e subir o servidor
python manage.py migrate
python manage.py runserver
```

Depois, abra http://localhost:8000.

---

## Modelagem de dados

```
Usuário
 └── Quadro (Board)      título, dono, membros, data de criação
      ├── Etiqueta (Label)   nome, cor
      └── Lista (List)       título, posição
           └── Cartão (Card) título, descrição, prazo, etiquetas, responsável, posição
```

---

## Roteiro

### Etapa 0 — Ambiente
- [x] Criar o projeto Django e o ambiente virtual
- [x] Criar o app `graphic`
- [x] Registrar o app em `INSTALLED_APPS`
- [x] Criar o `requirements.txt`
- [x]  Criar o `.gitignore` (venv, db.sqlite3, `__pycache__`)
- [x] *(depois)* Dockerfile, docker-compose e PostgreSQL

### Etapa 1 — Models e admin
- [x] Criar os models Board, List, Card e Label
- [x] Rodar `makemigrations` e `migrate` sem erro
- [x] Registrar os models no admin e criar dados de teste
- [X] Apagar um quadro apaga as listas e os cartões dele

### Etapa 2 — Login
- [ ] Login e logout
- [ ] Página de cadastro
- [ ] Páginas protegidas redirecionam para o login

### Etapa 3 — Ver os quadros
- [ ] Página "meus quadros"
- [ ] Página do quadro, com as listas lado a lado
- [ ] Usuário não consegue abrir o quadro de outra pessoa (404)
- [ ] Número de queries otimizado (`prefetch_related`)

### Etapa 4 — Criar, editar e excluir
- [ ] Formulários para quadros, listas e cartões
- [ ] Novos itens entram no fim da lista
- [ ] Confirmação antes de excluir
- [ ] Mensagens de feedback

### Etapa 5 — Arrastar e soltar
- [ ] Arrastar cartões entre listas (SortableJS)
- [ ] View que recebe o movimento e salva no banco
- [ ] A nova posição continua igual depois de recarregar a página

### Etapa 6 — Testes
- [ ] Acesso sem login
- [ ] Acesso ao quadro de outro usuário
- [ ] Mover um cartão
- [ ] Criar um cartão no fim da lista

### Extras
- [ ] Destacar cartões com prazo vencido
- [ ] Filtrar por etiqueta ou por responsável
- [ ] Comentários nos cartões
- [ ] Class-Based Views
- [ ] HTMX
- [ ] API com Django REST Framework
- [ ] Deploy

---

## O que estou aprendendo

- Models, relacionamentos (`ForeignKey`, `ManyToManyField`) e migrations
- Sistema de autenticação do Django
- Formulários (`ModelForm`) e validação
- Permissões: cada usuário só acessa os próprios quadros
- Otimização de queries
- Comunicação entre o JavaScript (`fetch`) e o Django (`JsonResponse`, CSRF)
- Testes automatizados

---

## Referências

- [Documentação do Django](https://docs.djangoproject.com/en/stable/)
- [Sistema de autenticação](https://docs.djangoproject.com/en/stable/topics/auth/default/)
- [ModelForms](https://docs.djangoproject.com/en/stable/topics/forms/modelforms/)
- [QuerySet API](https://docs.djangoproject.com/en/stable/ref/models/querysets/)
- [SortableJS](https://github.com/SortableJS/Sortable)
- [MDN: Fetch API](https://developer.mozilla.org/pt-BR/docs/Web/API/Fetch_API/Using_Fetch)
