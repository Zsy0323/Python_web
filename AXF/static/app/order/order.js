$(function () {

    //需要集成第三方支付
   //支付
    $('#pay').click(function () {
        //支付后将订单状态修改
        $.get('/app/orderchangestatus/',{'orderid':$(this).attr('orderid'),'status':'1'},function (data) {
            console.log(data);
            if(data.status == 1){
                location.href = '/app/mine/'
            }else {
                console.log(data.msg)
            }
        })
    })

});