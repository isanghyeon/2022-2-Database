
let product_name = "니트";
let product_price = 15000;
let n = 1;


// 상품 이름 바꾸기
document.getElementById("name").innerText = product_name;

//상품 가격 바꾸기
product_price = "\u20A9 " + product_price.toLocaleString('ko-kR');
document.getElementById("price").innerText = product_price;

//상품 이미지 바꾸기
document.getElementById("image").setAttribute('src', '/images/products/product-'+n.toString()+'.jpg');

//product 페이지로 값 전달
localStorage.setItem('name',product_name);
localStorage.setItem('price', product_price);
localStorage.setItem('num', n);