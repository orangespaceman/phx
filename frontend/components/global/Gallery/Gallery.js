var Gallery = {
  els: {
    container: ".js-Gallery",
    items: ".js-Gallery-item",
    back: ".js-Gallery-control--back",
    forward: ".js-Gallery-control--forward",
  },
  transitionTime: 3000,
  timeout: null,
  isLoaded: false,

  init: function () {
    this.current = 0;

    this.container = document.querySelector(this.els.container);
    if (!this.container) return false;

    this.items = this.container.querySelectorAll(this.els.items);

    if (this.items.length < 2) {
      return false;
    }

    this.container.classList.add("is-active");

    // lazyload subsequent images
    for (var i = 1; i < this.items.length; i++) {
      var container = this.items[i];
      container.style.backgroundImage = "url(" + container.dataset.img + ")";
    }

    // start transition once first new bg image has loaded
    var img = new Image();
    img.addEventListener("load", this.imageLoaded.bind(this));
    img.src = container.dataset.img;

    // init controls if found
    this.back = this.container.querySelector(this.els.back);
    if (this.back) {
      this.back.addEventListener("click", this.transitionBack.bind(this));
    }
    this.forward = this.container.querySelector(this.els.forward);
    if (this.forward) {
      this.forward.addEventListener("click", this.transitionForward.bind(this));
    }
  },
  imageLoaded: function () {
    this.isLoaded = true;
    this.queueTransition();
    this.container.addEventListener(
      "mouseover",
      this.clearTransition.bind(this)
    );
    this.container.addEventListener(
      "mouseout",
      this.queueTransition.bind(this)
    );
  },
  queueTransition: function () {
    this.clearTransition();
    this.timeout = setTimeout(this.transition.bind(this), this.transitionTime);
  },
  clearTransition: function () {
    clearTimeout(this.timeout);
  },
  transitionBack: function () {
    this.back.blur();
    if (!this.isLoaded) return;
    this.clearTransition();
    this.transition("back");
  },
  transitionForward: function () {
    this.forward.blur();
    if (!this.isLoaded) return;
    this.clearTransition();
    this.transition("forward");
  },
  transition: function (direction) {
    for (var i = 0; i < this.items.length; i++) {
      this.items[i].style.opacity = 0;
    }
    if (direction === "back") {
      this.current =
        this.current != 0 ? this.current - 1 : this.items.length - 1;
    } else {
      this.current =
        this.current != this.items.length - 1 ? this.current + 1 : 0;
    }
    this.items[this.current].style.opacity = 1;

    this.queueTransition();
  },
};

module.exports = Gallery;
