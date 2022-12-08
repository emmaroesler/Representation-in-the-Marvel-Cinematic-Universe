import pybase64
import datetime
import pyexcel
from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd
import os
import json
import dash_bio
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#images
#age of ultron gender representation
def images(filename):
    with open(filename,'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + pybase64.b64encode(image).decode('utf-8')

#movie table
def generate_table(tab):
    df = pd.read_csv('Movie Sales.csv')
    rows=[]
    hold=pd.DataFrame({'A' :[]})
    rep_rank = tab+' Rank'
    rep_score = tab+' Rating'
    for i in range(35):
        if tab != 'Sexuality' or i < 9:
            if not hold.empty:
                row=[html.Td(i)]
                row.append(html.Td(hold['movie']))
                row.append(html.Td(hold[rep_score]))
                hold = pd.DataFrame({'A' :[]})
            else:
                row=[html.Td(i + 1)]
                temp=df[df[rep_rank] == i+1]
                if len(temp) == 2:
                    hold = temp.iloc[1]
                    temp2 = temp.iloc[0]
                    row.append(html.Td(temp2['movie']))
                    row.append(html.Td(temp2[rep_score]))
                else:
                    row.append(html.Td(temp['movie']))
                    row.append(html.Td(temp[rep_score]))
            rows.append(html.Tr(row))
        else:
            temp=df[df[rep_rank] == i+1]
            for i in range(len(temp)):
                temp2 = temp.iloc[i]
                row=[html.Td(10)]
                row.append(html.Td(temp2['movie']))
                row.append(html.Td(temp2[rep_score]))
                rows.append(html.Tr(row))
    return html.Table(
        [html.Tr([html.Th('Rank'), html.Th("Movie"), html.Th('Score')])]+
        rows
    )

DATAPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

app = Dash(__name__)

app.layout = html.Div(children=[
        html.Header(
        id='header',
        className='app-header',
        children=[
            html.H1('Representation in the Marvel Cinematic Universe'),
            html.H2('By Emma Roesler'),
            html.H4("Fall 2022 Honors Thesis")
    ]),
        html.Div(
        id = 'body',
        className='app-body',
        children=[
#Representation
            html.H2('Gender, Race, and Sexuality'),
            dcc.RadioItems(
                id="rep_choice",
                options=["All Characters", "Only Main Characters", "Only Side Characters"],
                value = "All Characters",
                style={'font-family':'Tahoma'},
                inline=True
            ),
            dcc.Dropdown(
                id="dropdown",
                options=[
                    {"label":html.Div(['Gender']),
                     "value":"Gender",},
                    {"label":html.Div(['Race']),
                     "value":"Race",},
                    {"label":html.Div(['Sexuality']),
                     "value":"Sexuality",},],
                value="Gender",
                style={'font-family':'Tahoma'},
                clearable=False
                ),
#            dcc.Checklist(
#                 id="rep_panther",
#                 options=["Omit Black Panther Characters"],
#                 style={'font-family':'Tahoma'},
#                 inline=True
#             ),
            html.Div([
                dcc.Graph(id="rep_bar_graph", style={'display': 'inline-block'}),
                dcc.Graph(id="rep_time_graph", style={'display': 'inline-block'}),
                ]),
            html.Div(
                id='single_representation',
                className='control-tabs',
                children=[
                    dcc.Tabs(id='rep-tabs', value='what-is', children=[
                        dcc.Tab(
                            label='Gender',
                            value='what-is',
                            children=html.Div(className='control-tab', children=[
                                html.H3(className='what-is', children='Gender'),
                                html.P("It is no secret that superhero franchises have been dominated by men and that women are clearly underrepresented. However, despite advancements in the film industry, the Marvel Cinematic Universe remains problematic and the majority of movies either completely fail or barely pass the Bechdel test. In the franchise, women have mainly appeared in one of four primary roles. The first role is that of the assistant. Women in this role exist to make the lives of main characters easier. These women typically have no life outside of their role in relation to the main character and lack depth. Pepper Potts often falls into this role as her literal job description was Tony Stark’s assistant."),
                                html.P("The second primary role women fall into is known as being a “woman in a refrigerator.” Women in this role are depowered in some way via rape, torture, kidnapping, murder, or some other form of injury to advance the story of a man, usually a main character. These women are the classic damsels in distress that are unable to save themselves. Typically, the only reason they suffer is to inspire or influence the hero in some way. Like the classic assistant role, women in this role are usually two-dimensional. While Gamora, a member of the Guardians of the Galaxy, is a main character, her death in Avengers: Infinity War was used to justify Peter Quill’s actions and advance the plot."),
                                html.P("The emotionally unavailable warrior is a third trope to which women frequently fall victim. Women are typically seen as emotional and unable to control their feelings. So, it is not a surprise that in an effort to appear progressive, writers often rid women of emotions altogether. Valkyrie is a prime example of this as she is simply too tough for emotions. She is emotionally distant and does not connect with other characters in the film. Women who fall into this category often have traumatic pasts that involve brutal murders, rape, or some other form of violence."),
                                html.P("Finally, the infantilization and hypersexualization of female characters occurs frequently in the Marvel franchise. Almost every woman, even those who fall victim to previously discussed tropes, is seen as a sex object, a child, or both. The love interest of the hero is often hypersexualized with slow motion scenes and hair that is somehow always being blown by a breeze. These women are defined by their role as a potential girlfriend or wife. For Steve Rogers, Peggy Carter fits this role. Conversely, there is also a trend of classifying women as children. Despite being in charge of technological innovations for all of Wakanda and her legal status as an adult, Shuri is seen as a child and the viewer is often reminded of how young she is. "),
                                html.Img(id='bw_aou_img', src=images('bw_aou.png')),
                                html.H3(className='what-is', children='Avengers: Age of Ultron'),
                                html.H4(className='what-is', children='Natasha Romanoff'),
                                html.P("Natasha Romanoff, Black Widow, makes her first appearance in Iron Man 2 (2010). It quickly becomes apparent to the viewer that she falls into the hypersexualized woman stereotype. The superpowers that she has in the comic books are disregarded to make Tony Stark appear more important as the only superhero in the film. Avengers: Age of Ultron (2015) only furthers this narrative. Natasha fights in a low-cut, skin-tight suit with little-to-no protective armor or padding. Her bright red hair is kept down for the entirety of the movie, inhibiting her sight in several scenes and her boots have 3 inch heels."),
                                html.P("It’s visually apparent that Natasha Romanoff is seen as an object, and her actions support her objectification. In the first scene of the movie, we see Natasha leave a fight to find the Hulk, who needs her to turn back into Bruce Banner. Later, Natasha gets kidnapped and sits patiently in her cage until Bruce comes to her rescue. Rather than taking her to join the fight, he insists that she rest because she’s too traumatized. The movie concludes with the Hulk disappearing on a jet and Natasha pleading with him to come back to her. This reductionistic view centers Natasha’s character around what she can do for Bruce."),
                                html.P("In addition to being his “calming presence,” Natasha also spends the film flirting with Bruce and trying to get him to start a relationship with her. This dynamic peaks when Bruce tells Natasha that he can’t be in a relationship because the Hulk is unpredictable. Natasha responds by revealing that Bruce isn’t “the only monster in the room” and that she was sterilized as part of her training. The reduction of a woman to her reproductive abilities is obviously troubling and the objectification is very clear."),
                                html.Img(id='sw_aou_img', src=images('sw_aou.jpeg')),
                                html.H4(id='wanda', className='what-is', children='Wanda Maximoff'),
                                html.P("Wanda Maximoff, the Scarlet Witch, is arguably the most powerful character in the Marvel Cinematic Universe. But, the trauma that her character suffers is used to justify her routine infantilization. Besides a post-credit scene, Wanda first appears in Avengers: Age of Ultron. Almost immediately, her character is described by Steve Rogers as “young and enhanced.” Wanda demonstrates her power by single-handedly incapacitating the Avengers, stopping a moving train, destroying countless robots, and ripping out a heart. Yet, she is the only character to suffer an emotional breakdown during the final fight and relies on a pep-talk from Clint Barton, arguably one of the least powerful characters. This reliance on male, paternal characters becomes a theme for Wanda throughout multiple movies."),
                                html.H3(id='infinity_war', className='what-is', children='Avengers: Inifinity War'),
                                html.Img(id='bw_aiw_img', src=images('bw_aiw.png')),
                                html.H4(className='what-is', children='Natasha Romanoff'),
                                html.P("In Avengers: Infinity War (2018), Natasha Romanoff fades into the background while remaining hypersexualized. She still wears a tight, low-cut outfit, but is given more padding and armor than in the previous movies. Additionally, her hair is a short, blonde bob that is slightly more practical for battle. Natasha spends most of the movie following Steve Rogers. While she fights in the important scenes, she is given no character development or significant plot points."),
                                html.P("Natasha Romanoff appears in 7 movies from Iron Man 2 to Avengers: Endgame, but only given a total of 1 hour 49 minutes 45 seconds of screen time (Olufidipe & Echezabal). Natasha plays the textbook role of a strong, token-female warrior. She is portrayed as being “too strong” to succumb to emotions like other women and she has very little emotional range. While her ability to procreate is not a focus of the film, she falls into another stereotype as the woman who is too tough to have feelings."),
                                html.Img(id='sw_aiw_img', src=images('sw_aiw.jpeg')),
                                html.H4(className='what-is', children='Wanda Maximoff'),
                                html.P("Wanda Maximoff first appears in Avengers: Infinity War with her love interest, Vision. The couple is attacked by two of Thanos’ children while walking on the street. With her incredible power, Wanda should have been able to defeat the attackers completely on her own, but this is not the case. As Wanda and Vision are about to be defeated, Captain America makes a heroic appearance, rescuing both of them. The directors, Anthony and Joe Russo, later admitted that the scene was intentionally created to give Steve Rogers a “grand entrance” (Olufidipe & Echezabal). As a result, Wanda’s character is once again reliant on male characters to protect both her and her loved ones."),
                                html.P("Her infantilization also continues throughout the film as characters discuss ways to stop Thanos and protect Vision, the possessor of the mind stone. Rather than asking Wanda, the most powerful avenger, her opinion, other characters talk around her and make decisions on her behalf. It is decided that Wanda will stay in a secure location with Vision during the main fight and only take action to protect or kill him. Wanda makes the decision to leave the location upon seeing the massacre that Thanos is creating. Within seconds of her arrival at the scene, the battle’s tide begins to turn. Despite the implication that Wanda is too young and immature to make important decisions, she murders Vision to protect humanity. Her sacrifice and trauma ultimately do not matter after Thanos uses the time stone to reverse Vision’s death and tear the mind stone from his head, killing him again. Wanda turns to dust shortly after and is not given the opportunity to process her trauma until much later in WandaVision (2021)."),
                            ])),
                        dcc.Tab(
                            label='Race',
                            children=html.Div(className='control-tab', children=[
                                html.H3(className='what-is', children='Race'),
                                html.Img(id='race_img', src=images('race_img.png')),
                                html.P("Much like gender, non-white people are underrepresented. While people of color are proportionally better represented than women, this is only because there are more non-white side characters. The representation of people of color is significantly worse when looking at only main characters. Additionally, most of the non-white main characters are from films like the Black Panther and Shang-Chi."),
                                html.P("Typically, people of color are side characters that fall into several categories. If they are not angry thugs working for a main villain, they are typically the supporting character for a main superhero. Sam Wilson, the Falcon, and James Rhodes, War Machine, often appear on screen to inspire Captain America and Iron Man. They crack a few jokes and go into battle to back up the star of the movie. These characters rarely interact with one another and primarily exist as the two-dimensional friend of the main character."),
                                html.P("There are several exceptions to these stereotypes, most of which appear in more recent films. Black Panther, Shang-Chi, the Eternals, and the Falcon and the Winter Soldier are all Marvel productions that feature a person of color as the hero. Notably, many of these heroes have scenes where they discuss the importance of their race or heritage. The other main exception to the stereotypes is Nick Fury. Unfortunately, he is portrayed as secretive, untrustworthy, and skeptical. While Nick Fury is a spy, these traits are highlighted and emphasized more than his white counterparts (Moon). He even manipulates the death of beloved Phil Coulson to get what he wants and unite the Avengers. Meanwhile, Tony Stark is able to maintain his moral fortitude despite creating a robot that killed millions of people and selling nuclear weapons."),
                            ])),
                        dcc.Tab(
                            label='Sexuality',
                            children=html.Div(className='control-tab', children=[
                                html.H3(className='what-is', children='Sexuality'),
                                html.Img(id='sexuality_img', src=images('sexuality_img.png')),
                                html.P("There are only eight characters in the Marvel Cinematic Universe that are confirmed members of the LGBTQ+ community. Loki first appeared on screen in 2011, Korg and Valkyrie in 2017, and Phastos and Sylvie in 2021. The other three characters are side characters all appearing in 2021 or later. Despite Loki, Korg, and Valkyrie’s early appearances, none of their sexualities were confirmed until 2021. Notably, all five main characters are not human. While their sexuality is not villainized and there is not any blatant homophobia, the subliminal message being conveyed is that homosexuality is unnatural and inhuman. Furthermore, there has yet to be a transgender, non-binary, or gender non-conforming character in the MCU. This complete lack of representation speaks for itself. When it comes to sexuality, Marvel has a long way to go."),
                                html.P("Unfortunately, there is very little to analyze when it comes to the representation of sexuality in the Marvel Cinematic Universe because of how little representation exists. While the sexuality of some characters is implied, it remains unconfirmed. This could be because their sexuality does not influence the plot, or it could be because the writers and/or directors do not want to upset their viewers. While the unwillingness to upset homophobic viewers is extremely disappointing, there could also be other issues at play. A lack of LGBTQ+ writers and directors involved in Marvel films make it difficult for LGBTQ+ characters to be portrayed in a positive way or be portrayed at all. Representation extends beyond the characters and is vital throughout all parts of the filmmaking process."),
                            ]))
                    ])
                ]),
            
#Intersectionality
            html.H2('Intersectionality'),
            dcc.Checklist(
                id="checklist",
                options=["Gender", "Race", "Sexuality"],
                value=["Gender"],
                style={'font-family':'Tahoma'},
                inline=True
            ),
            html.Div([
                dcc.Graph(id="int_pie_graph", style={'display': 'inline-block'}),
                dcc.Graph(id="int_bar_graph", style={'display': 'inline-block'}),
                ]),
            html.Div(
                id='intersectionality',
                children=[
                    html.P("Intersectionality is a framework for analyzing how a person’s social and political identities interact with one another and impact the person as a whole. For example, a black woman faces discrimination because of her gender and her race, but a white woman only faces discrimination for her gender. Individuals with multiple marginalized identities must face multiple oppressive societal structures. When looking at any societal issue, it is important to acknowledge intersectionality. If one were to attempt to solve sexual harassment in the workplace by focusing solely on gender, they would overlook the role that race and sexuality play."),
                    html.P("When looking at representation in Marvel films, it is important to acknowledge intersectionality for a similar reason. Valkyrie and Monica Rambeau’s Captain Marvel are some of the first black female superheroes in the MCU, appearing in 2017 and 2019 respectively. That is close to a decade after the first movie in the Marvel Cinematic Universe was released. In total, there are the same number of white women and women of color in the MCU, but it is much easier to think of white female superheroes. When looking at white men, there are almost twice the amount of white men compared to men of color and three times the amount compared to women of color."),
                    html.P("Unfortunately, there are simply not enough members of the LGBTQ+ community to comprehensively examine the role of sexuality in intersectionality. From the little representation that does exist, gender in the community is evenly divided and there are more people of color in the community than white people. As a whole, straight white men are the dominant demographic represented in the MCU. They make up almost half of all Marvel characters. The lack of intersectional representation in the MCU suggests that it is not a priority for the directors, writers, and producers of the films. This makes sense considering that those career fields are dominated by straight white men."),
                ]),
#Morality
            html.H2('Morality'),
            dcc.Dropdown(
                id="mor_dropdown",
                options=["Gender", "Race", "Sexuality"],
                value="Gender",
                style={'font-family':'Tahoma'},
                clearable=False,
            ),
            html.Div([
                dcc.Graph(id="mor_bar_graph", style={'display': 'inline-block'}),
                dcc.Graph(id="mor_pie_chart", style={'display': 'inline-block'}),
                ]),
            html.Div(
                id='Morality_representation',
                className='cont-tabs',
                children=[
                    html.Img(id='villian_img', src=images('villians.jpeg')),
                    html.P("There are more evil men than evil women. This is likely because of the stereotypes about women that are present in the MCU. Women are often portrayed as innocent or child-like while frequently filling the role of the helpful assistant or love interest. Additionally, there are many cases in which women are placed in films to motivate the main superhero by playing the damsel in distress. Their characters are created to be victims of the villian. These character traits do not lend themselves to evil."),
                    html.P("Marvel villains are often cool and calculated. While fueled by rage, they are smart and intentional about their actions. Women are characterized as irrational and overly emotional, a direct contradiction to Marvel’s villain archetype. Finally, because women are defined by their relationship to men, they tend not to be fully developed as characters. Without a tragic backstory or internal struggle, this lack of depth makes it difficult for women to be compelling villains."),
                    html.P("There are more evil white people than evil people of color both numerically and proportionally. Similar to women, this could be because people of color are often the moral support for a main character. As a result, their character is underdeveloped and lacking the proper backstory to be a quality villain. All of the evil characters in the MCU have been straight. Like the representation of sexuality in general, this is likely the result of a lack of representation in the film industry as a whole. "),
                ]),
            
            html.H2('Representation in Movies'),
            dcc.Dropdown(
                id="rating_dropdown",
                options=[
                    {"label":html.Div(['Gender']),
                     "value":"Gender",},
                    {"label":html.Div(['Race']),
                     "value":"Race",},
                    {"label":html.Div(['Sexuality']),
                     "value":"Sexuality",},
                    {"label":html.Div(['Overall']),
                     "value":"Overall",},],
                value="Gender",
                style={'font-family':'Tahoma'},
                clearable=False
                ),
            dcc.RadioItems(
                id="score_choice",
                options=["Critic Score", "Audience Score"],
                value = "Critic Score",
                style={'font-family':'Tahoma'},
                inline=True
            ),
            dcc.Graph('rating_table'),
            html.Div(
                id='movie_rep',
                className='cont-tabs',
                children=[
                    dcc.Tabs(id='rating-tabs', value='what-is', children=[
                        dcc.Tab(
                            label='Gender',
                            value='what-is',
                            children=html.Div(className='cont-tab', children=[
                                html.H4(id='movies1',className='what-is', children='Movies by Gender'),
                                html.Div(id='table', children=[generate_table('Gender')]),
                                html.P('In terms of critic score, the only film that is rated noticeably lower than the other films is Eternals. The film is ranked 3rd in sexuality, 8th in race and 27th in gender. While the gender ranking is low, the film features a woman of color as the main character. Outside of this film, there is not a significant discernable pattern relating representation and critic rating. This could be because the critic rating reflects the opinions of critics from different demographics. Critics are predominantly straight white men, but the ratings of other critics may have countered some bias. Further research should be done to examine the impact of critic demographics on reviews.'),
                                html.P('In terms of audience score, the only ratings that are noticeably lower than others are Ms. Marvel and She Hulk: Attorney at Law. While Captain Marvel did not rank high, both MCU productions center around a strong female superhero. Barring these productions, there is not an apparent trend relating audience rating to representation. Like the critic score, the audience score is not broken down by demographic. This should also be examined in future research.'),
                                html.P('Finally, when evaluating the relationship between representation and relationships, more research should be done on how characters are represented. Black Panther features many strong women, but the main superhero is a man. This differs from Captain Marvel, a male dominated movie with a female main superhero. The role that characters have may influence audience reviews or critic reviews more than the quantitative representation.'),
                                html.Img(id='mcu_rep_img', src=images('mcu_rep.png'), width=600),
                            ])),
                        dcc.Tab(
                            label='Race',
                            children=html.Div(className='cont-tab', children=[
                                html.H4(id='movie2',className='what-is', children='Movies by Race'),
                                html.Div(id='table2', children=[generate_table('Race')]),
                                html.P('In terms of critic score, the only film that is rated noticeably lower than the other films is Eternals. The film is ranked 3rd in sexuality, 8th in race and 27th in gender. While the gender ranking is low, the film features a woman of color as the main character. Outside of this film, there is not a significant discernable pattern relating representation and critic rating. This could be because the critic rating reflects the opinions of critics from different demographics. Critics are predominantly straight white men, but the ratings of other critics may have countered some bias. Further research should be done to examine the impact of critic demographics on reviews.'),
                                html.P('In terms of audience score, the only ratings that are noticeably lower than others are Ms. Marvel and She Hulk: Attorney at Law. While Captain Marvel did not rank high, both MCU productions center around a strong female superhero. Barring these productions, there is not an apparent trend relating audience rating to representation. Like the critic score, the audience score is not broken down by demographic. This should also be examined in future research.'),
                                html.P('Finally, when evaluating the relationship between representation and relationships, more research should be done on how characters are represented. Black Panther features many strong women, but the main superhero is a man. This differs from Captain Marvel, a male dominated movie with a female main superhero. The role that characters have may influence audience reviews or critic reviews more than the quantitative representation.'),
                                html.Img(id='mcu_rep_img1', src=images('mcu_rep.png'), width=600),
                            ])),
                        dcc.Tab(
                            label='Sexuality',
                            children=html.Div(className='cont-tab', children=[
                                html.H4(id='movie3',className='what-is', children='Movies by Sexuality'),
                                html.Div(id='table3', children=[generate_table('Sexuality')]),
                                html.P('In terms of critic score, the only film that is rated noticeably lower than the other films is Eternals. The film is ranked 3rd in sexuality, 8th in race and 27th in gender. While the gender ranking is low, the film features a woman of color as the main character. Outside of this film, there is not a significant discernable pattern relating representation and critic rating. This could be because the critic rating reflects the opinions of critics from different demographics. Critics are predominantly straight white men, but the ratings of other critics may have countered some bias. Further research should be done to examine the impact of critic demographics on reviews.'),
                                html.P('In terms of audience score, the only ratings that are noticeably lower than others are Ms. Marvel and She Hulk: Attorney at Law. While Captain Marvel did not rank high, both MCU productions center around a strong female superhero. Barring these productions, there is not an apparent trend relating audience rating to representation. Like the critic score, the audience score is not broken down by demographic. This should also be examined in future research.'),
                                html.P('Finally, when evaluating the relationship between representation and relationships, more research should be done on how characters are represented. Black Panther features many strong women, but the main superhero is a man. This differs from Captain Marvel, a male dominated movie with a female main superhero. The role that characters have may influence audience reviews or critic reviews more than the quantitative representation.'),
                                html.Img(id='mcu_rep_img2', src=images('mcu_rep.png'), width=600),
                            ])),
                        dcc.Tab(
                            label='Overall',
                            children=html.Div(className='cont-tab', children=[
                                html.H4(id='movie4',className='what-is', children='Movies Overall'),
                                html.Div(id='table4', children=[generate_table('Overall')]),
                                html.P('In terms of critic score, the only film that is rated noticeably lower than the other films is Eternals. The film is ranked 3rd in sexuality, 8th in race and 27th in gender. While the gender ranking is low, the film features a woman of color as the main character. Outside of this film, there is not a significant discernable pattern relating representation and critic rating. This could be because the critic rating reflects the opinions of critics from different demographics. Critics are predominantly straight white men, but the ratings of other critics may have countered some bias. Further research should be done to examine the impact of critic demographics on reviews.'),
                                html.P('In terms of audience score, the only ratings that are noticeably lower than others are Ms. Marvel and She Hulk: Attorney at Law. While Captain Marvel did not rank high, both MCU productions center around a strong female superhero. Barring these productions, there is not an apparent trend relating audience rating to representation. Like the critic score, the audience score is not broken down by demographic. This should also be examined in future research.'),
                                html.P('Finally, when evaluating the relationship between representation and relationships, more research should be done on how characters are represented. Black Panther features many strong women, but the main superhero is a man. This differs from Captain Marvel, a male dominated movie with a female main superhero. The role that characters have may influence audience reviews or critic reviews more than the quantitative representation.'),
                                html.Img(id='mcu_rep_img3', src=images('mcu_rep.png'), width=600),
                            ]))
                    ])
                ]),

#Notes
            html.H2("Author's Notes"),
            html.Div([
                html.H4('Character Dataset'),
                html.P("This dataset does not include any information from Black Panther 2 (2022) or later. The characters in the dataset are classified as main characters or side characters. Main characters have a primary role, a speaking part, and a name. They are responsible for driving the plot in some way. Side characters are almost always named and must have a speaking part. There are very few characters in the dataset without names. Those that do not have names were included because they play an important role in the film, but are not a main character. All other characters without names or without speaking parts were not included."),
                html.P("The default sexuality for all characters was straight. Characters were only labeled as a member of the LGBTQ+ community if they discussed and/or identified their sexuality through a conversation or undoubtable on-screen relationship. While there are characters in the dataset who hint that they are not straight, if their sexuality has not been stated explicitly in some way, they are classified as straight."),
                html.H4('Morality Classification'),
                html.P("The default morality for all characters was good. Characters were only classified under a different morality if their actions excluded them from the good category. The types of morality were defined by K. Ray. Good characters have altruism, respect for life, and concern for other sentient beings. Generally, these characters are willing to make personal sacrifices to help others. Neutral characters feel guilt when innocent people are killed or seriously injured, but they are not willing to make sacrifices to help others. They only help people to which they have positive personal connections. Finally, evil characters hurt and kill others with no compassion or remorse. They pursue evil for enjoyment or out of a sense of duty to a malevolent master."),
                html.H4('Movie Rankings'),
                html.P("The critic and audience ratings are reflective of the groups as a whole. This could explain why there does not appear to be a pattern based on representation. To evaluate and rate movies based on representation, the percentage of women, people of color, and members of the LGBTQ+ community was calculated. These calculations included main characters and side characters. If a character was confirmed to be a member of the LGBTQ+ community at any point, they were considered to be a member of the LGBTQ+ community in films prior to the confirmation of their sexuality. To calculate the overall representation, the three percentages were added together. The purpose of the addition is to ensure that intersectionality is considered. Finally, the films were placed in order from highest percentage to lowest percentage. This ranking does not take into account how the characters were portrayed, simply the amount of representation."),
                ]),
            
#Citations
            html.H2('Citations and Resources'),
            html.Div([
                html.H4('Sources for Analysis'),
                html.P("Ray, K. (2020). Gender Portrayal in Marvel Cinematic Universe Films: Gender Representation, Moral Alignment, and Rewards for Violence (Order No. 28119666). Available from ProQuest Dissertations & Theses Global. (2441557971). http://cowles-proxy.drake.edu/login?url=https://www.proquest.com/dissertations-theses/gender-portrayal-marvel-cinematic-universe-films/docview/2441557971/se-2"),
                html.P("Olufidipe, F., & Echezabal, Y. (2021). Superheroines and Sexism: Female Representation in the Marvel Cinematic Universe. Journal of Student Research, 10(2). https://doi.org/10.47611/jsrhs.v10i2.1430"),
                html.P("Moon, M. R. (2016). “Thought We Wouldn’T Notice, But We Did”: An Analysis Of Critical Transmedia Literacy Among Consumers Of The Marvel Cinematic Universe (thesis)."),
                html.H4('Sources for Coding'),
                html.P("https://plotly.com/python"),
                html.P("https://dash.plotly.com"),
                html.P("https://github.com"),
                html.P("https://w3schools.com/sql/"),
                html.P("https://www.tutorialspoint.com/sql/index.htm"),
                ]),
            
        ]
)])


#intersectionality pie chart
@app.callback(
    Output("int_pie_graph", "figure"), 
    Input("checklist", "value")
    )
def update_int_pie_chart(representation):
    df = pd.read_csv('Marvel Dataset.csv')
    if len(representation) == 1:
        fig = px.pie(df[representation], names=representation[0], color_discrete_sequence=['#103383', '#BBBFC7', '#A18B59','#8C1B1B'])
    if len(representation) == 2:
        search = representation[0] + " and " + representation[1]
        if search == "Gender and Race":
            search = "Race and Gender"
        if search == "Sexuality and Gender":
            search = "Gender and Sexuality"
        if search == "Race and Sexuality":
            search = "Sexuality and Race"
        fig = px.pie(df[search], names=search, color_discrete_sequence=['#103383', '#BBBFC7', '#A18B59','#8C1B1B'])
    if len(representation)==3:
        fig = px.pie(df["Gender, Race, and Sexuality"], names="Gender, Race, and Sexuality", color_discrete_sequence=['#103383', '#BBBFC7', '#A18B59','#8C1B1B'])
    fig.update_layout(font_family='Tahoma',paper_bgcolor="#EAE4E4"),
    return fig
#intersectionality bar graph
@app.callback(
    Output("int_bar_graph", "figure"), 
    Input("checklist", "value")
    )
def update_int_bar_graph(representation):
    df = pd.read_csv('Marvel Dataset.csv')
    if len(representation) == 1:
        fig = px.histogram(df[representation], x=representation[0], color_discrete_sequence=['#103383', '#BBBFC7', '#A18B59','#8C1B1B'])
    if len(representation) == 2:
        fig = px.histogram(df, x=representation[0], color=representation[1], color_discrete_sequence=['#103383', '#BBBFC7', '#A18B59','#8C1B1B'])
    if len(representation)==3:
        search = representation[1] + " and " + representation[2]
        if search == "Gender and Race":
            search = "Race and Gender"
        if search == "Sexuality and Gender":
            search = "Gender and Sexuality"
        if search == "Race and Sexuality":
            search = "Sexuality and Race"
        fig = px.histogram(df, x=representation[0], color=search, color_discrete_sequence=['#103383', '#BBBFC7', '#A18B59','#8C1B1B'])
    fig.update_layout(font_family='Tahoma',paper_bgcolor="#EAE4E4", barmode='group'),
    return fig
#representation bar graph
@app.callback(
    Output("rep_bar_graph", "figure"), 
    Input("dropdown", "value"),
    Input("rep_choice","value")
    )
def update_bar_chart(representation, characters):
    if characters == 'All Characters':
        df = pd.read_csv('Marvel Dataset.csv')
    if characters == 'Only Main Characters':
        df = pd.read_csv('Main Marvel Dataset.csv')
    if characters == 'Only Side Characters':
        df = pd.read_csv('Side Marvel Dataset.csv')
    fig = px.histogram(df[representation], x=representation, color_discrete_sequence=['#103383'] )
    fig.update_layout(font_family='Tahoma',paper_bgcolor="#EAE4E4"),
    return fig
#representation time graph
@app.callback(
    Output("rep_time_graph", "figure"),
    Input("dropdown", "value"),
    Input("rep_choice","value")
    )
def update_time_graph(representation, characters):
    f_total=0
    f_list = []
    s_total=0
    s_list = []
    if characters == 'All Characters':
        df = pd.read_csv('Marvel Dataset.csv')
    if characters == 'Only Main Characters':
        df = pd.read_csv('Main Marvel Dataset.csv')
    if characters == 'Only Side Characters':
        df = pd.read_csv('Side Marvel Dataset.csv')
    if representation == 'Gender':
        f_amount = 'Women'
        s_amount = 'Men'
    if representation == 'Race':
        f_amount = 'POC'
        s_amount = 'White'
    if representation == 'Sexuality':
        f_amount = 'Straight'
        s_amount = 'LGBTQ+'
        t_amount = 'Confirmed LGBTQ+'
    temp = df.groupby(["First Appeared", representation]).size()
    temp1 = temp.rename('size').reset_index()
    first_amount = temp1[temp1[representation] == f_amount]
    for number in first_amount['size']:
        f_total += number
        f_list.append(f_total)
    second_amount = temp1[temp1[representation] == s_amount]
    for number in second_amount['size']:
        s_total += number
        s_list.append(s_total)
    fig = go.Figure(data=[
        go.Line(name=f_amount, x=first_amount['First Appeared'], y=f_list, line=dict(color='#103383')),
        go.Line(name=s_amount, x=second_amount['First Appeared'], y=s_list, line=dict(color='#8C1B1B'))
        ])
    fig.update_layout(font_family='Tahoma',paper_bgcolor="#EAE4E4")
    return fig

#morality bar graph
@app.callback(
    Output("mor_bar_graph", "figure"), 
    Input("mor_dropdown", "value")
    )
def update_mor_bar_chart(representation):
    df = pd.read_csv('Marvel Dataset.csv')
    option=[representation, 'Morality']
    gig = px.histogram(df[option], x=option[0], color=option[1], barmode='group', color_discrete_sequence=['#103383', '#8C1B1B','#BBBFC7'])
    gig.update_layout(font_family='Tahoma',paper_bgcolor="#EAE4E4")
    return gig

#morality pie chart
@app.callback(
    Output("mor_pie_chart", "figure"), 
    Input("mor_dropdown", "value")
    )
def update_mor_pie_chart(representation):
    df = pd.read_csv('Marvel Dataset.csv')
    if representation == 'Gender':
        representation1 = 'Women'
        representation2 = 'Men'
        color_choice = ['#8C1B1B','#BBBFC7','#103383']
    elif representation == 'Race':
        representation1 = 'POC'
        representation2 = 'White'
        color_choice = ['#103383','#BBBFC7','#8C1B1B']
    else:
        representation1 = 'LGBTQ+'
        representation2 = 'Straight'
        color_choice = ['#103383','#8C1B1B','#8C1B1B']
    temp1 = df[df[representation]==representation1]
    temp2 = df[df[representation]==representation2]
    fig = make_subplots(rows=2, cols=1, specs=[[{'type':'domain'}], [{'type':'domain'}]])
    fig.add_trace(go.Pie(labels=temp2['Morality'], name=representation1, marker_colors=color_choice), 1, 1)
    fig.add_trace(go.Pie(labels=temp1['Morality'], name=representation2), 2, 1)
    fig.update_layout(font_family='Tahoma',paper_bgcolor="#EAE4E4",
                      annotations=[dict(text=representation1, x=0.5, y=-0.1, showarrow=False, font_size=15), dict(text=representation2, x=0.5, y=0.52, showarrow=False, font_size=15)]),
    fig.update_traces(hoverinfo='label+value')
    return fig

#movie rating table
@app.callback(
    Output("rating_table","figure"),
    Input("rating_dropdown", "value"),
    Input("score_choice", "value"),
    )
def movie_rating_table(representation, score):
    df = pd.read_csv('Movie Sales.csv')
    if score == "Critic Score":
        review = "rt_critic_score"
    if score == "Audience Score":
        review = "rt_audience_score"
    if representation == 'Gender':
        order = ['Captain America: The First Avenger','Captain America: The Winter Soldier','Doctor Strange','Iron Man','Spider-Man: No Way Home','Thor','Guardians of the Galaxy Vol. 2','The Avengers','Eternals','The Incredible Hulk','Ant-Man','Iron Man 2','Thor: The Dark World','Loki','Captain Marvel','Avengers: Age of Ultron','Thor: Ragnarok','Ant-Man and the Wasp','Captain America: Civil War','Spider-Man: Homecoming','Spider-Man: Far From Home','The Falcon and the Winter Soldier','Avengers: Infinity War','Iron Man 3','She-Hulk: Attorney at Law','Guardians of the Galaxy','Hawkeye','Avengers: Endgame','Shang-Chi and the Legend of the Ten Rings','Doctor Strange in the Multiverse of Madness','Moon Knight','WandaVision','Ms. Marvel','Black Panther','Black Widow']
    if representation == 'Race':
        order = ['Captain America: The First Avenger','The Avengers','Avengers: Age of Ultron','Iron Man 2','Iron Man 3','Captain America: The Winter Soldier','Guardians of the Galaxy Vol. 2','Guardians of the Galaxy','Thor: The Dark World','Captain America: Civil War','The Incredible Hulk','Thor: Ragnarok','Captain Marvel','Thor','Ant-Man and the Wasp','Avengers: Endgame','Hawkeye','Ant-Man','Loki','Iron Man','Spider-Man: No Way Home','Avengers: Infinity War','WandaVision','Black Widow','Doctor Strange in the Multiverse of Madness','Doctor Strange','Spider-Man: Homecoming','Eternals','Spider-Man: Far From Home','She-Hulk: Attorney at Law','The Falcon and the Winter Soldier','Moon Knight','Black Panther','Ms. Marvel','Shang-Chi and the Legend of the Ten Rings']
    if representation == 'Sexuality':
        order = ['Captain America: The First Avenger','Avengers: Age of Ultron','Iron Man 2','Iron Man 3','Captain America: The Winter Soldier','Guardians of the Galaxy Vol. 2','Guardians of the Galaxy','Captain America: Civil War','The Incredible Hulk','Captain Marvel','Ant-Man and the Wasp','Hawkeye','Ant-Man','Iron Man','Spider-Man: No Way Home','WandaVision','Black Widow','Doctor Strange','Spider-Man: Homecoming','Spider-Man: Far From Home','She-Hulk: Attorney at Law','The Falcon and the Winter Soldier','Moon Knight','Black Panther','Ms. Marvel','Shang-Chi and the Legend of the Ten Rings','Avengers: Infinity War','Thor: The Dark World','Doctor Strange in the Multiverse of Madness','Avengers: Endgame','Thor','The Avengers','Eternals','Loki','Thor: Ragnarok']
    if representation == 'Overall':
        order = ['Captain America: The First Avenger','Captain America: The Winter Soldier','The Avengers','Iron Man 2','Guardians of the Galaxy Vol. 2','Avengers: Age of Ultron','The Incredible Hulk','Iron Man 3','Thor','Captain Marvel','Captain America: Civil War','Thor: The Dark World','Iron Man','Guardians of the Galaxy','Spider-Man: No Way Home','Ant-Man and the Wasp','Ant-Man','Doctor Strange','Hawkeye','Thor: Ragnarok','Avengers: Infinity War','Avengers: Endgame','Loki','Spider-Man: Homecoming','Spider-Man: Far From Home','Eternals','Doctor Strange in the Multiverse of Madness','WandaVision','She-Hulk: Attorney at Law','The Falcon and the Winter Soldier','Black Widow','Moon Knight','Shang-Chi and the Legend of the Ten Rings','Black Panther','Ms. Marvel']
    fig = px.bar(df, x="movie", y=review, color_discrete_sequence=['#103383', '#8C1B1B','#BBBFC7'])
    fig.update_layout(font_family='Tahoma',paper_bgcolor="#EAE4E4", xaxis={'categoryorder':'array', 'categoryarray':order})
    return fig

if __name__=='__main__':
    app.run_server(debug=True, port=8050)