function dark() {
    
    var bgBody = window.document.querySelectorAll(".bgBody");
    var bgNav = window.document.querySelectorAll(".bgNav");
    var bgWhite = window.document.querySelectorAll(".bgWhite");
    var themabackground = window.document.getElementsByClassName("themabackground");

    if ( themabackground.style.backgroundImage == 'url(../img/sun.svg)') {

        bgBody.style.backgroundColor = "#090909";
        bgNav.style.backgroundColor = "#FFFFFF32";
        bgWhite.style.backgroundColor = "#090909";
        themabackground.style.backgroundImage = "url(../img/moon.svg)";

    }else {

        bgBody.style.backgroundColor = "#f9f9f9";
        bgNav.style.backgroundColor = "#FFFFFF32";
        bgWhite.style.backgroundColor = "#f9f9f9";
        themabackground.style.backgroundImage = "url(../img/sun.svg)";
       
    }
}
 /*talvez n mude a imagem pq esta sendo executado em outro dir*/