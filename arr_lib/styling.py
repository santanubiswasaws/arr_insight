
BUTTON_STYLE="""
    <style>
    div.stButton > button:first-child {
        background-color: #eeeeee;
        color: #666666;
        height: 2em;
        border-radius:6px;
        border:1px solid #aaaaaa;
        font-size:14px;
        font-weight: bold;
        margin: auto;
        display: grey;
    }

    div.stButton > button:hover {
        background-color:#dddddd;
    }

    div.stButton > button:active {
        background-color:#fefefe;
    }
                                    
    </style>"""


GLOBAL_STYLING = """
<style>
.title:after{
    content: 'TEST';
    }

.title{
    content: 'TEST';
    }
.StatusWidget-enter{
    visibility: hidden;
}

.StatusWidget-exit{
    visibility: hidden;
}

.StatusWidget-exit-done{
    visibility: hidden;
}


.stStatusWidget{
    visibility: hidden;
}
.stStatusWidget>div{
    visibility: hidden;
}
.stStatusWidget>div>img{
    visibility: hidden;
}
.stStatusWidget>div>label{
    visibility: hidden;
}
.stStatusWidget>div>span{
    visibility: hidden;
}

.stToolbar{
    visibility: None;
}
</style>
"""