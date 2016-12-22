/* -----------------------------------------------
   KOOP Webapp jQuery for Touch devices
   Version: 0.99                
   Date: 20-11-2014     
-----------------------------------------------*/  

// Change Date field to support touch date picker
$('input.date_picker').prop('type', 'date');
$('a.date_picker').css('display','none');
$('a.date_today').css('display','none');


//Touch in content tree shows children
if(($("a.parent_link").length) > 0){
    $("a.parent_link").bind('touchstart', function(e){
        //e.preventDefault();
        if ($(this).prev().attr("class")==="folding"){
            $(this).prev().removeClass("folding");
            $(this).prev().addClass("unfolding");
            $(this).parent().children("ul:first").addClass("hidden");
            $(this).nextAll("span:first").removeClass("hidden");
        }
        else {
            $(this).prev().removeClass("unfolding");
            $(this).prev().addClass("folding");
            $(this).parent().children("ul:first").removeClass("hidden");
            $(this).nextAll("span:first").addClass("hidden");
        }
    });     
}
        

