odoo.define('discount_task.FixedDiscountButton', function (require) {
"use strict";

var core = require('web.core');
var screens = require('point_of_sale.screens');
var models = require('point_of_sale.models');
var field_utils = require('web.field_utils');

var _t = core._t;


var FixedDiscountButton = screens.ActionButtonWidget.extend({
    template: 'FixedDiscountButton',
    button_click: function(){
//       alert("button clicked");
//       }
        var self = this;
        this.gui.show_popup('number',{
            'title': _t('Discount Percentage'),
            'value': this.pos.config.discount_pc,
            'confirm': function(val) {
                val = Math.round(Math.max(0,Math.min(100,field_utils.parse.float(val))));
                console.log("value",val);
                self.apply_discount(val);
            },
           });

    },
    apply_discount: function(pc) {
        var order    = this.pos.get_order();
        console.log("order",order);
        var lines    = order.get_orderlines();
        console.log("lines",lines);
        var product  = this.pos.db.get_product_by_id(this.pos.config.discount_product_id[0]);
        console.log("pro",product);
        if (product === undefined) {
            this.gui.show_popup('error', {
                title : _t("No discount product found"),
                body  : _t("The discount product seems misconfigured. Make sure it is flagged as 'Can be Sold' and 'Available in Point of Sale'."),
            });
            return;
        }

        // Remove existing discounts
        var i = 0;
        while ( i < lines.length ) {
            if (lines[i].get_product() === product) {
                order.remove_orderline(lines[i]);
            } else {
                i++;
            }
        }
         // Add discount
        // We add the price as manually set to avoid recomputation when changing customer.
        var base_to_discount = order.get_total_without_tax();
        console.log("base",base_to_discount);
//        if (product.taxes_id.length){
//            var first_tax = this.pos.taxes_by_id[product.taxes_id[0]];
            if (first_tax.price_include) {
                base_to_discount = order.get_total_with_tax();
            }

        var discount = - pc / 100.0 * base_to_discount;

        if( discount < 0 ){
            order.add_product(product, {
                price: discount,
                lst_price: discount,
                extras: {
                    price_manually_set: true,
                },
            });
        }
    }
});
screens.define_action_button({
    'name': 'discount',
    'widget': FixedDiscountButton,
    'condition': function(){
        return this
    },
    })


return {
    FixedDiscountButton: FixedDiscountButton,
}
});
//odoo.define('discount_task.FixedDiscountButton', function(require) {
//    'use strict';
//
//    const PosComponent = require('point_of_sale.PosComponent');
//    const ProductScreen = require('point_of_sale.ProductScreen');
//    const { useListener } = require('web.custom_hooks');
//    const Registries = require('point_of_sale.Registries');
//    var models = require('point_of_sale.models');
////    models.load.fields('product.product');
//    class FixedDiscountButton extends PosComponent {
//        constructor() {
//            super(...arguments);
//            useListener('click', this.onClick);
//            }
//             async onClick(){
////                alert("Clicked")
//
//
//
//            var self = this;
//
//            const { confirmed, payload } = await this.showPopup('NumberPopup',{
//            title: this.env._t('Discount'),
//            startingValue: this.env.pos.config.discount_pc,
//            });
//            if (confirmed) {
//                const val = Math.round(Math.max(0,Math.min(100,parseFloat(payload))));
//                console.log("ppp",val);
//                await self.apply_discount(val);
//                }
//                }
////                var order    = this.env.pos.get_order();
////                var lines    = order.get_orderlines();
////                var product  = this.env.pos.db.get_product_by_id(this.env.pos.config.discount_product_id[0]);
////                console.log("yyyy",order);
////                console.log("pro",product);
////                console.log("lines",lines);
////                console.log(this);
////                console.log(this.env.pos.config);
//
//
//
//
//            async apply_discount(pc) {
//            var order    = this.env.pos.get_order();
//            console.log("order",order)
//            var lines    = order.get_orderlines();
//            var product  = this.env.pos.db.get_product_by_id(this.env.pos.config.discount_product_id[0]);
//            console.log("jshsh",product);
//            if (product === undefined) {
//                await this.showPopup('ErrorPopup', {
//                    title : this.env._t("No discount product found"),
//                    body  : this.env._t("The discount product seems misconfigured. Make sure it is flagged as 'Can be Sold' and 'Available in Point of Sale'."),
//                });
//                return;
//            }
////            remove existing discount
//            var i = 0;
//            while ( i < lines.length ) {
//                if (lines[i].get_product() === product) {
//                    order.remove_orderline(lines[i]);
//                } else {
//                    i++;
//                }
//            }
//            var base_to_discount = order.get_total_without_tax();
//            console.log("base",base_to_discount);
//            console.log("length",product.taxes_id.length);
////            if (product.taxes_id.length){
////                var first_tax = this.pos.taxes_by_id[product.taxes_id[0]];
////                console.log("firsttax",this.pos.taxes_by_id[product.taxes_id[0]]);
////                if (first_tax.price_include) {
////                    base_to_discount = order.get_total_with_tax();
////                }
////            }
////            }
//
//
//
//
//
//////            if (confirmed) {
//////                self.apply_discount_value(val);
//////                console.log(discount_value)
//////                }
////
//////            if(discount_amount_type=='discount_percentage')
//////            const { confirmed, payload } = await this.showPopup('NumberPopup',{
//////             title: this.env._t('Discount'),
//////             startingValue: this.env.pos.config.discount_value,
//////             });
////             if (confirmed) {
////                const val = Math.round(Math.max(0,Math.min(100,parseFloat(payload))));
////                await self.apply_discount_value(val)
////             }
////            }
////
////            async discount_value(pc) {
////            var order    = this.env.pos.get_order();
////            var discount_amount_type = this.pos.config.discount_type;
////            var lines    = order.get_orderlines();
////            console.log(get_orderlines)
////            var product  = this.env.pos.db.get_product_by_id(this.env.pos.config.discount_product_id[0]);
////            if (product === undefined) {
////                await this.showPopup('ErrorPopup', {
////                    title : this.env._t("No discount product found"),
////                    body  : this.env._t("The discount product seems misconfigured. Make sure it is flagged as 'Can be Sold' and 'Available in Point of Sale'."),
////                });
////                return;
////            }
////
////             // Remove existing discounts
////            var i = 0;
////            while ( i < lines.length ) {
////                if (lines[i].get_product() === product) {
////                    order.remove_orderline(lines[i]);
////                } else {
////                    i++;
////                }
////            }
////             var base_to_discount = order.get_total_without_tax();
////              if (product.taxes_id.length){
////                var first_tax = this.pos.taxes_by_id[product.taxes_id[0]];
////                if (first_tax.price_include) {
////                    base_to_discount = order.get_total_with_tax();
////                }
////            }
////            console.log(this.pos.config);
//            var discount_amount_type = this.env.pos.config.discount_type;
//            console.log("type",discount_amount_type);
//            if (discount_amount_type === 'discount_percentage'){
//            var discount =  -pc / 100.0 * base_to_discount
//            }
//            else{
//            var discount = base_to_discount - pc
//             }
//            if( discount < 0 ){
//                order.add_product(product, {
//                    price: discount,
//                    lst_price: discount,
//                    extras: {
//                        price_manually_set: true,
//                    },
//                });
//             }
//             }
//             }
//
//
//
//     FixedDiscountButton.template = 'FixedDiscountButton';
////           }
////           }
////           }
//
//        ProductScreen.addControlButton({
//        component: FixedDiscountButton,
//        condition: function(){
//           return this
//        },
//    })
//
//    Registries.Component.add(FixedDiscountButton);
//
//    return FixedDiscountButton;
//});
