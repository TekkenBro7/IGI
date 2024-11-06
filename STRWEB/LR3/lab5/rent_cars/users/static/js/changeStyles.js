function rgbToHex(rgb) {
    const result = rgb.match(/\d+/g);
    return "#" + result.map(x => {
        const hex = parseInt(x).toString(16);
        return hex.length === 1 ? "0" + hex : hex;
    }).join('');
}
const switchSettings = document.getElementById('switchSettings');
const styleSettings = document.getElementById('styleSettings');
const privacyPolicySettings = document.getElementById('privacy_policy');

const originalFontSize = window.getComputedStyle(privacyPolicySettings).fontSize;
const originalTextColor = window.getComputedStyle(privacyPolicySettings).color;
const originalBgColor = window.getComputedStyle(document.body).backgroundColor;


const element = document.getElementById('privacy_policy');
const elemFontSize = window.getComputedStyle(element).fontSize.replace('px', '');
document.getElementById('fontSize').value = elemFontSize;

const textColor = window.getComputedStyle(document.body).color;
document.getElementById('textColor').value = rgbToHex(textColor);
const backgroundColor = window.getComputedStyle(document.body).backgroundColor;
document.getElementById('bgColor').value = rgbToHex(backgroundColor);

const fontSizeInput = document.getElementById('fontSize');
const textColorInput = document.getElementById('textColor');
const bgColorInput = document.getElementById('bgColor');

switchSettings.addEventListener('change', function() {
    if (this.checked) {
        styleSettings.style.display = 'block';
    } else {
        styleSettings.style.display = 'none';
    }
});

fontSizeInput.addEventListener('input', function() {
    privacyPolicySettings.style.fontSize = this.value + 'px';
});

textColorInput.addEventListener('input', function() {
    privacyPolicySettings.style.color = this.value;
});

bgColorInput.addEventListener('input', function() {
    document.body.style.backgroundColor = this.value;
});

resetButton.addEventListener('click', function() {
    privacyPolicySettings.style.fontSize = originalFontSize;
    privacyPolicySettings.style.color = originalTextColor;
    document.body.style.backgroundColor = originalBgColor;

    fontSizeInput.value = parseInt(originalFontSize, 10);
    textColorInput.value = rgbToHex(originalTextColor);
    bgColorInput.value = rgbToHex(originalBgColor);
});