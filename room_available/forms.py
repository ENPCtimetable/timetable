from django import forms

class ContactForm(forms.Form):
    #Récupérer les infos du dico d'extract pour le label
    salle1 = forms.BooleanField(label="Salle de cours",required=False)
    salle2 = forms.BooleanField(label="Salle informatique",required=False)
    salle3 = forms.BooleanField(label="Amphitheatre",required=False)
    salle4 = forms.BooleanField(label="Labo de langues",required=False)
    
    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        salle1 = cleaned_data.get('salle1')
        salle2 = cleaned_data.get('salle2')
        salle3 = cleaned_data.get('salle3')
        salle4 = cleaned_data.get('salle4')
        choix = salle1 + salle2 + salle3 + salle4
        if (choix >= 2):
            raise forms.ValidationError("Ne choisissez qu'un type de salle")
        if (choix == 0):
            raise forms.ValidationError("Choisissez un type de salle")
        return cleaned_data

    def display(self,salle1,salle2,salle3,salle4):
        if salle1 :
            return ("1. Salle de cours")    
        if salle2 :
            return ("1. Salle de TP")    
        if salle3 :
            return ("1. Amphithéatre")   
        if salle4 :
            return ("1. Labo de langues")   
            
