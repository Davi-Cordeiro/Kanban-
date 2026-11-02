const editButton = document.querySelector('#edit-mode');
const deleteButton = document.querySelector('#delete-mode');
const cancelButton = document.querySelector('#cancel-mode');

const lists = document.querySelectorAll('list__item')

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
            console.log('Editar etapa:', listId);
        }

        if (editMode === 'delete') {
            console.log('Excluir etapa:', listId);
        }

    });

});