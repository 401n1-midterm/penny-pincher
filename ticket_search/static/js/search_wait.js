let dateFrom;
let dateTo;

$("#id_date_from").datepicker({
  disableDates: function (date) {
    const currentDate = new Date();
    date.setHours(0, 0, 0, 0);
    currentDate.setHours(0, 0, 0, 0);
    dateFrom = currentDate;
    if (date >= currentDate) {
      return true;
    } else {
      return false;
    }
  },
  uiLibrary: "bootstrap",
  format: "yyyy-mm-dd",
});

$("#id_date_to").datepicker({
  disableDates: function (date) {
    date.setHours(0, 0, 0, 0);
    dateTo = date;
    if (date >= dateFrom) {
      return true;
    } else {
      return false;
    }
  },
  uiLibrary: "bootstrap",
  format: "yyyy-mm-dd",
});
