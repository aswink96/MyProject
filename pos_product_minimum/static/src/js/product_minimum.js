odoo.define('pos_product_minimum.product_minimum', function (require) {
"use strict";

//var core = require('web.core');
//var screens = require('point_of_sale.screens');
var models  = require('point_of_sale.models');

models.load_fields("product.product",['contained_quantity']);
console.log("m",models);

var _super_orderline = models.Orderline.prototype;
models.Orderline =models.Orderline.extend({
    initialize: function(attr,options){
    _super_orderline.initialize.apply(this,arguments);
        this.get_quantity();
        if (this.product.contained_quantity!== 0){
        this.set_quantity(this.product.contained_quantity);
        }
        else{
        this.set_quantity(1)}
        console.log("aar",this.get_quantity());
        console.log("bb",this);


        },

});
});