class Slider {
    constructor(options) {
        this.slider = document.getElementById(options.sliderId);
        this.slides = this.slider.querySelectorAll('.slide');
        this.totalSlides = this.slides.length;
        this.currentSlide = 0;
        this.loop = options.loop;
        this.navs = options.navs;
        this.pags = options.pags;
        this.auto = options.auto;
        this.delay = options.delay || 5000;
        this.timer = null;
        this.prevBtn = document.getElementById('prevBtnImg');
        this.nextBtn = document.getElementById('nextBtnImg');
        this.dots = document.querySelectorAll('.dot');
        this.init();
    }

    init() {
        this.showSlide(this.currentSlide);
        if (this.auto) {
            this.startAutoSlide();
            this.slider.addEventListener('mouseenter', () => {
                this.stopAutoSlide();
            });
            this.slider.addEventListener('mouseleave', () => {
                this.startAutoSlide();
            });
        }
        if (this.navs) {
            this.prevBtn.style.display = 'block';
            this.nextBtn.style.display = 'block';
            this.prevBtn.addEventListener('click', () => {
                this.changeSlide(this.currentSlide - 1);
                this.restartAutoSlide();
            });
            this.nextBtn.addEventListener('click', () => {
                this.changeSlide(this.currentSlide + 1);
                this.restartAutoSlide();
            });
        } else {
            this.prevBtn.style.display = 'none';
            this.nextBtn.style.display = 'none';
        }
        if (this.pags) {
            this.dots.forEach((dot, index) => {
                dot.style.display = 'inline-block';
                dot.addEventListener('click', () => {
                    if (index !== this.currentSlide) {
                        this.changeSlide(index);
                        this.restartAutoSlide();
                    }
                });
            });
        } else {
            this.dots.forEach(dot => {
                dot.style.display = 'none';
            });
        }
    }
    showSlide(index) {
        this.slider.style.transform = `translateX(${-index * 100}%)`;
        this.slider.style.transition = 'transform 0.5s ease';
        this.dots.forEach((dot, idx) => {
            dot.classList.toggle('active', idx === index);
        });
        document.getElementById('slideCount').innerText = `${index + 1}/${this.totalSlides}`;
    }
    changeSlide(index) {
        if (index >= this.totalSlides) {
            this.currentSlide = this.loop ? 0 : this.totalSlides - 1;
        } else if (index < 0) {
            this.currentSlide = this.loop ? this.totalSlides - 1 : 0;
        } else {
            this.currentSlide = index;
        }

        this.showSlide(this.currentSlide);
    }
    stopAutoSlide() {
        clearInterval(this.timer);
    }
    startAutoSlide() {
        this.timer = setInterval(() => {
            this.changeSlide(this.currentSlide + 1);
        }, this.delay);
    }
    restartAutoSlide() {
        this.stopAutoSlide();
        if (this.auto) {
            this.startAutoSlide();
        }
    }
}

const curDelay = parseInt(document.getElementById('currentDelay').innerText, 10)
const loopSetting = document.getElementById('loopSetting').innerText === 'Да';
const navsSetting = document.getElementById('navsSetting').innerText === 'Включена';
const pagsSetting = document.getElementById('pagsSetting').innerText === 'Включена';
const autoSetting = document.getElementById('autoSetting').innerText === 'Включен';

const sliderOptions = {
    sliderId: 'slider',
    loop: loopSetting,
    auto: autoSetting,
    delay: curDelay,
    navs: navsSetting,
    pags: pagsSetting
};

let slider = new Slider(sliderOptions);

/*

function populateFormWithInitialValues() {
    document.getElementById('loop').checked = sliderOptions.loop;
    document.getElementById('auto').checked = sliderOptions.auto;
    document.getElementById('delay').value = sliderOptions.delay;
    document.getElementById('navs').checked = sliderOptions.navs;
    document.getElementById('pags').checked = sliderOptions.pags;
}

/*

function updateSliderSettings() {
    const loop = document.getElementById('loop').checked;
    const auto = document.getElementById('auto').checked;
    const delay = parseInt(document.getElementById('delay').value, 10);
    const navs = document.getElementById('navs').checked;
    const pags = document.getElementById('pags').checked;

    alert(auto);

    sliderOptions.loop = loop;
    sliderOptions.auto = auto;
    sliderOptions.delay = delay;
    sliderOptions.navs = navs;
    sliderOptions.pags = pags;

    slider.stopAutoSlide();
    slider = new Slider(sliderOptions);
}

window.onload = populateFormWithInitialValues;

*/