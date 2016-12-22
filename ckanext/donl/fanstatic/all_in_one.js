/* Modernizr 2.8.3 (Custom Build) | MIT & BSD
 * Build: http://modernizr.com/download/#-fontface-borderradius-boxshadow-flexbox-csstransforms-csstransforms3d-csstransitions-canvas-touch-mq-cssclasses-teststyles-testprop-testallprops-prefixes-domprefixes-load
 */
;window.Modernizr=function(a,b,c){function A(a){j.cssText=a}function B(a,b){return A(m.join(a+";")+(b||""))}function C(a,b){return typeof a===b}function D(a,b){return!!~(""+a).indexOf(b)}function E(a,b){for(var d in a){var e=a[d];if(!D(e,"-")&&j[e]!==c)return b=="pfx"?e:!0}return!1}function F(a,b,d){for(var e in a){var f=b[a[e]];if(f!==c)return d===!1?a[e]:C(f,"function")?f.bind(d||b):f}return!1}function G(a,b,c){var d=a.charAt(0).toUpperCase()+a.slice(1),e=(a+" "+o.join(d+" ")+d).split(" ");return C(b,"string")||C(b,"undefined")?E(e,b):(e=(a+" "+p.join(d+" ")+d).split(" "),F(e,b,c))}var d="2.8.3",e={},f=!0,g=b.documentElement,h="modernizr",i=b.createElement(h),j=i.style,k,l={}.toString,m=" -webkit- -moz- -o- -ms- ".split(" "),n="Webkit Moz O ms",o=n.split(" "),p=n.toLowerCase().split(" "),q={},r={},s={},t=[],u=t.slice,v,w=function(a,c,d,e){var f,i,j,k,l=b.createElement("div"),m=b.body,n=m||b.createElement("body");if(parseInt(d,10))while(d--)j=b.createElement("div"),j.id=e?e[d]:h+(d+1),l.appendChild(j);return f=["&#173;",'<style id="s',h,'">',a,"</style>"].join(""),l.id=h,(m?l:n).innerHTML+=f,n.appendChild(l),m||(n.style.background="",n.style.overflow="hidden",k=g.style.overflow,g.style.overflow="hidden",g.appendChild(n)),i=c(l,a),m?l.parentNode.removeChild(l):(n.parentNode.removeChild(n),g.style.overflow=k),!!i},x=function(b){var c=a.matchMedia||a.msMatchMedia;if(c)return c(b)&&c(b).matches||!1;var d;return w("@media "+b+" { #"+h+" { position: absolute; } }",function(b){d=(a.getComputedStyle?getComputedStyle(b,null):b.currentStyle)["position"]=="absolute"}),d},y={}.hasOwnProperty,z;!C(y,"undefined")&&!C(y.call,"undefined")?z=function(a,b){return y.call(a,b)}:z=function(a,b){return b in a&&C(a.constructor.prototype[b],"undefined")},Function.prototype.bind||(Function.prototype.bind=function(b){var c=this;if(typeof c!="function")throw new TypeError;var d=u.call(arguments,1),e=function(){if(this instanceof e){var a=function(){};a.prototype=c.prototype;var f=new a,g=c.apply(f,d.concat(u.call(arguments)));return Object(g)===g?g:f}return c.apply(b,d.concat(u.call(arguments)))};return e}),q.flexbox=function(){return G("flexWrap")},q.canvas=function(){var a=b.createElement("canvas");return!!a.getContext&&!!a.getContext("2d")},q.touch=function(){var c;return"ontouchstart"in a||a.DocumentTouch&&b instanceof DocumentTouch?c=!0:w(["@media (",m.join("touch-enabled),("),h,")","{#modernizr{top:9px;position:absolute}}"].join(""),function(a){c=a.offsetTop===9}),c},q.borderradius=function(){return G("borderRadius")},q.boxshadow=function(){return G("boxShadow")},q.csstransforms=function(){return!!G("transform")},q.csstransforms3d=function(){var a=!!G("perspective");return a&&"webkitPerspective"in g.style&&w("@media (transform-3d),(-webkit-transform-3d){#modernizr{left:9px;position:absolute;height:3px;}}",function(b,c){a=b.offsetLeft===9&&b.offsetHeight===3}),a},q.csstransitions=function(){return G("transition")},q.fontface=function(){var a;return w('@font-face {font-family:"font";src:url("https://")}',function(c,d){var e=b.getElementById("smodernizr"),f=e.sheet||e.styleSheet,g=f?f.cssRules&&f.cssRules[0]?f.cssRules[0].cssText:f.cssText||"":"";a=/src/i.test(g)&&g.indexOf(d.split(" ")[0])===0}),a};for(var H in q)z(q,H)&&(v=H.toLowerCase(),e[v]=q[H](),t.push((e[v]?"":"no-")+v));return e.addTest=function(a,b){if(typeof a=="object")for(var d in a)z(a,d)&&e.addTest(d,a[d]);else{a=a.toLowerCase();if(e[a]!==c)return e;b=typeof b=="function"?b():b,typeof f!="undefined"&&f&&(g.className+=" "+(b?"":"no-")+a),e[a]=b}return e},A(""),i=k=null,e._version=d,e._prefixes=m,e._domPrefixes=p,e._cssomPrefixes=o,e.mq=x,e.testProp=function(a){return E([a])},e.testAllProps=G,e.testStyles=w,g.className=g.className.replace(/(^|\s)no-js(\s|$)/,"$1$2")+(f?" js "+t.join(" "):""),e}(this,this.document),function(a,b,c){function d(a){return"[object Function]"==o.call(a)}function e(a){return"string"==typeof a}function f(){}function g(a){return!a||"loaded"==a||"complete"==a||"uninitialized"==a}function h(){var a=p.shift();q=1,a?a.t?m(function(){("c"==a.t?B.injectCss:B.injectJs)(a.s,0,a.a,a.x,a.e,1)},0):(a(),h()):q=0}function i(a,c,d,e,f,i,j){function k(b){if(!o&&g(l.readyState)&&(u.r=o=1,!q&&h(),l.onload=l.onreadystatechange=null,b)){"img"!=a&&m(function(){t.removeChild(l)},50);for(var d in y[c])y[c].hasOwnProperty(d)&&y[c][d].onload()}}var j=j||B.errorTimeout,l=b.createElement(a),o=0,r=0,u={t:d,s:c,e:f,a:i,x:j};1===y[c]&&(r=1,y[c]=[]),"object"==a?l.data=c:(l.src=c,l.type=a),l.width=l.height="0",l.onerror=l.onload=l.onreadystatechange=function(){k.call(this,r)},p.splice(e,0,u),"img"!=a&&(r||2===y[c]?(t.insertBefore(l,s?null:n),m(k,j)):y[c].push(l))}function j(a,b,c,d,f){return q=0,b=b||"j",e(a)?i("c"==b?v:u,a,b,this.i++,c,d,f):(p.splice(this.i++,0,a),1==p.length&&h()),this}function k(){var a=B;return a.loader={load:j,i:0},a}var l=b.documentElement,m=a.setTimeout,n=b.getElementsByTagName("script")[0],o={}.toString,p=[],q=0,r="MozAppearance"in l.style,s=r&&!!b.createRange().compareNode,t=s?l:n.parentNode,l=a.opera&&"[object Opera]"==o.call(a.opera),l=!!b.attachEvent&&!l,u=r?"object":l?"script":"img",v=l?"script":u,w=Array.isArray||function(a){return"[object Array]"==o.call(a)},x=[],y={},z={timeout:function(a,b){return b.length&&(a.timeout=b[0]),a}},A,B;B=function(a){function b(a){var a=a.split("!"),b=x.length,c=a.pop(),d=a.length,c={url:c,origUrl:c,prefixes:a},e,f,g;for(f=0;f<d;f++)g=a[f].split("="),(e=z[g.shift()])&&(c=e(c,g));for(f=0;f<b;f++)c=x[f](c);return c}function g(a,e,f,g,h){var i=b(a),j=i.autoCallback;i.url.split(".").pop().split("?").shift(),i.bypass||(e&&(e=d(e)?e:e[a]||e[g]||e[a.split("/").pop().split("?")[0]]),i.instead?i.instead(a,e,f,g,h):(y[i.url]?i.noexec=!0:y[i.url]=1,f.load(i.url,i.forceCSS||!i.forceJS&&"css"==i.url.split(".").pop().split("?").shift()?"c":c,i.noexec,i.attrs,i.timeout),(d(e)||d(j))&&f.load(function(){k(),e&&e(i.origUrl,h,g),j&&j(i.origUrl,h,g),y[i.url]=2})))}function h(a,b){function c(a,c){if(a){if(e(a))c||(j=function(){var a=[].slice.call(arguments);k.apply(this,a),l()}),g(a,j,b,0,h);else if(Object(a)===a)for(n in m=function(){var b=0,c;for(c in a)a.hasOwnProperty(c)&&b++;return b}(),a)a.hasOwnProperty(n)&&(!c&&!--m&&(d(j)?j=function(){var a=[].slice.call(arguments);k.apply(this,a),l()}:j[n]=function(a){return function(){var b=[].slice.call(arguments);a&&a.apply(this,b),l()}}(k[n])),g(a[n],j,b,n,h))}else!c&&l()}var h=!!a.test,i=a.load||a.both,j=a.callback||f,k=j,l=a.complete||f,m,n;c(h?a.yep:a.nope,!!i),i&&c(i)}var i,j,l=this.yepnope.loader;if(e(a))g(a,0,l,0);else if(w(a))for(i=0;i<a.length;i++)j=a[i],e(j)?g(j,0,l,0):w(j)?B(j):Object(j)===j&&h(j,l);else Object(a)===a&&h(a,l)},B.addPrefix=function(a,b){z[a]=b},B.addFilter=function(a){x.push(a)},B.errorTimeout=1e4,null==b.readyState&&b.addEventListener&&(b.readyState="loading",b.addEventListener("DOMContentLoaded",A=function(){b.removeEventListener("DOMContentLoaded",A,0),b.readyState="complete"},0)),a.yepnope=k(),a.yepnope.executeStack=h,a.yepnope.injectJs=function(a,c,d,e,i,j){var k=b.createElement("script"),l,o,e=e||B.errorTimeout;k.src=a;for(o in d)k.setAttribute(o,d[o]);c=j?h:c||f,k.onreadystatechange=k.onload=function(){!l&&g(k.readyState)&&(l=1,c(),k.onload=k.onreadystatechange=null)},m(function(){l||(l=1,c(1))},e),i?k.onload():n.parentNode.insertBefore(k,n)},a.yepnope.injectCss=function(a,c,d,e,g,i){var e=b.createElement("link"),j,c=i?h:c||f;e.href=a,e.rel="stylesheet",e.type="text/css";for(j in d)e.setAttribute(j,d[j]);g||(n.parentNode.insertBefore(e,n),m(c,0))}}(this,document),Modernizr.load=function(){yepnope.apply(window,[].slice.call(arguments,0))};
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
        
        if( $( "body" ).hasClass( "dataset-aanmelden" ) ) {
            $('#dataset-edit input').change(function(){
                //Is er een waarde ingevoerd?
                if( $( this ).val() != ''  ) {
                    //remove 'missende waarde'
                    
                    $(this).siblings(".error-block").remove();
                    $(this).parent().parent().removeClass('error');
                }
            });
            $('#dataset-edit textarea').change(function(){
                //Is er een waarde ingevoerd?
                if( $( this ).val() != ''  ) {
                    //remove 'missende waarde'
                    
                    $(this).siblings(".error-block").remove();
                    $(this).parent().parent().removeClass('error');
                }
            });
            
        }
        /* //for : snippets\package_basic_fields.html */
        
        
        /* for : package\read_base.html */
        
         
        //Set the permalink from the permalink href (browser adds domain, this does not come from CKAN)
        if( $("#permalink").length ) {
            $("#permalink_showlink").html( $("#permalink")[0].href );
        }
        
        //When click outside the permalink_popup, hide permalink_popup
        $( window ).click( function( e ) {
            //Dont hide when we click the permalink show button
            if( (e.toElement !== null) && typeof e.toElement == 'object' ) {
            if( e.toElement.id != "permalink" ) {
                if( ! $(e.toElement).hasClass('permalink_popup') ) {
                    $("#permalink_popup").removeClass('show').addClass('hidden');
                }
            }
            }
        });
        
        //Show/hide permalink_popup via Permalink button
        $( "#permalink" ).click( function( e ) {
            if( $("#permalink_popup").hasClass("show") ) {
                $("#permalink_popup").removeClass('show').addClass('hidden');
            }
            else {
                $("#permalink_popup").removeClass('hidden').addClass('show');
            }
            //No default click action
            e.preventDefault();
        });
                
        //Copy permalink
        $('#permalink_popup_copy_btn').click( function( e ) { 
            var permalink = $("#permalink")[0].href;
            
            //No default click action
            e.preventDefault();
            
            //Copy link to clipboard
            clipboard.copy(permalink).then(function(){
                //report success
                $('#permalink_popup .copy_status').append('<span class="text-info">De permalink is gekopieerd.</span>');
                //remove popup
                setTimeout(function(){ $("#permalink_popup").removeClass('show').addClass('hidden'); }, 2000 );
            }, function(err){
                //report error
                $('#permalink_popup .copy_status').append('<span class="text-error">De permalink kon niet gekopieerd worden.</span>');
                //remove popup
                setTimeout(function(){ $("#permalink_popup").removeClass('show').addClass('hidden'); }, 2000 );
                
            });
        } );
        
        
        
        /* //for : package\read_base.html */
        
        
        /* for adding a new dataset */
        
        //Checks if a date is valid and in dd-mm-yyyy format, returns true|false
        function isValidDate(date) {
            //First get the d,m,y parts of the date with a regexp
            var matches = /^(\d{1,2})-(\d{1,2})-(\d{4})$/.exec(date);
            
            //There should be matches
            if (matches == null) return false;
            
            //Get from matches
            var d = matches[1];
            var m = matches[2];
            var y = matches[3];
            
            //Check for valid day and month
            if( d > 31 || m > 12 ) { return false; }
            
            //javascript month is 0 based!
            m--;
            
            //Create a new date with the parts
            var composedDate = new Date(y, m, d);
            
            //Compare the new date with the parts  (javascript keeps on counting in new date : 32-11-2016 == 1-1-2017)
            return composedDate.getDate() == d && 
            			 composedDate.getMonth() == m &&
                   composedDate.getFullYear() == y;
        }
        
        function checkDateField( fieldID ) {
          var d = document.getElementById(fieldID).value;
          var v = isValidDate( d )
          
          
          if( !v  ) {

            //Not a valid date, check if the error div is already visible
            if( ! $("#" + fieldID).next().is('div.error-block') ) {
              //No error div yet, show one
              if (fieldID == "field-modified" || fieldID == "field-date_planned") {
                $( "#" + fieldID ).after( '<div class="error-block"><div>Niet in dd-mm-jjjj formaat. Dit veld is verplicht.</div></div>' );
              }
              else {
                $( "#" + fieldID ).after( '<div class="error-block"><div>Niet in dd-mm-jjjj formaat</div></div>' );
              }
              
              $( "#" + fieldID ).parent().parent().addClass("error");
            }
            return false;
          }
          else {
            return true;
          }
          
        }

        $( "#dataset-edit div.control-group:has(#field-name)" ).css( { 'display' : 'none' } );
        $( "#dataset-edit" ).submit(function( event ) {

          //sets the fieldname, this is done in a hidden field as the GUID is not needed, also make it machine friendly
          document.getElementById("field-name").value = document.getElementById("field-title").value.replace(/\W/g,'-').replace(/[_]+$/,'').toLowerCase();

          /*
           * Check date fields
           */
          

          //Always check modified
          var modified = checkDateField( "field-modified" );
                    
          
          //Periode van == field-temporal_from
          var tFrom;
          if( document.getElementById("field-temporal_from").value === "" ) {
            tFrom = true; //No value, valid!
          }
          else {
            tFrom = checkDateField( "field-temporal_from" )
          }
          
          
          
          //Periode tot == field-temporal_to
          var tTo;
          if( document.getElementById("field-temporal_to").value === "" ) {
            tTo = true; //No value, valid!
          }
          else {
            tTo = checkDateField( "field-temporal_to" )
          }
          

          /*
          var planned;
          if( document.getElementById("field-date_planned").value === "" ) {
            planned = true; //No value, valid!
          }
          else {
            planned = checkDateField( "field-date_planned" )
          }
          */

          var planned;
          if ($('#div-date_planned').css('display') == 'none' ) {
            planned = true; //Not visible, valid!
          }
          else {
            planned = checkDateField( "field-date_planned" )
          }
          
          
          
          if( modified && tFrom && tTo && planned ) {
            //All are valid, continue!
            return;
          }
          
          //else {
          //    console.log( "Cannot submit!" );
          //}
          
          
          //No submit yet
          event.preventDefault();

        });        
        
        $( "#field-temporal_from" ).blur(function( event ) { 
            
            if( document.getElementById("field-temporal_from").value === "" ) {
                if( $("#field-temporal_from").next().is('div.error-block') ) {
                    $("#field-temporal_from").next().remove();
                    $( "#field-temporal_from" ).parent().parent().removeClass("error");
                }
            }
            
        });
        $( "#field-temporal_to" ).blur(function( event ) { 
            
            if( document.getElementById("field-temporal_to").value === "" ) {
                if( $("#field-temporal_to").next().is('div.error-block') ) {
                    $("#field-temporal_to").next().remove();
                    $( "#field-temporal_to" ).parent().parent().removeClass("error");
                }
            }
            
        });
        $( "#field-date_planned" ).blur(function( event ) { 
            
            if( document.getElementById("field-date_planned").value === "" ) {
                if( $("#field-date_planned").next().is('div.error-block') ) {
                    $("#field-date_planned").next().remove();
                    $("#field-date_planned").parent().parent().removeClass("error");
                }
            }
            
        });
        
        $.getJSON( "/service/waardelijsten/dataset_aanmelden_", function( data ) {
            
            $('#dataset-edit input').each(function () {
                if ( this.type != "hidden" && this.type != "checkbox"  ) {
                    for( var d in data ) {
                        if( this.id == data[d].name) {
                            $(this).after('<div class="description" style="display: none;">' + data[d].description + '</div>')
                                   .after('<button type="button" class="open">Toelichting bij het veld</button>');
      
                        }
                    }
                }
            });
            
            $('#dataset-edit select').each(function () {
                if ( this.type != "hidden" && this.type != "checkbox"  ) {
                    for( var d in data ) {
                        if( this.id == data[d].name) {
                            $(this).after('<div class="description" style="display: none;">' + data[d].description + '</div>')
                                   .after('<button type="button" class="open">Toelichting bij het veld</button>');
      
                        }
                    }
                }
            });
			
			$('#dataset-edit textarea').each(function () {
                if ( this.type != "hidden" && this.type != "checkbox"  ) {
                    for( var d in data ) {
                        if( this.id == data[d].name) {
                            $(this).after('<div class="description" style="display: none;">' + data[d].description + '</div>')
                                   .after('<button type="button" class="open">Toelichting bij het veld</button>');
      
                        }
                    }
                }
            });
            
            $( ".control-group button" ).click(function( e ) {
                if( $(this).hasClass("open") ) {
                    $(this).next( ".description" ).show(300);
                    $(this).html('Toelichting bij het veld').removeClass('open').addClass('close');
                }
                else {
                    $(this).next( ".description" ).hide(300);
                    $(this).html('Deze toelichting sluiten').removeClass('close').addClass('open');
                }
            });
            
            $("select[data-module='autocomplete']").each(function () {
               
               
                 $( this ).next().addClass('extraTopPad');
                
            });
            
        });
        
        
        if( $("form#dataset-edit").length && $("div.error-explanation").length ) {
          betterErrors();
        }
        if( $("body.dataset-aanmelden").length && $("div.error-explanation").length ) {
          betterErrors();
        }
        
        function betterErrors() {    
            $('div.error-explanation li').each(function(){
                var txt = $(this).text();


                if( txt.indexOf("Naam: Deze URL is al in gebruik") == 0) {
                    $("#field-title").after( '<div class="error-block"><div>De opgegeven titel is reeds in gebruik</div></div>' );
                    $("#field-title").parent().parent().addClass('error');
                }

//                if( txt.substring(0,6) == "Naam: " ) {
//                    $(this).remove();
//                }
//                else {
                    
                    txt = txt.replace( "Missende waarde", "Dit veld is verplicht");
                    txt = txt.replace( "Notes:", "Omschrijving:");
                    txt = txt.replace( "Modified:", "Wijzigingsdatum:");
                    txt = txt.replace( "Naam: Deze URL is al in gebruik.", "Titel: De opgegeven titel is reeds in gebruik.");
                    $(this).text( txt );
//                }
            });
            
            $('div.error-block div').each(function(){
                
                var txt = $(this).text();
                txt = txt.replace( "Missende waarde" ,"Dit veld is verplicht" );
                $(this).text( txt );
            });
            
            $('div.error-explanation').show();
            
        }

    });
    
    
})(jQuery);

Modernizr.load([{test : Modernizr.mq('only all'),nope : 'js/respond.min.js'},{test: Modernizr.touch,yep: 'js/KOOP_webapp_touch.js'},,]);


(function(f,c){"undefined"!==typeof module?module.exports=c():"function"===typeof define&&"object"===typeof define.amd?define(c):this[f]=c()})("clipboard",function(){if(!document.addEventListener)return null;var f={};f.copy=function(){var c=!1,d=null;document.addEventListener("copy",function(b){if(c){for(var e in d)b.clipboardData.setData(e,d[e]);b.preventDefault()}});return function(b){return new Promise(function(e,h){c=!0;d="string"===typeof b?{"text/plain":b}:b instanceof Node?{"text/html":(new XMLSerializer).serializeToString(b)}:
b;try{if(document.execCommand("copy"))c=!1,d=null,e();else throw Error("Unable to copy. Perhaps it's not available in your browser?");}catch(g){c=!1,d=null,h(g)}})}}();f.paste=function(){var c=!1,d,b;document.addEventListener("paste",function(e){if(c){c=!1;e.preventDefault();var h=d;d=null;h(e.clipboardData.getData(b))}});return function(e){return new Promise(function(h,g){c=!0;d=h;b=e||"text/plain";try{document.execCommand("paste")||(c=!1,g(Error("Unable to paste. Pasting only works in Internet Explorer at the moment.")))}catch(f){c=
!1,g(Error(f))}})}}();"undefined"===typeof ClipboardEvent&&("undefined"!==typeof window.clipboardData&&"undefined"!==typeof window.clipboardData.setData)&&(function(c){function d(a,b){return function(){a.apply(b,arguments)}}function b(a){if("object"!=typeof this)throw new TypeError("Promises must be constructed via new");if("function"!=typeof a)throw new TypeError("not a function");this._value=this._state=null;this._deferreds=[];l(a,d(f,this),d(g,this))}function e(a){var b=this;return null===this._state?
void this._deferreds.push(a):void n(function(){var c=b._state?a.onFulfilled:a.onRejected;if(null===c)return void(b._state?a.resolve:a.reject)(b._value);var m;try{m=c(b._value)}catch(d){return void a.reject(d)}a.resolve(m)})}function f(a){try{if(a===this)throw new TypeError("A promise cannot be resolved with itself.");if(a&&("object"==typeof a||"function"==typeof a)){var b=a.then;if("function"==typeof b)return void l(d(b,a),d(f,this),d(g,this))}this._state=!0;this._value=a;k.call(this)}catch(c){g.call(this,
c)}}function g(a){this._state=!1;this._value=a;k.call(this)}function k(){for(var a=0,b=this._deferreds.length;b>a;a++)e.call(this,this._deferreds[a]);this._deferreds=null}function p(a,b,c,d){this.onFulfilled="function"==typeof a?a:null;this.onRejected="function"==typeof b?b:null;this.resolve=c;this.reject=d}function l(a,b,c){var d=!1;try{a(function(a){d||(d=!0,b(a))},function(a){d||(d=!0,c(a))})}catch(f){d||(d=!0,c(f))}}var n=b.immediateFn||"function"==typeof setImmediate&&setImmediate||function(a){setTimeout(a,
1)},q=Array.isArray||function(a){return"[object Array]"===Object.prototype.toString.call(a)};b.prototype["catch"]=function(a){return this.then(null,a)};b.prototype.then=function(a,c){var d=this;return new b(function(b,f){e.call(d,new p(a,c,b,f))})};b.all=function(){var a=Array.prototype.slice.call(1===arguments.length&&q(arguments[0])?arguments[0]:arguments);return new b(function(b,c){function d(e,g){try{if(g&&("object"==typeof g||"function"==typeof g)){var h=g.then;if("function"==typeof h)return void h.call(g,
function(a){d(e,a)},c)}a[e]=g;0===--f&&b(a)}catch(k){c(k)}}if(0===a.length)return b([]);for(var f=a.length,e=0;e<a.length;e++)d(e,a[e])})};b.resolve=function(a){return a&&"object"==typeof a&&a.constructor===b?a:new b(function(b){b(a)})};b.reject=function(a){return new b(function(b,c){c(a)})};b.race=function(a){return new b(function(b,c){for(var d=0,e=a.length;e>d;d++)a[d].then(b,c)})};"undefined"!=typeof module&&module.exports?module.exports=b:c.Promise||(c.Promise=b)}(this),f.copy=function(c){return new Promise(function(d,
b){if("string"!==typeof c&&!("text/plain"in c))throw Error("You must provide a text/plain type.");window.clipboardData.setData("Text","string"===typeof c?c:c["text/plain"])?d():b(Error("Copying was rejected."))})},f.paste=function(){return new Promise(function(c,d){var b=window.clipboardData.getData("Text");b?c(b):d(Error("Pasting was rejected."))})});return f});
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
if ($('html').is('.lt-ie9')) {



/*! matchMedia() polyfill - Test a CSS media type/query in JS. Authors & copyright (c) 2012: Scott Jehl, Paul Irish, Nicholas Zakas. Dual MIT/BSD license */
/*! NOTE: If you're already including a window.matchMedia polyfill via Modernizr or otherwise, you don't need this part */
window.matchMedia=window.matchMedia||function(a){"use strict";var c,d=a.documentElement,e=d.firstElementChild||d.firstChild,f=a.createElement("body"),g=a.createElement("div");return g.id="mq-test-1",g.style.cssText="position:absolute;top:-100em",f.style.background="none",f.appendChild(g),function(a){return g.innerHTML='&shy;<style media="'+a+'"> #mq-test-1 { width: 42px; }</style>',d.insertBefore(f,e),c=42===g.offsetWidth,d.removeChild(f),{matches:c,media:a}}}(document);

/*! Respond.js v1.4.2: min/max-width media query polyfill * Copyright 2013 Scott Jehl
 * Licensed under https://github.com/scottjehl/Respond/blob/master/LICENSE-MIT
 **/
!function(a){"use strict";a.matchMedia=a.matchMedia||function(a){var b,c=a.documentElement,d=c.firstElementChild||c.firstChild,e=a.createElement("body"),f=a.createElement("div");return f.id="mq-test-1",f.style.cssText="position:absolute;top:-100em",e.style.background="none",e.appendChild(f),function(a){return f.innerHTML='&shy;<style media="'+a+'"> #mq-test-1 { width: 42px; }</style>',c.insertBefore(e,d),b=42===f.offsetWidth,c.removeChild(e),{matches:b,media:a}}}(a.document)}(this),function(a){"use strict";function b(){u(!0)}var c={};a.respond=c,c.update=function(){};var d=[],e=function(){var b=!1;try{b=new a.XMLHttpRequest}catch(c){b=new a.ActiveXObject("Microsoft.XMLHTTP")}return function(){return b}}(),f=function(a,b){var c=e();c&&(c.open("GET",a,!0),c.onreadystatechange=function(){4!==c.readyState||200!==c.status&&304!==c.status||b(c.responseText)},4!==c.readyState&&c.send(null))};if(c.ajax=f,c.queue=d,c.regex={media:/@media[^\{]+\{([^\{\}]*\{[^\}\{]*\})+/gi,keyframes:/@(?:\-(?:o|moz|webkit)\-)?keyframes[^\{]+\{(?:[^\{\}]*\{[^\}\{]*\})+[^\}]*\}/gi,urls:/(url\()['"]?([^\/\)'"][^:\)'"]+)['"]?(\))/g,findStyles:/@media *([^\{]+)\{([\S\s]+?)$/,only:/(only\s+)?([a-zA-Z]+)\s?/,minw:/\([\s]*min\-width\s*:[\s]*([\s]*[0-9\.]+)(px|em)[\s]*\)/,maxw:/\([\s]*max\-width\s*:[\s]*([\s]*[0-9\.]+)(px|em)[\s]*\)/},c.mediaQueriesSupported=a.matchMedia&&null!==a.matchMedia("only all")&&a.matchMedia("only all").matches,!c.mediaQueriesSupported){var g,h,i,j=a.document,k=j.documentElement,l=[],m=[],n=[],o={},p=30,q=j.getElementsByTagName("head")[0]||k,r=j.getElementsByTagName("base")[0],s=q.getElementsByTagName("link"),t=function(){var a,b=j.createElement("div"),c=j.body,d=k.style.fontSize,e=c&&c.style.fontSize,f=!1;return b.style.cssText="position:absolute;font-size:1em;width:1em",c||(c=f=j.createElement("body"),c.style.background="none"),k.style.fontSize="100%",c.style.fontSize="100%",c.appendChild(b),f&&k.insertBefore(c,k.firstChild),a=b.offsetWidth,f?k.removeChild(c):c.removeChild(b),k.style.fontSize=d,e&&(c.style.fontSize=e),a=i=parseFloat(a)},u=function(b){var c="clientWidth",d=k[c],e="CSS1Compat"===j.compatMode&&d||j.body[c]||d,f={},o=s[s.length-1],r=(new Date).getTime();if(b&&g&&p>r-g)return a.clearTimeout(h),h=a.setTimeout(u,p),void 0;g=r;for(var v in l)if(l.hasOwnProperty(v)){var w=l[v],x=w.minw,y=w.maxw,z=null===x,A=null===y,B="em";x&&(x=parseFloat(x)*(x.indexOf(B)>-1?i||t():1)),y&&(y=parseFloat(y)*(y.indexOf(B)>-1?i||t():1)),w.hasquery&&(z&&A||!(z||e>=x)||!(A||y>=e))||(f[w.media]||(f[w.media]=[]),f[w.media].push(m[w.rules]))}for(var C in n)n.hasOwnProperty(C)&&n[C]&&n[C].parentNode===q&&q.removeChild(n[C]);n.length=0;for(var D in f)if(f.hasOwnProperty(D)){var E=j.createElement("style"),F=f[D].join("\n");E.type="text/css",E.media=D,q.insertBefore(E,o.nextSibling),E.styleSheet?E.styleSheet.cssText=F:E.appendChild(j.createTextNode(F)),n.push(E)}},v=function(a,b,d){var e=a.replace(c.regex.keyframes,"").match(c.regex.media),f=e&&e.length||0;b=b.substring(0,b.lastIndexOf("/"));var g=function(a){return a.replace(c.regex.urls,"$1"+b+"$2$3")},h=!f&&d;b.length&&(b+="/"),h&&(f=1);for(var i=0;f>i;i++){var j,k,n,o;h?(j=d,m.push(g(a))):(j=e[i].match(c.regex.findStyles)&&RegExp.$1,m.push(RegExp.$2&&g(RegExp.$2))),n=j.split(","),o=n.length;for(var p=0;o>p;p++)k=n[p],l.push({media:k.split("(")[0].match(c.regex.only)&&RegExp.$2||"all",rules:m.length-1,hasquery:k.indexOf("(")>-1,minw:k.match(c.regex.minw)&&parseFloat(RegExp.$1)+(RegExp.$2||""),maxw:k.match(c.regex.maxw)&&parseFloat(RegExp.$1)+(RegExp.$2||"")})}u()},w=function(){if(d.length){var b=d.shift();f(b.href,function(c){v(c,b.href,b.media),o[b.href]=!0,a.setTimeout(function(){w()},0)})}},x=function(){for(var b=0;b<s.length;b++){var c=s[b],e=c.href,f=c.media,g=c.rel&&"stylesheet"===c.rel.toLowerCase();e&&g&&!o[e]&&(c.styleSheet&&c.styleSheet.rawCssText?(v(c.styleSheet.rawCssText,e,f),o[e]=!0):(!/^([a-zA-Z:]*\/\/)/.test(e)&&!r||e.replace(RegExp.$1,"").split("/")[0]===a.location.host)&&("//"===e.substring(0,2)&&(e=a.location.protocol+e),d.push({href:e,media:f})))}w()};x(),c.update=x,c.getEmValue=t,a.addEventListener?a.addEventListener("resize",b,!1):a.attachEvent&&a.attachEvent("onresize",b)}}(this);

}