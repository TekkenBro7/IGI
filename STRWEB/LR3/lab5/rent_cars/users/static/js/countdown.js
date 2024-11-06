/*

function formatTime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = seconds % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
}

function startCountdown(duration) {
    const countdownElement = document.getElementById('countdown');
    let timeLeft = duration;

    const interval = setInterval(() => {
        countdownElement.textContent = formatTime(timeLeft);
        timeLeft--;

        if (timeLeft < 0) {
            clearInterval(interval);
            countdownElement.textContent = 'Время вышло!';
        }

    }, 1000)
}

document.addEventListener("DOMContentLoaded", function() {
    const oneHour = 3600;
    startCountdown(oneHour);
});

*/

function formatTime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = seconds % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
}

function startCountdown(duration) {
    const countdownElement = document.getElementById('countdown');
    const interval = setInterval(() => {
        const currentTime = Math.floor(Date.now() / 1000);
        const remainingTime = duration - currentTime;
        countdownElement.textContent = formatTime(remainingTime);
        if (remainingTime < 0) {
            clearInterval(interval);
            countdownElement.textContent = 'Время вышло!';
        }

    }, 1000)
}

function getEndTime(duration) {
    const endTime = sessionStorage.getItem('countdownEndTime'); // или localStorage
    if (!endTime) {
        const nowSeconds = Math.floor(Date.now() / 1000);
        const endTimeSeconds = nowSeconds + duration;
        sessionStorage.setItem('countdownEndTime', endTimeSeconds); // или localStorage
        return endTimeSeconds;
    }
    return endTime
}


const oneHour = 3600;
const endTime = getEndTime(oneHour);
startCountdown(endTime);