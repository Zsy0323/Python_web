$(function () {
    $('#password').change(function () {

        $(this).val(md5($(this).val()))
    });

});