odoo.define('bi_general_ledger_filter.bi_general_ledger_filter_custom', function (require) {
'use strict';

var core = require('web.core');
var Widget = require('web.Widget');
var ControlPanelMixin = require('web.ControlPanelMixin');
var Dialog = require('web.Dialog');
var framework = require('web.framework');
var crash_manager = require('web.crash_manager');
var ActionManager = require('web.ActionManager');
var datepicker = require('web.datepicker');
var session = require('web.session');
var field_utils = require('web.field_utils');
var account_report_generic = require('account_reports.account_report');

var QWeb = core.qweb;
var _t = core._t;

account_report_generic.include({
	render_searchview_buttons: function() {
	    var self = this;
	    this._super.apply(this, arguments);

        this.$searchview_buttons.find('.o_account_reports_add_account_filter_auto_complete').select2();
        self.$searchview_buttons.find('[data-filter="custom_account_ids"]').select2("val", self.report_options.custom_account_ids);
        self.$searchview_buttons.find('[data-filter="custom_account_type_ids"]').select2("val", self.report_options.custom_account_type_ids);
        this.$searchview_buttons.find('.o_account_reports_add_account_filter_auto_complete').on('change', function(){
            self.report_options.custom_account_ids = self.$searchview_buttons.find('[data-filter="custom_account_ids"]').val();
            self.report_options.custom_account_type_ids = self.$searchview_buttons.find('[data-filter="custom_account_type_ids"]').val();
            return self.reload().then(function(){
                self.$searchview_buttons.find('.bi_account_filter').click();
            })
        });

        },

});

});
