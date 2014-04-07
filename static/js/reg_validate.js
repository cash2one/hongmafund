// JavaScript Document
//自定义信息
jQuery.fn.setError=function(msg){
	    var filed=$(this).parents("div").siblings(".field");
        filed.html("<div class='val_field val_field_error'>"+msg+"</div>")
	}
jQuery.fn.setRight=function(msg){
	    var filed=$(this).parents("div").siblings(".field");
        filed.html("<div class='val_field val_field_right'>"+msg+"</div>")
	}
 

// Email验证 
function reg_chkemail(obj){
	var $email =/\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*/ // Email
	var useremail = $("#useremail").val();
	if (useremail==""||useremail==null) {
		  obj.setError("邮箱为空"); 
           return;
       } 
	   else if ($email.test(useremail) == false) {
		    obj.setError("邮箱格式错误"); 
           return;
       } 
	   else {   
		$(".field").html("loading...");
		$.getJSON(check_email_url, {'email' : useremail}, function(data){
			if(data.flag){
				obj.setRight("邮箱可以使用"); 
			}else{
				obj.setError("邮箱已被占用"); 
			}
		});
	   }
}

// 判断密码
function reg_chkpwd(obj){
	var userpwd=$("#userpwd").val();
		   if (userpwd==""||userpwd==null) {
          obj.setError("密码为空"); 
           return;
       }
	   else if (userpwd.length < 6) {
          obj.setError("密码长度不能少于6位"); 
           return;
       }
	    else {
			//需要ajax验证
		  obj.setRight("密码正确"); 
       }


}

// 判断密码是否一致 
function reg_chkpwd1(obj){
       var password = $("#userpwd").val();
	   var password1 = $("#userpwd1").val();
       if (password != password1 || password == '') {
         obj.setError("确认密码和密码一致"); 
           return;
       } else {obj.setRight("密码正确")}
}


//注册提交
function do_reg(){
	if($(".val_field_error").length>0){
		return false;
    }else{
		reg_chkemail($("#useremail"));
		reg_chkpwd($("#userpwd"));
		reg_chkpwd1($("#userpwd1"));
		if($(".val_field_error").length>0){
			return false;
		}
		$("#success").html("&nbsp;<img src='http://i0.51fanli.net/img/load.gif'></img>&nbsp;<span style='font-size：14px;'>正在注册，请稍等...</span>");
		$("#reg_submit").attr("disabled",true);
		$.getJSON($("#reg_form").attr('action') + "/?jscallback=?", $("#reg_form").serialize(), function(data){
			if(data.flag){
				window.location.href = validate_email_url;
			}else{
				alert(data.msg);
				$("#success").html('');
				$("#reg_submit").attr("disabled",false);
			}
		});
    //$.ajax({
//	url：APP + "/Reg/ajaxUserReg",
//	data：data,
//	dataType：'jsonp',
//	jsonp：'jsoncallback',
//	beforeSend：function(){},
//	complete：function(){$("#reg_submit").attr("disabled",false);},
//	success：function(json){
//	    if (json.status.toString() == "10000"){
//		var go_url = $("#go_url").val();
//		if (go_url == ''){
//		    go_url = 'http：//www.yaoqing.com/regwelcome.php'
//		};
//		window.location = go_url;
//	    }else if(json.status.toString() == "10001"){
//		$("#success").html('&nbsp;<span style="font-size：14px;color：red;">' + json.info + '</span>');
//	    }else if(json.status.toString() == "10013"){
//		alert(json.info);
//		window.location = APP + '/login/';
//	    }else{
//		$("#"+json.data+"info").html('<span style="color：red">' + json.info + '</span>');
//		$("#success").html('');
//	    }
//	}
//    });
	}
}



 
$(function(){

	 $("#useremail").blur(function() {reg_chkemail($(this));})
	 $("#userpwd").blur(function() {reg_chkpwd($(this))})
	 $("#userpwd1").blur(function() {reg_chkpwd1($(this))})
	 $("#reg_form").submit(function(){
		 do_reg();
		return false;
	 });
})
