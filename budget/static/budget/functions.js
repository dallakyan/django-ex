function reload_account($account_month) {
  $account_month.css('height', $account_month.height());
  $account_month.html("Loading " + $account_month.attr('account-name') + "...");
  $account_month.append('&nbsp;&nbsp;<img src="/static/images/ajax-loader.gif" />');
  var account_id = $account_month.attr('account-id');
  var args = {
    month_id: $.fn.month.id,
    account_id: account_id
  };
  $.ajax($.urls.month_account, {
    data: args,
    success: function(data) {
      $account_month.html(data);
      $account_month.css('height', '');
    },
    error: function(xhr, status, error) {
      alert(error);
    }
  });
}

function validate_transaction($form) {
  console.log('Validating transaction');
  return { valid: true, errors: [] }
}

function submit_transaction($form, $account) {
  data = $form.serialize();
  $.ajax($.urls.add_transaction, {
    data: data,
    type: 'POST',
    success: function(data) {
      reload_account($account);
    },
    error: function(xhr, status, error) {
      alert(error);
    }
  });
}

function open_transaction_dialog(form, $account, title) {
  var $dialog = $('<div id="transaction-dialog"></div>');
  $form = $('<form></form>').html(form).appendTo($dialog);
  $form.append('<input type="submit" value="' + title + '" />');
  $form.append('<input type="hidden" name="csrfmiddlewaretoken" value="'
    + $.fn.csrf.csrf_token + '" />');
  $form.find('#id_date').datepicker({ dateFormat: 'mm/dd/yy' });
  $dialog.dialog({
      autoOpen: false,
      modal: true,
      height: 625,
      width: 600,
      title: title,
      close: function() {
        $dialog.remove();
      }
  });
  $('#transaction-dialog').find('form').submit(function(e) {
    console.log('Submit called');
    var result = validate_transaction($(this));
    if (result.valid) {
      submit_transaction($(this), $account);
      $dialog.dialog('close');
    } else {
      alert(result.errors);
    }
    e.preventDefault();
  });
  $dialog.dialog('open');
}

function open_info_dialog(html, title) {
  var $dialog = $('<div id="info-dialog"></div>');
  $(html).appendTo($dialog)
  $dialog.dialog({
      autoOpen: false,
      modal: true,
      height: 625,
      width: 800,
      title: title,
      close: function() {
        $dialog.remove();
      }
  });
  $dialog.dialog('open');
}

function open_info_dialog(html, title) {
  var $dialog = $('<div id="info-dialog"></div>');
  $(html).appendTo($dialog)
  $dialog.dialog({
      autoOpen: false,
      modal: true,
      height: 625,
      width: 800,
      title: title,
      close: function() {
        $dialog.remove();
      }
  });
  $dialog.dialog('open');
}

function create_new_recurring_transaction() {
  var $dialog = $('<div id="create-recurring-transaction-dialog"></div>');
  $('<div>Enter name: <input type="text" id="recurring-transaction-name"></div>').appendTo($dialog);
  $dialog.dialog({
      autoOpen: false,
      modal: true,
      height: 175,
      width: 300,
      title: "Recurring transaction",
      close: function() {
        var name = $("#recurring-transaction-name").val();
        if (name) {
          $.ajax($.urls.create_recurring_transaction, {
            data: {name: name},
            success: function(data) {
              $dialog.remove();
              get_recurring_transaction_spec(data, open_recurring_transaction_dialog);
            },
            error: function(xhr, status, error) {
              alert(error);
            }
          });
        }
      }
  });
  $('#recurring-transaction-name').keypress(function(e) {
    if (e.which == 13) {
      $dialog.dialog('close');
    }
  });
  $dialog.dialog('open');
}

function get_recurring_transaction_spec(id, callback) {
  $.ajax($.urls.get_recurring_transaction, {
      data: {id: id},
      success: function(data) {
        var transactions = $.parseJSON(data);
        var transactions_html = ""
        transactions_html += '<div>Apply to date:<input type="type" id="apply_to_date_input">'
        transactions_html += '</input><button type="button" id="apply_to_date">'
        transactions_html += 'Apply</button></div>'
        transactions_html += '<div class="recurring-transaction-entries" rte-id="' + id + '">'
        transactions.forEach(function(t) {
          transactions_html += '<div class="recurring-transaction-entry">';
          transactions_html += render_recurring_transaction(t);
          transactions_html += '</div>'
        });
        transactions_html += '</div>'
        transactions_html += '<div><button type="button" id="add_to_recurring_transaction">'
        transactions_html += 'Add Transaction</button></div>'
        transactions_html += '<div><button type="button" id="save_recurring_transaction">'
        transactions_html += 'Save</button></div>'
        callback(transactions_html)
      },
      error: function(xhr, status, error) { alert(error); }
  });
}

function open_recurring_transaction_dialog(transaction_html) {
  var $dialog = $('<div id="recurring-transaction-dialog"></div>');
  $('<div>' + transaction_html + '</div>').appendTo($dialog);
  $dialog.dialog({
      autoOpen: false,
      modal: true,
      height: 625,
      width: 800,
      title: "Recurring transaction",
      close: function() {
        $dialog.remove();
      }
  });
  $dialog.dialog('open');
  $('#add_to_recurring_transaction').click(add_to_recurring_transaction);
  $('#save_recurring_transaction').click(save_recurring_transaction);
  $('#apply_to_date').click(apply_recurring_transaction_to_date);
  $('#apply_to_date_input').datepicker({ dateFormat: 'mm/dd/yy' });
}

function render_recurring_transaction(transaction) {
  $div = $('<div></div>');
  $table = $('<table></table>');
  $table.appendTo($div);
  var account_select = get_account_select(transaction.account)
  $('<tr class="account"><td>Account:</td><td>' + account_select + '</td></tr>').appendTo($table);
  var location_select = get_location_select(transaction.location)
  $('<tr class="location"><td>Location:</td><td>' + location_select + '</td></tr>').appendTo($table);
  var subcategory_select = get_subcategory_select(transaction.subcategory)
  $('<tr class="subcat"><td>Subcategory:</td><td>' + subcategory_select + '</td></tr>').appendTo($table);
  var type_select = get_type_select(transaction.type)
  $('<tr class="type"><td>Type:</td><td>' + type_select + '</td></tr>').appendTo($table);
  var amount_box = get_amount_box(transaction.amount)
  $('<tr class="amount"><td>Amount:</td><td>' + amount_box + '</td></tr>').appendTo($table);
  var note_box = get_note_box(transaction.note)
  $('<tr class="note"><td>Note:</td><td>' + note_box + '</td></tr>').appendTo($table);
  return $div.html();
}

function add_to_recurring_transaction() {
  var html = '<div class="recurring-transaction-entry">';
  html += render_recurring_transaction({});
  html += '</div>'
  $('.recurring-transaction-entries').append(html);
}

function save_recurring_transaction() {
  var transactions = $(".recurring-transaction-entry");
  var jsonStr = JSON.stringify(transactions.map(get_transaction_object).get())
  var id = $(".recurring-transaction-entries").attr("rte-id")
  $.ajax($.urls.save_recurring_transaction, {
    data: {id: id, jsonStr: jsonStr},
    success: function(data) {
      alert(data);
    },
    error: function(xhr, status, error) {
      alert(error);
    }
  });
}

function apply_recurring_transaction_to_date() {
  var id = $(".recurring-transaction-entries").attr("rte-id");
  var date = $("#apply_to_date_input").val();
  $.ajax($.urls.apply_recurring_transaction_to_date, {
    data: {id: id, date: date},
    success: function(data) {
      alert(data);
      $("#recurring-transaction-dialog").dialog("close");
    },
    error: function(xhr, status, error) {
      alert(error);
    }
  });
}

function get_transaction_object(index, element) {
  var transaction = {};
  transaction.account = $(element).find(".account select").val();
  transaction.location = $(element).find(".location select").val();
  transaction.subcategory = $(element).find(".subcat select").val();
  transaction.type = $(element).find(".type select").val();
  transaction.amount = $(element).find(".amount input").val();
  transaction.note = $(element).find(".note input").val();
  return transaction;
}

function get_account_select(account_name) {
  return get_select_box($.fn.json.account_names, account_name);
}

function get_location_select(location_name) {
  return get_select_box($.fn.json.location_names, location_name);
}

function get_subcategory_select(subcat_name) {
  return get_select_box($.fn.json.subcategory_names, subcat_name);
}

function get_type_select(type) {
  var choices = ['Debit', 'Credit'];
  return get_select_box(choices, type);
}

function get_amount_box(amount) {
  return '<input type="text" value="' + amount + '">'
}

function get_note_box(note) {
  return '<input type="text" value="' + note + '">'
}

function get_select_box(options, selected) {
  var select = '<select>';
  options.forEach(function(option) {
    select += '<option value="' + option + '"';
    if (option == selected) {
      select += ' selected="selected"';
    }
    select += '>' + option + '</option>'
  });
  select += '</select>';
  return select;
}
