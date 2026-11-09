const editButton = document.querySelector('#edit-mode');
const deleteButton = document.querySelector('#delete-mode');
const cancelButton = document.querySelector('#cancel-mode');

const boards = document.querySelectorAll('.board__item')

let editMode = null;

function activateEditMode(mode) { 
    editMode = mode;

    boards.forEach(board => {
        board.classList.add('selection-mode');
    })

    editButton.hidden = true;
    deleteButton.hidden = true;
    cancelButton.hidden = false;
}

function cancelEditMode(mode){
    editMode = null;

    boards.forEach(board => {
        board.classList.remove('selection-mode')
    })

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
})

boards.forEach(board => {
    board.addEventListener('click', (event) => { 
        if (!editMode) return;

        const boardId = board.dataset.id;

        if (editMode === 'edit') {
            const title = board.querySelector('.title__board')

            if (title == null) return;

            const linkUrlTitle = title.getAttribute('href');
            event.preventDefault();


            const input = document.createElement('input');
            input.type = 'text';
            input.value = title.textContent.trim();

            const saveButton = document.createElement('button');
            saveButton.textContent = 'Salvar';
            saveButton.type = 'button';

            title.replaceWith(input);

            board.appendChild(saveButton);

            input.focus();

            saveButton.addEventListener('click', async (event) => {
                const newTitle = input.value.trim();

                event.preventDefault();

                if (!newTitle) {
                    alert('O título não pode estar vazio.');
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
                            action: 'edit_board',
                            board_id: boardId,
                            new_title: newTitle
                        })
                    })

                    const data = await response.json();

                    if (!response.ok){
                        throw new Error(data.error)
                        
                    }

                    const newTitleElement = document.createElement('a');
                    newTitleElement.classList.add('title__board');
                    newTitleElement.textContent = data.title;
                    newTitleElement.setAttribute('href', linkUrlTitle);

                    input.replaceWith(newTitleElement);

                    cancelEditMode();

                    saveButton.remove();
                } catch (error) {
                    alert(error.message);
                    location.reload();
                }
            });
    }
    
    if (editMode === 'delete') {
        const aviso = 'Excluir este quadro apagará todas as etapas e cartões dele. Continuar?';

        event.preventDefault()

        if (!confirm(aviso)) {
            return;
        };

        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
                },
            body: JSON.stringify({
                action: 'delete_board',
                board_id: boardId
            })
        })
            .then(async (response) => {
                const data = await response.json();
                if (!response.ok) throw new Error(data.error);
                board.closest('.home__items').remove();
                cancelEditMode();
                location.reload();
            })
            .catch (error => { alert(error.message) })
        }
    });
})