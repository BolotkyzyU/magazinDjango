// лайки функция
function pressLike(url){
    fetch( url , {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value, // Получаем CSRF-токен
        }
     })
    .then((response)=>{
        let linkElement = document.getElementById('likesCount');
        let likesCount = parseInt(linkElement.innerText)
        if (response.status == '200'){
            linkElement.innerHTML = `${likesCount+1}`
        }
        else{
            linkElement.innerHTML = `${likesCount-1}`
        }
    })
}

// рейтинги функция
async function setRating(url, rating, productId, getValueUrl){
    await fetch( `${url}?id=${productId}&points=${rating}` , {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value, // Получаем CSRF-токен
        }});

    await fetch(`${getValueUrl}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value, // Получаем CSRF-токен
        }}) 
        .then(response => response.json())
        .then(data => {
            let rating = document.getElementById('rating');
            rating.innerHTML = `${data['points']}`
        })
}

// количества товара для добавление в корзинку 
function quantityChange(operator){
    let quantityHtml = document.getElementById('quantity')
    let quantityInt = parseInt(quantityHtml.value)     
    if(operator == 'add'){
        quantityInt += 1
    }
    else if(operator != 'add' && quantityInt > 1){
        quantityInt -= 1
    }
    quantityHtml.value = `${quantityInt}`
}

function setShoppingCart(url, isProductDetails = false){
    
    let quantityInt = 1
    if(isProductDetails){
        let quantityHtml = document.getElementById('quantity')
        quantityInt = parseInt(quantityHtml.value)         
    }

    fetch(`${url}?quantity=${quantityInt}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value, // Получаем CSRF-токен
        }}) 
}


