
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
body {
  /*background: #353535; */
  line-height: 1.2rem;
}

.stActionButton {
    visibility: hidden;

}

.stDeployButton {
    visibility: hidden;
}

/* Form */
.css-1h109da{
    border: none;
    padding: 0px;
    margin:0px;
    margin-bottom:3px;
}

.StatusWidget-enter-done{
    visibility: hidden;
}

.StatusWidget-enter-active{
    visibility: hidden;
}

.StatusWidget-exit-active{
    visibility: hidden;
}

.title:before{
content: 'TEST';
}

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


.stActionButton{
    visibility: None;
}



.loader,
.loader:after {
  border-radius: 50%;
  width: 2rem;
  height: 2rem;
}
.loader {
  font-size: 10px;
  position: relative;
  /* text-indent: -9999em; */
  border-top: 0.3em solid rgba(255, 255, 255, 0.2);
  border-right: 0.3em solid rgba(255, 255, 255, 0.2);
  border-bottom: 0.3em solid rgba(255, 255, 255, 0.2);
  border-left: 0.3em solid #a2aab0;
  -webkit-transform: translateZ(0);
  -ms-transform: translateZ(0);
  transform: translateZ(0);
  -webkit-animation: load8 1.1s infinite linear;
  animation: load8 1.1s infinite linear;
}
@-webkit-keyframes load8 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}
@keyframes load8 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}


/* Multi Select */
.stMultiSelect>label{
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #00B7C2;
    position: absolute;
    left: 0%;
    height: 100%;
    padding: 0.31rem;
    border-bottom-left-radius: 4px;
    border-top-left-radius: 4px;
    z-index:1;
    min-width: 5.5rem;
    text-align: center;
    font-size: 14px;

}


.stMultiSelect>div>div>div:first-child{
    position: relative;
    left: 0rem;
    padding: 0rem;
    margin-left: 6rem;
    width: 20rem;
}

.stMultiSelect>div>div:hover{
    border: 2px solid #00B7C2;
}


.stSlider>div>div>div:first-child{
    height: 1rem;
}

.stSlider>div>div>div{
    font-weight: bold;
}

.stSlider>div>div>div>div>div{
    font-weight: bold;
}



.stSlider>div>div>div>div{
    background-color: white;
}

.stSlider>label{
    position: absolute;
    bottom: -10%;
    left: 25%;
    width: 100%;
    z-index: 1;
}


/* TEXT INPUT */
.stTextInput>label{
    background-color: #00B7C2;
    position: absolute;
    left: 0%;
    padding: 0.31rem;
    border-bottom-left-radius: 4px;
    border-top-left-radius: 4px;
    min-width: 5.5rem;
    max-width: 5.5rem;
    height: 100%;
    text-align: center;
    font-size: 14px;
    text-overflow: none;
    z-index: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.st-hu{
    background-color: #00B7C2;
}

.stTextInput>label:hover{
    background-color: #00B7C2;
    position: absolute;
    left: 0%;
    padding: 0.31rem;
    border-bottom-left-radius: 4px;
    border-top-left-radius: 4px;
    min-width: 5.5rem;
    max-width: 100%;
    height: 100%;
    text-align: center;
    font-size: 14px;
    text-overflow: none;
    z-index: 1;
    word-wrap: break-word;
    overflow-wrap: break-word;
}



.stTextInput>div>div>div, .stTextInput>div>div, .stTextInput>div>div>div>input, .stTextInput>div>div>input{
    padding: 0rem;
    max-width: 100%;
}

.stTextInput>div>div>input{
    position: relative;
    right: 0rem;
    padding: 0rem;
    margin-left: 6rem;
}

.stTextInput>div:hover{
    border: 2px solid #00B7C2;
}

.stTextInput>{
    padding: 0rem;
}


.css-15of2nd{
    background-color:whitesmoke;
}

.stTextInput>div{
    padding: 0rem;
}
.stTextInput>div>div>div>div{
    padding: 0rem;
}

/* Select Box */
.stSelectbox>label{
    background-color: #00B7C2;
    position: absolute;
    left: 0%;
    padding: 0.31rem;
    border-bottom-left-radius: 4px;
    border-top-left-radius: 4px;
    z-index:1;
    min-width: 5.5rem;
    height: 100%;
    text-align: center;
    font-size: 14px;;
}

.stSelectbox>div>div>div>div{
    padding: 0rem;
    max-width: 80%;
}

.stSelectbox>div>div>div:first-child{
    padding: 0rem;
    max-width: 80%;
    margin-left: 6rem;
}
.stSelectbox>div>div{
    padding: 0rem;
}

.stSelectbox>div>div:hover{
    border: 2px solid #00B7C2;
}
.stSlider{
    padding-left: 0.8rem;
    padding-right: 0.8rem;
    border-radius: 9px;
}

.css-uokr8j{
    color:whitesmoke;
}
.stTimeInput>div>div{
    padding-bottom:1px;
    padding-top:1px;
}

.stTimeInput>div>div>div{
    padding-bottom:1px;
    padding-top:1px;
}

.stTimeInput>div>div>div>input{
    padding-bottom:1px;
    padding-top:1px;
}

.stDateInput>div>div{
    padding-bottom:1px;
    padding-top:1px;
}

.stDateInput>div>div:hover{
    border: 2px solid #00B7C2;
}


.stDateInput>div>div>div{
    padding-bottom:1px;
    padding-top:1px;
}

.stDateInput{
    margin-top: 1rem;
}

.stDateInput>label{
    position: absolute;
    padding: 0%;
    left: 5%;
    top: -5.5%;
    background-color: #00B7C2;
    padding-right: 0.3rem;
    padding-left: 0.3rem;
    border-top-right-radius: 4px;
    border-top-left-radius: 4px;

}

.stDateInput>div>div>div>input{
    padding-bottom:1px;
    padding-top:1px;
}

/* Input titles */
.effi0qh0{
    padding-bottom: 0rem;
}

.stAlert>div{
    padding: 0.25rem;
    border-radius: 0px 9px 9px 0px;
    border-left-width: 5px;
}


.reportview-container>section:first-child>div>div:nth-child(2)>div>div>div>div>div>img{
    border:none;
    position: sticky;
    margin-top:-28%;
    margin-left: -12%;
}

.reportview-container>section:first-child>div>div:nth-child(2)>div>div>div>button{
    visibility: hidden;
    width: 0px;
    position: absolute;
    right:0px;
}

.reportview-container>section:first-child>div>div:nth-child(2)>div:nth-child(2){
    border: solid whitesmoke 2px;
}


.css-kywgdc{
    background-image:none;
}

.css-zyb2jl{
    color:#8270b3;
}

.generated_download:hover{
    text-decoration: none;
    color:whitesmoke;
}

div>div>div>img{
    border: 3px solid rgba(245, 245, 245, 0.322);
    border-radius: 9px;
    padding: 0.25rem;
}

.css-ggpqvm{
    width:100%;
    font-weight: bold;
}

/* MENU && FOOTER */
#MainMenu {visibility: hidden;}


.StatusWidget-enter-done>div>span{
    visibility:hidden;
}
#bui-2>div>ul>li:nth-child(4), /* Deploy App again? */
#bui-2>div>ul>li:nth-child(8), /* Ask a question */
#bui-2>div>ul>li:nth-child(9), /* Report a bug */
#bui-2>div>ul>li:nth-child(11), /* StreamLit for teams */
#bui-2>div>ul>li:nth-child(13) /* About */{ 
    visibility: hidden;
}

</style>

"""