$(function () {
   $('.add').click(function () {

       //var num = $(this).prev()
       var that = this;

       //获取购物车id
       var cartid = $(this).parents('.menuList').attr('cartid');

       $.get('/app/addnum/',{'cartid':cartid},function (data) {
           console.log(data);
            if(data.status == 1){
                $(that).prev().html(data.num)
            }
            else {

            }
            calculate();
       })
   });

   $('.reduce').click(function () {

       //var num = $(this).prev()
       var that = this;

       //获取购物车id
       var cartid = $(this).parents('.menuList').attr('cartid');

       $.get('/app/reducenum/',{'cartid':cartid},function (data) {
           console.log(data);
            if(data.status == 1){
                $(that).next().html(data.num)
            }
            else {

            }
            calculate();
       })
   });

   //删除
    $('.delbtn').click(function () {
        var cartid = $(this).parent().attr('cartid');
        var that = this;
        //
        $.get('/app/delbtn',{'cartid':cartid},function (data) {
            console.log(data);
            //location.reload()
            if(data.status == 1){
                $(that).parent().remove()
            }
            else {

            }
            isAllSelected()
        })
    });

    //勾选
    $('.select').click(function () {
        cartid = $(this).parents('.menuList').attr('cartid');
        var that = this;
        $.get('/app/cartselect/',{'cartid':cartid},function (data) {
            console.log(data);
            if(data.status == 1){
                $(that).find('span').html(data.is_select ? '√' : '')

            }
            else {

            }
            isAllSelected()

        });
    });


    $('#allselect').click(function () {
        //先判断是否全部勾选
        selects = [];  //保存所有选中的cartid
        unselects = [];  //未选中的

        //遍历所有的li
        $('.menuList').each(function (index) {
            var select = $(this).find('.select').children('span').html()
            if(select){
                selects.push($(this).attr('cartid'))
            }else{
                unselects.push($(this).attr('cartid'))
            }
        });

        //全部勾选
        if (unselects.length == 0){
            $.get('/app/cartselectall/',{'action':'cancelselect','selects':selects.join('#')},function (data) {
                console.log(data);
                if(data.status == 1){
                    $('.select').find('span').html('')

                }else{
                    console.log(data.msg);
                }
                isAllSelected()
            })
        }
        else{
            $.get('/app/cartselectall/',{'action':'select','selects':unselects.join('#')},function (data) {
                console.log(data);
                if(data.status == 1){
                    $('.select').find('span').html('√')

                }else{
                    console.log(data.msg);
                }
                isAllSelected()

            })
        }


    });


    //是否全选
    isAllSelected();
    function isAllSelected() {
        var count = 0;
        $('.select').each(function () {
            if($(this).find('span').html()){
                count++;
            }
        });

        //如果全选
        if(count == $('.select').length){
            $('#allselect').find('span').html('√');
        }else {
            $('#allselect').find('span').html('');
        }
        calculate();
    }


    //计算总价

    function calculate() {
        total = 0;
        $('.menuList').each(function () {
            if($(this).find('.select').find('span').html()){
                price = parseFloat($(this).find('.price').html());
                num = parseInt($(this).find('.num').html());
                total += price * num;
            }
        });

        //显示总价
        $('#totalPrice').html(total.toFixed(2))
    }


    //结算
    $('#calculate').click(function () {

        //让后台生成订单
        $.get('/app/orderadd/',function (data) {
            console.log(data);
            if(data.status == 1){
                location.href = '/app/order/' + data.orderid + '/'
            }else{
               console.log(data.msg)
            }
        })
    });

});