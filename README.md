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
| PostgreSQL | Banco de dados principal | ✅ Configurado (Docker) |
| Docker + Docker Compose | Ambiente | ✅ Configurado |
| HTML + CSS (Flexbox) | Interface | 🔄 Em andamento |
| JavaScript + SortableJS | Arrastar e soltar | ⏳ Planejado |

---

## Estrutura

```
Kanban-project/
├── Dockerfile
├── docker-compose.yml   # serviços: djangoapp (Django) e psql (PostgreSQL)
├── dotenv_files/        # .env e .env-example (NÃO versionado)
├── data/                # dados do Postgres, static e media (NÃO versionado)
├── project/
│   ├── manage.py
│   ├── requirements.txt
│   ├── account/         # usuários: login, cadastro, logout, reset de senha
│   │   ├── views.py
│   │   ├── forms.py     # LoginForm, RegisterForm
│   │   ├── urls.py      # sem app_name: rotas 'entrar', 'registrar', 'sair'
│   │   ├── tests.py
│   │   ├── static/css/style.css
│   │   └── templates/   # base.html, partials/, registration/
│   ├── kanban/          # quadros, listas, cartões e etiquetas
│   │   ├── models.py    # BoardInfo, ListInfo, CardInfo, LabelInfo
│   │   ├── admin.py
│   │   ├── views.py
│   │   ├── forms.py     # BoardForm, ListForm, CardForm
│   │   ├── urls.py      # app_name = 'kanban': rotas 'kanban:home', 'kanban:board'...
│   │   ├── tests.py
│   │   └── templates/kanban/   # home.html, board.html, board_form.html
│   └── project/         # settings, urls, wsgi, asgi
│                        # urls: '' → account, 'kanban/' → kanban
└── venv/                # ambiente virtual (não versionar)
```

---

## Como rodar (com Docker)

### Primeira vez em um PC novo

1. Clonar o repositório e entrar na pasta:
   ```bash
   git clone <url-do-repositorio> Kanban-project
   cd Kanban-project
   ```

2. Criar o arquivo de variáveis de ambiente. A pasta `dotenv_files/` está no
   `.gitignore`, então ela **não vem no clone**: é preciso criar na mão.
   ```bash
   mkdir dotenv_files
   nano dotenv_files/.env
   ```
   Conteúdo (troque os `CHANGE-ME`):
   ```env
   SECRET_KEY="CHANGE-ME"

   # 0 False, 1 True
   DEBUG="1"

   # Comma Separated values
   ALLOWED_HOSTS="127.0.0.1, localhost"

   DB_ENGINE="django.db.backends.postgresql"
   POSTGRES_DB="CHANGE-ME"
   POSTGRES_USER="CHANGE-ME"
   POSTGRES_PASSWORD="CHANGE-ME"
   POSTGRES_HOST="psql"
   POSTGRES_PORT="5432"
   ```
   - `POSTGRES_HOST` precisa ser **`psql`** (o nome do serviço no
     `docker-compose.yml`), e não `localhost`: dentro do container,
     `localhost` é o próprio container do Django.
   - Para gerar uma `SECRET_KEY`:
     ```bash
     python3 -c "import secrets; print(secrets.token_urlsafe(50))"
     ```

3. Subir os containers (o `--build` monta a imagem do Django):
   ```bash
   sudo docker compose up --build
   ```
   O container já roda `migrate` e `runserver` sozinho (veja o `CMD` do Dockerfile).

4. Em **outro terminal**, criar o superusuário:
   ```bash
   sudo docker compose exec djangoapp python manage.py createsuperuser
   ```

5. Abrir http://localhost:8000 (site) e http://localhost:8000/admin (admin).

### No dia a dia

```bash
sudo docker compose up            # subir
sudo docker compose down          # parar
sudo docker compose up --build    # depois de mudar requirements.txt ou Dockerfile

# rodar comandos do Django dentro do container
sudo docker compose exec djangoapp python manage.py makemigrations
sudo docker compose exec djangoapp python manage.py migrate
sudo docker compose exec djangoapp python manage.py shell
```

> A pasta `project/` é montada como volume, então mudanças no código aparecem
> na hora (o `runserver` recarrega sozinho), sem precisar rebuildar.

### Problemas comuns

| Erro | Causa provável |
| --- | --- |
| `env file ... not found` | Faltou criar `dotenv_files/.env` (passo 2) |
| `could not translate host name "localhost"` / `connection refused` | `POSTGRES_HOST` está como `localhost`, use `psql` |
| `relation "..." does not exist` | Faltou o `migrate` |
| `service "..." is not running` | Use `run --rm` no lugar de `exec`, ou suba com `up` antes |
| Permissão negada na pasta `data/` | Os arquivos foram criados pelo Docker como root: `sudo chown -R $USER data/` |

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
- [x] Criar o app de usuários (`boards`, depois renomeado para `account`)
- [x] Criar o app `kanban` (ver Etapa 2.5)
- [x] Registrar os apps em `INSTALLED_APPS`
- [x] Criar o `requirements.txt`
- [x]  Criar o `.gitignore` (venv, db.sqlite3, `__pycache__`)
- [x] *(depois)* Dockerfile, docker-compose e PostgreSQL

### Etapa 1 — Models e admin
- [x] Criar os models Board, List, Card e Label
- [x] Rodar `makemigrations` e `migrate` sem erro
- [x] Registrar os models no admin e criar dados de teste
- [X] Apagar um quadro apaga as listas e os cartões dele

### Etapa 2 — Login
- [x] Login e logout
- [x] Página de cadastro
- [x] Páginas protegidas redirecionam para o login (`@login_required` + `LOGIN_URL = 'entrar'`)
- [ ] Teste: abrir a `home` sem login redireciona para `entrar`

### Etapa 2.5 — Separar os apps `account` e `kanban`
- [x] Renomear o app `boards` para `account` (só autenticação)
- [x] Criar o app `kanban` e registrar em `INSTALLED_APPS`
- [x] Mover models e admin do Kanban para o `kanban`
- [x] Recriar as migrations no app novo (`kanban/migrations/0001_initial.py`)
- [x] Mover a `home` para o `kanban`, com namespace (`kanban:home`)
- [x] `python manage.py check` e testes passando
- [ ] Decidir a raiz `/`: hoje dá 404 (a home está em `/kanban/`). Opções: trocar
      `path('kanban/', ...)` por `path('', include('kanban.urls'))` no `project/urls.py`,
      ou fazer `/` redirecionar para `kanban:home`
- [ ] Limpeza: apagar `login_view` e `logout_view` do `account` (não são usadas)

<details>
<summary><b>O que foi feito e o que aprendi</b></summary>

**Divisão dos apps**
- `account` → login, cadastro, logout, reset de senha. Guarda também o
  `base.html`, os `partials/` e o `style.css`, que são usados pelo site todo
  (o `{% extends "base.html" %}` acha o arquivo em qualquer app).
- `kanban` → quadros, listas, cartões, etiquetas e as páginas deles.

**Migrations ao mover models entre apps**
O nome da tabela depende do app (`boards_boardinfo` → `kanban_boardinfo`).
Como estamos em desenvolvimento, o caminho foi **desfazer → mover → recriar**:
1. `migrate boards zero` com os models **ainda** no app antigo (apaga as tabelas;
   os usuários ficam, porque são do app `auth`);
2. mover o código e apagar a migration antiga;
3. `makemigrations kanban` e `migrate`.

O banco do Kanban foi zerado: criar dados de teste de novo pelo admin.

**Namespace de URLs**
- O prefixo `app:` vem do `app_name` do `urls.py` **onde a rota está definida**.
- `kanban/urls.py` tem `app_name = 'kanban'` → `kanban:home`, `kanban:board`...
- `account/urls.py` não tem → `entrar`, `registrar`, `sair` (sem prefixo).
- O `manage.py check` **não** pega nome de rota errado em `redirect`, `{% url %}`
  e `reverse`: só os testes (ou abrir a página) mostram o `NoReverseMatch`.
  Para achar todos os usos: `grep -rn "'home'\|\"home\"" project/`

**Templates com namespace**
Os templates do kanban ficam em `kanban/templates/kanban/` e a view usa
`render(request, 'kanban/home.html')`. A pasta com o nome do app evita que um
`home.html` de um app esconda o de outro.

**Rotina antes de commitar**
```bash
sudo docker compose exec djangoapp python manage.py check
sudo docker compose exec djangoapp python manage.py test
git add -A   # o -A faz o git reconhecer arquivos renomeados/movidos
```

</details>

### Etapa 3 — Ver os quadros ⬅️ **próximo passo**
- [ ] Ordenação por `position` em listas e cartões
- [ ] Página "meus quadros"
- [ ] Página do quadro, com as listas lado a lado
- [ ] Usuário não consegue abrir o quadro de outra pessoa (404)
- [ ] Número de queries otimizado (`prefetch_related`)

<details>
<summary><b>Como fazer a Etapa 3 (passo a passo)</b></summary>

> Dica: o banco do Kanban foi zerado na Etapa 2.5. Crie alguns quadros, listas
> e cartões pelo **admin** para ter dados de teste antes de ter os formulários.

> Tudo desta etapa fica no app **`kanban`**. Nomes de rota com namespace:
> `kanban:home`, `kanban:board`...

> ⚠️ Só use `{% url 'kanban:algo' %}` num template **depois** que a rota existir
> no `kanban/urls.py`. Antes disso a página dá erro 500 (`NoReverseMatch`).

**1. Ordenação nos models**
Em `ListInfo` e `CardInfo`, adicionar:
```python
class Meta:
    ordering = ['position']
```
Assim `board.lists.all` e `list.cards.all` já vêm em ordem. Rodar
`makemigrations` e `migrate` depois (o Django registra a mudança em uma migration).

**2. Quadros na home (`home_view`)**
Buscar os quadros em que o usuário é dono **ou** membro. O `Q` permite usar "ou"
no filtro:
```python
from django.db.models import Q

@login_required
def home_view(request):
    boards = BoardInfo.objects.filter(
        Q(owner=request.user) | Q(members=request.user)
    ).distinct().order_by('-created_at')
    return render(request, 'kanban/home.html', {'boards': boards})
```
- Com o `@login_required`, só usuário logado chega aqui: no `home.html`, o
  `{% if user.is_authenticated %} / {% else %}` deixa de ser necessário.
- O `.distinct()` evita quadro duplicado quando o usuário é dono e membro ao mesmo tempo.

- Imports em `kanban/views.py`: `from .models import BoardInfo`.

No `kanban/home.html`, trocar o comentário por um `for` com `empty`. Por enquanto
**só o título**, sem link (a rota `kanban:board` ainda não existe):
```django
{% for board in boards %}
    <div class="board-card">{{ board.title }}</div>
{% empty %}
    <p class="home__empty">Você ainda não tem nenhum quadro.</p>
{% endfor %}
```
Teste em `kanban/tests.py`: o usuário A vê os quadros dele e **não** vê os do
usuário B (`response.context['boards']`).

**3. Página do quadro**
- `kanban/urls.py`: `path('board/<int:pk>/', views.board_view, name='board')`
- `kanban/views.py`:
  - decorator `@login_required` (o `LOGIN_URL = 'entrar'` já está configurado);
  - buscar com `get_object_or_404`, **já filtrando pelo usuário** (mesmo `Q` do passo 2),
    assim trocar o número na URL dá 404 em vez de mostrar o quadro de outra pessoa;
  - renderizar `kanban/board.html` com `{'board': board}`.
- Agora que a rota existe, transformar o título na home em link:
  `<a class="board-card" href="{% url 'kanban:board' board.pk %}">{{ board.title }}</a>`
- O `painel.html` vazio que já existe em `kanban/templates/kanban/` pode virar o
  `board.html` (é só renomear).
- `kanban/board.html` (estende `base.html`): dois `for` aninhados:
  ```django
  <h1>{{ board.title }}</h1>
  <div class="kanban">
      {% for list in board.lists.all %}
          <div class="kanban__column">
              <h2 class="kanban__column-title">{{ list.title }}</h2>
              {% for card in list.cards.all %}
                  <div class="kanban__card">{{ card.title }}</div>
              {% endfor %}
          </div>
      {% endfor %}
  </div>
  ```

**4. CSS das colunas**
```css
.kanban {
  display: flex;
  gap: 1rem;
  overflow-x: auto;      /* rolagem horizontal quando há muitas listas */
  align-items: flex-start;
}

.kanban__column {
  flex: 0 0 280px;       /* largura fixa, não estica nem encolhe */
  background-color: var(--color-border);
  border-radius: var(--radius);
  padding: 0.75rem;
}

.kanban__card {
  background-color: var(--color-surface);
  border-radius: var(--radius);
  padding: 0.5rem 0.75rem;
  margin-bottom: 0.5rem;
}
```

**5. Otimizar as queries**
Sem otimização, cada lista faz uma query para buscar os cartões. Na view:
```python
.prefetch_related('lists__cards')
```
Para conferir: instalar o `django-debug-toolbar` ou contar as queries com
`from django.db import connection; len(connection.queries)` (com `DEBUG=1`).

</details>

### Etapa 4 — Criar, editar e excluir
- [ ] Formulários para quadros, listas e cartões
- [ ] Novos itens entram no fim da lista
- [ ] Confirmação antes de excluir
- [ ] Mensagens de feedback

<details>
<summary><b>Como fazer a Etapa 4 (resumo)</b></summary>

- Criar `ModelForm`s em `forms.py` (`BoardForm`, `ListForm`, `CardForm`) com só
  os campos que o usuário preenche (ex.: `fields = ['title']`).
- Na view: `form = BoardForm(request.POST or None)`; se `form.is_valid()`, fazer
  `obj = form.save(commit=False)`, preencher o que vem do sistema
  (`obj.owner = request.user`, `obj.board = board`...), `obj.save()` e `redirect`.
- **Fim da lista:** antes de salvar, calcular a próxima posição:
  ```python
  from django.db.models import Max
  ultimo = board.lists.aggregate(Max('position'))['position__max']
  obj.position = (ultimo or 0) + 1
  ```
- **Criar quadro:** rota `path('boards/novo/', views.board_create_view, name='criar_board')`
  e, depois dela existir, o botão na home:
  `<a class="btn" href="{% url 'kanban:criar_board' %}">+ Novo quadro</a>`
- **Excluir:** GET mostra uma página "Tem certeza?", POST apaga. Nunca apagar no GET.
- **Mensagens:** `from django.contrib import messages` →
  `messages.success(request, 'Quadro criado!')`, e exibir no `base.html` com
  `{% for message in messages %}`.
- Sempre usar `{% csrf_token %}` dentro do `<form method="post">`.

</details>

### Etapa 5 — Arrastar e soltar
- [ ] Arrastar cartões entre listas (SortableJS)
- [ ] View que recebe o movimento e salva no banco
- [ ] A nova posição continua igual depois de recarregar a página

<details>
<summary><b>Como fazer a Etapa 5 (resumo)</b></summary>

1. Colocar `data-list-id="{{ list.pk }}"` em cada coluna e
   `data-card-id="{{ card.pk }}"` em cada cartão.
2. Carregar o SortableJS no `board.html` e criar um `Sortable` para cada coluna,
   todos com o mesmo `group: 'cards'` (permite mover entre colunas).
3. No `onEnd` do Sortable, mandar um `fetch` (POST) para uma URL tipo
   `card/<id>/move/` com `{ list_id, position }` em JSON, enviando o CSRF no
   header `X-CSRFToken` (ler do cookie `csrftoken`).
4. Na view: conferir se o cartão e a lista de destino são de um quadro do usuário,
   atualizar `list` e `position` do cartão, reordenar os outros cartões da lista
   e responder com `JsonResponse({'ok': True})`.
5. Testar: mover, recarregar a página, o cartão deve continuar no lugar.

> Antes do arrastar e soltar, dá para fazer uma versão simples: um `<select>`
> no cartão para escolher a lista de destino.

</details>

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
