const $modalLinkEl = $("#link");
const $tableLinksEls = $("#table-body a");

// Add datatables to history table
$(() => {
  $("#history").DataTable({
    searching: true,
    scrollX: true,
    scrollCollapse: false,
    iDisplayLength: 50,
    order: [[0, "desc"]],
  });
});

// Set modal 'Yes' button value to the link of the clicked element
$tableLinksEls.click(function () {
  targetLink = $(this).attr("href");
  $modalLinkEl.attr("href", targetLink);
});
