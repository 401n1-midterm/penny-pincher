const $dateFromEl = $("#id_date_from");
const $dateToEl = $("#id_date_to");

const today = new Date(
  new Date().getFullYear(),
  new Date().getMonth(),
  new Date().getDate()
);

const tomorrow = new Date(
  new Date().getFullYear(),
  new Date().getMonth(),
  new Date().getDate() + 1
);

const datePickerOptions = {
  uiLibrary: "bootstrap4",
  iconsLibrary: "fontawesome",
  showOnFocus: true,
  showRightIcon: false,
  format: "yyyy-mm-dd",
  modal: true,
  header: true,
  footer: true,
  minDate: today,
};

// Render DatePickers
datePickerOptions["minDate"] = today;
$("#id_date_from").datepicker(datePickerOptions);

datePickerOptions["minDate"] = tomorrow;
$("#id_date_to").datepicker(datePickerOptions);

// When 'from' date is selected - set min date of 'to' date equal to 'from' date + 1 day
$dateFromEl.on("change", () => {
  selectedFromDate = $dateFromEl.val().split("-");

  minDate = new Date(
    parseInt(selectedFromDate[0]),
    parseInt(selectedFromDate[1]) - 1,
    parseInt(selectedFromDate[2]) + 1
  );

  $("#id_date_to").datepicker("destroy");
  datePickerOptions["minDate"] = minDate;
  $("#id_date_to").datepicker(datePickerOptions);
});
