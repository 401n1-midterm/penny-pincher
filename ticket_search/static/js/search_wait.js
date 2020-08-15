let dateFrom;
let dateTo;

const $searchSubmitEl = $("#search_submit");
const $departureCityEl = $("#id_departure_city");
const $arrivalCityEl = $("#id_arrival_city");
const $dateFromEl = $("#id_date_from");
const $dateToEl = $("#id_date_to");
// const $modalEl = $("#modal");

$searchSubmitEl.on("click", () => {
  if (
    $departureCityEl.val() &&
    $arrivalCityEl.val() &&
    $dateFromEl.val() &&
    $dateToEl.val()
  ) {
    $("#modal").modal("show");
  }
});

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
  modal: true,
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
  modal: true,
});
