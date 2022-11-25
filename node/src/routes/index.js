const express = require('express');
const router = express.Router();
const expressSession = require('express-session');
const crypto = require('crypto');

/* GET home page. */
router.get('/', function (req, res, next) {
    res.render('index', {title: 'Express', session: req.session});
});

/* GET users listing. */
router.get('/product', function (req, res, next) {
    res.render('product', {title: 'Express'});
});

/* GET users listing. */
router.get('/shop', function (req, res, next) {
    res.render('shop', {title: 'Express', session: req.session});
});

/* GET users listing. */
router.get('/cart', function (req, res, next) {
    res.render('cart', {title: 'Express'});
    // if (req.session.authorizationConsumer)
    //     res.render('cart', {title: 'Express'});
    // else
    //     return res.redirect('/');
});
/* GET users listing. */
router.get('/checkout', function (req, res, next) {
    res.render('checkout', {title: 'Express'});
    // if (req.session.authorizationConsumer)
    //     res.render('checkout', {title: 'Express'});
    // else
    //     return res.redirect('/');
});
module.exports = router;
