(function () {
  function fallbackCopy(text) {
    var textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "");
    textarea.style.position = "fixed";
    textarea.style.left = "-9999px";
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand("copy");
    document.body.removeChild(textarea);
  }

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    fallbackCopy(text);
    return Promise.resolve();
  }

  function initCopyBlocks() {
    var blocks = Array.prototype.slice.call(document.querySelectorAll("pre > code"));
    blocks.forEach(function (code) {
      var pre = code.parentElement;
      if (!pre || pre.parentElement.classList.contains("copy-block")) return;

      var wrapper = document.createElement("div");
      wrapper.className = "copy-block";

      var toolbar = document.createElement("div");
      toolbar.className = "copy-toolbar";

      var button = document.createElement("button");
      button.type = "button";
      button.className = "copy-button";
      button.textContent = "Copy";
      button.setAttribute("aria-label", "Copy text");

      pre.parentNode.insertBefore(wrapper, pre);
      wrapper.appendChild(toolbar);
      toolbar.appendChild(button);
      wrapper.appendChild(pre);

      button.addEventListener("click", function () {
        copyText(code.innerText).then(function () {
          button.textContent = "Copied";
          window.setTimeout(function () {
            button.textContent = "Copy";
          }, 1600);
        });
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initCopyBlocks);
  } else {
    initCopyBlocks();
  }
})();
