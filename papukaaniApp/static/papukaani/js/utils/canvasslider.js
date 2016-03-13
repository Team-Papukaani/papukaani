function CanvasSlider(uilayer, lineslayer, backgroundlayer) {

    var uilayer = document.getElementById(uilayer);
    var uilayerCtx = uilayer.getContext('2d');
    var lineslayer = document.getElementById(lineslayer);
    var lineslayerCtx = lineslayer.getContext('2d');
    var backgroundlayer = document.getElementById(backgroundlayer);
    var backgroundlayerCtx = backgroundlayer.getContext('2d');

    var lineHeight = 30; // line height in pixels

    var lines = [];
    var min, max;

    function add(line) {
        lines.push(line);
    }

    function remove(id) {
        for (var i = 0; lines.length; i++) {
            if (lines[i].id === id) {
                lines.splice(i, 1);
                break;
            }
        }
        if (lines.length === 0) {
            // all lines removed. Do cleanup
            clear(lineslayer);
        }
    }

    function draw(newMin, newMax) {
        min = newMin;
        max = newMax;
        drawLines();
    }

    function drawLines() {
        clear(lineslayer);
        for (var i = 0; i < lines.length; i++) {
            lineslayerCtx.fillStyle = lines[i].color;
            lineslayerCtx.fillRect(0, lineHeight * i, lineslayer.width, lineHeight);
        }
    }

    function clear(canvas) {
        canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
    }

    return {
        add: add,
        remove: remove,
        draw: draw
    }

}
