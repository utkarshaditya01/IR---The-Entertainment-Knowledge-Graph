----------------------------------------------------------
Group Members
----------------------------------------------------------
1)  Name: Utkarsh Ajay Aditya   Roll Number: S20180010182
    Name: Abhinav Talari        Roll Number: S20180010003

----------------------------------------------------------
Commands to run
----------------------------------------------------------
1) Install Python Libraries using the below command

pip install -r requirements.txt

NOTE : After viewing a PDF file please close it or else, it might give access denied permission error since the PDF would be open somewhere else.

2) Run below command to run any python code file
 
python filename.py

----------------------------------------------------------
Basic Setup of the IR System
----------------------------------------------------------
DOMAIN of project :  Entertainment (Movies, television programs and celebrity content)

NOTE : Scraping is not a task, we have just mentioned the scraping details. Tasks start from point no 2 for each individual.


INDIVIDUAL TASKS performed by Utkarsh Ajay Aditya(S20180010182)

	1) Web Scraping(Movies) : imdb_moviedata_scrape.py for scraping movie details of over 83,000 movies and storing it in final_dataset.csv

	2) Knowledge Graph for Movies(All its attributes and relationships) : KnowledgeGraph_movies_recommender_system.py defines 3 different types of knowledge graph
	structures related to movies:
		a) Movie detail graph for a single movie
		b) Movie Comparasion graph between two movies.
		c) Knowledge graph of 1000 movies. 
	It works on the basis of final_dataset_imdb.csv . Detailed analysis given in report.pdf
	
	3) Movie Recommendation System : KnowledgeGraph_movies_recommender_system.py also has the movie recommender code part, which returns a ranked list of 
	recommendations for a given input movie name.

	4) Spell Correction for the entertainment domain : Entertainment_domain_spell_correction.py is an autocorrect program file to correct incorrect 
		a) movie name or TV series name
		b) actors/actresses name
		c) director/write name

  
INDIVIDUAL TASKS performed by Abhinav Talari(S20180010003)

	1) Web Scraping(Actors) : Scraper_For_Actors.py for scraping actor data from wikipedia and storing it.

	2) Knowledge Graph for Actors(All its attributes and relationships) : Knowledge_Graph_for_Actors.py defines KG related code for actors.
	The actor dataset was tokenized and the Entity-Relation-Entity were identified and put into the Knowledge Graph.

	3) Ranked Retrival model(Actors) : RankedRetrieval_actors.py has the ranked model based on tfidf ranking which returns set of documents
	on basis of their score. 