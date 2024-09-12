odoo.define('your_module_name.MapWidget', function (require) {
    'use strict';

    var AbstractField = require('web.AbstractField');
    var FieldRegistry = require('web.field_registry');

    var MapWidget = AbstractField.extend({
        template: 'MapWidget',

        start: function () {
            this._super();
            this._initializeMap();
        },

        _initializeMap: function () {
            // Ensure Leaflet is loaded
            if (typeof L === 'undefined') {
                console.error("Leaflet library is not loaded!");
                return;
            }

            // Initialize the map
            var map = L.map(this.$el.find('#map')[0]).setView([51.505, -0.09], 13);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);
        },
    });

    FieldRegistry.add('map_widget', MapWidget);
});
