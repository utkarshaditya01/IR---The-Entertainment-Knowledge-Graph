import networkx as nx
import matplotlib.pyplot as plt
import csv
import numpy as np

class KnowledgeGraph():
    """
    Class to contain all the knowledge graph related code.
    """
    def similar_movies(self, language="Hindi", year="2020"):
        """
        Method to plot knowledge graph of 1000 Movies.
        """
        G = nx.MultiDiGraph()
        genres_read = []
        genres_colors = ['#5013ED', '#42853C', '#D4E907', '#2A257D', '#EF093B', '#8CA030', '#35B1DA', '#3F4F33', '#CAA341', '#B69BAE', '#E77FE2', '#9483F4', '#77DF5D', '#F3902F', '#E88182', '#713338', '#5CEFAB', '#863771', '#53EF26', '#FF80FF', '#6FF6FF']
        genres_color = {}
        color_map = []
        movies_genres = {}

        with open('final_dataset_imdb.csv',encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:  # Do not include the header from the data
                    line_count = 1
                    continue
                if row[3]!= year and row[8]!= language:
                    continue
                G.add_node(row[1])
                title = row[1]
                genres = list(row[5].split(", "))
                movies_genres[title]=genres
                for x in genres:
                    if x not in G:
                        G.add_node(x)
                        genres_read.append(x)
                        genres_color[x]=genres_colors[len(genres_color)]
                    G.add_edge(title, x)
                
                if line_count == 1000:
                    break
                line_count += 1

        edge_colors = [genres_color[e[1]] for e in G.edges]
        for node in G:
            if node in genres_read:
                color_map.append('blue')
            else: 
                hex_ = [genres_color[x] for x in movies_genres[str(node)]]
                avg = sum(list(map(lambda x: int(x[1:], 16), hex_)))//len(hex_)
                avg_color = f'#{avg:06x}'
                color_map.append(avg_color)

        plt.figure(figsize=(150,150))
        pos = nx.spring_layout(G,k=0.10,iterations=20)
        nx.draw(G, with_labels=True, node_color=color_map, edge_color=edge_colors, node_size = 4500, prog="dot", edge_cmap=plt.cm.Blues, font_size=16, pos=pos)
        plt.savefig("my_graph.pdf")
        print("\nPlease Check my_graph.pdf in the current code directory\n")
    
    def movie_details(self, title):
        """
        Method to plot detailed KG of a single movie.
        """
        G = nx.MultiDiGraph()
        color_map = []
        node_sizes = []
        colors = ['#5013ED', '#42853C', '#D4E907', '#2A257D', '#EF093B', '#8CA030', '#35B1DA', '#3F4F33', '#CAA341', '#B69BAE', '#E77FE2', '#9483F4', '#77DF5D', '#F3902F', '#E88182', '#713338', '#5CEFAB', '#863771', '#53EF26', '#FF80FF', '#6FF6FF']
        with open('final_dataset_imdb.csv',encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[2]==title:
                    row[1]=row[2]
                    a = row[1]
                    G.add_node(row[1])
                    color_map.append('red')
                    node_sizes.append(20000)
                    G.add_node(row[4])
                    color_map.append(colors[1])
                    node_sizes.append(7000)
                    G.add_edge(row[1],row[4], movie='Released on')
                    G.add_node("Genres")
                    color_map.append(colors[2])
                    node_sizes.append(7000)
                    G.add_edge(row[1],"Genres", movie='Genres include')
                    for i in list(row[5].split(", ")):
                        G.add_node(i)
                        color_map.append(colors[4])
                        node_sizes.append(7000)
                        G.add_edge("Genres", i)
                    G.add_node(row[6])
                    color_map.append(colors[5])
                    node_sizes.append(7000)
                    G.add_edge(row[1],row[6], movie='Duration(Mins)')
                    G.add_node(row[7])
                    color_map.append(colors[6])
                    node_sizes.append(7000)
                    G.add_edge(row[1],row[7], movie='Country released in')
                    G.add_node("Languages")
                    color_map.append(colors[7])
                    node_sizes.append(7000)
                    G.add_edge(row[1],"Languages", movie='languages released in')
                    count=0
                    for i in list(row[8].split(", ")):
                        G.add_node(i)
                        color_map.append(colors[18])
                        node_sizes.append(5000)
                        G.add_edge("Languages", i)
                        if count>4:
                            break
                        count+=1
                    G.add_node(row[9])
                    color_map.append(colors[8])
                    node_sizes.append(7000)
                    G.add_edge(row[1],row[9], movie='Directed by')
                    G.add_node("Cast")
                    color_map.append(colors[9])
                    node_sizes.append(7000)
                    G.add_edge(row[1],"Cast", movie='cast includes')
                    count=0
                    for i in list(row[12].split(", ")):
                        G.add_node(i)
                        color_map.append(colors[10])
                        node_sizes.append(5000)
                        G.add_edge("Cast", i)
                        if count>4:
                            break
                        count+=1
                    description = row[13]
                    G.add_node(row[14])
                    color_map.append(colors[11])
                    node_sizes.append(7000)
                    G.add_edge(row[1],row[14], movie='Rating')
                    break
                    
        plt.figure(figsize=(25,25))
        pos = nx.shell_layout(G)
        pos[a] = np.array([0, 0])
        nx.draw(G, with_labels=True, node_color=color_map, node_size = node_sizes, prog="dot", edge_cmap=plt.cm.Blues, font_size=20, pos=pos)
        edge_labels = nx.get_edge_attributes(G, 'movie')
        nx.draw_networkx_edge_labels(G, pos, labels=edge_labels, font_size=20)
        plt.savefig("movie_detail.pdf")
        print("Description of movie: ", description)
        print("\nPlease Check movie_detail.pdf in the current code directory\n")

    def movie_similarity(self, movie1, movie2):
        """
        Method to plot detailed KG of comparision of 2 movies.
        """
        G = nx.MultiDiGraph()
        color_map = []
        node_sizes = []
        with open('final_dataset_imdb.csv',encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[2]==movie1:
                    row[1]=row[2]
                    a=row[1]
                    movie1row = row
                    break
        with open('final_dataset_imdb.csv',encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                
                if row[2]==movie2:
                    row[1]=row[2]
                    b=row[1]
                    G.add_node(row[1])
                    color_map.append('red')
                    node_sizes.append(20000)
                    G.add_node(movie1row[1])
                    color_map.append('red')
                    node_sizes.append(20000)
                    
                    genres = list(row[5].split(", "))
                    for x in genres:
                        if x not in G:
                            G.add_node(x)
                            color_map.append('yellow')
                            node_sizes.append(7000)
                        G.add_edge(row[1], x)
                    genres = list(movie1row[5].split(", "))
                    for x in genres:
                        if x not in G:
                            G.add_node(x)
                            color_map.append('yellow')
                            node_sizes.append(7000)
                        G.add_edge(movie1row[1], x)
                    
                    count=0
                    for i in list(row[8].split(", ")):
                        if i not in G:
                            G.add_node(i)
                            color_map.append('blue')
                            node_sizes.append(7000)
                        G.add_edge(row[1], i)
                        if count>4:
                            break
                        count+=1
                    count=0
                    for i in list(movie1row[8].split(", ")):
                        if i not in G:
                            G.add_node(i)
                            color_map.append('blue')
                            node_sizes.append(7000)
                        G.add_edge(movie1row[1], i)
                        if count>4:
                            break
                        count+=1
                    
                    G.add_node(row[9])
                    color_map.append('green')
                    node_sizes.append(7000)
                    G.add_edge(row[1], row[9])
                    if movie1row[9] not in G:
                        G.add_node(movie1row[9])
                        color_map.append('green')
                        node_sizes.append(7000)
                    G.add_edge(movie1row[1], movie1row[9])
                    
                    break
                    
            plt.figure(figsize=(35,35))
            pos = nx.planar_layout(G)
            pos[a] = np.array([1, 0]) 
            pos[b] = np.array([-1, 0]) 
            nx.draw(G, with_labels=True, node_color=color_map, node_size = node_sizes, prog="dot", edge_cmap=plt.cm.Blues, font_size=16, pos=pos)
            plt.savefig("movie_similarity.pdf")
            print("\nPlease Check movie_similarity.pdf in the current code directory\n")
            
    def movie_recommend(self, movie1):
        """
        Method to return list of best matching movies based on a ranking system.
        """
        with open('final_dataset_imdb.csv',encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[2]==movie1:
                    movie1row = row
                    break
                    
        with open('IMDB_movies.csv',encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            best_score = 0
            best_movies = []
            best_movie = ''
            linen = 0 
            for row in csv_reader:
                if linen == 0:
                    linen = 1
                    continue
                if movie1row[1]==row[1] or int(row[15])<5000 or int(row[3])<1950:
                    continue
                score = 0 
                if movie1row[3] == row[3]:
                    score = score + 2
                genresa1 = list(movie1row[5].split(", "))
                genresb1 = list(row[5].split(", "))
                genres1 = set(genresa1)
                genres2 = set(genresb1)
                score = score + 7*len(genres1.intersection(genres2)) 
                diff = len(genres1.union(genres2))-len(genres1.intersection(genres2))
                score = score - diff
                if row[7] == movie1row[7]:
                    score=score+1
                languages1a = list(movie1row[8].split(", "))
                languages1b = list(row[8].split(", "))
                languages1 = set(languages1a)
                languages2 = set(languages1b)
                score = score + 1*len(languages1.intersection(languages2))
                
                if row[9] == movie1row[9]:
                    score=score+3
                
                if row[10] == movie1row[10]:
                    score=score+3
                
                actors1a = list(movie1row[12].split(", "))
                actors1b = list(row[12].split(", "))
                actors1 = set(actors1a)
                actors2 = set(actors1b)

                score = score + 4*len(actors1.intersection(actors2))
                if row[11] == movie1row[11]:
                    score=score+3

                score = score + 0.00000000000001*float(row[15])
                if (len(best_movies)<10):
                    best_movies.append((score, row[2]))
                
                best_movies = sorted(best_movies, reverse=True)
                
                if best_movies and score>best_movies[-1][0]:                   
                    best_movies.pop(-1)                    
                    best_movies.append((score, row[2]))
                
                if score>best_score:
                    best_score=score
                    best_movie=row[2]

        nn =1
        for i in best_movies:
            print("Rank ",nn,"==> ",i[1] , "\nScore: " , i[0] ,"\n")
            nn=nn+1
        print("\nBest movie match is :", best_movie, "\n")
        

if __name__ == "__main__":
    """
    Command line user interface with different options.
    """
    KG = KnowledgeGraph()
    while True:
        option = int(input("1. Enter 1 for movie detail graph\n2. Enter 2 for movie similarity graph between 2 movies.\n3. Enter 3 for knowledge graph of 1000 movies.\n4. Enter 4 for Movie Recommendations(Top 10 along with score)\n5. Enter 0 to exit\n"))
        if option == 0:
            exit()
        elif option == 1:
            movie_name = input("Enter Movie Name(Case Sensitive): ")
            try:
                KG.movie_details(movie_name)
            except:
                print("Movie not found in database. Check movie name again along with case.")
        elif option == 2:
            movie_1 = input("Enter Movie Name 1(Case Sensitive): ")
            movie_2 = input("Enter Movie Name 2(Case Sensitive): ")
            try:
                KG.movie_similarity(movie_1, movie_2)
            except:
                print("Movie/movies not found in database. Check movie names again along with case.")
        elif option == 3:
            year = input("Enter Year: ")
            language = input("Enter Language(first letter capital): ")
            KG.similar_movies(language=language, year=year)
        elif option == 4:
            movie_name = input("Enter Movie Name(Case Sensitive): ")
            try:
                KG.movie_recommend(movie_name)
            except:
                print("Movie not found in database. Check movie name again along with case.")
        