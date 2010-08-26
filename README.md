
UNLICENSE
----


[unlicense](http://unlicense.org/) 

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>

Original unlicensed with http://sam.zoy.org/wtfpl/


Usage
-------


// element 'type' is always assumed to be a div unless otherwise noted via 'type' attr
    fastFrag.create({
        css : "a_class_name",
        content : "string here"
    })


//returns Document Fragment
    <div class="a_class_name">string here</div>

Get more complex with with nested elements:

    fastFrag.create({
        css : "a_class_name",
        content : [{
            type : "a"
            content : "child one",
            attributes : {
                href : "http://whatever.com"
            }
        }, {
            content : "child two"
        }]
    })

// returns Document Fragment
    <div class="a_class_name">
        <a href="http://whatever.com">child one</a>
        <div>child two</div>
    </div>
    
    
    
// create the below html with fastFrag
    <div class="mainClass">
        <a href="http://github.com/gregory80/fastFrag">Fast Frag Repos</a> | <a href="#">link two</a>
    </div>    
    
    
    
    fastFrag.create({
        css : "mainClass",
        content : [{
            type : "a",
            content : "Fast Frag Repos"
            attributes : {
                href : "http://github.com/gregory80/fastFrag"
            }
        },{
            text : " | "
        },{
            type : "a",
            content : "link two"
            attributes : {
                href : "#"
            }
        }]
    })