function CanvasSlider(container, uilayer, lineslayer, backgroundlayer) {

    var container = $("#" + container);
    var uilayer = document.getElementById(uilayer);
    var uilayerCtx = uilayer.getContext('2d');
    var lineslayer = document.getElementById(lineslayer);
    var lineslayerCtx = lineslayer.getContext('2d');
    var backgroundlayer = document.getElementById(backgroundlayer);
    var backgroundlayerCtx = backgroundlayer.getContext('2d');

    var lineHeight = 12; // line height in pixels
    var offset = 5; // offset from top and bottom

    var lines = [];
    var min, max, minLength;

    var birdiesDiv = $("#birdies");

    resize(true);

    $(window).resize(function () {
        resize(true);
    });

    function add(line) {
        lines.push(line);
    }

    function remove(id) {
        for (var i = 0; lines.length; i++) {
            if (lines[i].id === id) {
                lines.splice(i, 1);
                drawLines();
                return;
            }
        }
    }

    function draw(newMin, newMax) {
        min = newMin;
        max = newMax;
        drawLines();
    }

    function drawLines() {
        clear(lineslayer);
        if (birdiesDiv.height() > 80 && birdiesDiv.height() != container.height()) {
            container.height(birdiesDiv.height());
            resize(false);
        }
        for (var i = 0; i < lines.length; i++) {

            var line = calculatePosition(datetimestringToUnixtime(lines[i].start), datetimestringToUnixtime(lines[i].end), lineslayer);
            lineslayerCtx.fillStyle = lines[i].color;
            var currentLinePosY = offset + (lineHeight + 2 * offset) * i;
            lineslayerCtx.fillRect(line[0], currentLinePosY, line[1] - line[0], lineHeight);
        }
    }

    function resize(redraw) {
        var width = container.width();
        var height = container.height();
        uilayer.width = width;
        uilayer.height = height;
        lineslayer.width = width;
        lineslayer.height = height;
        backgroundlayer.width = width;
        backgroundlayer.height = height;
        minLength = Math.ceil(width / 100.0);
        if (redraw) {
            drawLines();
        }
    }

    function clear(canvas) {
        canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
    }

    function calculatePosition(timeA, timeB, canvas) {

        var length = parseFloat(max - min);

        if (length <= 0) return [0, canvas.width]; // timeline length is zero

        timeA -= min;
        timeB -= min;

        var a = Math.min(Math.ceil(timeA / length * canvas.width), canvas.width);
        var b = Math.min(Math.ceil(timeB / length * canvas.width), canvas.width);

        if (b - a < minLength) { // only one datapoint. set minimum length for line.
            b = a + minLength;
        }
        if (a == canvas.width) { // left edge is at the right end of the canvas
            a -= minLength;
            b -= minLength;
        }

        return [a, b];
    }

    return {
        add: add,
        remove: remove,
        draw: draw
    }

}