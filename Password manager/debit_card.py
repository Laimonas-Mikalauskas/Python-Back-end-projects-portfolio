from cryptography.fernet import Fernet
SymmetricKey = Fernet.generate_key()
f = Fernet(SymmetricKey)

class Encrypter:
    def __init__(self, key: bytes):
        self.key = key
        self.fernet = Fernet(key)

    def encrypt(self, data: str) -> bytes:
        if not data:
            raise ValueError("Plaintext cannot be empty.")
        return self.fernet.encrypt(data.encode())

    def decrypt(self, cipher_text: bytes) -> str:
        if not cipher_text:
            raise ValueError("Cipher text cannot be empty.")
        return self.fernet.decrypt(cipher_text).decode()


class DebitCard:
    def __init__(self, card_number, expiration_date, cvv, bank_name):
        self.card_number = "5544 0088 1316 7710"
        self.expiration_date = "12/25"
        self.cvv = "256"
        self.bank_name = "Bank of America"

            
    def add_debit_card(self, debit_card):
        self.debit_cards.append(debit_card)
        
    def get_debit_card(self, card_number):
        for debit_card in self.debit_cards:
            if debit_card.card_number == card_number:
                return debit_card
        return None
    
    def remove_debit_card(self, card_number):
        debit_card = self.get_debit_card(card_number)
        if debit_card:
            self.debit_cards.remove(debit_card)
            return True
        return False 
    
if __name__ == "__main__":
    # Example usage
    debit_card = DebitCard(card_number="5544 0088 1316 7710", expiration_date="12/25", cvv="256", bank_name="Bank of America") 
    
    # Encrypter
    
    print("Symmetric Key:", SymmetricKey)
    
    # Encrypt and decrypt card number
    encrypted_card_number = f.encrypt(debit_card.card_number.encode())
    decrypted_card_number = f.decrypt(encrypted_card_number).decode()
    
    # Encrypt and decrypt expiration date
    encrypted_expiration_date = f.encrypt(debit_card.expiration_date.encode())
    decrypted_expiration_date = f.decrypt(encrypted_expiration_date).decode()
    
    # Encrypt and decrypt CVV
    encrypted_cvv = f.encrypt(debit_card.cvv.encode())
    decrypted_cvv = f.decrypt(encrypted_cvv).decode()

    # Print results
    print("Encrypted Card Number:", encrypted_card_number)
    print("Decrypted Card Number:", decrypted_card_number)
    print("Encrypted Expiration Date:", encrypted_expiration_date)
    print("Decrypted Expiration Date:", decrypted_expiration_date)
    print("Encrypted CVV:", encrypted_cvv)
    print("Decrypted CVV:", decrypted_cvv)
    
    
         
    
     