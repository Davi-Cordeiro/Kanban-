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
    if (!editMode) return;

    const boardId = board.dataset.id;

    if (editMode === 'edit') {
        const title = board.querySelector('.title__board')

        if (!title) return;

        const input = document.createElement('input');
        input.type = 'text';
        input.value = title.textContent.trim();

        const saveButton = document.createElement('button');
        saveButton.textContent = 'Salvar';
        saveButton.type = 'button';

        title.replaceWith(input);

        board.appendChild(saveButton);

        input.focus();

        
    }
})