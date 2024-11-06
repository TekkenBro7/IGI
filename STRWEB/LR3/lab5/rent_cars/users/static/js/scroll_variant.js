const car = document.querySelector(".car-anim");

function animateOnScroll() {
    const scrollY = window.scrollY;
    const maxScroll = document.body.scrollHeight - window.innerHeight;
    const translateX = Math.min(285, scrollY * 0.94);
    const translateY = Math.min(240, scrollY * 0.8);
    const scale = Math.min(4.5, 1 + (scrollY / maxScroll) * 80);
    const opacity = Math.min(1, scrollY / (maxScroll * 0.04));
    car.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
    car.style.opacity = opacity;
}

window.addEventListener("scroll", animateOnScroll);