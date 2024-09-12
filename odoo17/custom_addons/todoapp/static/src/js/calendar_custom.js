odoo.define('your_module_name.calendar_custom', function (require) {
    'use strict';

    var CalendarView = require('web.CalendarView');
    var core = require('web.core');
    var _t = core._t;

    CalendarView.include({
        _renderView: function () {
            this._super.apply(this, arguments);
            var self = this;
            this.$('.o_calendar_event').each(function () {
                var $event = $(this);
                var color = $event.data('color'); // Get color data attribute
                if (color) {
                    $event.css('background-color', color);
                }
            });
        },
    });
});
