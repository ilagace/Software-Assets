var startTime;
var totalTime = 0;
var Timer;
var IETimer;
var realTime = 0;
var javaTime = 0;
var timeCorr = 0;
var slideIndex = 0;
var i;
var slides = document.getElementsByClassName("mySlides");
for (i = 1; i < slides.length; i++) {
    slides[i].style.display = "none";
}
slides[0].style.display = "block";

var smilaudio = document.getElementById("smilaudio");

smilaudio.onplay = function() {
    restart();
};
smilaudio.onseeking = function() {
    seekdisplay();
    showSlides(true);  // need to clear timer
    clearTimeout(IETimer);
    IETimer = setTimeout(IEonplay(), 1000);  // IE does not fire .onplay event after seeking so must generate one via a timer
};
function IEonplay() {
    restart();
};
smilaudio.onpause = function() {
    showSlides(true);  // need to clear timer
};

function restart() {
    totalTime = 0;
    timeCorr = 0;
    javaTime = 0;
    for (i = 0; i < timing.length; i++) {
        if (totalTime > smilaudio.currentTime) {
            slideIndex = i - 1;
            timeCorr = Math.round((totalTime - timing[i-1] - smilaudio.currentTime) * 1000);
            startTime = new Date();
            showSlides(false);
            i = timing.length;
        } else {
            totalTime += timing[i];
        }
    }
}

function seekdisplay() {
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    totalTime = 0;
    timeCorr = 0;
    for (i = 0; i < timing.length; i++) {
        if (totalTime > smilaudio.currentTime) {
            slides[i-1].style.display = "block";
            i = timing.length;
        } else {
            totalTime += timing[i];
        }
    }
}

function showSlides(clearFlag) {
    if (smilaudio.seeking || smilaudio.paused || clearFlag) {
        clearTimeout(Timer);
        return;
    } else {
        if (slideIndex > 0) {
            slides[slideIndex-1].style.display = "none";
        }
    }
    if (slideIndex === slides.length) {
        return;
    }
    slideIndex++;
    slides[slideIndex-1].style.display = "block";
    realTime = new Date() - startTime;
    Timer = setTimeout(showSlides, (timing[slideIndex-1] * 1000) - realTime + javaTime + timeCorr); // Change image as per smil file timing
    javaTime += timing[slideIndex-1] * 1000 + timeCorr;
    timeCorr = 0;
}
