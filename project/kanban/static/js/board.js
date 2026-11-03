const editButton = document.querySelector('#edit-mode');
const deleteButton = document.querySelector('#delete-mode');
const cancelButton = document.querySelector('#cancel-mode');

const lists = document.querySelectorAll('.list__item')

let editMode = null;

function activateEditMode(mode) {
    editMode = mode;

    lists.forEach(list => {
        list.classList.add('selection-mode');
    });

    editButton.hidden = true;
    deleteButton.hidden = true;
    cancelButton.hidden = false;
}

function cancelEditMode(mode){
    editMode = null;

    lists.forEach(list => {
        list.classList.remove('selection-mode');
    });
    
    editButton.hidden = false;
    deleteButton.hidden = false;
    cancelButton.hidden = true;
}

editButton.addEventListener('click', () => {
    activateEditMode('edit');
});

deleteButton.addEventListener('click', () => {
    activateEditMode('delete');
});

cancelButton.addEventListener('click', () => {
    cancelEditMode();
});


lists.forEach(list => {

    list.addEventListener('click', () => {

        if (!editMode) return;

        const listId = list.dataset.id;

        if (editMode === 'edit') {
            if (editMode === 'edit') {
                const title = list.querySelector('.list__title');

                if (!title) return;

                const input = document.createElement('input');
                input.type = 'text';
                input.value = title.textContent.trim();

                const saveButton = document.createElement('button');
                saveButton.textContent = 'Salvar';
                saveButton.type = 'button';

                title.replaceWith(input);

                list.appendChild(saveButton);

                input.focus();

                saveButton.addEventListener('click', async (event) => {
                    event.stopPropagation();

                    const newTitle = input.value.trim();

                    if (!newTitle) {
                        alert('O título não pode ficar vazio.');
                        return;
                    }

                    try {
                        const response = await fetch(window.location.href, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': csrfToken,
                            },
                            body: JSON.stringify({
                                action: 'edit_list',
                                list_id: listId,
                                new_title: newTitle,
                            })
                        });

                        const data = await response.json();

                        if (!response.ok) {
                            throw new Error(data.error);
                        }

                        const newHeading = document.createElement('h2');
                        newHeading.className = 'list__title';
                        newHeading.textContent = data.title;

                        input.replaceWith(newHeading);
                        saveButton.remove();

                    } catch (error) {
                        alert(error.message);
                    }
                });
            }
        }

        if (editMode === 'delete') {
            const temCards = list.querySelector('.card__item');
            const aviso = temCards
                ? 'Excluir esta etapa também excluirá todos os cartões dela. Tem certeza que deseja continuar?'
                : 'Tem certeza que deseja excluir esta etapa?';

            if (!confirm(aviso)) return;

            fetch(window.location.href, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({
                    action: 'delete_list',
                    list_id: listId,
                }),
            })
                .then(async (response) => {
                    const data = await response.json();
                    if (!response.ok) throw new Error(data.error);
                    list.remove();
                })
                .catch((error) => alert(error.message));
        }
    });
});