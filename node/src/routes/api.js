const express = require('express');
const router = express.Router();
const {communication} = require("../controller/api.js");

/* GET users listing. */
router.get('/sign', async function (req, res, next) {
    res.send('respond with a resource');
});

/* GET users listing. */
router.get('/product', async function (req, res, next) {
    let apiData = await communication("product");
    res.json(apiData);

});

/* GET users listing. */
router.get('/shop', async function (req, res, next) {
    res.send('respond with a resource');
});


module.exports = router;
