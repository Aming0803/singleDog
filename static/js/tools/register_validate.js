/**
 * Created by wan on 16/5/24.
 * register form validate
 */

$(function(){
    $("#form").submit(function(){
        console.log("11111111111111");
        var username = $("#username").val(),
            password = $("#password").val(),
            email = $("#email").val(),
            telephone = $("#telephone").val();
        var warning = $("#warning");
        var email_re = /(\w)+@(\w)+\.(\w)+/;
        var phone_re = /^1[3|4|5|7|8]\d{9}$/;
        if(!username){
            warning.html("用户名不能为空");
            return false;
        }
        if(!password){
            warning.html("密码不能为空");
            return false;
        }
        if(!email){
            warning.html("邮箱不能为空");
            return false;
        }
        if(!telephone){
            warning.html("联系方式不能为空");
            return false;
        }
        if(!email_re.test(email)){
            warning.html("邮箱格式不正确");
            return false;
        }
        if(!phone_re.test(telephone)){
            warning.html("联系方式格式不正确");
            return false;
        }
        return true;
    })
});