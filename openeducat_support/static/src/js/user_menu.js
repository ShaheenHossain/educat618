odoo.define('web_user_menu', function(require) {
    "use strict";

    var UserMenu = require('web.UserMenu');

    UserMenu.include({
        on_menu_documentation: function() {
            window.open('http://www.eagle-it-services.com/', '_blank');
        },
        on_menu_support: function() {
            window.open('https://www.eagle-it-services.com', '_blank');
        },
        on_menu_account: function() {
            window.open('https://wwww.eagle-it-services.com', '_blank');
        },
    });
});
