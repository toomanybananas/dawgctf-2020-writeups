# Vigenere Cipher (Polyalphabetic Substitution Cipher)
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)
#
# Altered:
#  - using new message
#  - using shift based on date

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def main():

    myMessage = """How do you keep a programmer in the shower all day?
Give him a bottle of shampoo which says Lather rinse repeat DawgCTF{ClearEdge_crypto}"""

    myKeyArray = []
    # Elizebeth Friedman's birthday, otherwise known as the day on which she'd eat cake
    for digit in '08261892':
      myKeyArray.append(LETTERS[int(digit)])
    myKey = ''.join(myKeyArray)

    myMode = 'encrypt' # Set to either 'encrypt' or 'decrypt'.

#     myMessage= """Hwyjpgxwkmgvbxaqgzcsnmaknbjktpxyezcrmlja?
# GqxkiqvcbwvzmmxhspcsqwxyhqentihuLivnfzaknagxfxnctLcchKCH{CtggsMmie_kteqbx}
# """
#     myMode = 'decrypt'

    if myMode == 'encrypt':
        translated = encryptMessage(myKey, myMessage)
    elif myMode == 'decrypt':
        translated = decryptMessage(myKey, myMessage)

    print('%sed message:' % (myMode.title()))
    print(translated)
    print()


def encryptMessage(key, message):
    return translateMessage(key, message, 'encrypt')

def decryptMessage(key, message):
    return translateMessage(key, message, 'decrypt')

def translateMessage(key, message, mode):
  translated = [] # Stores the encrypted/decrypted message string.

  keyIndex = 0
  key = key.upper()

  for symbol in message: # Loop through each symbol in message.
    num = LETTERS.find(symbol.upper())

    if num != -1: # -1 means symbol.upper() was not found in LETTERS.
      if mode == 'encrypt':
        num += LETTERS.find(key[keyIndex]) # Add if encrypting.
      elif mode == 'decrypt':
        num -= LETTERS.find(key[keyIndex]) # Subtract if decrypting.

      num %= len(LETTERS) # Handle any wraparound.

      # Add the encrypted/decrypted symbol to the end of translated:
      if symbol.isupper():
        translated.append(LETTERS[num])
      elif symbol.islower():
        translated.append(LETTERS[num].lower())

      keyIndex += 1 # Move to the next letter in the key.
      if keyIndex == len(key):
        keyIndex = 0
    else:
      if (symbol != " "):
        # Append the symbol without encrypting/decrypting:
        translated.append(symbol)

  return ''.join(translated)

# If vigenereCipher.py is run (instead of imported as a module), call
# the main() function:
if __name__ == '__main__':
  main()