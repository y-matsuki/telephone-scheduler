function delete_alert(alert_id) {
  $('.ui.delete.modal').modal({
    closable: false,
    onDeny: function() {
    },
    onApprove: function() {
      $.ajax({
  			"url" : '/alert/' + alert_id,
  			"type" : "DELETE",
        "success": function() {
          window.location.reload(true);
        }
  		});
    }
  }).modal('show');
};
