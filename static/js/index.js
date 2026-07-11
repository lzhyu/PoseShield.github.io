window.HELP_IMPROVE_VIDEOJS = false;

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("model-viewer[poster]").forEach((viewer) => {
    const shell = viewer.closest(".pose-viewer-shell");
    const poster = viewer.getAttribute("poster");
    if (!shell || !poster) {
      return;
    }

    if (!shell.style.getPropertyValue("--viewer-fallback")) {
      shell.style.setProperty("--viewer-fallback", `url("${poster.replace(/^\.\/static\//, "../")}")`);
    }
    viewer.addEventListener(
      "load",
      () => {
        shell.classList.add("is-loaded");
      },
      { once: true },
    );
  });

  document.querySelectorAll(".motion-grid figure").forEach((figure) => {
    const video = figure.querySelector("[data-motion-video]");
    const slider = figure.querySelector("[data-motion-slider]");
    const toggle = figure.querySelector("[data-motion-toggle]");
    if (!video || !slider) {
      return;
    }

    let scrubbing = false;

    const setToggleLabel = () => {
      if (!toggle) {
        return;
      }
      const isEnded = Number.isFinite(video.duration) && video.duration > 0 && video.currentTime >= video.duration;
      toggle.textContent = isEnded ? "Replay" : video.paused ? "Play" : "Pause";
      toggle.setAttribute("aria-label", `${toggle.textContent} motion example`);
    };

    const syncSlider = () => {
      if (scrubbing || !Number.isFinite(video.duration) || video.duration <= 0) {
        return;
      }
      slider.value = Math.round((video.currentTime / video.duration) * Number(slider.max));
    };

    const seekFromSlider = () => {
      if (!Number.isFinite(video.duration) || video.duration <= 0) {
        return;
      }
      video.currentTime = (Number(slider.value) / Number(slider.max)) * video.duration;
      setToggleLabel();
    };

    const togglePlayback = () => {
      if (Number.isFinite(video.duration) && video.duration > 0 && video.currentTime >= video.duration) {
        video.currentTime = 0;
      }
      if (video.paused) {
        video.play().catch(() => {
          video.controls = true;
        });
      } else {
        video.pause();
      }
    };

    slider.addEventListener("pointerdown", () => {
      scrubbing = true;
      video.pause();
    });
    slider.addEventListener("pointerup", () => {
      seekFromSlider();
      scrubbing = false;
    });
    slider.addEventListener("input", () => {
      video.pause();
      seekFromSlider();
    });
    if (toggle) {
      toggle.addEventListener("click", togglePlayback);
    }
    video.addEventListener("click", togglePlayback);
    video.addEventListener("timeupdate", syncSlider);
    video.addEventListener("loadedmetadata", () => {
      video.currentTime = 0;
      syncSlider();
      setToggleLabel();
    });
    video.addEventListener("play", setToggleLabel);
    video.addEventListener("pause", setToggleLabel);
    video.addEventListener("ended", setToggleLabel);
  });
});
