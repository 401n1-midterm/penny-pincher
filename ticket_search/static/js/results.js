// Set modal 'Yes' button value to the link of the clicked element
const $modalLinkEl = $("#link");
const $tableLinksEls = $("#table-body a");

$tableLinksEls.click(function () {
  targetLink = $(this).attr("href");
  $modalLinkEl.attr("href", targetLink);
});
