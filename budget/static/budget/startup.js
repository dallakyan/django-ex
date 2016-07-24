$(document).ready(function() {

$('.edit_category_budget').editable($.urls.edit_budget, {
  event : "dblclick",
  submitdata : function(value, settings) {
    var subcat_id = $(this).parent().attr('id').split('-')[1];
    var month_id = $(this).attr("month");
    if (typeof month_id == 'undefined' || month_id == false) {
      month_id = $.fn.month.id;
    }
    return {
        subcategory_id : subcat_id,
        month_id : month_id,
        csrfmiddlewaretoken : $.fn.csrf.csrf_token
      }
  }
});

$('.edit-location-expense').editable($.urls.edit_expenses, {
  event : "dblclick",
  submitdata : function(value, settings) {
    var location_id = $(this).attr('location');
    var category_name = $(this).attr('category');
    return {
        location_id : location_id,
        category_name : category_name,
        csrfmiddlewaretoken : $.fn.csrf.csrf_token
      }
  }
});

$('.account-month').each(function () {
  reload_account($(this));
});

$('.account-month').on('click', '.pending-checkbox', function() {
  $this = $(this);
  var transaction_id = $(this).parents('tr').attr('transaction-id');
  var is_pending = $(this).is(':checked');
  var args = {
    transaction_id: transaction_id,
    is_pending: is_pending
  };
  $.ajax($.urls.update_pending, {
    data: args,
    success: function(data) {
      reload_account($this.parents('.account-month'));
    },
    error: function(xhr, status, error) {
      alert(error);
    }
  });
});

$('.account-month').on('click', '.transaction-date div', function() {
  $this = $(this);
  $this.editable($.urls.edit_transaction_date, {
    event: "click",
    submitdata: function(value, settings) {
      var transaction_id = $this.parents('tr').attr('transaction-id');
      return {
          transaction_id : transaction_id,
          csrfmiddlewaretoken : $.fn.csrf.csrf_token
        }
    },
    callback: function() {
      reload_account($this.parents('.account-month'));
    }
  });
});

$('.account-month').on('click', '.transaction-location div', function() {
  $this = $(this);
  $.ajax($.urls.get_location_selector, {
    success: function(data) {
      $this.editable($.urls.edit_transaction_location, {
        event: "click",
        type: 'select',
        submit: 'OK',
        data: data,
        submitdata: function(value, settings) {
          var transaction_id = $this.parents('tr').attr('transaction-id');
          var location_str = $(this).find('select').val();
          var location_id = location_str.rsplit('-', 1)[1];
          $this.attr('location-id', location_id);
          return {
              transaction_id : transaction_id,
              location_id : location_id,
              csrfmiddlewaretoken : $.fn.csrf.csrf_token
            }
        },
      });
    },
    error: function(xhr, status, error) {
      alert(error);
    }
  });
});

$('.account-month').on('click', '.add-transaction a', function(e) {
  e.preventDefault();
  $this = $(this);
  var account_id = $this.parents('.account-month').attr('account-id');
  var args = {
    account_id: account_id
  };
  $.ajax($.urls.add_transaction_form, {
    data: args,
    success: function(data) {
      open_transaction_dialog(data,
                              $this.parents('.account-month'),
                              "Add transaction");
    },
    error: function(xhr, status, error) {
      alert(error);
    }
  });
});

$('.account-month').on('click', '.edit-transaction a', function(e) {
  e.preventDefault();
  $this = $(this);
  var account_id = $this.parents('.account-month').attr('account-id');
  var transaction_id = $this.parents('tr').attr('transaction-id');
  var args = {
    account_id: account_id,
    transaction_id: transaction_id
  };
  $.ajax($.urls.add_transaction_form, {
    data: args,
    success: function(data) {
      open_transaction_dialog(data,
                              $this.parents('.account-month'),
                              "Edit transaction");
    },
    error: function(xhr, status, error) {
      alert(error);
    }
  });
  return false;
});

$('.subcategory').on('click', 'a', function(e) {
  e.preventDefault();
  $this = $(this);
  if (typeof $.fn.month === 'undefined') {
    var month_id = $this.parents('td').attr('month');
  } else {
    var month_id = $.fn.month.id;
  }
  var subcat_id = $this.parents('.subcategory').attr('subcategory-id');
  var subcat_name = $this.parents('.subcategory').attr('subcategory-name');
  var args = {
    month_id: month_id,
    subcategory_id: subcat_id
  };
  $.ajax($.urls.subcategory_transactions, {
    data: args,
    success: function(data) {
      open_info_dialog(data, subcat_name + " transactions");
    },
    error: function(xhr, status, error) {
      alert(error);
    }
  });
  return false;
});

$('body').on('blur', '#transaction-dialog #id_amount', function(e) {
  var value = $(this).val();
  $('#transaction-dialog #id_expensecategory_set-0-amount').val(value);
});

$('#add_location a').click(function(e) {
  e.preventDefault();
  $('#add_location_form').dialog('open');
  return false;
});

$('#id_location_name').on('keyup keypress', function(e) {
  var code = e.keyCode || e.which;
  if (code  == 13) {
    e.preventDefault();
    return false;
  }
});

$('#add_location_form').dialog({
  autoOpen: false,
  height: 250,
  width: 350,
  modal: true,
  buttons: {
    "Add Location": function() {
      link = $.urls.add_location;
      $dialog = $(this);
      args = {
        name: $('#id_location_name').val(),
      };
      $.ajax(link, {
        data: args,
        async: false,
        success: function(data) {
          $dialog.dialog("close");
          alert(data);
        },
        error: function(xhr, status, error) {
          $dialog.dialog("close");
          alert('error!');
        }
      });
    },
    "Cancel": function() {
      $(this).dialog("close");
    }
  },
  close: function() {
    $('#id_location_name').val("");
  }
});

$('#recurring-transaction-select').on('change', function(e) {
  var selected = $(this).val();
  if (selected == "add") {
    create_new_recurring_transaction()
  } else if (selected != "-1") {
    get_recurring_transaction_spec(selected, open_recurring_transaction_dialog)
  }
});

});
