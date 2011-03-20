// 
//  fraglet.js
//  fastFrag
//  
//  Created by gregory tomlinson on 2011-03-19.
//  Copyright 2011 the public domain. All rights reserved.
// 
// A Convience fastFrag template manager thingie
/*
    filename : fraglet.js
    http://unlicense.org/
    author: gregory tomlinson
    Sat Mar 19 18:00:14 EDT 2011
*/

(function(global_frame) {
    
    /*
        opts
            Options
            {
                frag : an existing fastFrag structure
                root : the root element of this fraglet
            }
    */
    
    var F,FragLet=function( name, opts ){
        this.name=name;
        this.frag=opts && opts.frag || null;
        this.root=opts && opts.root || null;
        this.__t;
    }, fraglet = function( name, opts ) {
        // return new F( name, opts );
        return new F(name,opts);
        // no this is bad, then i will have all this little objects every where
        // i am trying to 'MANAGE' this crap, i need to hide..
    }
     /*  
        The ART of Lazy
            methods to handle methods that do stuff.. hooray
     
    */
    fraglet.update=function( _fragLet, name ){
            var anchor;
            if(_fragLet && name) {
                anchor=_fragLet;
                _fragLet.name=name; // this will alter the original
            } else {

                name=_fragLet;
                anchor=this(name);// if no object, create it
            }
            console.log(anchor);
            return anchor;
            // console.log( this( name ) );
    }
    
    /////////////////////
    F=FragLet; // set to the same so the object will say 'Fraglet' not 'F'...
    F.prototype = {
        make : function( type, opts ) {
            console.log("make is called")
        },
        extend : function() {
            //this.__t
        },
        append : function( el, frag ) {
            // el is optional
            if(el && frag) {
                if(!this.root) this.root=el; // default                
            } else if(el) {
                frag=el;
            }
            this.root.append( fastFrag.create( frag  ) );
        },
        draw : function( el, frag ) {
            var r_frag=frag || this.frag;
            el.appendChild( fastFrag.create( r_frag ) );
        },
        draw_all : function(el, frag) {
            var r_frag=frag || this.frag;
            
        }
    }
    
    global_frame['fraglet'] = fraglet;
        
})(this);