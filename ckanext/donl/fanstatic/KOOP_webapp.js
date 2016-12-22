
/* -----------------------------------------------
    Default actions after loading page
    Version: 0.99                
    Date: 20-11-2014      
-----------------------------------------------*/
function loadPageEventsAndPresentation() {
    
    /* Responsive menu for samll and mid screen devices */
    configureResponsiveMenu();
    
    /* Replace logo with highres on Retina*/
    if (window.devicePixelRatio > 1) {
	    var lowres = $('#logotype').attr('src');
        var highres = lowres.replace(".", "2x.");
		$('#logotype').attr('src', highres);
	}
    
    /* Specifici class for no IE8 browser */
    if (!$("html").hasClass("ie8")) {
        $("html").addClass("no-ie8");
    }
    
    /* Popup menu */ 
    $('#skip-to-menu').collapsable();
    
     $("#document_history").click(function(e) {
		e.preventDefault();
        loadHistoryPopup();
	});
        
    $("#background_popup").click(function() {
		closePopup();  
	});
    
    $("#toTop").click(function() {
          $('body,html').animate({scrollTop:0},400);
    });	

    // Actions for [Esc] key
    $(this).keyup(function(event) {
        if (event.which === 27) { // 27 is 'Ecs' in the keyboard
            closePopup();  // function close pop up
        }  	
    });
}


/* -----------------------------------------------
	  Left Menu bar events 
-----------------------------------------------*/
function loadMenuBarEvents() {
// Mouse over effect in facetten
    $( ".facet_selected li a" ).hover(function() {
            $(this).parent().addClass("highlight");
        }, function() {
            $(this).parent().removeClass("highlight");
        });
    
    $("a.doctype_popup").click(function(e) {
		e.preventDefault();
        loadDocTypeSelectionPopup();
	});
    
    $("a.country_popup").click(function(e) {
		e.preventDefault();
        loadCountrySelectionPopup();
	});
    
    }
/* -----------------------------------------------
	  Search form events 
-----------------------------------------------*/    
function loadFormEvents() {
        
    // Default text in Input field
    $(".default_text").focus(function()
    {
        if ($(this).val() === $(this)[0].title)
        {
            $(this).removeClass("default_text_active");
            $(this).val("");
        }
    });
        
    $(".default_text").blur(function()
    {
         
        if ($(this).val() === "")
        {
            $(this).addClass("default_text_active");
            $(this).val($(this)[0].title);
        }
    });
    
    $("p.info").each(function() {
        $(this).before(
		$("<a />", {
                addClass : "info",
                html : "?",
                click : function() {
				    $(this).next().toggleClass("info_active");
                }
              })); 
    });

    
    // Default text for docnumber is filled by select
    $(".default_text_docnumber").focus(function()
    {
        {
            $(this).removeClass("default_text_docnumber");
            $(this).val("");
        }
    });
    
    $("#doc_number_select").change(function(){
        $("#doc_number").attr("value", $(this).val());
        $("#doc_number").attr("title", $(this).val());
	});
    
    
    $(".default_text").blur(); 
    
    
    $("#date_till").addClass("hidden");
	$('#date_window').change(function() {	
     	var valueSelected = $("#date_window option:selected").val();
					
		if (valueSelected==="tussen"){
			$("#date_till").removeClass("hidden");
		}
		else {
			$("#date_till").addClass("hidden");
		}
	});
    
    // Mouse over effect bij kenmerken
    $( ".feature li a" ).hover(function() {
            $(this).parent().addClass("highlight");
        }, function() {
            $(this).parent().removeClass("highlight");
        }
    ); 
}


/* -----------------------------------------------
    Scroll to top functionality
 -----------------------------------------------*/
$(window).scroll(function(){
    if($(this).scrollTop() !== 0) {
        $('#toTop').fadeIn();
    } else {
        $('#toTop').fadeOut();
    }
});


/* -----------------------------------------------
    Popup menu for small screen device
-----------------------------------------------*/
$.fn.collapsable = function () {
    // iterate and reformat each matched element
    return this.each(function () {
        var knopje = $(this);
        var navigatie = $(knopje.attr('href'));
        var smallMenu = function () {
            return (document.body.clientWidth < 500);
        };
        if (smallMenu()) {
            navigatie.hide();
        }
        knopje.click(function (event) {
            if (smallMenu()) {
                event.preventDefault();
                navigatie.toggle();
            }
        });
        $(window).resize(function () {
            if (smallMenu()) {
                navigatie.hide();
            } else {
                navigatie.show();
            }
        });
    });
};

/* -----------------------------------------------
	  START Responsive functionality for menu
 -----------------------------------------------*/ 
function configureResponsiveMenu() {
     var windowState = 'large'; // variable to hold current window state - small, medium, or large

      // check intital width of the screen, respond with appropriate menu
     var sw = document.body.clientWidth;
     if (sw < 500) {
         smMenu();
     } else if (sw >= 500 && sw <= 968) {
             medMenu();
     } else {
             lgMenu();
     }

      // take care of resizing the window
      $(window).resize(function() {
          var sw = document.body.clientWidth;
          if (sw < 500 && windowState !== 'small') {
             smMenu();
          }
          if (sw > 499 && sw < 968 && windowState !== 'medium') {
             medMenu();
          }  
          if (sw > 968 && windowState !== 'large') {
             lgMenu();
          } 
          closeNavigatorPopupEvent();
      });

    function smMenu() {
        windowState = 'small';
        if (!$('.handle').length) { // Add handle to open leftmenu bar
             addMenuHandler();
        }
        
    }

    function medMenu() {
        windowState = 'medium';
        if (!$('.handle').length) { // Add handle to open leftmenu bar
            addMenuHandler();   
        }
    }

    function lgMenu() {
        windowState = 'large';
        $('.handle').remove(); // Remove handle for leftmenu bar
    }
} //configureResponsiveMenue


/* -----------------------------------------------
   Place handler for left menu
 -----------------------------------------------*/ 
function addMenuHandler(){    
    //console.log('add handle');
    var navigator = $();
    if ($('#content_navigation').length) {
        navigator = $('#content_navigation');
    } 
    if ($('#sub_form ').length) {
        navigator = $('#sub_form');
    }
    if ($('#aside ').length) {
        navigator = $('#aside');
    }
    
    if (navigator) {
        navigator.after( '<div class="handle">.<br />.<br />.</div>' ); 
        $('#main').off();
        $('#main').on('click', '.handle', function(event) {
            event.preventDefault();
            //openNavigatorPopupEvent(navigator);
            var navigatorWidth = navigator.width();
            navigator.toggleClass('open_navigation');
            $('.handle').toggleClass('open_navigation_handle');
            if (navigator.hasClass('open_navigation')) {
                navigator.removeClass('hidden');
                $("#background_popup").css("opacity", "0.3"); // css opacity, supports IE7, IE8
                $("#background_popup").fadeIn("fast");
                
                navigator.animate({
		    	     left: "0px"
	    	      });
                $('.handle').animate({
		    	     left: navigatorWidth
	    	      });
                
            } else {
                $("#background_popup").fadeOut("fast");
                navigator.animate({
		    	     left: -navigatorWidth
	    	      });
                $('.handle').animate({
		    	     left: "0px"
	    	      });
            }
        });
        
        // Open and close on focus and focus out
        navigator.focusin(function(e) {
            openNavigatorPopupEvent(navigator); 
        }); 
        $("#content").focusin(function(e) {
            closeNavigatorPopupEvent();
        }); 
        $("#footer").focusin(function(e) {
            closeNavigatorPopupEvent();
        });   
    }
}

/* -----------------------------------------------
   Show left menu
 -----------------------------------------------*/ 
function openNavigatorPopupEvent(navigatorElement) {
    var navigatorWidth = navigatorElement.width();
    if (!navigatorElement.hasClass('open_navigation')) {
        navigatorElement.addClass('open_navigation');
        $('.handle').toggleClass('open_navigation_handle');
        navigatorElement.removeClass('hidden');
        $("#background_popup").css("opacity", "0.3"); 
        $("#background_popup").fadeIn("fast");    
        navigatorElement.animate({
             left: "0px"
          });
        $('.handle').animate({
             left: navigatorWidth
          });
    }
}

/* -----------------------------------------------
   Hide left menu
 -----------------------------------------------*/ 
function closeNavigatorPopupEvent() {
    var navigator = $();
    if ($('#content_navigation').length) {
        navigator = $('#content_navigation');
    }
    if ($('#sub_form ').length) {
        navigator = $('#sub_form ');
    }
    if ($('#aside ').length) {
        navigator = $('#aside');
    }
    if (navigator) {
        if (navigator.hasClass('open_navigation')) {
            $("#background_popup").fadeOut("fast"); 
            var navigatorWidth = navigator.width();
            navigator.removeClass('open_navigation');
            $('.handle').removeClass('open_navigation_handle');
            navigator.animate({
		    	 left: -navigatorWidth
	           });
            $('.handle').animate({
		    	 left: "0px"
            });
        }
    }
    showHandle();
}

// Hide handle when a popup is loaden
function hideHandle() {
    $('.handle').css( 'z-index', '1' );
} 

//Show handle when a popup is closed
function showHandle() {
    $('.handle').css( 'z-index', '300' );
}

/* -----------------------------------------------
	 END  Responsive functionality for menu
 -----------------------------------------------*/ 


/* -----------------------------------------------
	 Lido releation events 
 -----------------------------------------------*/ 
function loadLidoLinkActions()
{
	
    $("a.relation_link").click(function(e) {
    	e.preventDefault();
        loadRelationPopup();
	});
    
    $(".show_lido_links").each(function() {
			$(this).click(function(e){
				e.preventDefault();
                if ($(this).hasClass("show_lido_links")){  
					$(this).removeClass("show_lido_links");
					$(this).addClass("hide_lido_links");
                    
					$(this).parent().children("ul").removeClass("hidden");
                    $(this).parent().parent().children("ul").removeClass("hidden");
				}
				else {
					$(this).removeClass("hide_lido_links");
					$(this).addClass("show_lido_links");
					$(this).parent().children("ul").addClass("hidden");
                    $(this).parent().parent().children("ul").addClass("hidden");
				}		
			});   
	});
    
    $(".show_ind_links").each(function() {
			$(this).click(function(e){
				e.preventDefault();
                if ($(this).hasClass("show_ind_links")){  
					$(this).removeClass("show_ind_links");
					$(this).addClass("hide_ind_links");
                    
					$(this).parent().children("ul").removeClass("hidden");
                    $(this).parent().parent().children("ul").removeClass("hidden");
				}
				else {
					$(this).removeClass("hide_ind_links");
					$(this).addClass("show_ind_links");
					$(this).parent().children("ul").addClass("hidden");
                    $(this).parent().parent().children("ul").addClass("hidden");
				}		
			}); 
	});
}

function setRelationlinkMouseOver()
{
    // Mouse over effect in content
    $( ".bwb_format .relation_link" ).hover(function() {
            $(this).parentsUntil("#content").removeClass("section_highlight");
            $(this).parent().addClass("section_highlight");
        }, function() {
            //$(this).parent().removeClass("section_highlight");
            $(this).parentsUntil("#content").removeClass("section_highlight");
        }
    );
    
}

/* -----------------------------------------------
	 END Lido links inside the Lidobox
 -----------------------------------------------*/

function loadCountrySelectionPopup() {
	$("#background_popup").css("opacity", "0.3"); // css opacity, supports IE7, IE8
	$("#background_popup").fadeIn("fast");
    $("#popup_selection").removeClass("hidden");
    
    $("#popup_selection").empty();
    
    $.get("_Land_selection.html", function (data) {
        $("#popup_selection").append(data);
    });
    hideHandle();
}

function loadDocTypeSelectionPopup() {
	$("#background_popup").css("opacity", "0.3"); // css opacity, supports IE7, IE8
	$("#background_popup").fadeIn("fast");
    $("#popup_selection").removeClass("hidden");
    
    $("#popup_selection").empty();
    
    $.get("_Doctype_selection.html", function (data) {
        $("#popup_selection").append(data);
    });
    hideHandle();
}

function loadRelationPopup() {
	$("#background_popup").css("opacity", "0.3"); // css opacity, supports IE7, IE8
	$("#background_popup").fadeIn("fast");
    $("#popup_relations").removeClass("hidden");
    hideHandle();
}

function loadHistoryPopup() {
	$("#background_popup").css("opacity", "0.3"); // css opacity, supports IE7, IE8
	$("#background_popup").fadeIn("fast");
    $("#popup_history").removeClass("hidden");
    hideHandle();
}

function closePopup() { 
	$("#background_popup").fadeOut("fast");  
	$("#popup_selection").addClass("hidden");
    $("#popup_relations").addClass("hidden");
    $("#popup_history").addClass("hidden");
    closeNavigatorPopupEvent();
}


/* -----------------------------------------------
    Chapter tree events + loading
    fold the chapter tree  
-----------------------------------------------*/
function loadChapterTreeEventsAndFold()  {
	if(($(".folding").length) > 0){
		$(".folding").click(function(e) {
			e.preventDefault();
            if ($(this).attr("class")==="folding"){
				$(this).removeClass("folding");
				$(this).addClass("unfolding");
				$(this).parent().children("ul:first").addClass("hidden");
                $(this).nextAll("span:first").removeClass("hidden");
			}
			else {
				$(this).removeClass("unfolding");
				$(this).addClass("folding");
				$(this).parent().children("ul:first").removeClass("hidden");
                $(this).nextAll("span:first").addClass("hidden");
			}
		});
        
        $("#fold_all").click(function() {
		  chapTreeFoldAll();  
	    });
    
        $("#unfold_all").click(function() {
		  chapTreeUnfoldAll();  
	    });
        
		//Fold the complete tree
		chapTreeFoldAll();	
	}
}

function chapTreeFoldAll() {     
		$( ".folding" ).each(function() {
			$(this).parent().children("ul:first").addClass("hidden");
		 	$(this).removeClass("folding");
		 	$(this).addClass("unfolding");
            $(this).nextAll("span:first").removeClass("hidden");
        });
   	}
	
function chapTreeUnfoldAll() {     
	$( ".unfolding" ).each(function() {
            $(this).parent().children("ul:first").removeClass("hidden");
            $(this).removeClass("unfolding");
            $(this).addClass("folding");
            $(this).nextAll("span:first").addClass("hidden");
		});
}