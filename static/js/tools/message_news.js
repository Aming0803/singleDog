/**
 * Created by wan on 16/6/1.
 * message news
 */
$(function(){
    var article_id_list = [];
    var is_new_media = false;
    var danger_ele = $("#danger");
    var success_ele = $("#success");

    $("input[name='media_choose']").click(function(){
        var val = $(this).val();
        if(val === 'old'){
            $("#old_media").removeClass("hidden");
            $("#new_media").addClass("hidden");
            is_new_media = false;
        }else{
            $("#old_media").addClass("hidden");
            $("#new_media").removeClass("hidden");
            is_new_media = true;
        }
    });

    $("#multi-select").multiselect({
        nonSelectedText: "未选择图文",
        allSelectedText: "全部选择",
        buttonWidth: "270px",
        onChange: function(option, checked){
            var val = $(option).val();
            if(checked){
                article_id_list.push(val)
            }else{
                var index = $.inArray(val, article_id_list);
                if(index !== -1){
                    article_id_list.splice(index, 1);
                }
            }

        }
    });

    $("#submit_tag").click(function(){
        sendMessage("tag");
    });

    $("#submit_openid").click(function(){
        sendMessage("openid");
    });

    function sendMessage(category){
        var postData = {};
        var id = $("#media_id").val();
        postData._xsrf = getCookie("_xsrf");
        postData.is_new_media = "new"?is_new_media:"old";
        postData.category = category;
        if(is_new_media){
            postData.ids = article_id_list;
        }else{
            postData.media_id = id;
        }
        $.post(
            "/admin/wx/news/message",
            postData,
            function (response) {
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
});