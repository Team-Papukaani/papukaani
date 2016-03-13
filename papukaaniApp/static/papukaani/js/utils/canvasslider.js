function CanvasSlider(uilayer, lineslayer, backgroundlayer) {

    var uilayer = document.getElementById(uilayer);
    var uilayerCtx = uilayer.getContext('2d');
    var lineslayer = document.getElementById(lineslayer);
    var lineslayerCtx = lineslayer.getContext('2d');
    var backgroundlayer = document.getElementById(backgroundlayer);
    var backgroundlayerCtx = backgroundlayer.getContext('2d');

    var lineHeight = 20; // line height in pixels

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

            var line = calculatePosition(datetimestringToUnixtime(lines[i].start), datetimestringToUnixtime(lines[i].end), lineslayer);
            if (line.length === 0) continue;

            lineslayerCtx.fillStyle = lines[i].color;
            lineslayerCtx.fillRect(line[0], 10 + (10 + lineHeight) * i, line[1], lineHeight);
        }
    }

    function clear(canvas) {
        canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
    }

    function calculatePosition(timeA, timeB, canvas) {
        if (timeA < min && timeB >= min) {
            timeA = min;
        }
        if (timeB > max && timeA <= max) {
            timeB = max;
        }
        if (timeB < min || timeA > max) {
            return [];
        }

        var a = timeA - min;
        var b = timeB - min;

        var length = parseFloat(max - min);
        if (length <= 0) return [0, canvas.width];
        a = Math.floor(a / length * canvas.width);
        b = Math.floor(b / length * canvas.width);
        return [a, b];
    }

    return {
        add: add,
        remove: remove,
        draw: draw
    }

}
