# Unique Meal-plan Prepration  
### Short Summary    
Abstract— In the project, we took a nutrition value dataset (which is in csv format) and created a bipartite graph from this dataset. In this graph, one level will be having all ingredients lined up and the other level with the nutrient values. These two levels are connected based on the edge list values the components shared. Upon this graph, we performed Deep-Walk embedding and then K-Means clustering to group similar food items together.  

### Why this Project ?  
According to a survey most of the adults in the United States have specific eating patterns otherwise also known as special diets for the purpose of eating patterns, allergies, or disease they are suffering from. That means they must follow some dietary restrictions while preparing the meals by avoiding or substituting the ingredients they are allergic to. Also, we have often seen many individuals with vivid diseases, illnesses, and allergies. There can never be one stipulated medical methodology that caters to all problems. Different sicknesses have different medical charts and different proportions of doses. When covid had hit the nerve of the world, more than 30% of the deaths accounted for during that time did not cause mortality due to corona, but for other diseases which were heightened due to Corona. We all lost somebody in that span of 2 years, and are grateful to be doing well now, but it left us thinking, how better could we be on a personal level? We cannot create a magical potion that will help anyone and everyone, but we thought of getting changes to dietary routines with this project. Our model will help them to find a substitute for the ingredient they are allergic to and keep the recipes the same. This model can be used in hospitals to prepare meals for the patient without much human intervention in deciding the recipes.    

### ~Future Scope~ Current Stage  
We plan to expand on this project by further introducing an allergy or dietary restriction dataset( now using 1Million Recipie datset). Seeking knowledge from this dataset, it will act as another bias in our embedding stage. This new dataset will be another level in the bipartite graph, making it a tripartite graph. With this graph structure, we will be enhancing the clustering algorithm by introducing Graph Neural Networks or GANs. We are further deciding upon other technologies that need to be used as per the convenience. We also wish to add a recipe preparation model that will take care of minute nutrient values and consider the surrounding situations like broiling a vegetable will cause a loss in nutrients than in its raw form.  

### Requirements:  
scikit-learn == 1.0.2  
pandas == 1.4.1  
numpy == 1.22.2  
matplotlib == 3.5.1  
matplotlib-inline == 0.1.3  
seaborn == 0.11.2  
[gembed](https://github.com/pranavacharya/graph_embedding) == 1.0.2  

### Created package - [gembed](https://github.com/pranavacharya/graph_embedding)  
