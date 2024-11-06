const car1 = document.querySelector('#car1');
const car2 = document.querySelector('#car2');
const car3 = document.querySelector('#car3');
const car4 = document.querySelector('#car4');
const text1 = document.querySelector('#text1_scroll');
const text2 = document.querySelector('#text2_scroll');

window.addEventListener('scroll', () => {
    let value = window.scrollY;

    // Движение машин
    car1.style.transform = `translateX(${value * 2}px) rotate(${Math.sin(value * 0.05) }deg)`;
    car2.style.transform = `translateX(${-value * 2}px) rotate(${Math.sin(value * 0.05)}deg)`;
    car3.style.transform = `translateX(${-value * 1.3}px) rotate(${Math.sin(value * 0.05)}deg)`;
    car4.style.transform = `translateX(${value * 0.5}px) rotate(${Math.sin(value * 0.05)}deg)`;
    car1.style.filter = `blur(${value * 0.003}px)`;
    car2.style.filter = `blur(${value * 0.004}px)`;
    car3.style.filter = `blur(${value * 0.002}px)`;
    car4.style.filter = `blur(${value * 0.002}px)`;

    // Движение и анимация текста
    text1.style.opacity = `${1 - value * 0.001}`; // Изменение непрозрачности

    text1.style.transform = `translateY(${-value * 0.5}px) scale(${1 - value * 0.001})`; // Текст1 движется вверх и уменьшается
    text2.style.transform = `translateY(${value * 0.7}px) scale(${1 + value * 0.001})`;
    text2.style.opacity = `${1 - value * 0.0012}`; // Изменение непрозрачности

    text1.style.textShadow = `${value * 0.1}px ${value * 0.05}px 5px rgba(0, 0, 0, 0.4)`;
    text2.style.textShadow = `${-value * 0.05}px ${value * 0.0}px 5px rgba(0, 0, 0, 0.4)`;
});