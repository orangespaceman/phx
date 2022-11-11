var Nav = {
  els: {
    nav: ".js-Nav",
    toggle: ".js-Nav-toggle",
  },

  init: function () {
    this.navEl = document.querySelector(this.els.nav);
    this.toggleEl = document.querySelector(this.els.toggle);

    if (!this.toggleEl) {
      return false;
    }
    this.toggleEl.addEventListener("click", this.toggleNav.bind(this));
  },

  toggleNav: function (e) {
    e.preventDefault();
    this.navEl.classList.toggle("Nav--open");
  },
};

export default Nav;
