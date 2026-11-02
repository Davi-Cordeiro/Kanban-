const editButton = document.querySelector('#edit-mode');
const deleteButton = document.querySelector('#delete-mode');
const cancelButton = document.querySelector('#cancel-mode');

const lists = documento.querySelector('list__item')

const editMode = null;

function activateEditMode(mode) {
    editMode = mode;

    list.forEach(list => {
        list.classList.add('selection-mode');
    });
}