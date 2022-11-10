/*
 * FixturesList filter
 */

"use strict";

var filter;
var filterTableSearch;
var filterTableRows;
var filterClear;
var filterCategories;
var selectedFilterCategory = "";

function init() {
  filter = document.querySelector(".js-FixturesList-filter");
  if (!filter) return;

  filter.classList.remove("u-hidden");

  filterTableRows = document.querySelectorAll(".js-FixturesList-row");

  filterTableSearch = filter.querySelector(".js-FixturesList-filterInput");
  filterTableSearch.addEventListener("input", onFilterUpdate);

  filterClear = filter.querySelector(".js-FixturesList-filterClear");
  filterClear.addEventListener("click", onFilterClear);

  filterCategories = filter.querySelectorAll(".js-FixturesList-filterLink");
  Array.prototype.forEach.call(filterCategories, function (filterCategory) {
    filterCategory.addEventListener("click", onCategorySelected);
  });
}

function onCategorySelected(e) {
  e.preventDefault();
  Array.prototype.forEach.call(filterCategories, function (filterCategory) {
    setInactiveState(filterCategory);
  });
  setActiveState(e.target);

  selectedFilterCategory = e.target.dataset.category;
  onFilterUpdate();
}

function setActiveState(el) {
  el.classList.remove("is-inactive");
}

function setInactiveState(el) {
  el.classList.add("is-inactive");
}

function showClear() {
  filterClear.classList.add("is-active");
}

function hideClear() {
  filterClear.classList.remove("is-active");
}

function onFilterClear() {
  filterTableSearch.value = "";
  filterTableSearch.focus();
  hideClear();
  onFilterUpdate();
}

function onFilterUpdate() {
  var searchValue = filterTableSearch.value.toLowerCase();

  if (!searchValue) {
    hideClear();
  } else {
    showClear();
  }

  Array.prototype.forEach.call(filterTableRows, function (row) {
    if (
      (row.dataset.categories.toLowerCase().indexOf(searchValue) > -1 ||
        row.textContent.toLowerCase().indexOf(searchValue) > -1) &&
      row.dataset.categories.toLowerCase().indexOf(selectedFilterCategory) > -1
    ) {
      setActiveState(row);
    } else {
      setInactiveState(row);
    }
  });
}

export default {
  init: init,
};
