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
	container.find('.tabs li:first').addClass('selected');
    autoroll();
    hookThumb();
    var i=-1; //第i+1个tab开始
    var offset = 2500; //轮换时间
    var timer = null;
	var tabs=container.find(".tabs li");
	alert(tabs.html())
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


	

$(function () {
    var len = $(".switch_btn li").length;
    var index = 0;
    var adTimer;
    $(".switch_btn li").mouseover(function () {
        index = $(".switch_btn li").index(this);
        showImg(index);
    }).eq(0).mouseover();
    //滑入 停止动画，滑出开始动画.
    $('.banner').hover(function () {
        clearInterval(adTimer);
   }, function () {
        adTimer = setInterval(function () {
            showImg(index)
            index++;
            if (index == len) { index = 0; }
        }, 5000);
    }).trigger("mouseleave");
})
//// 通过控制top ，来显示不同的幻灯片
function showImg(index) {
    var adHeight = $(".banner").height();
    $(".banner .pic ul").stop(true, false).animate({ top: -adHeight * index }, 1000);
    $(".switch_btn li").removeClass("curr").eq(index).addClass("curr");
}
