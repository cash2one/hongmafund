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
       }else{
		   obj.setRight("邮箱格式正确");
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
       }else{
		   obj.setRight('密码格式正确');
	   }


}

//注册提交
function do_login(){
	if($(".val_field_error").length>0){
		return false;
    }else{
		reg_chkemail($("#useremail"));
		reg_chkpwd($("#userpwd"));
		if($(".val_field_error").length>0){
			return false;
		}
		$("#success").html("&nbsp;<img src='http://i0.51fanli.net/img/load.gif'></img>&nbsp;<span style='font-size：14px;'>正在登录，请稍等...</span>");
		$("#reg_submit").attr("disabled",true);
		$.getJSON($("#member_login").attr('action') + "/?jscallback=?", $("#member_login").serialize(), function(data){
			if(data.flag){
				$("#success").html('登录成功');
				$("#reg_submit").attr("disabled",false);
				window.location.href = data.url;
			}else{
				$("#useremail").setError(data.msg);
				$("#success").html('');
				$("#reg_submit").attr("disabled",false);
			}
		});
	}
}

$(function(){

	 $("#useremail").blur(function() {reg_chkemail($(this));})
	 $("#userpwd").blur(function() {reg_chkpwd($(this))})
	 $("#member_login").submit(function(){
	 	reg_chkemail( $("#useremail"));
		reg_chkpwd( $("#userpwd"));
		do_login();
		return false;
	 });
})