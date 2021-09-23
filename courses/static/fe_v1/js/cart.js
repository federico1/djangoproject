(function ($) {

    $.GlobalCartManager = function (options) {

        var that = this;

        var keyName = '__nyc_cart__data__';

        var settings = $.extend({}, options);

        var addCourseToMemory = function (dataObject) {

            var memoryData = getMemoryData();

            if (!('_ps_' in memoryData)) {
                memoryData['_ps_'] = [];
            }

            var dataList = memoryData['_ps_'];

            var itemIndex = dataList.findIndex(a => a.id == dataObject.id);

            if (itemIndex >= 0) {
                dataList[itemIndex].qty = 1;
            } else {
                dataList.push(dataObject);
            }

            memoryData['_ps_'] = dataList;

            localStorage.setItem(keyName, JSON.stringify(memoryData));

            onChangeCart();

            console.log('cart updated.');

            swal({
                    title: "Success",
                    text: "Course has been added to cart.",
                    icon: "success",
                    buttons: {
                        cancel: "OK",
                        catch: {
                            text: "View My Cart",
                            value: "catch",
                        },
                    },
                })
                .then((value) => {
                    if (value == 'catch') {
                        window.location.href = '/cart';
                    }
                })

        };

        var onChangeCart = function () {

            var memoryData = getMemoryData();

            var count = 0;
            var totalPrice = parseFloat('0.00');

            if (!('_ps_' in memoryData)) {
                count = 0;
            } else {
                count = memoryData['_ps_'].length;

                $(memoryData['_ps_']).each(function (ix, item) {
                    var price = item.discounted_price > 0 ? item.discounted_price : item.price;
                    price = parseFloat(price);
                    totalPrice = totalPrice + price;
                });

            }
            $(".lbl-cart-items-count").html('(' + count + ')');
            $(".lbl-cart-items-price").html('$' + parseFloat(totalPrice).toFixed(2));

        };

        var getMemoryData = function () {

            try {

                var memoryData = localStorage.getItem(keyName);

                var parsedMemoryData = {};

                if (memoryData) {
                    parsedMemoryData = JSON.parse(memoryData);
                }

                return parsedMemoryData;

            } catch (error) {
                return {};
            }

        };

        var registerEvent = function () {
            $("div").on("click", '.link-add-cart', function (e) {
                e.stopPropagation();
                var parent = $(this).closest('.course-item').eq(0);

                var id = parent.find('input[name="id"]').val();
                var title = parent.find('input[name="title"]').val();
                var subject = parent.find('input[name="subject"]').val();
                var price = parent.find('input[name="price"]').val();
                var discounted_price = parent.find('input[name="discounted_price"]').val();
                var modules = parent.find('input[name="modules"]').val();

                var item = {
                    id: id,
                    title: title,
                    subject: subject,
                    price: price,
                    discounted_price: discounted_price,
                    modules: modules,
                    qty: 1
                };

                addCourseToMemory(item);

            });
        };

        var init = function () {
            registerEvent();
            onChangeCart();
        };

        init();

        return this;

    };


}(jQuery));

$(document).ready(function () {
    var globalCart = new $.GlobalCartManager({});
});