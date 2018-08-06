odoo.define('dusal_pos.dusal_pos', function(require) {
  "use strict";

  var gui = require('point_of_sale.gui');
  var models = require('point_of_sale.models');
  var screens = require('point_of_sale.screens');
  var rpc = require('web.rpc');
  var core = require('web.core');
  var _t = core._t;

  models.load_models({
    model: 'res.company',
    fields: ['logo'],
    loaded: function(self, companies) {
      $.each(companies, function() {
        $.extend(self.company || {}, this);
      });
    },
  });

  screens.ReceiptScreenWidget.include({
    render_receipt: function() {
      var self = this;
      this._super();
      var ticketBarcode = $("#ticket-barcode").text().trim();
      $("#ticket-barcode").barcode(ticketBarcode, "code128", {
        'showHRI': false,
        barWidth: 2,
        output: 'bmp'
      });
    },
  });

  var PosModelSuper = models.PosModel;
  models.PosModel = models.PosModel.extend({
    initialize: function(session, attributes) {
      var self = this;
      models.load_fields('product.product',['qty_available']);
      PosModelSuper.prototype.initialize.call(this, session, attributes);

      this.ready.then(function () {
          var domain = [['sale_ok','=',true],['available_in_pos','=',true]];
          rpc.query({
              model: 'product.product',
              method: 'search_read',
              domain: domain,
              fields: ['qty_available'],
              context: {'location': self.config.stock_location_id[0]},
          }).done(function(products) {
            if (products) {
                _.each(products, function(prod){
                    _.extend(self.db.get_product_by_id(prod.id), prod);
                    self.refresh_qty_available(prod);
                });
            }
          });
      });
    },
    get_unit: function(product) {
      var self = this;
      var unit_id = product.uom_id;
      if (!unit_id) {
        return undefined;
      }
      var unit_id0 = unit_id[0];
      if (!self.units_by_id[unit_id0]) {
        return undefined;
      }
      return self.units_by_id[unit_id0];
    },
    refresh_qty_available: function(product) {
      if (this.pos !== undefined) {
        var pos = this.pos;
      } else {
        var pos = this;
      }
      var qty_available_round;
      var $elem = $("span.product[data-product-id='" + product.id + "'] .qty-tag");
      var unit = this.get_unit(product);
      if (unit && unit.rounding) {
        qty_available_round = Math.ceil(Math.log(1.0 / unit.rounding) / Math.log(10));
      }
      if (!qty_available_round) {
        qty_available_round = 2;
      }
      $elem.html(product.qty_available.toFixed(qty_available_round));
      if (product.qty_available <= 0) {
        if (pos.config !== undefined && pos.config.zero_product == "hide") {
          $("span.product[data-product-id='" + product.id + "']").hide();
        } else if (!$elem.hasClass('not-available')) {
          $elem.addClass('not-available');
        }
      }
    },
    push_order: function(order, opts) {
      var self = this;
      var pushed = PosModelSuper.prototype.push_order.call(this, order, opts);
      if (order) {
        order.orderlines.each(function(line) {
          var product = line.get_product();
          product.qty_available -= line.get_quantity();
          self.refresh_qty_available(product);
        });
      }
      return pushed;
    },
    push_and_invoice_order: function(order) {
      var self = this;
      var invoiced = PosModelSuper.prototype.push_and_invoice_order.call(this, order);

      if (order && order.get_client()) {
        if (order.orderlines) {
          order.orderlines.each(function(line) {
            var product = line.get_product();
            product.qty_available -= line.get_quantity();
            self.refresh_qty_available(product);
          });
        } else if (order.orderlines) {
          order.orderlines.each(function(line) {
            var product = line.get_product();
            product.qty_available -= line.get_quantity();
            self.refresh_qty_available(product);
          });
        }
      }

      return invoiced;
    }
  });

  var PosOrderSuper = models.Order;
  models.Order = models.Order.extend({
    add_product: function(product, options) {
      options = options || {};
      if (this.pos !== undefined && this.pos.config.zero_product == "restrict" && product.qty_available < 1) {
        this.pos.gui.show_popup('error', {
          'title': _t('Out of stock'),
          'body': _t('You can not sell this product. This product is currently out of stock.')
        });
        return;
      }

      PosOrderSuper.prototype.add_product.call(this, product, options);
    }
  });


  var PosOrderlineSuper = models.Orderline;
  models.Orderline = models.Orderline.extend({
    initialize: function(attr, options) {
      this.count = true;
      this.category_selected = true;
      this.select = false;
      PosOrderlineSuper.prototype.initialize.call(this, attr, options);
    },
    get_category: function() {
      var product = this.product.pos_categ_id[1];
      return (product ? this.product.pos_categ_id[1] : undefined) || '';
    },
    get_category_id: function() {
      return this.product.pos_categ_id[0];
    },
    set_selected_product: function(count) {
      this.count = count;
      this.trigger('change', this);
    },
    set_selected_category: function(selected) {

      this.category_selected = selected;
      this.trigger('change', this);
    },
    is_selected_product: function() {
      return this.count;
    },
    set_select: function(selected) {
      this.select = selected;
      this.trigger('change', this);
    },
    is_select: function() {
      return this.select;

    },
    is_selected_category: function() {
      return this.category_selected;
    },
  });

  screens.PaymentScreenWidget = screens.PaymentScreenWidget.include({
    validate_order: function(force_validation) {

      if (this.pos.config.max_payment_limit > 0) {
        var currentOrder = this.pos.get('selectedOrder');
        var payment_odds = currentOrder.get_total_paid() - currentOrder.get_total_with_tax();
        if (payment_odds > 0 && this.pos.config.max_payment_limit <= payment_odds) {
          this.gui.show_popup('error', {
            'title': _t('Max limit exceeded!'),
            'body': _t('Please correct payment amount.'),
          });
          return;
        }
      }

      this._super(force_validation);
    },
  });

  screens.NumpadWidget = screens.NumpadWidget.include({
    start: function() {
      var self = this;
      // SuperNumpadWidget.prototype.start.call(self);
      this._super();
      // $('.pos .input-button.amount-char').click(_.bind(this.clickAddAmount, this));
      // $('.pos .input-button.toggle-hidden-buttons').click(_.bind(this.toggleHiddenButtons, this, false));
      // $('.pos .input-button.toggle-hidden-buttons2').click(_.bind(this.toggleHiddenButtons, this, true));
      // var one_clicks = self.pos.config.one_click_pays.split(",");
      // for(i=0; i<one_clicks.length; i++){
      //   $('.pos #one_click_pay' + i).text(one_clicks[i].trim());
      // }
      var replaceButton = '<button class="input-button"></button>';

      if (self.pos.config.hide_discount_button == true) {
        $("button.mode-button[data-mode='discount']").replaceWith(replaceButton);
      }

      if (self.pos.config.hide_price_button == true) {
        $("button.mode-button[data-mode='price']").replaceWith(replaceButton);
      }


    },
    // clickAddAmount: function(event) {
    //     var Amount;
    //     Amount = event.currentTarget.innerText || event.currentTarget.textContent;
    //     if(Amount.indexOf("k") > -1) {
    //       Amount = Amount.replace("k", "");
    //       Amount = parseInt(Amount) * 1000;
    //     } else {
    //       Amount = parseInt(Amount);
    //     }
    //     return this.state.appendAmountToTotal(Amount);
    // },
    // toggleHiddenButtons: function(more, event) {
    //   if(more) {
    //     $('.pos div.numpad-hidden-buttons2').toggleClass("oe_hidden");
    //   } else {
    //     $('.pos div.numpad-hidden-buttons').toggleClass("oe_hidden");
    //   }
    // },
  });

  screens.ProductScreenWidget = screens.ProductScreenWidget.include({
    show: function(reset) {
      var self = this;
      this._super();

      if (self.pos.config.zero_product == "hide") {
        $("span.product .not-available").parents('span.product').hide();
      }
    },
  });

});
