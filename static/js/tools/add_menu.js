/**
 * Created by wan on 16/5/24.
 * add menu
 */

$(function(){
    $("#menu").addClass("active").siblings().removeClass("active");
    $("#menu_name").tooltip();
    $("#menu_type_tooltip").tooltip({html : true });

    $("#category").change(function(){
        var category = $("#category").val();
        var menu_id = $("#id").val();
        if(category === '2'){
            $.get(
                "/admin/wx/parent/menu/list",
                {'id': menu_id},
                function(data){
                    $("#menu_category").after(data);
                },
                'html'
            )
        }else{
            var ele = $("#parent_id");
            if(ele){
                ele.remove();
            }
        }
    });
    $("#category").trigger("change");

    $("#submit").click(function(){
        var postData = {};
        var danger_ele = $("#danger");
        var success_ele = $("#success");
        postData._xsrf = getCookie("_xsrf");
        postData.menu_id = $("#id").val();
        postData.name = $("#name").val();
        postData.value = $("#value").val();
        postData.category = $("#category").val();
        postData.menu_type = $("#menu_type").val();
        postData.parent_id = $("#parent_menu_id").val();
        if(!postData.name || !postData.value){
            danger_ele.removeClass("hidden").addClass("show").html("输入框不能为空值");
            success_ele.removeClass("show").addClass("hidden");
        }else if(postData.category === '2' && !postData.parent_id){
            danger_ele.removeClass("hidden").addClass("show").html("请选择父级菜单");
            success_ele.removeClass("show").addClass("hidden");
        }else{
            $.post(
                "/admin/wx/menu/editor",
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