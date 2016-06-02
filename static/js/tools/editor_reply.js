/**
 * Created by wan on 16/5/27.
 * editor_reply
 */
$(function(){
    $("#reply").addClass("active").siblings().removeClass("active");
    $("#submit").click(function(){
        var postData = {"_xsrf": getCookie("_xsrf")},
            danger_ele = $("#danger"),
            success_ele = $("#success");

        postData.key = $("#key").val();
        postData.reply_type = $("#reply_type").val();
        postData.content = $("#content").val();

        if(!postData.key || !postData.reply_type || !postData.content){
            danger_ele.removeClass("hidden").addClass("show").html("输入框不能为空值");
            success_ele.removeClass("show").addClass("hidden");
        }else{
            var reply_id = $("#reply_id").val();
            postData.reply_id = reply_id?reply_id:null;
            $.post(
                "/admin/wx/reply/editor",
                postData,
                function(response){
                    if(response.success){
                        success_ele.html(response.msg).removeClass("hidden").addClass("show");
                        danger_ele.removeClass("show").addClass("hidden");
                    }else{
                        danger_ele.html(response.msg).removeClass("hidden").addClass("show");
                        success_ele.removeClass("show").addClass("hidden");
                    }
                },
                'json'
            )
        }
    })
});