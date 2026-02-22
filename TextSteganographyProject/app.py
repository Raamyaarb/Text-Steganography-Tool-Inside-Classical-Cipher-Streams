from flask import Flask, render_template, request

app = Flask(__name__)

# ================= VIGENERE CIPHER =================
def vigenere_encrypt(text, key):
    text = text.upper()
    key = key.upper()
    result = ""
    j = 0
    for c in text:
        if c.isalpha():
            result += chr((ord(c) + ord(key[j % len(key)]) - 130) % 26 + 65)
            j += 1
    return result

def vigenere_decrypt(text, key):
    key = key.upper()
    result = ""
    j = 0
    for c in text:
        result += chr((ord(c) - ord(key[j % len(key)]) + 26) % 26 + 65)
        j += 1
    return result


# ================= CAESAR CIPHER =================
def caesar_encrypt(text, shift):
    result = ""
    for c in text.upper():
        if c.isalpha():
            result += chr((ord(c) - 65 + shift) % 26 + 65)
    return result

def caesar_decrypt(text, shift):
    result = ""
    for c in text.upper():
        if c.isalpha():
            result += chr((ord(c) - 65 - shift) % 26 + 65)
    return result


# ================= RAIL FENCE CIPHER =================
def rail_fence_encrypt(text, rails):
    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1

    for c in text.upper():
        if c.isalpha():
            fence[rail].append(c)
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction *= -1

    return ''.join([''.join(row) for row in fence])

def rail_fence_decrypt(cipher, rails):
    pattern = list(range(rails)) + list(range(rails-2, 0, -1))
    indexes = pattern * (len(cipher)//len(pattern) + 1)

    rail_len = [0] * rails
    for i in range(len(cipher)):
        rail_len[indexes[i]] += 1

    rails_text = []
    k = 0
    for l in rail_len:
        rails_text.append(cipher[k:k+l])
        k += l

    result = ""
    rail_pos = [0] * rails
    for i in range(len(cipher)):
        r = indexes[i]
        result += rails_text[r][rail_pos[r]]
        rail_pos[r] += 1

    return result


# ================= STEGANOGRAPHY =================
def embed(cipher, carrier):
    length_header = f"{len(cipher):04d}"
    payload = length_header + cipher
    binary = ''.join(format(ord(c), '08b') for c in payload)

    alpha_count = sum(1 for c in carrier if c.isalpha())
    if alpha_count < len(binary):
        raise ValueError("Carrier text too short.")

    result = ""
    i = 0
    for c in carrier:
        if c.isalpha() and i < len(binary):
            result += c.upper() if binary[i] == '1' else c.lower()
            i += 1
        else:
            result += c
    return result

def extract(stego):
    bits = ""
    for c in stego:
        if c.isalpha():
            bits += '1' if c.isupper() else '0'

    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        chars.append(chr(int(byte, 2)))

    message = ''.join(chars)
    msg_len = int(message[:4])
    return message[4:4 + msg_len]


# ================= ROUTES =================
@app.route("/")
def home():
    return render_template("index.html")




@app.route("/embed", methods=["POST"])
def embed_route():
    try:
        secret = request.form["secret"]
        carrier = request.form["carrier"]
        algo = request.form["algorithm"]
        key = request.form["key"]

        if algo == "vigenere":
            cipher = vigenere_encrypt(secret, key)
        elif algo == "caesar":
            cipher = caesar_encrypt(secret, int(key))
        elif algo == "railfence":
            cipher = rail_fence_encrypt(secret, int(key))

        # Embed algorithm info inside cipher
        cipher = f"[{algo}]{cipher}"
        stego = embed(cipher, carrier)


        return render_template(
            "index.html",
            stego=stego,
            enc_algo=algo,
            enc_key=key,
            secret=secret,
            carrier=carrier
        )

    except ValueError as e:
        return render_template(
            "index.html",
            error=str(e),
            enc_algo=algo,
            enc_key=key,
            secret=secret,
            carrier=carrier
        )




@app.route("/extract", methods=["POST"])
def extract_route():
    try:
        stego = request.form["stego"]
        algo = request.form["algorithm"]
        key = request.form["key"]

        # Extract hidden cipher from stego text
        cipher = extract(stego)

        # -------- Algorithm validation --------
        if not cipher.startswith("[") or "]" not in cipher:
            raise ValueError("Invalid stego format")

        stored_algo = cipher[1:cipher.index("]")]
        actual_cipher = cipher[cipher.index("]") + 1:]

        if stored_algo != algo:
            raise ValueError(
                f"Algorithm mismatch! Encrypted with {stored_algo}, not {algo}"
            )
        # -------------------------------------

        # Decrypt ONLY with correct algorithm
        if algo == "vigenere":
            secret = vigenere_decrypt(actual_cipher, key)
        elif algo == "caesar":
            secret = caesar_decrypt(actual_cipher, int(key))
        elif algo == "railfence":
            secret = rail_fence_decrypt(actual_cipher, int(key))
        else:
            raise ValueError("Unsupported algorithm")

        return render_template(
            "index.html",

            # 🔓 Decryption output
            recovered=secret,
            dec_algo=algo,
            dec_key=key,
            stego_text=stego,

            # 🔐 KEEP ALL ENCRYPTION FIELDS
            stego=stego,
            enc_algo=stored_algo,
            enc_key=key,
            secret=secret,        # keeps secret textbox filled
            carrier=request.form.get("carrier", "")
        )

    except Exception as e:
        return render_template(
            "index.html",
            error=str(e),

            # 🔓 Decryption state
            dec_algo=algo if 'algo' in locals() else "",
            dec_key=key if 'key' in locals() else "",
            stego_text=stego if 'stego' in locals() else "",

            # 🔐 KEEP ALL ENCRYPTION FIELDS
            stego=stego if 'stego' in locals() else "",
            enc_algo=algo if 'algo' in locals() else "",
            enc_key=key if 'key' in locals() else "",
            secret=request.form.get("secret", ""),
            carrier=request.form.get("carrier", "")
        )




if __name__ == "__main__":
    app.run(debug=True)
