const express = require('express');
const router = express.Router();
const expressSession = require('express-session');
const crypto = require('crypto');
const {communication} = require("../controller/api.js");
const {v4} = require('uuid');

/* GET home page. */
router.get('/', function (req, res, next) {
    res.render('index', {title: 'Express', userSession: req.session});
});

/* GET users listing. */
router.get('/shop', async (req, res, next) => {
    try {
        if (req.query.productType) {
            let apiData = await communication("product/filter/" + req.query.productType);
            res.render('shop', {title: 'Express', userSession: req.session, productData: apiData});
        } else {
            let apiData = await communication("product");
            res.render('shop', {title: 'Express', userSession: req.session, productData: apiData});
        }
    } catch (e) {
        res.redirect('/');
    }
});

/* GET users listing. */
router.get('/product', async (req, res, next) => {
    try {
        if (req.query.productID) {
            let apiData = await communication("product/" + req.query.productID);
            res.render('product', {title: 'Express', userSession: req.session, productData: apiData});
        }
        res.render('product', {title: 'Express'});
    } catch (e) {
        res.redirect('/');
    }
});

router.post('/product', async (req, res, next) => {
    try {
        if (typeof req.session.authorization === 'undefined') {
            res.send("<script>alert('로그인 후 이용가능합니다.'); location.href='/shop';</script>");
        }

        const TIME_ZONE = 3240 * 10000;
        const d = new Date();

        const date = new Date(+d + TIME_ZONE).toISOString().split('T')[0];
        const time = d.toTimeString().split(' ')[0];

        let ConsumerApiData = await communication("consumer/consumer/" + req.session.authorization, "GET");
        let ProductApiData = await communication("product/" + req.body.productID, "GET");

        let dataPackage = {
            CartProductName: req.body.productName,
            CartProductID: req.body.productID,
            CartProductCost: req.body.productCost,
            CartProductImage: ProductApiData.ProductImage,
            ConsumerIdentifyNumber: ConsumerApiData.IdentifyNumber,
            CartBuyChecked: false,
            UpdateTimestamp: date + ' ' + time,
        };

        let apiData = await communication("cart/register", "POST", dataPackage);

        if (apiData.status === '201')
            res.redirect('/cart/' + req.session.authorization);
        else {
            res.status(400);
        }
    } catch (e) {
        res.status(400);
    }
});

/* GET users listing. */
router.get('/cart/:id', async (req, res, next) => {
    if (typeof req.session.authorization === 'undefined' || req.params.id === undefined || req.params.id !== req.session.authorization) {
        res.redirect('/');
    }
    try {
        let ConsumerApiData = await communication("consumer/consumer/" + req.params.id, "GET"),
            productApiData = await communication("cart/products/" + ConsumerApiData.IdentifyNumber, "GET");

        console.log("======== productApiData =======");
        console.log(productApiData);
        let totalCost = 0;
        if (productApiData !== "error") {
            productApiData.forEach((item) => {
                totalCost += item.CartProductCost;
            });
        }
        res.render('cart', {title: 'Express', userSession: req.session, cartData: productApiData, totalCost: totalCost});
    } catch (e) {
        res.redirect('/');
    }
});

/* GET users listing. */
router.get('/mypage', async (req, res, next) => {
    if (typeof req.session.authorization === 'undefined') {
        res.redirect('/');
    }

    try {
        let apiData = await communication("consumer/consumer/" + req.session.authorization, "GET");
        res.render('mypage', {title: 'Express', userSession: req.session, consumerData: apiData});
    } catch (e) {
        res.redirect('/');
    }
});

/* GET users listing. */
router.get('/mypage/buy', async (req, res, next) => {
    try {
        if (typeof req.session.authorization === 'undefined') {
            res.redirect('/');
        }

        let ConsumerApiData = await communication("consumer/consumer/" + req.session.authorization, "GET");
        let productApiData = await communication("cart/products/buy/" + ConsumerApiData.IdentifyNumber, "GET");

        let totalCost = 0;
        if (productApiData !== "error") {
            productApiData.forEach((item) => {
                totalCost += item.CartProductCost;
            });
        }
        res.render('buyList', {title: 'Express', userSession: req.session, consumerData: productApiData, totalCost: totalCost});
    } catch (e) {
        res.redirect('/');
    }
});


router.post('/mypage/buy', async (req, res, next) => {
    try {
        if (typeof req.session.authorization === 'undefined') {
            res.redirect('/');
        }

        let ConsumerApiData = await communication("consumer/consumer/" + req.session.authorization, "GET");
        console.log(ConsumerApiData);
        let cartData = await communication("cart/buy/" + ConsumerApiData.IdentifyNumber, "PATCH");
        console.log("========= cartData ====== ");
        console.log(cartData);
        res.redirect('/mypage/buy');
    } catch (e) {
        res.redirect('/');
    }
});

/* GET users listing. */
router.get('/signup', function (req, res, next) {
    if (typeof req.session.authorization !== 'undefined') {
        res.redirect('/');
    }
    res.render('signup', {title: 'Express', userSession: req.session});
});

router.post('/signup', async (req, res, next) => {
    if (typeof req.session.authorization !== 'undefined') {
        res.status(400).redirect('/');
    }

    const TIME_ZONE = 3240 * 10000;
    const d = new Date();

    const date = new Date(+d + TIME_ZONE).toISOString().split('T')[0];
    const time = d.toTimeString().split(' ')[0];

    try {
        let dataPackage = {
            ConsumerEmail: req.body.formUserEmail,
            ConsumerPWD: req.body.formUserPWD,
            ConsumerName: req.body.formUserName,
            Address: req.body.formUserAddress,
            PhoneNumber: req.body.formUserPhoneNumber,
            ClassificationNumber: 0,
            IdentifyNumber: v4(),
            LastLogin: date + ' ' + time,
            CreateTime: date + ' ' + time
        };

        let apiData = await communication("consumer/signup", "POST", dataPackage);
        if (apiData.status === '201')
            req.session.authorization = dataPackage.ConsumerEmail;
        else {
            res.redirect('/signup');
        }
        res.redirect('/');
    } catch (e) {
        res.redirect('/');
    }
});

router.get('/signin', function (req, res, next) {
    if (typeof req.session.authorization !== 'undefined') {
        res.redirect('/');
    }
    res.render('signin', {title: 'Express', userSession: req.session, action: "/signin"});
});

router.post('/signin', async (req, res, next) => {
    if (typeof req.session.authorization !== 'undefined') {
        res.redirect('/');
    }

    try {

        let dataPackage = {
            ConsumerEmail: req.body.formUserEmail,
            ConsumerPWD: req.body.formUserPWD
        };

        let apiData = await communication("consumer/signin", "POST", dataPackage);
        if (apiData.status === '201')
            req.session.authorization = dataPackage.ConsumerEmail;
        else {
            res.redirect('/signup');
        }
        res.redirect('/');
    } catch (e) {
        res.redirect('/');
    }
});

router.get('/admin/signin', function (req, res, next) {
    if (typeof req.session.authorization !== 'undefined' || typeof req.session.admin !== 'undefined') {
        res.redirect('/');
    }
    res.render('signin', {title: 'Express', userSession: req.session, action: "/admin/signin"});
});

router.post('/admin/signin', async (req, res, next) => {
    if (typeof req.session.authorization !== 'undefined' || typeof req.session.admin !== 'undefined') {
        res.redirect('/');
    }

    try {

        let dataPackage = {
            ProducerEmail: req.body.formUserEmail,
            ProducerPWD: req.body.formUserPWD
        };

        let apiData = await communication("producer/signin", "POST", dataPackage);
        if (apiData.status === '201') {
            req.session.authorization = dataPackage.ProducerEmail;
            req.session.admin = true;
        } else {
            res.redirect('/admin/signin');
        }
        res.redirect('/');
    } catch (e) {
        res.redirect('/');
    }
});

router.get('/admin/product/create', async (req, res, next) => {
    res.send("<script>prompt('추가할 상품 정보', '상품 1'); alert('정상적으로 등록되었습니다.'); location.href='/shop';</script>");
});


router.get('/admin/product/delete', async (req, res, next) => {
    res.send("<script>prompt('삭제할 상품 정보', ''); alert('정상적으로 삭제되었습니다.'); location.href='/shop';</script>");
});


router.get('/logout', function (req, res) {
    req.session.destroy(function () {
        req.session;
    });
    res.redirect('/');
});

router.get('/search', function (req, res) {
    res.render('search', {title: 'Express', userSession: req.session, data: undefined});
});

router.post('/search', async (req, res) => {
    if (typeof req.body.searchKey === 'undefined' || !req.body.searchKey)
        res.render('search', {title: 'Express', userSession: req.session, data: undefined});

    try {
        let apiData = await communication("product/search/" + req.body.searchKey, "GET");

        for (let i = 0; i < apiData.length; i++) {
            console.log(apiData[i].ProductCost);
        }

        if (apiData === 'error') res.render('search', {title: 'Express', userSession: req.session, data: undefined});
        else res.render('search', {title: 'Express', userSession: req.session, data: apiData});

    } catch (e) {
        res.redirect('/');
    }

});


module.exports = router;
