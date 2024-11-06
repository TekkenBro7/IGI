const btnSpeach = document.getElementById("btnSpeach");
const voiceSelect = document.getElementById("selectSpeach");
const speachText = document.getElementById("speachText");
let voices = [];

window.speechSynthesis.onvoiceschanged = () => {
    voices = window.speechSynthesis.getVoices();
    voiceSelect.innerHTML = '';
    voices.forEach((voice, i) => {
        const option = new Option(`${voice.name} (${voice.lang})`, i);
        voiceSelect.add(option);
    });
};

function populateJokeInTextarea() {
    const setupText = document.getElementById("jokeSetup").innerText;
    const punchlineText = document.getElementById("jokePunchline").innerText;
    const fullText = document.getElementById("jokeFullText").innerText;
    speachText.value = `${setupText}\n${punchlineText}\n${fullText}`;
}

function textToSpeech() {
    const text = speachText.value;
    if (!text) return;
    const utterance = new SpeechSynthesisUtterance(text);
    const selectedVoiceIndex = voiceSelect.value;
    if (voices[selectedVoiceIndex]) {
        utterance.voice = voices[selectedVoiceIndex];
    }
    window.speechSynthesis.cancel(); // Без этого ошибка
    window.speechSynthesis.speak(utterance);
}

btnSpeach.addEventListener("click", textToSpeech);

window.addEventListener("load", populateJokeInTextarea);