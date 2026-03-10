

//Programma che riceve input utente di pià numeri e restituisce il prodotto e la media su schermo

#include <stdio.h>  //per printf() e fgets() quindi input/outup
#include <stdlib.h> //per atof() che convertirà testo in numeri
#include <string.h> //for strlen() che controllerà input vuoto

int main()
{

    //ottengo prima il prodotto finale delle moltiplicazioni

    double numeri[100];      //faccio un array con disponibili 100 slots che permette inserimento di numeri decimali
    int count=0;             //contatore di quanti numeri l'utente ha inserito, parte da 0
    char input[50];          //servirà per registrare cosa inserisce l'utente
    
    printf("Inserisci i numeri. Premi ENTER quando hai finito.\n"); // \n fa in modo che si passi a nuova linea


    while (1) {               //while True loop
        printf("Enter number %d: ", count+1); //Prompt utente di inserire un numero, aumenta il counter numeri inseriti ogni volta, %d: fa in modo che si rimanga sulla stessa linea
        fgets(input, sizeof(input), stdin);   //fgets legge la linea intera inserita dall'utente. vede dove registrare gli input dell'user, controlla che non sorpassi dimensioni massime caratteri, e che sia input standard da tastiera

        if (strlen(input)<=1){
            break; //necessario così che se user inserisce uno o meno numeri il loop si interrompe subito, 
            //se user dovesse premere solo enter, questo verebbe letto come \n quindi dopo non dovrebbe dare fastidio
        }

        numeri[count]=atof(input); //atof converte il testo inserito da user in un numero vero e proprio (ad esempio riconoscendo "x.y\n" solo come x.y e inserendolo nel nostro array "numeri"
        count++; //aumento il counter di numeri inseriti di 1, questo influenza anche printf di prima che ora mostrerà in output il numero successivo da inserire.
    }

    if (count==0){
        printf("Non hai inserito alcun numero, riprova.\n");
        return 1; //esce da programma
    }

    double prodotto = 1; //dichiaro la variabile di prodotto tra i numeri e le assegno il valore 1 in quanto la moltiplicheremo con gli altri valori

    for (int i=0; i<count; i++){        //standard ciclo dove inizio da indice slot 0, termino quando questo indice raggiunge count dell'ultimo numero aggiunto, e aumenta di 1 l'indice 
        prodotto = prodotto*numeri[i]; //prendo il prodotto corrente e lo moltiplico per il nuovo numero inserito
    }
     printf("Il prodotto di tutti i numeri inseriti è: %.2f\n", prodotto); //output del prodotto finale, %.2f specifica che il numero double in output deve avere al massimo 2 cifre decimali.
    
    //ora posso iniziare il calcolo della media

    double somma = 0.0; //dichiaro variabile "somma" che verrà poi divisa per il numero totale di input "count" per ottenere la media

    for (int i=0; i<count; i++){    //un altro standardissimo ciclo con indice che parte da 0 e aumenta a ogni reiterazione finchè non raggiunge il valore di count
        somma = somma+numeri[i]; //come il ciclo di prima però invece che moltiplicare, facciamo semplicemente la somma complessiva
    }
    
    double media = somma/count; //dichiaro la variabile decimale "media" che è uguale alla somma diviso la quantità count totale dei numeri inseriti
    printf("La media di tutti i numeri inseriti è: %.2f\n", media);
    
    
    return 0;
}





