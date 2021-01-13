odoo.define('website_quantity_limit.quantity_limit', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var core = require('web.core');
var VariantMixin = require('sale.VariantMixin');
var wSaleUtils = require('website_sale.utils');
const wUtils = require('website.utils');
var _t = core._t;
console.log(" test",publicWidget)




//var limit_quantity = publicWidget.Widget.extend(VariantMixin, {
//    selector: '.oe_website_sale',
//    events: _.extend({}, VariantMixin.events || {},
//     {
//        'change form .js_product:first input[name="add_qty"]': '_onChangeAddQuantity',
//        'mouseup .js_publish': '_onMouseupPublish',
//        'touchend .js_publish': '_onMouseupPublish',
//        'change .oe_cart input.js_quantity[data-product-id]': '_onChangeCartQuantity',
//        'click .oe_cart a.js_add_suggested_products': '_onClickSuggestedProduct',
//        'click a.js_add_cart_json': '_onClickAddCartJSON',
//        'click .a-submit': '_onClickSubmit',
//        'change form.js_attributes input, form.js_attributes select': '_onChangeAttribute',
//        'mouseup form.js_add_cart_json label': '_onMouseupAddCartLabel',
//        'touchend form.js_add_cart_json label': '_onMouseupAddCartLabel',
//        'click .show_coupon': '_onClickShowCoupon',
//        'submit .o_wsale_products_searchbar_form': '_onSubmitSaleSearch',
//        'change select[name="country_id"]': '_onChangeCountry',
//        'change #shipping_use_same': '_onChangeShippingUseSame',
//        'click .toggle_summary': '_onToggleSummary',
//        'click #add_to_cart, #buy_now, #products_grid .o_wsale_product_btn .a-submit': 'async _onClickAdd',
//        'click input.js_product_change': 'onChangeVariant',
//        'change .js_main_product [data-attribute_exclusions]': 'onChangeVariant',
//        'change oe_optional_products_modal [data-attribute_exclusions]': 'onChangeVariant',
//    }),
//
////    init: function () {
////        this._super.apply(this, arguments);
////
////        this._changeCartQuantity = _.debounce(this._changeCartQuantity.bind(this), 500);
////        then(function (data) {
////            $input.data('update_change', false);
////            var check_value = parseInt($input.val() || 0, 10);
////            console.log("check",data)
////            if (isNaN(check_value)) {
////                check_value = 1;
////            }
////            if (value !== check_value) {
////                $input.trigger('change');
////                return;
////            }
////            if (!data.cart_quantity) {
////                return window.location = '/shop/cart';
////            }
//init: function () {
//        this._super.apply(this, arguments);
publicWidget.registry.WebsiteSale.include({
_changeCartQuantity: function ($input, value, $dom_optional, line_id, productIDs) {
        _.each($dom_optional, function (elem) {
            $(elem).find('.js_quantity').text(value);
            productIDs.push($(elem).find('span[data-product-id]').data('product-id'));
            console.log("chng",line_id)
        })
        $input.data('update_change', true);
        console.log("pst");
        this._rpc({
            route: "/shop/cart/update_json",
            params: {
                line_id: line_id,
                product_id: parseInt($input.data('product-id'), 10),
                set_qty: value
//                console.log("set",set_qty)
            },

        }).then(function (data) {
//        if(data.max_qty1 != 0 && data.quantity >= data.max_qty1 ){
//              alert("aaaaa")
//              return false
//              }
//        else{
            console.log("max",data,data['max_qty1'])
            $input.data('update_change', false);
            var check_value = parseInt($input.val() || 0, 10);
            console.log("check",check_value)
            console.log("value",value)
//            while(data.max_qty1 != 0){
            if(data.max_qty1 != 0 && data.quantity > data.max_qty1 ){
            $input.val(data['max_qty1'])
//
              alert("Maximum Quantity Limit is "+ data.max_qty1)
               $input.data('update_change', false);
            var check_value = parseInt($input.val() || 0, 10);
            if (isNaN(check_value)) {
                check_value = 1;
            }
            if (value !== check_value) {
                $input.trigger('change');
                return;
            }
            if (!data.cart_quantity) {
                return window.location = '/shop/cart';
            }
            wSaleUtils.updateCartNavBar(data);
            $input.val(data.quantity);
            $('.js_quantity[data-line-id='+line_id+']').val(data.quantity).html(data.quantity);

            if (data.warning) {
                var cart_alert = $('.oe_cart').parent().find('#data_warning');
                if (cart_alert.length === 0) {
                    $('.oe_cart').prepend('<div class="alert alert-danger alert-dismissable" role="alert" id="data_warning">'+
                            '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> ' + data.warning + '</div>');
                }
                else {
                    cart_alert.html('<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> ' + data.warning);
                }
                $input.val(data.quantity);
            }

              }

            else if(data.quantity < data.min_qty1){
           $input.val(data['min_qty1'])
           var minqty1val = $input.val(data['min_qty1'])
//
              alert("minimum allowed quantity is  " + data.min_qty1)
               $input.data('update_change', false);
            var check_value = parseInt($input.val() || 0, 10);
            if (isNaN(check_value)) {
                check_value = 1;
            }
            if (value !== check_value) {
                $input.trigger('change');
                return;
            }
            if (!data.cart_quantity) {
                return window.location = '/shop/cart';
            }
            wSaleUtils.updateCartNavBar(data);
            $input.val(data.quantity);
            $('.js_quantity[data-line-id='+line_id+']').val(data.quantity).html(data.quantity);

            if (data.warning) {
                var cart_alert = $('.oe_cart').parent().find('#data_warning');
                if (cart_alert.length === 0) {
                    $('.oe_cart').prepend('<div class="alert alert-danger alert-dismissable" role="alert" id="data_warning">'+
                            '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> ' + data.warning + '</div>');
                }
                else {
                    cart_alert.html('<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> ' + data.warning);
                }
                $input.val(data.quantity);
            }

              }


//              $('.oe_cart').prepend('<div class="alert alert-danger alert-dismissable" role="alert" id="data_warning">'+
//                '<button type="button" class="close" data-dismiss="alert" aria-label="close">×</button> <strong>You cannot order product more than limit.</strong> '  + '</div>');
//              $input.val(data.max_qty1);





            if (isNaN(check_value)) {
                check_value = 1;
                }

            if (value !== check_value) {
                $input.trigger('change');
                return;
            }
            if (!data.cart_quantity) {
                return window.location = '/shop/cart';
            }

            wSaleUtils.updateCartNavBar(data);
            $input.val(data.quantity);
            $('.js_quantity[data-line-id='+line_id+']').val(data.quantity).html(data.quantity);




            if (data.warning) {
                var cart_alert = $('.oe_cart').parent().find('#data_warning');
                if (cart_alert.length === 0) {
                    $('.oe_cart').prepend('<div class="alert alert-danger alert-dismissable" role="alert" id="data_warning">'+
                            '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> ' + data.warning + '</div>');
                }
                else {
                    cart_alert.html('<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> ' + data.warning);
                }
                $input.val(data.quantity);
                }

            });
            },




    _onClickAdd: function (ev) {
        ev.preventDefault();
        console.log("ev",ev)
        this.isBuyNow = $(ev.currentTarget).attr('id') === 'buy_now';
        return this._handleAdd($(ev.currentTarget).closest('form'));
    },
    // adding quantity from cart
     _onClickAddCartJSON: function (ev){
     console.log("evv",ev)


        this.onClickAddCartJSON(ev);
    },
    //adding product to cart
    _onChangeAddQuantity: function (ev) {
       console.log("ev",ev)
        this.onChangeAddQuantity(ev);
    },

    });
    });
