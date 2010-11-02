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
    
    
    var stash_string = null;
    
    function display_frags( target_el, json_data ) {
        var frag_sample = json_data,
            frag_items=[{ type : "option", content : "fastFrag JSON Samples", attrs : { value : "" }  }]
            
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
        $( target_el  ).prepend( fastFrag_response );
        $('#samples_select').bind('change', function(e) {
            e.preventDefault();
            if(e.target.value && e.target.value !== "") {
                //console.log( "show this", e.target.value, frag_sample[ e.target.value  ] );
                // todo, stash what's currently in there, add an option 'stashed'
                var $txt_box = $('#frag_text_output');
                var curr_display_value = $txt_box.val();
                
                if( curr_display_value !== "" && stash_string===null) {
                    stash_string = curr_display_value;
                    frag_sample['stashed_value'] = [null, stash_string];
                    var stash_frag = fastFrag.create({
                        type : "option",
                        id : 'stashed_value',
                        content : 'stashed_value',
                        attributes : {
                            name : 'stashed_value',
                            value : 'stashed_value'     
                        }
                    });
                    $(this).append(  stash_frag  );
                }
                
                $('#frag_text_output').val( frag_sample[ e.target.value  ][1] )
            }
            
            
        })        
    }
        
})();