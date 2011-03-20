// 
//  fraglet.js
//  fastFrag
//  
//  Created by gregory tomlinson on 2011-03-20.
//  Copyright 2011 the public domain. All rights reserved.
//          requires fastFrag 1.1.3.1
/*
    filename : fraglet.js
    http://unlicense.org/
    author: gregory tomlinson
    Sun Mar 20 10:10:16 EDT 2011
*/

(function(global_frame) {
    var fraglet,F,_F,__ns={}; // declare, don't set
    
    fraglet =  {
        update : function( key ) {

        },
        init : function( key ) {
            if(! __ns[key]) { __ns[key]=new F( key ); }
            var ns=__ns[key];
            //tmplte.add()
        },
        t : function( key, action, payload ) {
            if(! __ns[key]) { __ns[key]=new F( key ); }
            var ns=__ns[key];
            ns[action].apply( ns, payload );
            console.log(ns)
        },
        r : function( key, el ) {
            if(! __ns[key]) { __ns[key]=new F( key ); }   
            var ns=__ns[key];
            el.appendChild( fastFrag.create( ns.__t  ) ); 
        },
        render : function(el, frag, opts) {
            var type = typeof el, ns=opts&opts.ns || null, item;
            if( type.toLowerCase === "object" ) {
                
            } else if (type.toLowerCase === "string") {
                
            } else {
                // this is an actual dom element??
            }
            if(ns) {
                item=__ns[ns]
            } else {
               item=el.appendChild( fastFrag.create(frag) );
            }
        }
    };
    
    F=function( ns ){
        this.__t=[];
        this.ns=ns;
    };
    
    F.prototype={
        // commands?? like a string of things to do??
        //
        append : function( frag_item, opts ) {
            this.__t.push( frag_item  );
            // I want to add
            // opts.events
            // there are FUNCTIONS, and I attach them to the 'this' object
            
        },
        css : function( opts, set ) {
            var type=typeof opts;
            // if(type.toLowerCase() === "string") {
            //     
            // }
        },
        extend : function() {
            // which element to extend??
        },
        extend_all : function() {
            // 
            var f,i;
            for(i=0;i<this.__t.length; i++) {
                f=this.__t[i];
            }
        },
        
        /// this is neat..
        simple_list : function( type, data, opts ) {
            console.log(this)
            var frag, i=0, items=[], f_items=[], wrapper_type="ul";
            for( ; i<data.length; i++) {
                frag = {
                    'type' : type,
                    'c' : data[i]
                }
                items.push(frag)
            }
            f_items=items;
            if(type.toLowerCase() !== "li") {  wrapper_type="div"; }
            f_items={ 
                'c' : items,
                'type' : wrapper_type
            };
            this.__t.push(f_items);
        },
        
        find : function() {
            
        }
    }
    
    global_frame['fraglet'] = fraglet;
        
})(this);