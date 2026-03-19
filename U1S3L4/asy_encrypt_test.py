
#Basic Asymmetric Encryption Test

import random #serve per scelta randomica di una chiave pubblica
import secrets #riga 15 per scelta randomica chiave privata tra 0-255

PUBLIC_KEYS=[
    {"id":"PublicKey1", "label":"A", "e":11, "n":149}, #qui ogni chiave avra "e" (XOR Scramble per ogni carattere)
    {"id":"PublicKey2", "label":"B", "e":27, "n":211}, #"n" è il modulus che impedisce che i numeri diventano troppo grandi, tutti tra 0 e 256 (ASCII ha codici da 0-127 e poi io estendo fino a 255)
    {"id":"PublicKey3", "label":"C", "e":53, "n":103}, #così che XOR scarmble rimanga sotto ai 256 caratteri, penso che utilizzare numeri primi sia convenzione
    {"id":"PublicKey4", "label":"D", "e":69, "n":199},
    {"id":"PublicKey5", "label":"E", "e":115, "n":89}
]

private_key = secrets.randbelow(256) #chiave privata è un integer che solo il ricevente conosce

def hint_calc(ciph_num:list[int], key_ind: int)-> int: #calcolo un "indizio" che precede il ciphertext così che il ricevente sappia quale chiave publica è stat utilizzata dal pool di quelle dipsonibili
    ciph_sum=sum(ciph_num)%97 #modulo(con numero primo scelto arbitrariamente) della somma di tutti i numeri cipher
    hint=(ciph_sum+key_ind*13)%251 #13 e 251 ancora una volta numeri scelti arbitrariamente
    return hint 
#in questa funzione key_ind ovvero l'index della chiave pubblica è strettamente compreso tra 0-4 (in quanto ho 5 opzioni nel pool di chiavi), questo numero viene moltiplicato per 13 per distanziare tra loro le chiavi

def encrypt(plaintext:str, private_key: int)-> tuple[str,dict,int]: #plaintext sarà il testo da dover cifrare che è una string, private_key è la chiave privata del ricevente, in output restituisco ciphertext
    key_ind=random.randint(0,len(PUBLIC_KEYS)-1) #prendo index chiave randomicamente come un integer tra 0 e la quantità di chiavi pubbliche-1
    pick_key=PUBLIC_KEYS[key_ind]#chiave publica scelta 
    e=pick_key["e"]#XOR scramble per questa chiave
    n=pick_key["n"]#modulus per questa chiave

    print(f"Randomly selected public key: {pick_key['id']}, {pick_key['label']}, e={e}, n={n} ") #mostro a schermo quale chiave ho scelto per test Es. PublicKey1, A, e=11, n=149
    
    cipher_num =[]

    for char in plaintext: #per ogni carattere in "plaintext"
        char_code=ord(char) #lo converto con ord() nell'intege che rappressenta il carattere sulla tavola ASCII
        scrmbl=char_code^e #ora effetto lo  scramble con char_code XOR il valore e dello scramble corrispettivo
        scrmbl=scrmbl%n #ora applico modulo con n per limitare il range dei numeri cipher
        scrmbl=scrmbl^(private_key & 0xFF)#solo ricevente può decifrare questa parte, la chiave privata è aggiunta in XOR così che se intercettata da qualcuno senza la private_key esso non possa decifrare il messaggio
        #& 0xFF (esadecimale per 255) fa in modo che possiamo utilizzare solo il range basso 8bit
        cipher_num.append(scrmbl)#ogni carattere cifrato viene salvato una volta finito lo "scramble" su lista cipher_num sotto forma di un integer
    hint=hint_calc(cipher_num,key_ind) #indizio "hint" dice al ricevente quale chiave pubblica ha usato
    print(f"Indizzio chiave pubblica: {hint}") #test per mostrare in output quale hint è stato scelto

    hint_str=str(hint).zfill(3) #.zfill aggiunge tanti 0 a sinistra finchè il valore di hint(trasformato in string) non raggiunge 3 caratteri in questo caso
    num_str=" ".join(str(scrmbl).zfill(3) for scrmbl in cipher_num) #per ogni carattere "scrambled" nella lista cipher_num lo converto in string e utilizzo .zfill per formattarlo e con " ".join li separo da spazio vuoto
    ciphertext = f"{hint_str}:{num_str}" #cipher text completamente cifrato tramite questi passaggi

    return ciphertext, pick_key

def decrypt(ciphertext:str, private_key:int) -> tuple[str|None, dict|None]: #il tuple è un suggerimento di quale sarà il tipo di informazione ritornata, in questo caso str/dict OR none (fallimento)
    try:
        hint_part, num_part = ciphertext.split(":",1) #separo hint dai numeri cifrati, indico che va fatto solo 1 volta all'inizio
    except ValueError:
        print("Errore: format messaggio cifrato invalido.")
        return None, None
    
    hint_sndr=int(hint_part) #the hint the sender attached to the ciphertext
    cipher_num=[int(scrmbl) for scrmbl in num_part.strip().split()] #.strip() rimuove spazi a inizio e fine in eccesso, con .split() separo ogni numero separato da spazio vuoto (come deciso prima) in argomento proprio
    #una volta resi tutti i numeri in num_part in argomenti proprio per ogni numero scrmbl che abbiamo separato lo trasformo in integer
    # ["1 2 3 4 5"] -> ["1", "2", "3", "4", "5"] -> [1, 2, 3, 4, 5]

    print(f"Hint del sender: {hint_sndr}, ricevuto: {len(cipher_num)} numeri cifrati")

    #per ora ricevente non sà quale chiave pubblica deve usare

    key_match = None #match della chiave ancora nullo
    ind_match = None #indice chiave pubblica ancora nullo

    for k, poss_key in enumerate(PUBLIC_KEYS): #ci serve che for restituisca sia item chiave che la posizione della chiave, con enumerate() include l'intera lista e restituisce entrambi oggetto-indice
      poss_hint=hint_calc(cipher_num, k)
      matched="MATCHED" if poss_hint==hint_sndr else "NOT MATCHED"
      print(f"{poss_key['id']} {poss_key['label']}\nHint: {poss_hint} {matched}\n")

      if poss_hint==hint_sndr: #se combaciano gli hint ricevuto con gli hint di una chiave pubblica allora abbiamo un match, da cui otteniamo correlato oggetto e indice
         key_match=poss_key
         ind_match=k
    
    if key_match is None: #se non ci sta un match con chiave pubblica
        print("No public key matched")
        return None, None
    
    print(f"Chiave pubblica identificata: {key_match['id']}, {key_match['label']}") #test output di quale è la chiave pubblica che ha match con quella ricevuta da ricevente
    e=key_match["e"]
    
    plaintext_char=[]

    for scrmbl in cipher_num:
        scrmbl=scrmbl^(private_key & 0xFF) #inverso della cifratura XOR con chiave privata
        scrmbl=scrmbl^e #inverso dello scramble XOR 
        plaintext_char.append(chr(scrmbl)) #chr() al contrario di ord() convertirà il numero assegnato al carattere di nuovo al carattere originale
    
    plaintext="".join(plaintext_char) #ricongiungo i caratteri per riottenere il messaggio originale
    return plaintext, key_match



#TEST

plaintext = input("Enter your message:\n")
print(f"Private Key: {private_key}")

ciphertext, pick_key = encrypt(plaintext, private_key) #uso lal funzione encrypt sul plaintext di input dalla quale voglio poi ricevere il ciphertext (per vedere funzionamento cifraggio) e la chiave scelta
print(f"Chiave pubblica usata: {pick_key['id']}, {pick_key['label']}\n")
print(f"Testo Cifrato:\n{ciphertext}") #mostro testo cifrato come abbiamo fatto noi con XOR scramble

recovered, found_key = decrypt(ciphertext, private_key)
print(f"Messagio decifrato: {recovered}\n")
print(f"Match: {'MESSAGGIO RICEVUTO' if recovered == plaintext else 'FALLIMENTO OPERAZIONE'}")
