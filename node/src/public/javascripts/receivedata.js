let product_name = localStorage.getItem('name')
let product_price = localStorage.getItem('price')
let n = localStorage.getItem('num')

function add_cart(){

}

// 상품 이름 바꾸기
document.getElementById("name").innerText = product_name;

//상품 가격 바꾸기
product_price = product_price.toLocaleString('ko-kR');
document.getElementById("price").innerText = product_price;

//상품 이미지 바꾸기
document.getElementById("image").setAttribute('src', '/images/products/product-'+n.toString()+'.jpg');

document.getElementById('add_cart').addEventListener('click', add_cart)