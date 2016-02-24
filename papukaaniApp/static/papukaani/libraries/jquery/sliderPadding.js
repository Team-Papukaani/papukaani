(function ($, undefined) {
    $.ui.slider.prototype.options =
        $.extend(
            {},
            $.ui.slider.prototype.options,
            {
                paddingMin: 0,
                paddingMax: 0
            }
        );

    $.ui.slider.prototype._refreshValue =
        function () {
            var
                oRange = this.options.range,
                o = this.options,
                self = this,
                animate = ( !this._animateOff ) ? o.animate : false,
                valPercent,
                _set = {},
                elementWidth,
                elementHeight,
                paddingMinPercent,
                paddingMaxPercent,
                paddedBarPercent,
                lastValPercent,
                value,
                valueMin,
                valueMax;

            if (self.orientation === "horizontal") {
                elementWidth = this.element.outerWidth();
                paddingMinPercent = o.paddingMin * 100 / elementWidth;
                paddedBarPercent = ( elementWidth - ( o.paddingMin + o.paddingMax) ) * 100 / elementWidth;
            }
            else {
                elementHeight = this.element.outerHeight();
                paddingMinPercent = o.paddingMin * 100 / elementHeight;
                paddedBarPercent = ( elementHeight - ( o.paddingMin + o.paddingMax) ) * 100 / elementHeight;
            }

            if (this.options.values && this.options.values.length) {
                this.handles.each(function (i, j) {
                    valPercent =
                        ( ( self.values(i) - self._valueMin() ) / ( self._valueMax() - self._valueMin() ) * 100 )
                        * paddedBarPercent / 100 + paddingMinPercent;
                    _set[self.orientation === "horizontal" ? "left" : "bottom"] = valPercent + "%";
                    $(this).stop(1, 1)[animate ? "animate" : "css"](_set, o.animate);
                    if (self.options.range === true) {
                        if (self.orientation === "horizontal") {
                            if (i === 0) {
                                self.range.stop(1, 1)[animate ? "animate" : "css"]({left: valPercent + "%"}, o.animate);
                            }
                            if (i === 1) {
                                self.range[animate ? "animate" : "css"]({width: ( valPercent - lastValPercent ) + "%"}, {
                                    queue: false,
                                    duration: o.animate
                                });
                            }
                        } else {
                            if (i === 0) {
                                self.range.stop(1, 1)[animate ? "animate" : "css"]({bottom: ( valPercent ) + "%"}, o.animate);
                            }
                            if (i === 1) {
                                self.range[animate ? "animate" : "css"]({height: ( valPercent - lastValPercent ) + "%"}, {
                                    queue: false,
                                    duration: o.animate
                                });
                            }
                        }
                    }
                    lastValPercent = valPercent;
                });
            } else {
                value = this.value();
                valueMin = this._valueMin();
                valueMax = this._valueMax();
                valPercent =
                    ( ( valueMax !== valueMin )
                        ? ( value - valueMin ) / ( valueMax - valueMin ) * 100
                        : 0 )
                    * paddedBarPercent / 100 + paddingMinPercent;

                _set[self.orientation === "horizontal" ? "left" : "bottom"] = valPercent + "%";

                this.handle.stop(1, 1)[animate ? "animate" : "css"](_set, o.animate);

                if (oRange === "min" && this.orientation === "horizontal") {
                    this.range.stop(1, 1)[animate ? "animate" : "css"]({width: valPercent + "%"}, o.animate);
                }
                if (oRange === "max" && this.orientation === "horizontal") {
                    this.range[animate ? "animate" : "css"]({width: ( 100 - valPercent ) + "%"}, {
                        queue: false,
                        duration: o.animate
                    });
                }
                if (oRange === "min" && this.orientation === "vertical") {
                    this.range.stop(1, 1)[animate ? "animate" : "css"]({height: valPercent + "%"}, o.animate);
                }
                if (oRange === "max" && this.orientation === "vertical") {
                    this.range[animate ? "animate" : "css"]({height: ( 100 - valPercent ) + "%"}, {
                        queue: false,
                        duration: o.animate
                    });
                }
            }
        };

    $.ui.slider.prototype._normValueFromMouse =
        function (position) {
            var
                o = this.options,
                pixelTotal,
                pixelMouse,
                percentMouse,
                valueTotal,
                valueMouse;

            if (this.orientation === "horizontal") {
                pixelTotal = this.elementSize.width - (o.paddingMin + o.paddingMax);
                pixelMouse = position.x - this.elementOffset.left - o.paddingMin - ( this._clickOffset ? this._clickOffset.left : 0 );
            } else {
                pixelTotal = this.elementSize.height - (o.paddingMin + o.paddingMax);
                pixelMouse = position.y - this.elementOffset.top - o.paddingMin - ( this._clickOffset ? this._clickOffset.top : 0 );
            }

            percentMouse = ( pixelMouse / pixelTotal );
            if (percentMouse > 1) {
                percentMouse = 1;
            }
            if (percentMouse < 0) {
                percentMouse = 0;
            }
            if (this.orientation === "vertical") {
                percentMouse = 1 - percentMouse;
            }

            valueTotal = this._valueMax() - this._valueMin();
            valueMouse = this._valueMin() + percentMouse * valueTotal;

            return this._trimAlignValue(valueMouse);
        };
})(jQuery);