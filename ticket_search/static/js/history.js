$(() => {
  $("#history").DataTable({
    searching: true,
    scrollX: true,
    scrollCollapse: false,
    iDisplayLength: 50,
    order: [[0, "desc"]],
  });
});
