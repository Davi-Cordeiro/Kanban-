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

                    cancelEditMode()
                    saveButton.remove();

                } catch (error) {
                    alert(error.message);
                    location.reload()
                }
            });
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
                    location.reload()
                })
                
                .catch((error) => alert(error.message));
        }
    });
});

const cardList = document.querySelectorAll(".card_list")

document.addEventListener("dragstart", (e) => {
    const card = e.target.closest(".card__item");
    if (card) card.classList.add("dragging");
});

document.addEventListener("dragend", (e) => {
    const card = e.target.closest(".card__item");
    if (!card) return;

    card.classList.remove("dragging");
    salvarOrdem(card.closest(".card_list"));
})


async function salvarOrdem(list) {
    const cards = [...list.querySelectorAll('.card__item')];

    const ordem = cards.map((card, index) => ({
        id: card.dataset.cardId,
        position: index
    }))

    console.log(ordem)

    await fetch(window.location.href, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            action: 'move_card',
            list_card_id: list.dataset.listId,
            card_id: ordem
        })
    })
        .then(async (response) => {
            const data = await response.json();
            if (!response) throw new Error(data.error);
        })

        .catch((error) => alert(error.message))
    

}

cardList.forEach((card__item) => {
    card__item.addEventListener("dragover", (e) => {
        e.preventDefault();

        const dragging = document.querySelector(".dragging")
        const applyAfter = getNewPosition(card__item, e.clientY)

        if (applyAfter) {
            applyAfter.insertAdjacentElement("afterend", dragging);
        } else {
            card__item.prepend(dragging)
        }
    })
})

function getNewPosition(cardList, posY) {
    const cards = cardList.querySelectorAll(".card__item:not(.dragging)");
    let result;

    for (let refer_card of cards) {
        const box = refer_card .getBoundingClientRect();
        const boxCenterY = box.y + box.height / 2;

        if (posY >=boxCenterY) result = refer_card;
    }

    return result
}