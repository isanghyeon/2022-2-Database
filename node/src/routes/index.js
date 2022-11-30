const express = require('express');
const router = express.Router();
const expressSession = require('express-session');
const crypto = require('crypto');
const {communication} = require("../controller/api.js");

/* GET home page. */
router.get('/', function (req, res, next) {
    console.log(req.session.authorization);
    res.render('index', {title: 'Express', userSession: req.session});
});

/* GET users listing. */
router.get('/product', async function (req, res, next) {
    if (req.query.productID) {
        let apiData = await communication("product/" + req.query.productID);
        console.log(apiData);
        res.render('product', {title: 'Express', userSession: req.session, productData: apiData});
    }
    res.render('product', {title: 'Express'});
});

/* GET users listing. */
router.get('/shop', async function (req, res, next) {
    if (req.query.productType) {
        console.log(req.query.productType);
        let apiData = await communication("product/filter/" + req.query.productType);
        res.render('shop', {title: 'Express', userSession: req.session, productData: apiData});
    } else {
        console.log("All product");
        let apiData = await communication("product");
        res.render('shop', {title: 'Express', userSession: req.session, productData: apiData});
    }
});

/* GET users listing. */
router.get('/cart', function (req, res, next) {
    res.render('cart', {title: 'Express'});
});

/* GET users listing. */
router.get('/signup', function (req, res, next) {
    res.render('signup', {title: 'Express', userSession: req.session});
});

router.get('/signin', function (req, res, next) {
    res.render('signin', {title: 'Express', userSession: req.session});
});


module.exports = router;
