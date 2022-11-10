var Hero = {
  els: {
    container: ".js-Hero",
    items: ".js-Hero-item",
  },
  transitionTime: 4000,
  timeout: null,

  init: function () {
    this.current = 0;

    this.container = document.querySelector(this.els.container);
    if (!this.container) return false;

    this.items = this.container.querySelectorAll(this.els.items);

    if (this.items.length < 2) {
      return false;
    }

    // lazyload subsequent images
    for (var i = 1; i < this.items.length; i++) {
      var container = this.items[i];
      container.style.backgroundImage = "url(" + container.dataset.img + ")";
    }

    // start transition once first new bg image has loaded
    var img = new Image();
    img.addEventListener("load", this.imageLoaded.bind(this));
    img.src = container.dataset.img;
  },
  imageLoaded: function () {
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
  transition: function () {
    for (var i = 0; i < this.items.length; i++) {
      this.items[i].style.opacity = 0;
    }
    var next = this.current != this.items.length - 1 ? this.current + 1 : 0;
    this.items[next].style.opacity = 1;

    this.current = next;

    this.queueTransition();
  },
};

export default Hero;
