function changeTextColor(className,SwitchCase) {
    var elems = document.querySelectorAll(className);
    var index = 0, length = elems.length;
    if(SwitchCase === 0) {
        for ( ; index < length-1; index++) {
            elems[index].style.color = "#fff";
            elems[index].style.fontWeight = "700";
        };
    }else{
        for ( ; index < length-1; index++) {
            elems[index].style.color = "#013289";
        };
    }
}

window.onscroll = function(ev) {
    if (window.pageYOffset < 1) {
        document.getElementById("header").style.background = "none";
    }
    else if (window.pageYOffset != 0){
        if (Math.round((window.innerHeight + window.pageYOffset)) >= document.body.offsetHeight) {
            document.getElementById("header").style.background = "#010E21";
            document.getElementById("LogoText").style.color = "#fff"
            //var ss = document.styleSheets[0];
            //ss.insertRule('::-webkit-scrollbar-track {box-shadow: inset 0 0 6px #012970;}', 0);
            changeTextColor(".navbar a",0);
        }
        else{
            document.getElementById("header").style.background = "#fff";
            document.getElementById("LogoText").style.color = "#012970"
            changeTextColor(".navbar a",1);
        }
    }
};

function launch_toast() {
    var x = document.getElementById("toast")
    x.className = "show";
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
}

function delay(callback, ms) {
    var timer = 0;
    return function () {
      var context = this,
        args = arguments;
      clearTimeout(timer);
      timer = setTimeout(function () {
        callback.apply(context, args);
      }, ms || 0);
    };
}
$(document).ready(function () {
    $("#letter").keyup(
        delay(function (e) {
        $.ajax({
            data: $(this).serialize(),
            url: "{% url 'IndexHome:newsletter' %}",
            // on success
            success: function (response) {
            if (response.is_subscribe == true) {
                $("#error").html("Email already subscribed!");
                $(".enableOnInput").prop("disabled", true);
            }else if(response.is_subscribe == "None") {
                $("#error").html("Failed Request");
            }
            else {
                $(".enableOnInput").prop("disabled", false);
                $("#error").html("");
            }
            },
            error: function (response) {
            console.log(response.responseJSON.errors);
            },
        });
        return false;
        }, 500)
    );
});