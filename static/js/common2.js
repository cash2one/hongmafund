//设为首页
function SetHomePage(obj,url){
try{
obj.style.behavior='url(#default#homepage)';obj.setHomePage(url);
}catch(e){
if(window.netscape){
try{
netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
}catch (e){
return false;
}
var prefs = Components.classes['@mozilla.org/preferences-service;1'].getService(Components.interfaces.nsIPrefBranch);
prefs.setCharPref('browser.startup.homepage',url);
}
}
}
//加入收藏
function AddFavorite(url, title){
try{
window.external.addFavorite(url, title);
}catch (e){
try{
window.sidebar.addPanel(title, url, "");
}catch (e){
return false;
}
}
} 

//图片滚动
function imgscroll(container){
	 var num_nav_li = container.find(".adv_num_nav li");
	 var pic = container.find(".adv_pic");
	 var num_nav_li = container.find(".adv_num_nav li")
     var len  = container.find(".adv_num_nav li").length; 
	 var index = 0;
	 var adTimer;
	 num_nav_li.mouseover(function(){
		index  =   num_nav_li.index(this);
		showImg(index);
	 }).eq(0).mouseover();
	 //滑入 停止动画，滑出开始动画.
	 container.hover(function(){
			 clearInterval(adTimer);
		 },function(){
			 adTimer = setInterval(function(){
			    showImg(index)
				index++;
				if(index==len){index=0;}
			  } , 3000);
	 }).trigger("mouseleave");

// 通过控制top，来显示不同的幻灯片
		function showImg(index){
				var adHeight = container.height();
				
				pic.stop(true,false).animate({top : -adHeight*index},1000);
				num_nav_li.removeClass("on").eq(index).addClass("on");
		}
}


//滑动门
/*
选项条ul的class为"tabs"；
内容的class为"tabs_con"；
选中项的样式为selected；
*/
function showtabs(container){
	 $('.tabs li:first').addClass('selected');
        $('.tabs_con:first').css('display','block');
    autoroll();
    hookThumb();
    var i=-1; //第i+1个tab开始
    var offset = 2500; //轮换时间
    var timer = null;
	var tabs=container.find(".tabs li");
	var len=container.find(".tabs li").length;
	var cons=container.find(".tabs_con");
    function autoroll(){
        n = tabs.length-1;
        i++;
        if(i > n){
            i = 0;
        }
        slide(i);
            timer = window.setTimeout(autoroll, offset);
    }
    function slide(i){
        tabs.eq(i).addClass('selected').siblings(".tabs li").removeClass('selected');
        cons.eq(i).css('display','block').siblings('.tabs_con').css('display','none');
    }
    function hookThumb(){    
    tabs.hover(
        function () {
            if (timer) {
                clearTimeout(timer);
                i = $(this).prevAll().length;
                slide(i);
                }
            },
        function () {      
            timer = window.setTimeout(autoroll, offset);  
            this.blur();            
            return false;
        }
        );
    }
	}
/**
+-----------------------------------------------------------
* 基于jquery的input默认值清空插件
* @author peter
+-----------------------------------------------------------
* 参数
* @ dvalue input表单提示默认值
* @ focusClass 在指定的input执行focus时替换的样式名class
+----------------------------------------------------------
*使用方法:
* $("#xxx").autotip();
* @ #xxx 为需要提示的input的id
*/
$.fn.autoTip = function(dvalue,focusClass){
	if ($(this).val() == ""||$(this).val() == dvalue){
		$(this).val(dvalue).focus(function(){
				if($(this).val() == dvalue){
					$(this).val("");}
				$(this).addClass(focusClass)
				})
				.blur(function(){
				if($(this).val() == ""){
				  $(this).val(dvalue);
				}
				$(this).removeClass(focusClass)
				});
	}
	else{	
		$(this).focus(function(){$(this).addClass(focusClass)}).blur(function(){$(this).removeClass(focusClass)});
		}
	
}

//用户中心表格效果
function tablecss(){	
	$(".u_table tbody tr:even").find("td").addClass("td_even");	
	$(".u_table tbody td").hover(function(){	
		$(this).addClass("td_hover");
		$(this).siblings("td").addClass("td_hover_b");
		})
		.mouseleave(function(){
		$(this).removeClass("td_hover");
		$(this).siblings("td").removeClass("td_hover_b")
		var i=$($(".u_table tr td")).index(this);
			})
$(".u_table th span").hover(function(){
	
	$(this).parents("th").addClass("th_hover");
	}).mouseleave(function(){$(this).parents("th").removeClass("th_hover");})
	}

//
$(document).ready(function(){
    $(".header_input").autoTip("输入商品链接","header_input_focus");
	$(".s_input").autoTip("粘贴宝贝地址，查询宝贝佣金","f333");
	$(".link_input").autoTip("请输入您要查询的商家、商品、活动的链接，以获得您的私募链接","f333");
	$(".edit_text_input").autoTip("请输入您要更改的文本","f333");
	$(".edit_img_input").autoTip("请输入您要更改的图片的网址","f333");
		$(".inv_email_name").autoTip("输入对方姓名","f333");
	$(".inv_email_address").autoTip("对方的邮件地址","f333");
		$(".task_numcheck").autoTip("请输入您的手机号码","f333");
			$(".task_codecheck").autoTip("请输入您收到的验证码","f333");
	{}
	
   imgscroll($("#adv_show"));
   imgscroll($("#act_subject")) ;
   imgscroll($("#taobaobanner")) ;
   //顶部菜单"我的私募网"展示
	$(".menu").hover(function(){		
		$(this).find("dl").show();
		$(this).addClass("menu_hover")
		}).mouseleave(function(){
			$(this).find("dl").hide();
		$(this).removeClass("menu_hover")	})
	//用户中心消息提示框效果
	$(".u_tips .close,.clare .close").click(function(){
	$(this).parents(".u_tips,.clare").slideUp();
	
	});
	
	//用户中心表格js效果
	tablecss();
	})
	

//回到顶部
$(document).scroll(function(){
	var btnHeight=$("#gototop").height();
	if($(document).scrollTop()>0)
	{
	$("#gototop").fadeIn();

	}
	else{
		$("#gototop").fadeOut()
	
}});
$(window).scroll(function(){
$("#gototop").css("top",$(window).scrollTop()+$(window).height()-$("#gototop").height());

$("#kefu").css("top",$(window).scrollTop()+200);

});
		
	
	
$(".kefu_btn").click(function(){
	$(".kefu_con").toggleClass("width120");

	})	
$(".kefu_close").click(function(){
	$("#kefu").hide();
	})
	
$(document).ready(function(){
$("#gototop").click(function(){
$("body,html").animate({scrollTop:0},1000);
});});

