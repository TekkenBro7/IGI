const rect = document.getElementById("rect");
const framesRect = [{
    marginLeft: "-450px",
    transform: "rotate(0deg)",
    scale: "1",
    offset: 0
}, {
    marginLeft: "-150px",
    transform: "rotate(360deg)",
    scale: "1.3",
    offset: 0.3
}, {
    marginLeft: "150px",
    transform: "rotate(720deg)",
    scale: "1.3",
    offset: 0.6
}, {
    marginLeft: "460px",
    transform: "rotate(1080deg)",
    scale: "1",
    offset: 1
}];
const configRect = {
    duration: 800,
    easing: "ease-in-out",
    iterations: Infinity,
    direction: "alternate"
};
const animation = rect.animate(framesRect, configRect);

document.getElementById("pause").addEventListener("click", () => animation.pause());
document.getElementById("play").addEventListener("click", () => animation.play());
document.getElementById("cancel").addEventListener("click", () => animation.cancel());
document.getElementById("faster").addEventListener("click", () => animation.playbackRate *= 2);
document.getElementById("slower").addEventListener("click", () => animation.playbackRate /= 2);

const bntDetectPos = document.getElementById("buttonDetect");

bntDetectPos.addEventListener("click", () => {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(onSuccess, onError);
    } else {
        bntDetectPos.innerText = "Ваш браузер не поддерживается"
    }
});

function onSuccess(position) {
    bntDetectPos.innerText = "Определяем вашу позицию...";
    let { latitude, longitude } = position.coords;
    let api_key = '1857b74d045e406a969b4e2cf3909e41';
    fetch(`https://api.opencagedata.com/geocode/v1/json?q=${latitude}+${longitude}&key=${api_key}`)
        .then(response => response.json()).then(result => {
            let allDetails = result.results[0].components;
            let { continent, country, city, road, building } = allDetails;
            bntDetectPos.innerText = `Ваша позиция: ${continent}, ${country}, ${city}, ${road}`;
            console.table(allDetails);

            initMap(latitude, longitude);
        }).catch(() => {
            bntDetectPos.innerText = "Ошибка получения местоположения";
        })
}

function onError(error) {
    if (error.code == 1) {
        bntDetectPos.innerText = "Вы отклонили запрос";
    } else if (error.code == 2) {
        bntDetectPos.innerText = "Локация недоступна";
    } else {
        bntDetectPos.innerText = "Что-то пошло не так";
    }
    bntDetectPos.setAttribute("disabled", "true");
}

function initMap(latitude, longitude) {
    const existingMapContainer = document.getElementById("map");
    if (existingMapContainer) {
        existingMapContainer.remove();
    }
    const mapContainer = document.createElement("div");
    mapContainer.id = "map";
    mapContainer.style.width = "100%";
    mapContainer.style.height = "600px";
    document.querySelector(".container-position").appendChild(mapContainer);
    ymaps.ready(function() {
        const map = new ymaps.Map("map", {
            center: [latitude, longitude],
            zoom: 12,
            type: 'yandex#hybrid',
            controls: []
        });
        const placemark = new ymaps.Placemark([latitude, longitude], {
            iconContent: "Ваше местонахождение",
            balloonContent: "Вы находитесь здесь",
        });
        map.geoObjects.add(placemark);
        ymaps.geocode("Минск, ул. Колесникова 44, офис 3а").then(function(res) {
            const destination = res.geoObjects.get(0).geometry.getCoordinates();
            ymaps.route([
                [latitude, longitude],
                destination
            ]).then(function(route) {
                map.geoObjects.add(route);
                map.setBounds(route.getBounds(), { checkZoomRange: true });
            }, function(error) {
                console.error("Не удалось построить маршрут:", error);
                bntDetectPos.innerText = "Ошибка построения маршрута";
            });
        }).catch(() => {
            bntDetectPos.innerText = "Ошибка при получении координат пункта назначения";
        });
    });
}