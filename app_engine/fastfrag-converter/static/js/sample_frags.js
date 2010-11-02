/*
    filename : sample_frags
    http://unlicense.org/
    author: gregory tomlinson
    Tue Nov  2 13:10:36 EDT 2010
*/

(function() {
    
    var sample_frags =  {
        
        init : function( target_el, json_data ) {
            display_frags( target_el, json_data  )
        }
    }
    
    window.sample_frags = sample_frags;
    
    function display_frags( target_el, json_data ) {
        var frag_sample = json_data
        console.log( frag_sample );
        
        var frag_items=[{ type : "option", content : "fastFrag JSON Samples", attrs : { value : "" }  }]
        for(var k in frag_sample) {
            frag_items.push({
                type : "option",
                id : k,
                content : k,
                attributes : {
                    name : k,
                    value : k     
                }
            })
        }
        
        var frag_form_structure = {
            type : "select",
            id : "samples_select",
            attributes : {
                name : "samples_select",
            },
            content : frag_items
        }
        // need enry point to pass in div
        var fastFrag_response = fastFrag.create(  { id : "samples_list", type : "form", content : frag_form_structure } );
        $( target_el  ).append( fastFrag_response );
        $('#samples_select').bind('change', function(e) {
            e.preventDefault();
            if(e.target.value && e.target.value !== "") {
                console.log( "show this", e.target.value, frag_sample[ e.target.value  ] );
                // todo, stash what's currently in there, add an option 'stashed'
                $('#frag_text_output').val( frag_sample[ e.target.value  ][1] )
            }
            
            
        })        
    }
        
})();