$(document).ready(function() {
  // page is now ready, initialize the calendar...
  $('#calendar').fullCalendar({
    // put your options and callbacks here
    events: '/schedules',
    eventClick: function(calEvent, jsEvent, view) {
      console.log('Event: ' + calEvent.id);
      console.log('Event: ' + calEvent.title);
      console.log('Event: ' + calEvent.start);
      console.log('Event: ' + calEvent.end);
      delete_schedule(calEvent.id);
    }
  });
});

function add_schedule() {
  $('.ui.add.modal').modal('show');
};

function delete_schedule(schedule_id) {
  $('.ui.delete.modal').modal({
    closable: false,
    onDeny: function() {
    },
    onApprove: function() {
      $.ajax({
  			"url" : '/schedule/' + schedule_id,
  			"type" : "DELETE",
        "success": function() {
          window.location.reload(true);
        }
  		});
    }
  }).modal('show');
};
