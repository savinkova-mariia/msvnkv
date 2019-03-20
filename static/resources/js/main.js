(function blogNamespace(){

    function onReady(payload){
        if (document.attachEvent ? document.readyState === "complete" : document.readyState !== "loading"){
            payload();
        } else {
            document.addEventListener('DOMContentLoaded', payload);
        }
    }

    function scaleProjectTitles() {
        let headings = document.querySelectorAll('.project__heading');
        Array.prototype.forEach.call(headings, function(el, i){
            let length = el.textContent.length;

            let fontSize = 25;

            if (length < 12) {
                fontSize = 70;
            } else if (length < 24) {
                fontSize = 50;
            } else if (length < 48) {
                fontSize = 30;
            }

            el.style.fontSize = fontSize + 'px';
        });
    }

    function init() {
        scaleProjectTitles();
    }

    onReady(init);
})();
