$(function () {
    $('#child_type').click(function () {
        $('#child_type_container').toggle();
        $('#child_type_icon').toggleClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
        $('#sort_rule_container').triggerHandler('click')

    });
    // 点击空白区域
    $('#child_type_container').click(function () {
        $(this).hide();
        $('#child_type_icon').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');

    });

    $('#sort_rule').click(function () {
        $('#sort_rule_container').toggle();
        $('#sort_rule_type').toggleClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
        // 触发事件
        $('#child_type_container').triggerHandler('click')
    });

    $('#sort_rule_container').click(function () {
        $(this).hide();
        $('#sort_rule_type').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');

    });

    //加入购物车

    //数量增加
    $('.add').click(function () {
        //$(this).parent().find('.number')
        $num = $(this).prev();
        $num.html(parseInt($num.html()) + 1);
    });

    $('.reduce').click(function () {
        //$(this).parent().find('.number')
        $num = $(this).next();
        n = parseInt($num.html()) - 1;
        if (n < 1) {
            n = 1;
        }
        $num.html(n);
    });

    //点击加入
    $('.addtocart').click(function () {
        //获取当前要加入购物车的商品id
        goodsid = $(this).attr('goodsid');

        //获取数量
        num = parseInt($(this).prev().find('.number').html());

        //提交数据
        $.get('/app/addcart/', {goodsid: goodsid, num: num}, function (data) {
            // console.log(data)
            if (data.status == 1){
                alert(data.msg)
            }else if (data.status == 0) {
                //location.assign()
                location.href = '/app/login/'
            }

        })
    })
});