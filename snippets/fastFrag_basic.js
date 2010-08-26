/* 'list' tab triggered  */
{
    type : "ul",
    css : "${1:ul_list}",
    content : [{
       type : "li",
       content : {
           type : "a",
           content : "${2:my link}",
           attributes : {
               href : "#"
           }
       } 
    },{
        type : "li",
        content : {
            type : "a",
            content : "${3:my link}",
            attributes : {
                href : "#"
            }
        }        
    }]
}

/*   'link' -- tab triggers  */
{
    type : "a",
    css : "${1:myClass}",
    content : "${2:'my content'}"
    attributes : {
        href : "${3:#}"
    }
}

/* input  */

{
    type : "input",
    id : "${2:some_name}",
    attributes : {
        type : "${1:submit/text/hidden/checkbox/radio}",
        name : "${2:some_name}",
        value : "${3:some_value}"     
    }
}