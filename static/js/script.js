let slides = document.querySelectorAll(".hero-slide");
let index = 0;

const showSlide = (i) => {
    slides.forEach(slide => slide.classList.remove("active"));
    slides[i].classList.add("active");
};

// Next
document.querySelector(".next").addEventListener("click", () => {
    index = (index + 1) % slides.length;
    showSlide(index);
});

// Prev
document.querySelector(".prev").addEventListener("click", () => {
    index = (index - 1 + slides.length) % slides.length;
    showSlide(index);
});

// Auto slide
setInterval(() => {
    index = (index + 1) % slides.length;
    showSlide(index);
}, 4000);



function updateCountdown() {
    document.querySelectorAll(".countdown-timer").forEach(timer => {

        let endTime = new Date(timer.getAttribute("data-end")).getTime();
        let now = new Date().getTime();
        let diff = endTime - now;

        if (diff < 0) return;

        let days = Math.floor(diff / (1000 * 60 * 60 * 24));
        let hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        let minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        let seconds = Math.floor((diff % (1000 * 60)) / 1000);

        timer.querySelector(".days").innerText = days;
        timer.querySelector(".hours").innerText = hours;
        timer.querySelector(".minutes").innerText = minutes;
        timer.querySelector(".seconds").innerText = seconds;
    });
}

setInterval(updateCountdown, 1000);
updateCountdown();
