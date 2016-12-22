"use strict";

(function ($) {

    $(document).ready(function() {
        // Collapse the list on load
        $('ul.accordion-tree > li > ul').hide();
        $('ul.accordion-tree > li').click(function() {
            $(this).toggleClass('open');
            $(this).find('ul').slideToggle(300);
        });
    });

	$(document).ready(function(){
		donl_update_number_of_results();
		$('#search-maintainer').keyup(function(){
			donl_filter_maintainer();
		});
		$('#search-maintainer-form').submit(function(e){
			e.preventDefault();
			donl_filter_maintainer();
		});
        $('.page-dashboard')
		function donl_filter_maintainer() {
		   var valThis = $('#search-maintainer').val().toLowerCase();
		    if(valThis == ""){
		        $('#maintainer_list > li').show();
		    } else {
		        $('#maintainer_list > li').each(function(){
		            var text = $(this).text().toLowerCase();
		            (text.indexOf(valThis) >= 0) ? $(this).show() : $(this).hide();
		        });
		   };
		   donl_update_number_of_results();
		}
		function donl_update_number_of_results() {
			var res = $('#maintainer_list > li:visible').length;
			$('#search-maintainer-results').text(res);
		}
	});
    
    $(document).ready(function () {
        loadPageEventsAndPresentation(); 
        
        /* for : snippets\package_basic_fields.html */
        if( $( "body" ).hasClass( "dataset-aanmelden" ) ) {
            $('#field-dataset_status').change(function(){
              $('#div-date_planned').toggle($('#field-dataset_status').val() == "http://data.overheid.nl/status/gepland");
            });
        }
        /* //for : snippets\package_basic_fields.html */
        
        
        /* for : package\read_base.html */
        
        //Reposition permalink popup after resize
        $( window ).resize(function() {
            if( $('#permalink_popup').length ) {
                $('#permalink_popup').css(
                    {
                    'top'      : ( $("#permalink").offset().top +  $("#permalink").outerHeight() ) + 'px',
                    'left'     : ( $('article.module').offset().left + 10 ) + 'px'
                    }
                );
            }
        });
        
        //When click outside the popup, remove popup
        $( window ).click( function( e ) {
            if( ! $(e.toElement).hasClass('permalink_popup') ) {
                $("#permalink_popup").fadeOut('fast', function(){ $(this).remove(); });
            }
        });
        
        //Click on permalink button
        $( "#permalink" ).click( function( e ) {
            //Permalink opslaan (this is niet in context in de copy-click functie)            
            var permalink = this.href;
            
            //No default click action
            e.preventDefault();
            
            if( ! $('#permalink_popup' ).length ) {
                //Create popup window
                html = $('<div id="permalink_popup" class="permalink_popup">')
                    .append( $('<div class="popup_row copy_status permalink_popup">') )
                    .append( 
                        //label and link as tekst
                        $('<div class="popup_row permalink_popup">')
                            .append('<label class="permalink_popup">Permalink</label>')
                            .append("<span class='permalink permalink_popup'>" + permalink + "</span>")
                         )
                    //button for click-to-copy
                    .append( 
                        $('<div class="popup_row permalink_popup">')
                            .append( 
                                $('<a class="btn permalink_popup" href="#"><i class="icon-copy permalink_popup"></i>Kopieer</a>').click( function( e ) { 
                                    //No default click action
                                    e.preventDefault();
                                    //Copy link to clipboard
                                    clipboard.copy(permalink).then(function(){
                                        //report success
                                        $('#permalink_popup .copy_status').append('<span class="text-info">De permalink is gekopieerd.</span>');
                                        //remove popup
                                        setTimeout(function(){ $("#permalink_popup").fadeOut('slow', function(){ $(this).remove(); }); }, 2000 );
                                    }, function(err){
                                        //report error
                                        $('#permalink_popup .copy_status').append('<span class="text-error">De permalink kon niet gekopieerd worden.</span>');
                                        //remove popup
                                        setTimeout(function(){ $("#permalink_popup").fadeOut('slow', function(){ $(this).remove(); }); }, 2000 );
                                        
                                    });
                                } )
                            )
                        )
                    ;
                
                $('body').append(html);
                
                //Deel van de styling kan eventueel naar CSS, maar top/left moet hier blijven
                $('#permalink_popup').css(
                    {
                        'background-color' : '#d9ebf7',
                        'border' : '1px solid #154273',
                        'padding' : '10px',
                        'width' : ( $('article.module').width() - 40 ) + 'px',
                        
                        'position' : 'absolute',
                        'top'      : ( $(this).offset().top +  $(this).outerHeight() ) + 'px',
                        'left'     : ( $('article.module').offset().left + 10 ) + 'px'
                    }
                );
            }
            
            return false;
        } );
        
        /* //for : package\read_base.html */
        
        
        /* for adding a new dataset */
        $( "div.control-group:has(#field-name)" ).css( { 'display' : 'none' } );
        $( "#dataset-edit" ).submit(function( event ) {
          
          //sets the fieldname, this is done in a hidden field as the GUID is not needed, also make it machine friendly
          document.getElementById("field-name").value = document.getElementById("field-title").value.replace(/\W/g,'_').replace(/[_]+$/,'').toLowerCase();
          console.log( document.getElementById("field-name").value );
          
        });
                    
        
        
    });
    
    
})(jQuery);

Modernizr.load([{test : Modernizr.mq('only all'),nope : 'js/respond.min.js'},{test: Modernizr.touch,yep: 'js/KOOP_webapp_touch.js'},,]);

