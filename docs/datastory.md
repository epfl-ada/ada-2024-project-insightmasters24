---
layout: page
title: The Evolution of Gender and Ethnic Representation in Cinema
---

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

# Effects of Diversity on Movie Revenue 

Before further diving into our story, here is a picture of Patagonia, Argentina:

Isn’t it lovely ? 🥰 While Patagonia does not have anything to do with the project, studies suggest that reader’s attention tends to fade away after 6 minutes of reading. By putting an image of beautiful Patagonia, I wanted to surprise your brain and fully reengage you in the lecture of our story! (This method was used by an amazing Statistics professor at EPFL (sorry I forgot his name)  in the undergraduate course Probabilities & Statistics, and it has proven very efficient!)

<span style="color: red;">Back on the track!</span>

In order to convince you about the importance of diversity representation in cinema, take a look at the Spearman correlation matrix I made just for you 🥰 : 

{% include plots/gender_distribution.html %}

Just so that you know : computing the Spearman correlation instead of the Pearson correlation WAS a choice. In fact, Spearman correlation is better suited to detect monotonic, but not necessarily linear relationships, thus providing more robust results. “robuster”? “more robust”?   Well , you get the idea.

To further analyze the impact of gender representation, ethnic representation, and movie genres on movie revenue, we ran multiple linear regressions while focusing on the statistically significant effects.

To account for potential non-linearity caused by time dependence (e.g., a feature that strongly influenced revenue in 1900 may not have the same effect in 2000), we segmented our data into 5-year time periods. This approach allows us to capture how the influence of these features on movie revenue evolves over time.

The plots below showcase the most influential features for movies released in 1990, providing insights into the key factors driving box office performance during that specific period.

Notice some trends? Well, we do! In fact, while science fiction movies seem to have gained significant popularity in recent years, new themes—such as those centered around Jewish communities—have also emerged and grown in popularity since the early 2000s.

Interestingly, a somewhat thought-provoking trend can be observed in the 1990s, where movies exploring themes of politics and war found remarkable success, just as the world was emerging from the Cold War. 

Another amusing trend appears to be the popularity of movies showcasing the LGBTQ+ community by the end of the 20th century. While LGBTQ+ representation remained controversial at the time (as one can notice during the AIDS/HIV crisis between 1980 and 1990), there was however growing advocacy for visibility and rights. From our model, we can thus infer that this societal shift and progress in cultural values has opened the door for movies that explored LGBTQ+ themes to gain wider acceptance and curiosity.


## Local URLs in project sites {#local-urls}

When hosting a *project site* on GitHub Pages (for example, `https://USERNAME.github.io/MyProject`), URLs that begin with `/` and refer to local files may not work correctly due to how the root URL (`/`) is interpreted by GitHub Pages. You can read more about it [in the FAQ](https://beautifuljekyll.com/faq/#links-in-project-page). To demonstrate the issue, the following local image will be broken **if your site is a project site:**

![Crepe](/assets/img/crepe.jpg)

If the above image is broken, then you'll need to follow the instructions [in the FAQ](https://beautifuljekyll.com/faq/#links-in-project-page). Here is proof that it can be fixed:

![Crepe]({{ '/assets/img/crepe.jpg' | relative_url }})