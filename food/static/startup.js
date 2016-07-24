function add_ingredient() {
  $.ajax($.urls.add_ingredient, {
    success: function(data) {
      $('#new-ingredient').before(data).remove();
    },
    error: function(xhr, status, error) {
      alert(error);
    }
  });
}

function updatePlannedFood($this, food_id, $to_remove) {
  var plan_id = $this.attr('plan-id');
  var meal = $this.attr('meal');
  var date = $this.attr('for-date');
  var args = {
    planned_food: food_id,
    plan_id: plan_id,
    meal: meal,
    date: date
  };
  $.ajax($.urls.plan_food, {
    data: args,
    success: function(data) {
      var $new_div = $('<div class="food-item"></div>');
      $new_div.append(data);
      $to_remove.parent().after($new_div);
      $to_remove.remove();
    },
    error: function(xhr, status, error) {
      alert(error);
    }
  });
}

$(document).ready(function() {

$('#add_dose_button').click(function() {
  $('#add_dose_form').dialog('open');
});

$('#add_dose_form').dialog({
  autoOpen: false,
  height: 250,
  width: 350,
  modal: true,
  buttons: {
    "Create dose": function() {
      link = $.urls.create_dose;
      $dialog = $(this);
      args = {
        amount: $('#id_amount').val(),
        measure: $('#id_measure').val()
      };
      $.ajax(link, {
        data: args,
        async: false,
        success: function(data) {
          $dialog.dialog("close");
          $('#id_dose').parent().html(data);
        },
        error: function(xhr, status, error) {
          $dialog.dialog("close");
          alert('error!');
        }
      });
    },
    Cancel: function() {
      $(this).dialog("close");
    }
  },
  close: function() {
    $('#id_amount').val("");
    $('#id_measure').val("");
  }
});

$('#food-calendar').on('change', '.plan-food-select', function() {
  var $this = $(this);
  var food_id = $this.find(':selected').attr('value');
  updatePlannedFood($this, food_id, $this);
});

$('#food-calendar').on(
  'selectChoice',
  '.plan-food-autocomplete',
  function(e, choice, autocomplete) {
    var $this = $(this);
    var $to_remove = $this.parent();
    var food_id = choice.attr('data-value');
    updatePlannedFood($this, food_id, $to_remove);
  }
);

});
