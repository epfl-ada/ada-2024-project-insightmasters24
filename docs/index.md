---
layout: home
title: The Evolution of Gender and Ethnic Representation in Cinema
subtitle: Analyzing diversity trends in the film industry
---

# Motivation 

The evolution of gender, ethnic and other apparent physical features representation in cinema serves as a lens reflecting societal values and cultural shifts over decades. In this project, we seek to explore these dynamics by analyzing the physical characteristics of main actors—gender, ethnicity, sexual orientation, height, and age—across decades and genres, using the CMU movie summary corpus as our main data source. Together, we will investigate how specific archetypes emerge, evolve, and influence genre conventions and movie revenues, shedding light on diversity’s role in shaping audience engagement and the movie industry in general.
By examining trends in character archetypes in the movie industry, we aim to identify shifts in societal norms and values, allowing us to better understand the role of cinema in mirroring and potentially driving cultural changes.


# Introduction

Hello reader,  
Do you know that 5 out of 4 people struggle with math?  
...Wait, what?!  
    
While this joke has nothing to do with the project, something curious happens as you read this text. You probably hear a voice in your head—don’t worry, that’s just me, your narrator. I am here to guide you through this data story, where every number and insight reveals a new chapter. Follow me, I will be your tour guide.     

Let me brief you first : Did you notice that in today's movies, we see more and more characters representing diverse ethnicities, sexual orientations, gender identities, and physical features?    

The growing number of movies and TV shows featuring LGBTQ+ characters, diverse ethnicities, and varying gender identities reflects a significant shift in societal attitudes.  The modern audience, especially younger generations (Millennials and Gen Z), demand inclusivity and are willing to support films that reflect diverse experiences. And the movie industry understood the assignment!  According to a 2018 McKinsey & Company study and subsequent reports from the USC Annenberg Inclusion Initiative, movies with diverse casts consistently outperform those with less representation. In fact, films with casts that are 41–50% diverse earned, on average, $26.8 million more in global box office revenue compared to those with less than 11% diversity.    

Thankfully, today's society is more open and inclusive, embracing stories that represent a broader spectrum of human experiences. But was it always the case?    

Obviously not! Fifty or sixty years ago, representation of LGBTQ+ characters, racial diversity, and non-conforming gender identities in movies was far less common—and often met with strong resistance. Societal norms, censorship, and prejudices limited the stories that could be told and the characters that could be represented. In the United States, the Hays Code (1934–1968) regulated movie content, prohibiting explicit depictions of sexuality, “immoral” behavior, and any form of homosexuality, which was labeled as "sexual perversion." As a result, LGBTQ+ characters were either omitted, villainized, or their identities were subtly implied through coded language or stereotypes.    

By using movie revenue as a metric to assess how well a movie was received by the public, we aim to analyze the archetypes of characters portrayed in successful movies, shedding light on the audience's evolving interests and preferences, and thus offering insights into how societal norms and perceptions have shifted over the years.


# A few words on our analysis :

You’ve probably figured it out by now: our study relies heavily on movie revenue to uncover trends. And yes, I can already hear the criticism coming from miles away: “But how can you compare movies from different eras? You need to adjust for inflation and time value of money!"    

Relax, nerds, we’ve got you covered. To ensure our analysis is solid, we split the data into smaller time frames (5 years each). This allows us to draw meaningful conclusions while conveniently sidestepping the pesky effects of inflation and the changing value of money over time.

Alright, let’s get serious for a moment. Your concern is completely valid: by computing the Pearson correlation between movie revenue and release year, I found a correlation of 0.19, meaning that movie release date HAS an influence on revenue. This observation is made obvious simply by looking at the graph of average movie revenue per year - as recent movies tend to generate significantly higher revenues :

![Average Movie Revenue per Year](/assets/img/plots/Movie-revenue-per-year.png)

While such an increase can be explained by democratization of cinema over the years,  time value of money also plays an important role. In fact, we estimate that $100 in the early 1900’s corresponds to a purchasing power of nearly $3800 today!    

In order to account for all these effects, we chose to split our analysis into 5-year periods. This approach not only helps us overcome the inflation and other time-related issues, but also allows us to detect how the impact of each of our features (gender representation, ethnic representation, movie genre, etc.) on movie revenue evolves over time—because, as we’ll see, their influence isn’t static; it changes with the years!    

Moreover, due to data imbalance when it comes to movie release language, I decided to focus only on movies released in English (I would expect our model to fail to determine meaningful relationships between movie language and movie revenue anyways due to lack of data in some languages). WITNESS THE IMBALANCE ! 😱

![Average Movie Revenue per Year](/assets/img/plots/language-distribution-barplot.png)    


# Effects of Diversity on Movie Revenue : 

Before further diving into our story, here is a picture of Patagonia, Argentina :    

![Beautiful Patagonia](/assets/img/images/Patagonia.jpeg) 

Isn’t it lovely ? 🥰 While Patagonia does not have anything to do with the project, studies suggest that reader’s attention tends to fade away after 6 minutes of reading. By putting an image of beautiful Patagonia, I wanted to surprise your brain and fully reengage you in the lecture of our story! (This method was used by an amazing Statistics professor at EPFL (sorry I forgot his name)  in the undergraduate course Probabilities & Statistics, and it has proven very efficient!)    

<span style="color: red;">Back on the track!</span>

In order to convince you about the importance of diversity representation in cinema, take a look at the Spearman correlation matrix I made just for you 🥰 : 

![Spearman Corr](/assets/img/plots/spearman-corr-matrix.png)

Notice anything special ? The gender ratio, as well as the presence of some ethnicities such as actors from Jewish communities or African American ethnicities are positively correlated with the movie revenue (with a Spearman correlation of 0.20 and 0.26 respectively with movie revenue). Besides, movie genres seem also to affect the movie revenue, but I kept this chapter of our story  for later, so stay tuned!    

Ah! Just before I forget : computing the Spearman correlation instead of the Pearson correlation WAS a choice. In fact, Spearman correlation is better suited to detect monotonic, but not necessarily linear relationships, thus providing more robust results. “robuster”? “more robust”?   Well , you get the idea.    



![Gender distribution](/assets/img/plots/gender-distribution-pie.png)
