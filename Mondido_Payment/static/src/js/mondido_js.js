var onSuccess = function (transaction) {
                if(window.mondido.hasCallback){
                    return;
                }
                alert('Thank you for the payment!');
                window.mondido.hasCallback = true;
            };
            var onError = function (error,data) {
                if(window.mondido.hasCallback){
                    return;
                }
                if (data != null) {
                    alert(data.description);
                }
                window.mondido.hasCallback = true;
            };

            var onBefore = function(){
                window.mondido = {hasCallback: false};
            };

            $('#mondidopayform')
                .mondido({type:"ajax"})
                .on('payment:before', onBefore)
                .on('payment:success', onSuccess)
                .on('payment:fail', onError);

            var payment_ref = Math.floor((Math.random() * 10000) + 1).toString(); //random payment reference
            var secret = "$2a$10$k/wS5qecZLyMmqo0e8GV9."; // ssshhh, this is the secret.
            var merchant_id = "3";
            var customer_ref = "customer1";
            var amount = "1.00";
            var h_str = merchant_id+payment_ref+amount+customer_ref+"sek"+"test"+secret;
            var hash = md5(h_str);

            $('input[name="customer_ref"]').val(customer_ref);
            $('input[name="merchant_id"]').val(merchant_id);
            $('input[name="payment_ref"]').val(payment_ref);
            $('input[name="hash"]').val(hash);
            $('input[name="amount"]').val(amount);
//var onSuccess = function (transaction) {
//        if(window.mondido.hasCallback){
//            return;
//        }
//        $('body').removeClass("loading");
//        alert('Thank you for the payment!, look in the debug console for details');
//        if(console){
//            console.log(transaction);
//        }
//        window.mondido.hasCallback = true;
//    };
//    var onError = function (error,data) {
//        if(window.mondido.hasCallback){
//            return;
//        }
//        $('body').removeClass("loading");
//        var desc = "";
//        if (data != null) {
//            desc = data.description;
//            alert(desc);
//        }
//        if(console){
//            console.log(data);
//        }
//        window.mondido.hasCallback = true;
//    };

//    var onBefore = function(){
//        window.mondido = {hasCallback: false};
//        $('body').addClass("loading");
//    };

//    $('#mondidopayform')
//      .mondido({type:"ajax"})
//      .on('payment:before', onBefore)
//      .on('payment:success', onSuccess)
//      .on('payment:fail', onError);
//    $('#btnPay').on('click',function(e){
//        return validateInlineForm();
//    });

//    var payment_ref = Math.floor((Math.random() * 10000) + 1).toString(); //random payment reference
//    var secret = '$2a$10$k/wS5qecZLyMmqo0e8GV9.'; // ssshhh, this is the secret.
//    var merchant_id = "3";
//    var customer_ref = "";
//    var amount = "1.00";
//    var h_str = merchant_id+payment_ref+customer_ref+amount+"eur"+"test"+secret;
//    var hash = md5(h_str);

//    $('input[name="merchant_id"]').val(merchant_id);
//    $('input[name="payment_ref"]').val(payment_ref);
//    $('input[name="hash"]').val(hash);
//    $('input[name="amount"]').val(amount);

//    $('.storeCardInfo').on('click', function(){
//      alert('Click to store card information for future transactions')
//    });

//    function validateInlineForm() {
//        var checks = true;
//        var errString = 'All fields need to be filled. What\'s missing is:\n';

//        if (!ccvalid) {
//            errString += "Card number, ";
//            checks = false;
//        }
//        if (!cardholdervalid) {
//            errString += "Name, ";
//            checks = false;
//        }
//        if (!cardcvvvalid) {
//            errString += "CVV-code, ";
//            checks = false;
//        }
//        if (!cardexpiryvaid) {
//            errString += "Expiry";
//            checks = false;
//        }
//        if (!checks) {
//            alert(errString.removeEnd(', '));
//            $('body').removeClass("loading");
//            return false;
//        }
//        return true;
//    }



