/**
 * Created by wan on 16/5/24.
 * add article
 */

$(function(){
    $("#article").addClass("active").siblings().removeClass("active");
    var ue = UE.getEditor('container', {
                initialFrameWidth: 888,
                initialFrameHeight:400,
                zIndex: 1100
            });


    $("#submit").click(function(){
        var postData = {};
        var danger_ele = $("#danger");
        var success_ele = $("#success");

        postData._xsrf = getCookie("_xsrf");
        postData.title = $("#title").val();
        postData.author = $("#author").val();
        postData.digest = $("#digest").val();
        postData.content_source_url = $("#content_source_url").val();
        postData.thumb_media_id = $("#thumb_media_id").val();
        postData.show_cover_pic = $("#show_cover_pic").val();
        postData.content = ue.getContent();
        if(!postData.title || !postData.author || !postData.digest || !postData.show_cover_pic){
            danger_ele.removeClass("hidden").addClass("show").html("输入框不能为空值");
            success_ele.removeClass("show").addClass("hidden");
        }else{
            $.post(
                "/admin/wx/article/add",
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