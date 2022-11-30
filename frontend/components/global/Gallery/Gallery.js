var Gallery = {
  containers: [],
  galleries: [],
  els: {
    container: ".js-Gallery",
  },
  init: function () {
    this.containers = document.querySelectorAll(this.els.container);
    if (!this.containers) return false;

    for (var i = 0; i < this.containers.length; i++) {
      var container = this.containers[i];
      var gallery = new GalleryInstance();
      gallery.init(container);
      this.galleries.push(gallery);
    }
  },
};

var GalleryInstance = function () {
  this.els = {
    container: ".js-Gallery",
    items: ".js-Gallery-item",
    back: ".js-Gallery-control--back",
    forward: ".js-Gallery-control--forward",
  };
  this.current = 0;
  this.container = null;
  this.items = [];
  this.transitionTime = 3000;
  this.timeout = null;
  this.isLoaded = false;
};

GalleryInstance.prototype.init = function (container) {
  this.current = 0;

  this.container = container;

  this.items = this.container.querySelectorAll(this.els.items);

  if (this.items.length < 2) {
    return false;
  }

  this.container.classList.add("is-active");

  // lazyload subsequent images
  for (var i = 1; i < this.items.length; i++) {
    var lazyloadedImg = this.items[i];
    lazyloadedImg.style.backgroundImage =
      "url(" + lazyloadedImg.dataset.img + ")";
  }

  // start transition once first new bg image has loaded
  var img = new Image();
  img.addEventListener("load", this.imageLoaded.bind(this));
  img.src = this.items[1].dataset.img;

  // init controls if found
  this.back = this.container.querySelector(this.els.back);
  if (this.back) {
    this.back.addEventListener("click", this.transitionBack.bind(this));
  }
  this.forward = this.container.querySelector(this.els.forward);
  if (this.forward) {
    this.forward.addEventListener("click", this.transitionForward.bind(this));
  }
};
GalleryInstance.prototype.imageLoaded = function () {
  this.isLoaded = true;
  this.queueTransition();
  this.container.addEventListener("mouseover", this.clearTransition.bind(this));
  this.container.addEventListener("mouseout", this.queueTransition.bind(this));
};
GalleryInstance.prototype.queueTransition = function () {
  this.clearTransition();
  this.timeout = setTimeout(this.transition.bind(this), this.transitionTime);
};
GalleryInstance.prototype.clearTransition = function () {
  clearTimeout(this.timeout);
};
GalleryInstance.prototype.transitionBack = function () {
  this.back.blur();
  if (!this.isLoaded) return;
  this.clearTransition();
  this.transition("back");
};
GalleryInstance.prototype.transitionForward = function () {
  this.forward.blur();
  if (!this.isLoaded) return;
  this.clearTransition();
  this.transition("forward");
};
GalleryInstance.prototype.transition = function (direction) {
  for (var i = 0; i < this.items.length; i++) {
    this.items[i].style.opacity = 0;
  }
  if (direction === "back") {
    this.current = this.current != 0 ? this.current - 1 : this.items.length - 1;
  } else {
    this.current = this.current != this.items.length - 1 ? this.current + 1 : 0;
  }
  this.items[this.current].style.opacity = 1;

  this.queueTransition();
};

export default Gallery;
