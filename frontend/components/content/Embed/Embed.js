import iframeResizer from "iframe-resizer";

var Embed = {
  els: {
    container: ".js-Embed",
  },
  init: function () {
    this.embedEls = document.querySelectorAll(this.els.container);
    if (this.embedEls.length === 0) return false;
    this.embedEls.forEach(this.initEmbed.bind(this));
  },
  initEmbed: function (embedEl) {
    if (embedEl.classList.contains("Embed--fullSize")) {
      var iframe = embedEl.querySelector("iframe");
      if (!iframe) return false;
      iframe.addEventListener("load", this.setIframeHeight.bind(this));
    }
  },
  setIframeHeight: function (event) {
    var iframe = event.target;
    iframeResizer.iframeResize({ autoResize: true }, iframe);
  },
};

export default Embed;
