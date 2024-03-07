odoo.define('school.demo_js', function (require) {
    'use strict';

    var FormController = require('web.FormController');
    var core = require('web.core');
    var _t = core._t;

    FormController.include({
        events: _.extend({}, FormController.prototype.events, {
            'click .oe_highlight': 'onDownloadButtonClick',
        }),

        start: function () {
            this._super.apply(this, arguments);

            // Additional initialization code if needed
        },

        onDownloadButtonClick: function (event) {
            // Your custom logic when the button is clicked
            console.log("anil");
        },
    });
});
