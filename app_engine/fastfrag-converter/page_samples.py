

page_samples = {

    
    'two_children' : """{
        "css" : "a_class_name",
        "content" : [{
            "type" : "a",
            "content" : "child one",
            "attrs" : {
                "href" : "http://whatever.com"
            }
        }, {
            "content" : "child two"
        }]
    }""",
    
    
    'link_sample' : """{
        "css" : "mainClass",
        "content" : [{
            "type" : "a",
            "content" : "fastFrag Repo",
            "attrs" : {
                "href" : "http://github.com/gregory80/fastFrag"
            }
        },{
            "text" : " | "
        },{
            "type" : "a",
            "content" : "converter home",
            "attrs" : {
                "href" : "/"
            }
        }]
    }""",    
    

    'script_injection_attack' : """{
        "content": [{
            "attrs": {
                "href": "/"
            }, 
            "content": {
                "text": "fastFrag neat JSON"
            }, 
            "css": "my_class", 
            "type": "a"
        },{ 
            "content" : "<script>alert('pwned');</script>"
        }], 
        "css": "my_class", 
        "id": "my_id"
    }""",
    
    'user_script_execute' : """{
        "content": [{
            "attrs": {
                "href": "/"
            }, 
            "content": {
                "text": "fastFrag neat JSON"
            }, 
            "css": "my_class", 
            "type": "a"
        },{  
            "type" : "script", 
            "content" : "alert('not so pwned');"
        }], 
        "css": "my_class", 
        "id": "my_id"
    }""",
    
    'link_sample' : """{
        "css" : "mainClass",
        "content" : [{
            "type" : "a",
            "content" : "fastFrag Repo",
            "attrs" : {
                "href" : "http://github.com/gregory80/fastFrag"
            }
        },{
            "text" : " | "
        },{
            "type" : "a",
            "content" : "converter home",
            "attrs" : {
                "href" : "/"
            }
        }]
    }""",


}