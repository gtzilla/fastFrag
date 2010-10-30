/*
    name : fastfrag
    file : jquery.fastfrag.js
    http://unlicense.org/
    author: gregory tomlinson
    ///////////////////////////
    ///////////////////////////        
    dependencies : jQuery 1.4.2
    ///////////////////////////
    ///////////////////////////
    
    
    This isn't really needed, but written for people who really want to be lazy (like me ;)
        
*/

(function(){
    /*
            fastFrag
                Turn JSON into HTML, http://github.com/gregory80/fastFrag
    */

    var fastFrag = {
        create : function( params ) {
            return drawHTML(params);
        },
        version : "1.1"

    };
    window.fastFrag = fastFrag;

    var d = document;

    function drawHTML( params ) {
        var frag = d.createDocumentFragment(), k, el;
        if(params && params.length === undefined) {
            el = _singleNode( params );
            frag.appendChild( el );
        } else {
            for(k in params) {
                el = _singleNode( params[k] );
                frag.appendChild( el );
            }
        }
        return frag;
    }

    function _mke(elem) {
        return document.createElement( elem );
    }
    function _mke_attribute( el, attrs ) {
        var safe_value;
        for(var k in attrs) { 
            // yuck
            if(k === "disabled" && !attrs[k]) { continue; }
            el.setAttribute(k, _safe( attrs[k] ) );                                         
        }
        return el;
    }
    function _make_element( o ) {
        var el_name, el;
        el_name = o.type || "div";
        el = _mke( el_name );
        if(o.attributes || o.attr || o.attrs) { _mke_attribute( el, o.attributes || o.attr  || o.attrs ); }
        el.id = (o.id) ? o.id : null;  el.className = (o.css) ? o.css : null;
        return el;
    }
    function _safe( string ) {
        return (d.createTextNode(string).nodeValue).toString();  // put in a text node, then grab it
    }
    function _process_node( o ) {
        var txt=null, content_type = typeof o.content, txt_value;
        if( content_type === "object") {
            txt = drawHTML( o.content );
        } else if(content_type === "string") {
            txt = d.createTextNode( o.content );
        } else {
            txt_value = (o.content !== undefined) ? (o.content.toString() || "")  : "";
            txt = d.createTextNode( txt_value );
        }
        return txt        
    }
    function _singleNode( o ) {
        var frag = d.createDocumentFragment(), el, txt;
        if( o.text !== undefined ) {
            el = d.createTextNode( o.text || "" );
        } else {
            el = _make_element( o );
            txt = _process_node( o );                                            
            try{
                el.appendChild( txt );                        
            } catch(e){}
        }
        
        if(el){ frag.appendChild(el); }
        return frag;
    }
})();


(function($) {
    
    $.fn.fastfrag = function( frag_json, options ) {
        // extend the defaults settings
        var el = this, o = $.extend(true, defaults, options);
        if(o.overwrite){ this.html('') }
        this.each(function(idx,elem){
            $(elem).append( fastFrag.create( frag_json ) );
        });
        return this;

    }
    
    var defaults = {
        overwrite : true
    };
    
    
    
    
    
})(jQuery);



