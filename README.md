# ΕΡΓΑΣΙΑ Σ.Δ.Β.Δ. Μαρία Δημακογιάννη, Π17025, Αργύρης Γκιζίνος, Π18027, Νίκος Αρκουλής, Π18012

## 1	WHERE statement enrichment

### 1.1	OPERATORS

Για να προστεθούν με επιτυχία, στο where statement, τα ζητούμενα operators, θα πρέπει να προηγηθούν κάποιες ενέργειες.
  Αρχικά, στο αρχείο database.py, θα πρέπει να πραγματοποιηθεί αλλαγή στη συνάρτηση select (στην παρακάτω εικόνα φαίνεται αναλυτικά).  
  Πρέπει να δούμε, αν κάποιο operator από αυτά που παρουσιάζονται παρακάτω, βρίσκεται στο condition της select. Αν ναι, πρέπει να απομονωθεί το εκάστοτε operator από τη συνθήκη, οπότε εκτελούμε την μέθοδο split(), η οποία χρησιμοποιείται για να «σπάει» ένα string σε μικρότερα.



![Screenshot 2023-02-15 153734](https://user-images.githubusercontent.com/43910499/219042558-1263b5ce-0925-4eca-9bc9-6975bc9ab7c0.png)



#### Εικόνα 1: Αλλάγές στο αρχείο database.py, όσο αφορά τα operators.


#### 1.1.1	NOT

Στο αρχείο table.py, πηγαίνουμε στην συνάρτηση _select_where(). Εκεί, εξετάζουμε αν υπάρχει το NOT. Αν ναι, εκτελούμε τη μέθοδο .split(“NOT”), απομονώνοντας το ΝΟΤ, όπως εξηγήσαμε στην αρχή ότι με τη συγκεκριμένη μέθοδο το πετυχαίνουμε αυτό, από την υπόλοιπη συνθήκη. 
  Μετά, εκτελούμε την συνάρτηση parse_condition , η οποία θα χρησιμοποιηθεί ως όρισμα για να εκτελεστεί η ΝΟΤ.
  Τέλος, εκτελούμε την reverse_op, για να στείλουμε στον πίνακα rows[] το αποτέλεσμα της συνθήκης.


![Screenshot 2023-02-15 154438](https://user-images.githubusercontent.com/43910499/219044080-c6847b48-56e8-427c-b6c8-c2a83f2036a8.png)



#### Εικόνα 2: Αλλάγές στο αρχείο table.py, όσο αφορά τo NOT.
		


#### 1.1.2	BETWEEN

Στο αρχείο table.py, αφού έχουμε ελέγξει ότι στην συνάρτηση condition, υπάρχει έστω μία από τις λέξεις “Between” ή “between”, εκτελούμε την split() στην condition. 
  Αν η συνθήκη between είναι σωστά δομημένη (περιέχεται το and ανάμεσα από αριθμούς),  εισάγουμε 3 μεταβλητές (αριστερά και δεξιά αριθμό, όνομα στήλης).
  Τέλος, το αποτέλεσμα της συνθήκης συμπληρώνεται και στον πίνακα rows[], αν οι τιμές είναι αριθμοί.



![Screenshot 2023-02-15 153927](https://user-images.githubusercontent.com/43910499/219043169-8b60e4dd-9a0e-4e9c-95d1-a11ee62bfdc4.png)



#### Εικόνα 3: Αλλάγές στο αρχείο table.py, όσο αφορά τo BETWEEN.



#### 1.1.3	AND

Στο αρχείο table.py, όσο αφορά το AND, εκτελούμε τη μέθοδο split(),  και εξετάζουμε αν υπάρχει. Αν ναι, απομονώνουμε τις 2 συνθήκες, εκτελώντας την .split(“AND”).
  Τέλος, στον πίνακα rows[] βάζουμε το αποτέλεσμα του ελέγχου για κάθε condition. 


![Screenshot 2023-02-15 154247](https://user-images.githubusercontent.com/43910499/219043651-5c02b792-24d7-423f-ab1c-430acca924e6.png)



#### Εικόνα 4: Αλλάγές στο αρχείο table.py, όσο αφορά τo AND.






#### 1.1.4	OR

Στο αρχείο table.py, όσο αφορά το OR, εκτελούμε τη μέθοδο split(),  και εξετάζουμε αν υπάρχει. Αν ναι, απομονώνουμε τις συνθήκες, εκτελώντας την .split(“OR”). Το αποτέλεσμα κάθε συνθήκης πάει στον πίνακα row_lists[].
  Τέλος, ελέγχουμε για διπλότυπα και περνάμε στον row[] όλα τα στοιχεία του row_list[].


![Screenshot 2023-02-15 154402](https://user-images.githubusercontent.com/43910499/219043942-24511594-49f9-4ccd-bcf0-bfa85baa80e1.png)


#### Εικόνα 5: Αλλάγές στο αρχείο table.py, όσο αφορά τo OR.


## 2 Indexing functionality enrichment

Αρχικά, στο αρχείο mdb.py, πρέπει να γίνουν κάποιες ενέργειες, οι οποίες είναι:

•	Επειδή η miniDB δεν μπορεί να δεχθεί ως όρισμα κάποια στήλη, αλλάζουμε, όπως φαίνεται στην παρακάτω εικόνα, την συνάρτηση interpret(query), ώστε να δέχεται στήλες σαν όρισμα.


![Screenshot 2023-02-15 155250](https://user-images.githubusercontent.com/43910499/219046305-0b5adb92-76cf-41cf-9b43-9da94137edd0.png)



#### Εικόνα 6: Αλλάγές στο αρχείο mdb.py, για να δέχεται στήλες ως ορίσματα η miniDB.


•	Στη συνάρτηση create_query_plan(), πρέπει να βλέπουμε εάν ο χρήστης θέλει να φτιάξει index. Άρα, εισάγουμε τον έλεγχο που φαίνεται στην εικόνα. Αν τελικά το επιθυμεί ο χρήστης, εκτελείται η split(), αφαιρώντας τις παρενθέσεις, για να μείνει η δηλωθείσα στήλη.



•	Δημιουργούμε το λεξικό, το οποίο εκτελείται στην execute_dic(dic).


### 2.1	B-Tree index over unique (non-PK) columns

Όσο αφορά το Β-Tree, και αφού έχουν εκτελεστεί τα παραπάνω, πηγαίνουμε στο αρχείο database.py. Πρέπει να αυξήσουμε τον αριθμό των στηλών του πίνακα meta_indexes[] κατά 1. Αυτό φαίνεται στην παρακάτω εικόνα.


![Screenshot 2023-02-15 160140](https://user-images.githubusercontent.com/43910499/219048360-b08a4857-55b8-477f-bd6a-616be224f394.png)



#### Εικόνα 7: Αλλάγές στο αρχείο database.py, όσο αφορά τον πίνακα meta_indexes[].


  Έπειτα, θέλουμε να δέχεται ως όρισμα την επιπλέον στήλη που έβαλε ο χρήστης, άρα γίνεται μετατροπή των ορισμάτων της create_index(). 
  Τέλος, γίνεται έλεγχος για το αν υπάρχει το όνομα του index που έδωσε ο χρήστης. 
 

### 2.2	Hash index over PK or unique columns

Όσο αφορά το Hash, στο αρχείο database.py, και διενεργούμε έλεγχο αν η μεταβλητή (index_type) είναι B-Tree ή Hash. Αν ισχύει το δεύτερο, προστίθεται η στήλη του index στον πίνακα meta_indexes[].
  Στη συνέχεια, στην συνάρτηση _construct_index_hash(), δημιουργείται το λεξικό που θα είναι το Hash Map. Προσθέτουμε επίσης ένα υπό-λεξικό (nested dictionary), καθώς έτσι διευρύνουμε το είδος των πληροφοριών που μπορούμε να μοντελοποιήσουμε στο πρόγραμμα, και τις στήλες στην πρώτη θέση του.

  Μόλις παραχθεί το index του Hash, τα στοιχεία της στήλης προστίθενται στο εκάστοτε υπο-λεξικό. Για να μην υπάρχει σύγχυση μεταξύ των στοιχείων, χρησιμοποιείται ένα Hash Index για όλα τα υπο-λεξικά.

  Όμως, ένα λεξικό δεν μπορεί να εκτελέσει την συνάρτηση find() του B-Tree, άρα θα εκτελεστεί η _select_where_with_hash(), στο αρχείο table.py.

  Στην παρακάτω εικόνα φαίνεται αναλυτικά το Hash Index.
  
  
  ![Screenshot 2023-02-15 160523](https://user-images.githubusercontent.com/43910499/219049225-046e428b-3662-4fec-8f7c-3394e5f12aaf.png)

  

#### Εικόνα 8: Αλλάγές στο αρχείο database.py, όσο αφορά το Hash Index.


## 3	MiniDB’s query optimizer implementation

### 3.1	Equivalent query plans based on respective RA expressions

Σχετικά με τα Query Plans, σύμφωνα και με τους τύπους της Σχεσιακής Άλγεβρας (ΣΑ), δημιουργούμε τα παρακάτω 3 πλάνα (που είναι και οι αντίστοιχοι τύποι):
1.	Ε1 ⊲⊳ θ(Ε2) = Ε2 ⊲⊳ θ(Ε1)
2.	σθ1 ∧ θ2(Ε) = σθ2(σθ1(Ε))
3.	σθ2 ∧ θ2(Ε) = σθ1(σθ2(Ε))

#### 3.1.1	Ε1 ⊲⊳ θ(Ε2) = Ε2 ⊲⊳ θ(Ε1) and σθ1 ∧ θ2(Ε) = σθ2(σθ1(Ε))

Σε αυτή την περίπτωση, φαίνεται πως θα γίνει το πλάνο σύμφωνα με τον τύπο του τίτλου. Για να επιτευχθεί, κάνουμε τα εξής:
•	Βγάζουμε τις παρενθέσεις, με κατάλληλες ενέργειες 
•	Εκτελούμε την split()
•	Στέλνουμε κάθε συνθήκη στην interpret()

Στην παρακάτω εικόνα φαίνεται αναλυτικά.


![Screenshot 2023-02-15 161139](https://user-images.githubusercontent.com/43910499/219050805-2ade97cd-4bad-4c13-ab84-6726ac1a7d63.png)



#### Εικόνα 9: Query Plan, με τύπο ΣΑ:  σθ1 ∧ θ2(Ε) = σθ2(σθ1(Ε))


#### 3.1.2        Ε1 ⊲⊳ θ(Ε2) = Ε2 ⊲⊳ θ(Ε1) and	σθ1 ∧ θ2(Ε) = σθ1(σθ2(Ε))

Σε αυτή την περίπτωση, φαίνεται πως θα γίνει το πλάνο σύμφωνα με τον τύπο του τίτλου. Για να επιτευχθεί, κάνουμε τα εξής:
•	Βγάζουμε τις παρενθέσεις, με κατάλληλες ενέργειες 
•	Εκτελούμε την split()
•	Στέλνουμε κάθε συνθήκη στην interpret()

Στην παρακάτω εικόνα φαίνεται αναλυτικά.


![Screenshot 2023-02-15 161312](https://user-images.githubusercontent.com/43910499/219051184-e49427d1-9852-4916-b8bc-62433919a49f.png)



#### Εικόνα 10: Query Plan, με τύπο ΣΑ:  σθ1 ∧ θ2(Ε) = σθ1(σθ2(Ε))



![Screenshot 2023-02-18 142048](https://user-images.githubusercontent.com/43910499/219865715-b1451000-0310-4c6a-a76e-0f7323d0072e.png)



#### Εικόνα 11: Screenshot από το άνοιγμα της miniDB σε virtual machine (linux)
