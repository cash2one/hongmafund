if($.cookie('user_nick')){
	$(".top_nav_off").hide();
	$(".top_nav_on").show();
	$(".user_emial").text($.cookie('user_nick'));
}else{
	$(".top_nav_off").show();
	$(".top_nav_on").hide();
}
/**copy text */
function toClipboard(copy_id,input_id) {
    var textMsg = document.getElementById(input_id).value;
	var clip = new ZeroClipboard.Client();  
	clip.setHandCursor(true);  
	clip.setText(textMsg);
	clip.addEventListener('complete', function (client) {  
		alert("复制成功");  
	});  
	clip.glue(copy_id);  
}