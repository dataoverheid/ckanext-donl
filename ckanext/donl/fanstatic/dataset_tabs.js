$( document ).ready(function() {
    
    //Deactivate tabs that have no content
    $('ul.tab li a').each(function(){
        if( $(this).text() != "Metadata" && $(this.hash + "-content ul").children().length == 0 ) {
        	//Remove the link and add a span in its place (so it will be visible, but not clickable!)
        	$(this).parent().append("<span class='disabledTab'>" + $(this).text() + "</span>")
        	$(this).remove();
        	//Hide the content section for the disabled link
        	$(this.hash).empty().css( { 'display' : 'none' } );
        	
      	}
    });

    //Show & Hide : Tabs & Content
    $('ul.tab').each(function(){
        //Get all links in tab
    	var $links = $(this).find('a');
        
        //Get the first 'a' and use that for the active item
        var $active = $($links.filter('[href="'+location.hash+'"]')[0] || $links[0]);
        $active.addClass('active');
        
        //Show the active item
        $($active[0].hash).show();
        
        //Hide the remaining items
        $links.not($active).each(function () {
            $(this.hash).hide();
        });
        
        //Get object that should be shown when the a is clicked
        var $content = $($active[0].hash);
        
        //Clicky clicky
        $(this).on('click', 'a', function(e){
            //Old is no longer active
            $active.removeClass('active');
            $content.hide();

            //New on is
            $active = $(this).addClass('active');
            $content = $(this.hash).show();

            //Don't do normal browser click
            e.preventDefault();
        });
    });

}); //Document ready