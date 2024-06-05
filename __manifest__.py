{
    'name': 'Gestion Clinique',
    'summary': 'Gérer les rendez-vous, les dossiers médicaux et les factures dans une clinique.',
    'description': 'Ce module permet de gérer les opérations de base d\'une clinique médicale, y compris les rendez-vous, les diagnostics, les ordonnances et la facturation.',
    'author': 'elfdil meryem',
    'category': 'Santé',
    'version': '1.0',
    'depends': ['base','web'],
    'application': True, 
    'data':[
        ###secrity
        'security/ir.model.access.csv',
        
         ###views
        'views/patient.xml',
        'views/rendezvous.xml',
        'views/fichier.xml',
        'views/medecin.xml',
 
        'views/ordonnance.xml',
        'views/symptome.xml',
        'views/medicament.xml',
        'views/maladie.xml',
        'views/operation.xml',
        'views/horaire.xml',     
        'views/diagnostic.xml',
        'views/paiment.xml',
        'reports/diagno_temp.xml',
        'reports/diagnostic_p_viewq.xml',
        'reports/ordonnance_temp.xml',
        'reports/ordonnance_p_view.xml',
        'reports/paiment_temp.xml',
        'reports/paiment_p_view.xml',
        

        
        

   
        ###menus
        'views/menu.xml',

  ] ,
        'installable': True,
        'application': True,     
  
}
 
