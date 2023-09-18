## -*- coding: utf-8 -*-

import streamlit as st
st.set_page_config(layout="wide")
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import requests
import time

st.set_option('deprecation.showPyplotGlobalUse', False)


def main():

    # Titre de la page
    st.title("Répartir les rôles sur une pièce de théâtre")
    st.text("Données client : ")

    #values = df['SK_ID_CURR'].values
    values = ['http://www.theatre-classique.fr/pages/txt/MOLIERE_MALADEIMAGINAIRE.txt','http://www.theatre-classique.fr/pages/txt/ABEILLE_ARGELIE.txt',
     'http://www.theatre-classique.fr/pages/txt/ABEILLE_CORIOLAN.txt',
     'http://www.theatre-classique.fr/pages/txt/ABEILLE_LYNCEE.txt',
     'http://www.theatre-classique.fr/pages/txt/ABOUT_RISETTE.txt',
     'http://www.theatre-classique.fr/pages/txt/ADENIS_HOMMEQUINEPEUTPASSIFFLER.txt',
     'http://www.theatre-classique.fr/pages/txt/AIGUEBERRE_AVAREAMOUREUX.txt',
     'http://www.theatre-classique.fr/pages/txt/AIGUEBERRE_PANETDORIS.txt',
     'http://www.theatre-classique.fr/pages/txt/AIGUEBERRE_POLIXENE.txt',
     'http://www.theatre-classique.fr/pages/txt/AIGUEBERRE_PROLOGUE.txt',
     'http://www.theatre-classique.fr/pages/txt/ALAINLEGRAND_EPREUVERECIPROQUE.txt',
     'http://www.theatre-classique.fr/pages/txt/ALLAINVAL_ECOLEDESBOURGEOIS.txt',
     'http://www.theatre-classique.fr/pages/txt/ALLAINVAL_HIVER.txt',
     'http://www.theatre-classique.fr/pages/txt/ALLAIS_BONBOUGRE.txt',
     'http://www.theatre-classique.fr/pages/txt/ALLAIS_MECONTENT.txt',
     'http://www.theatre-classique.fr/pages/txt/ANCELOT-ARAGO_PAPILLOTES.txt',
     'http://www.theatre-classique.fr/pages/txt/ANCELOT-AUGER_SEDUCTION.txt']
    titre = st.sidebar.selectbox(
        "Veuillez sélectionner une pièce de théâtre",
        values)

    #Le bouton de prédiction
    input_data = {'url_':str(titre)}
    print('url_', json.dumps(input_data))

    if st.button("visualisation"):
        t1 = time.time()
        #resultat = requests.post(url="http://monapp.herokuapp.com/predict",data=json.dumps(input_data))
        #result = requests.post(url="http://127.0.0.1:8000/visu_gen",data=json.dumps(input_data))
        #result = requests.post(url="http://fastapi:8000/visu_gen", data=json.dumps(input_data))

        # récupération des données pour le graphe
        #with open(r"C:\Users\John\Desktop\Formation\TH-NL-P1-decoupage_des_roles_d_une_piece_de_theatre\docker\backend\data_visu.pickle", 'rb') as f:
        #    data_visu = pickle.load(f)

        # Define the FastAPI endpoint URL
        fastapi_url = "http://127.0.0.1:8000/visu_gen"  # Update with your FastAPI server URL
        fastapi_url = "http://fastapi:8000/visu_gen"  # Update with your FastAPI server URL

        # Make a POST request to the FastAPI endpoint
        response = requests.post(fastapi_url, json=input_data)  # Modify the JSON input as needed

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data_visu = response.json()  # Parse the JSON response
            st.write(data_visu)  # Display the data in Streamlit
        else:
            st.error(f"Error: {response.status_code}")

            

        # construction du graphe
        fig, ax = plt.subplots(figsize=(15, 6))

        ax.scatter(data_visu['absi'], data_visu['ordo'],
                   s=data_visu['vale'], alpha=0.7)

        # Ajouter des boules pour le total par personnage
        for personnage, total in data_visu['tota'].items():
            ax.scatter(personnage, "Total", s=total, c='green', alpha=0.7)#, label=f'Total {personnage}')

        # Configuration des axes et du titre
        ax.set_xlabel('Personnage')
        ax.set_ylabel('Acte')
        ax.set_title('Graphique en boules - Nb de mots')
        plt.xticks(rotation=45)

        # Vérification
        #print(series.index.get_level_values('Personnage')) 
        #print(series.index.get_level_values('Acte'))

        # Afficher la valeur dans la boule pour le graphique initial
        for x, y, val in zip(data_visu['absi'], data_visu['ordo'], data_visu['vale']):
            ax.annotate(str(val), (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

        # Afficher la valeur dans la boule pour le total par personnage
        for personnage, total in data_visu['tota'].items():
            ax.annotate(str(total), (personnage, "Total"), textcoords="offset points", xytext=(0, 10), ha='center')

        # Légende pour les boules du total par personnage
        ax.legend()

        # Affichage du graphique
        plt.show()
        #print("temps de traitement = ", time.time()-t1)




        # Maintenant, vous pouvez afficher le graphe désérialisé
        #plt.show()
        st.pyplot()
        print('temps de traitement : ',time.time()-t1)
        
if __name__ == '__main__':
    main()


