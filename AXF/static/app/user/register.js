$(function () {

    flag1 = false;  // 用户名输入不合法
    flag2 = false;
    flag3 = false;  // 用户名输入不合法
    flag4 = false;


    $('#username').change(function () {
        var value = $(this).val();
        if (/^[a-zA-Z_]\w{5,17}$/.test(value)) {
            // console.log('输入正确');
            flag1 = true;

            $.get('/app/checkusername/', {username: $(this).val()}, function (data) {
                if (data.status == 1) {
                    $('#msg').html('用户名可以使用').css('color', 'green')
                }
                else if (data['status'] == 0) {
                    $('#msg').html(data.msg).css('color', 'red')
                }
                else {
                    $('#msg').html('用户名不合法').css('color', 'red')
                }
            })
        }
        else {
            // console.log('输入有误');
            flag1 = false;
            $('#msg').html('用户名输入有误').css('color', 'red')

        }
    });

    $('#password').change(function () {
        var value = $(this).val();
        if (/^.{8,}$/.test(value)) {
            // console.log('输入正确')
            flag2 = true;

        }
        else {
            // console.log('输入有误')
            flag2 = false;

        }
    });

    $('#again').change(function () {
        var value = $(this).val();
        if (value == $('#password').val()) {
            // console.log('输入正确')
            flag3 = true;

        }
        else {
            // console.log('输入有误')
            flag3 = false;

        }
    });

    $('#email').change(function () {
        var value = $(this).val();
        if (/^\w+@\w+\.\w+$/) {
            // console.log('输入正确')
            flag4 = true;

        }
        else {
            // console.log('输入有误')
            flag4 = false;

        }
    });

    //an
    $('#btn').click(function () {
        if (flag1 && flag2 && flag3 && flag4) {

            //表单提交加密密码
            $('#password').val(md5($('#password').val()));
            return true
        }
        else {
            return false
        }
    });
});


//检测用户名是否存在
// $('#username').change(function () {

// $.ajax({
//     type:'get',
//     url:'',
//     data:{},
//     async:true,
//     success:function (data) {
//
//     },
//     error:function (err) {
//
//     }
// })
// })

//         $.get('/app/checkusername/',{username:$(this).val()},function (data) {
//             if (data.status == 1){
//                 $('#msg').html('用户名可以使用').css('color','green')
//             }else if(data['status'] == 0){
//                 $('#msg').html(data.msg).css('color','green')
//             }else{
//                 $('#msg').html('用户名不合法').css('color','red')
//             }
//         })
// });