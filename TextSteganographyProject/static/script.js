function showError(msg) {
    const popup = document.getElementById("popup");
    popup.innerText = msg;
    popup.style.display = "block";
    setTimeout(() => popup.style.display = "none", 3000);
}

function updateKeyHint(type) {
    let algo, key;

    if (type === 'enc') {
        algo = document.getElementById("encAlgo").value;
        key = document.getElementById("encKey");
        syncDecryptionAlgo();   // 🔒 sync decrypt algorithm
    } else {
        algo = document.getElementById("decAlgo").value;
        key = document.getElementById("decKey");
    }

    if (algo === "caesar" || algo === "railfence") {
        key.placeholder = "Numeric key only (e.g. 3)";
    } else {
        key.placeholder = "Alphabetic key (e.g. SECRET)";
    }
}


function validateEmbed() {
    const algo = encAlgo.value;
    const key = encKey.value;

    if (!key) {
        showError("Encryption key is required.");
        return false;
    }

    if ((algo === "caesar" || algo === "railfence") && isNaN(key)) {
        showError("Numeric key required for selected algorithm.");
        return false;
    }

    if (algo === "vigenere" && /\d/.test(key)) {
        showError("Vigenère key must contain only letters.");
        return false;
    }

    return true;
}

function syncDecryptionAlgo() {
    const encAlgo = document.getElementById("encAlgo");
    const decAlgo = document.getElementById("decAlgo");
    const hidden = document.getElementById("decAlgoHidden");

    decAlgo.value = encAlgo.value;
    hidden.value = encAlgo.value;

    decAlgo.disabled = true;
}



window.onload = function () {
    const encAlgo = document.getElementById("encAlgo");
    const decAlgo = document.getElementById("decAlgo");
    const hidden = document.getElementById("decAlgoHidden");

    if (encAlgo && decAlgo && encAlgo.value) {
        decAlgo.value = encAlgo.value;
        hidden.value = encAlgo.value;
        decAlgo.disabled = true;
    }
};




/*function validateExtract() {
    const algo = decAlgo.value;
    const key = decKey.value;

    if (!key) {
        showError("Decryption key is required.");
        return false;
    }

    if ((algo === "caesar" || algo === "railfence") && isNaN(key)) {
        showError("Numeric key required for selected algorithm.");
        return false;
    }

    if (algo === "vigenere" && /\d/.test(key)) {
        showError("Vigenère key must contain only letters.");
        return false;
    }

    return true;
}
*/