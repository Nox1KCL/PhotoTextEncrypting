from PIL import Image

img = Image.open("../images/photo.png").convert("RGB")
pixels = img.load()


def current_bit(bits_data: str):
    for bit in bits_data:
        if bit == "2":
            return
        yield int(bit)


def text_to_bits(text: str) -> str:
    stop_marker = "#####"
    full_text = text + stop_marker
    return "".join(format(ord(i), "08b") for i in full_text)


def bits_to_text(bits_data: str):
    decoded_text = ""
    bit_letter = ""
    stop_marker = "#####"

    for bit in bits_data:
        bit_letter += bit
        if len(bit_letter) == 8:
            char = chr(int(bit_letter, 2))
            decoded_text += char
            bit_letter = ""


            if decoded_text.endswith(stop_marker):
                return decoded_text[: -len(stop_marker)]
    return decoded_text


bits_data = text_to_bits("Yo")
print("Word: Yo")
width: int
height: int
width, height = img.size
gen = current_bit(bits_data)

for x in range(width):
    try:
        for y in range(height):
            color = pixels[x, y] # type: ignore
            r, g, b = color # type: ignore

            new_r = (r & 254) | next(gen)
            new_g = (g & 254) | next(gen)
            new_b = (b & 254) | next(gen)

            pixels[x, y] = (new_r, new_g, new_b) # type: ignore
    except StopIteration:
        print("Secret symbol")
        break


all_bits = ""
found_secret = ""
stop_marker = "#####"

print("Starting decryption...")
try:
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]  # type: ignore


            for channel_val in (r, g, b):
                all_bits += str(channel_val % 2)


                if len(all_bits) % 8 == 0:
                    char_bits = all_bits[-8:]
                    char = chr(int(char_bits, 2))
                    found_secret += char

                    if found_secret.endswith(stop_marker):
                        raise StopIteration
except StopIteration:
    print("Market found, stopping decryption.")


if found_secret.endswith(stop_marker):
    final_result = found_secret[: -len(stop_marker)]
else:
    final_result = found_secret

print(f"Found text: {final_result}")

img.save("../images/photo.png")


