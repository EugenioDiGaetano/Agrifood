const filepath = 'Url.json';

let aggiungiUrl, homeUrl, eliminaUrl, prenotaUrl, aggiornaUrl;

// Funzione per applicare l'effetto di dissolvenza in entrata
function fadeIn(element) {
    element.style.opacity = '0';
    element.style.display = 'block';
    const fadeInEffect = setInterval(function() {
        if (element.style.opacity < 1) {
            element.style.opacity = parseFloat(element.style.opacity) + 0.1; 
        } else {
            clearInterval(fadeInEffect);
        }
    }, 50);
}

// Funzione per applicare l'effetto di dissolvenza in uscita
function fadeOut(element) {
    let opacity = 1;
    const fadeOutEffect = setInterval(function() {
        if (opacity > 0) {
            opacity -= 0.1;
            element.style.opacity = opacity;
        } else {
            clearInterval(fadeOutEffect);
            element.style.display = 'none';
        }
    }, 50);
}

// Funzione per recuperare i post dal backend
function fetchPostsFromBackend() {
    fetch(homeUrl)
    .then(response => {
        if (!response.ok) {
            throw new Error('Errore durante il recupero dei post');
        }
        return response.json();
    })
    .then(data => {
        const responseData = JSON.parse(data.body);
        responseData.sort((a, b) => new Date(b.date.S) - new Date(a.date.S));
        
        responseData.sort((a, b) => {
            const qtaA = parseInt(a.quantity.N);
            const qtaB = parseInt(b.quantity.N);
            
            if (qtaA === 0 && qtaB !== 0) {
                return 1;
            } else if (qtaA !== 0 && qtaB === 0) {
                return -1;
            } else {
                return 0;
            }
        });
        displayPosts(responseData);
    })
    .catch(error => {
        console.error('Si è verificato un errore durante il recupero dei post:', error);
    });
}

// Funzione per visualizzare i post recuperati
function displayPosts(posts) {
    const postList = document.getElementById('post-list');
    let postsHTML = '';

    posts.forEach(post => {
        // Verifica se i campi del post sono definiti prima di aggiungerli all'HTML
        const title = post.title !== undefined ? `<h3>${post.title.S}</h3>` : '';
        const description = post.description !== undefined ? `<p><b>Descrizione: </b>${post.description.S}</p>` : '';
        const date = post.date !== undefined ? `<p><b>Data di Pubblicazione:</b> ${post.date.S}</p>` : '';
        const totalQuantity = post.totalQuantity !== undefined ? `<p><b>Quantità Totale:</b> ${post.totalQuantity.N}</p>` : '';
        const quantity = post.quantity !== undefined ? `<p><b>Quantità Attualmente Disponibile:</b> ${post.quantity.N}</p>` : '';
        const fertilizers = post.fertilizers !== undefined ? `<p><b>Concimi Utilizzati:</b> ${post.fertilizers.S}</p>` : '';
        const cultivation = post.cultivation !== undefined ? `<p><b>Coltivazione:</b> ${post.cultivation.S}</p>` : '';
        const cropType = post.cropType !== undefined ? `<p><b>Tipologia di Coltura:</b> ${post.cropType.S}</p>` : '';
        const contactInfo = post.contactInfo !== undefined ? `<p><b>Informazioni di Contatto:</b> ${post.contactInfo.S}</p>` : '';
        const email = post.email !== undefined ? `<p><b>Email:</b> ${post.email.S}</p>` : '';

        postsHTML += `
            <div class="post">
                ${title}
                ${description}
                ${date}
                ${totalQuantity}
                ${quantity}
                ${fertilizers}
                ${cultivation}
                ${cropType}
                ${contactInfo}
                ${email}
                <button onclick="updatePost('${post.Id.S}')">Aggiorna</button>
                <button onclick="deletePost('${post.Id.S}')">Elimina</button>
                <button onclick="bookPost('${post.Id.S}')">Prenota</button>
            </div>
        `;
    });

    postList.innerHTML = postsHTML;
}

// Script per gestire l'eliminazione di un post
function deletePost(postId) {
    let password;
    do {
        password = prompt('Inserisci la password per confermare l\'eliminazione:');
        if (password === null) return;
        if (password.length < 1 || password.length > 10) {
            alert('La password deve essere composta da 1 a 10 caratteri.');
        }
    } while (password.length < 1 || password.length > 10);

	const delData = {
        "post_id": String(postId),
        "password": String(password)
    };

    var requestOptions = {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(delData),
        redirect: 'follow'
    };

    fetch(eliminaUrl, requestOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error('Errore durante l\'eliminazione del post');
				throw new (response);
            }
            return response.json();
        })
        .then(result => {
            alert(result.body);
			window.location.reload();

        })
        .catch(error => console.error('Si è verificato un errore durante l\'invio del post:', error));
}

// Script per gestire la prenotazione di un post
function bookPost(postId) {
    let quantity;
    do {
        quantity = prompt('Inserisci la quantità prenotata (solo numeri maggiori di 1):');
        if (quantity === null) return;
        quantity = parseInt(quantity);
    } while (isNaN(quantity) || quantity <= 0);
	
	const pren = {
        "post_id": String(postId),
        "qta_subtract": quantity
    };

    var requestOptions = {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(pren),
        redirect: 'follow'
    };

    fetch(prenotaUrl, requestOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error('Errore durante la prenotazione del post');
				throw new (response);
            }
            return response.json();
        })
        .then(result => {
            alert(result.body);
			window.location.reload();

        })
        .catch(error => console.error('Si è verificato un errore durante l\'invio del post:', error));

}

// Script per gestire l'aggiornamento della quantità disponibile di un post
function updatePost(postId) {
    let quantity, password;
    do {
        quantity = prompt('Inserisci la quantità da incrementare (solo numeri maggiori di 1):');
        if (quantity === null) return;
        quantity = parseInt(quantity);
    } while (isNaN(quantity) || quantity <= 0);
    do {
        password = prompt('Inserisci la password per confermare l\'aggiornamento della quantità disponibile:');
        if (password === null) return;
        if (password.length < 1 || password.length > 10) {
            alert('La password deve essere composta da 1 a 10 caratteri.');
        }
    } while (password.length < 1 || password.length > 10);
	
	const pren = {
        "post_id": String(postId),
        "qta_add": quantity,
		"password": password
    };

    var requestOptions = {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(pren),
        redirect: 'follow'
    };

    fetch(aggiornaUrl, requestOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error('Errore durante la prenotazione del post');
				throw new (response);
            }
            return response.json();
        })
        .then(result => {
            alert(result.body);
			window.location.reload();

        })
        .catch(error => console.error('Si è verificato un errore durante l\'invio del post:', error));
		
}

// Funzione per mostrare/nascondere il menu a tre puntini
function toggleDropdown(button) {
    button.nextElementSibling.classList.toggle('show');
}

//Recupero dati dal file json
function fetchLinksFromFile(jsonspath) {
    return fetch(jsonspath)
        .then(response => {
            if (!response.ok) {
                throw new Error('Errore durante il recupero del file JSON');
            }
            return response.json();
        })
        .catch(error => {
            console.error('Si è verificato un errore durante il recupero del file JSON:', error);
        });
}

// Funzione per inizializzare il tuo script dopo aver ottenuto i link dal file JSON
async function initializeScript(jsonspath) {
    try {
        const links = await fetchLinksFromFile(jsonspath);
        aggiungiUrl = links.aggiungi;
        homeUrl = links.home;
        eliminaUrl = links.elimina;
        prenotaUrl = links.prenota;
        aggiornaUrl = links.aggiorna; 
    } catch (error) {
        console.error('Si è verificato un errore durante l\'inizializzazione dello script:', error);
    }
}

// Script per gestire l'apertura/chiusura del modulo di inserimento di un nuovo post
document.querySelector('.new-post-heading').addEventListener('click', function() {
    const newPostContent = document.querySelector('.new-post-content');
    newPostContent.classList.toggle('hidden');
});

// Script per gestire l'invio del form per l'inserimento di un nuovo post
document.getElementById('post-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const quantity = parseInt(document.getElementById('quantity').value);
    const fertilizers = document.getElementById('fertilizers').value;
    const cultivation = document.getElementById('cultivation').value;
    const cropType = document.getElementById('crop_type').value;
    const contactInfo = document.getElementById('contact_info').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const postData = {};

	if (title !== '') postData.title = title;
    if (description !== '') postData.description = description;
    if (!isNaN(quantity)) {
        postData.quantity = quantity;
        postData.totalQuantity = quantity;
    }
    if (fertilizers !== '') postData.fertilizers = fertilizers;
    if (cultivation !== '') postData.cultivation = cultivation;
    if (cropType !== '') postData.cropType = cropType;
    if (contactInfo !== '') postData.contactInfo = contactInfo;
    if (email !== '') postData.email = email;
    if (password !== '') postData.password = password;

    var requestOptions = {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(postData),
        redirect: 'follow'
    };

    fetch(aggiungiUrl, requestOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error('Errore durante l\'invio del post');
            }
            return response.json();
        })
        .then(result => {
            alert(result.body);
			window.location.reload();
        })
        .catch(error => console.error('Si è verificato un errore durante l\'invio del post:', error));
});

// Script per gestire la ricerca dei post
document.getElementById('search-button').addEventListener('click', function() {
    const keyword = document.getElementById('search').value.trim().toLowerCase();
    const allPosts = document.querySelectorAll('.post');

    let foundPosts = false;

    allPosts.forEach(post => {
        const title = post.querySelector('h3').innerText.toLowerCase();
        const description = post.querySelector('p').innerText.toLowerCase();
        if (title.includes(keyword) || description.includes(keyword)) {
            fadeIn(post);
            foundPosts = true;
        } else {
            fadeOut(post);
        }
    });

    if (!foundPosts) {
        alert('Nessun post trovato.');
        window.location.reload();
    }
});

// Funzione per caricare i post quando la pagina è pronta
document.addEventListener('DOMContentLoaded', async function() {
	await initializeScript(filepath);	
    fetchPostsFromBackend();
});

window.addEventListener('resize', function() {
    var headerHeight = document.querySelector('.header').offsetHeight;
    var mainContainer = document.querySelector('.main-container');
    mainContainer.style.paddingTop = headerHeight + 'px';
});

// Aggiorna anche all'avvio della pagina
window.addEventListener('DOMContentLoaded', function() {
    var headerHeight = document.querySelector('.header').offsetHeight;
    var mainContainer = document.querySelector('.main-container');
    mainContainer.style.paddingTop = headerHeight + 'px';
});
