import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Head to Head","Win Prediction","Win Percentage","Toss Factor","Best Players"],
         icons=["yin-yang","pin","trophy","mortarboard-fill","tsunami"],
        default_index=0,
        menu_icon="cast", 
        orientation="vertical"
    )
df = pd.read_csv('matches.csv')
df['team1'] = df['team1'].str.replace('Delhi Daredevils','Delhi Capitals')
df['team2'] = df['team2'].str.replace('Delhi Daredevils','Delhi Capitals')

df['team1'] = df['team1'].str.replace('Deccan Chargers','Sunrisers Hyderabad')
df['team2'] = df['team2'].str.replace('Deccan Chargers','Sunrisers Hyderabad')

df['team1'] = df['team1'].str.replace('Rising Pune Supergiant','Rising Pune Supergiants')
df['team2'] = df['team2'].str.replace('Rising Pune Supergiant','Rising Pune Supergiants')

df['team1'] = df['team1'].str.replace('Rising Pune Supergiantss','Rising Pune Supergiants') #vo upar vale ki vajah se kiya hai
df['team2'] = df['team2'].str.replace('Rising Pune Supergiantss','Rising Pune Supergiants')

if selected == "Best Players":
    
    
    plt.figure(figsize=(8,3))
    x = list(df['player_of_match'].value_counts()[0:10].keys())
    y= list(df['player_of_match'].value_counts()[0:10])
    data = (x,y)
    df2=sns.barplot(x=x,y=y)
    df2.set_title('Top 10 man of  the Match')
    plt.xticks(rotation=90)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

    top_ten_winnings_teams =_team=df.groupby("winner")["winner"].agg(["count"]).reset_index().sort_values(by="count",ascending=False).head(10)
    plt.figure(figsize=(8,3))
    df3=sns.barplot(x='winner',y='count',data=top_ten_winnings_teams)
    df3.set_title('Top 10 winnings team ')
    plt.xticks(rotation=90)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

if selected == "Win Prediction":
    teams = ['Sunrisers Hyderabad',
    'Mumbai Indians',
    'Royal Challengers Bangalore',
    'Kolkata Knight Riders',
    'Kings XI Punjab',
    'Chennai Super Kings',
    'Rajasthan Royals',
    'Delhi Capitals']

    cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
        'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
        'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
        'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
        'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
        'Sharjah', 'Mohali', 'Bengaluru']

    pipe = pickle.load(open('pipe.pkl','rb'))
    st.title('IPL Win Predictor')

    col1, col2 = st.columns(2)

    with col1:
        batting_team = st.selectbox('Select the batting team',sorted(teams))
    with col2:
        bowling_team = st.selectbox('Select the bowling team',sorted(teams))

    selected_city = st.selectbox('Select host city',sorted(cities))

    target = st.number_input('Target')

    col3,col4,col5 = st.columns(3)

    with col3:
        score = st.number_input('Score')
    with col4:
        overs = st.number_input('Overs completed')
    with col5:
        wickets = st.number_input('Wickets out')

    if st.button('Predict Probability'):
        if score>=target:
            st.error("Score should be less than Target")
        elif overs>=20 and overs>0:
            st.error("Overs should be Greater than 0 and Less than or equal to 19")
        elif wickets>=10:
            st.error("Wickets should be less than 10")
        elif batting_team == bowling_team:
            st.error("Bowling and batting team can't be same!")
        else:
            runs_left = target - score
            balls_left = 120 - (overs*6)
            wickets = 10 - wickets
            crr = score/overs
            rrr = (runs_left*6)/balls_left

            input_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'city':[selected_city],'runs_left':[runs_left],'balls_left':[balls_left],'wickets':[wickets],'total_runs_x':[target],'crr':[crr],'rrr':[rrr]})

            result = pipe.predict_proba(input_df)
            loss = result[0][0]
            win = result[0][1]
            st.header(batting_team + "- " + str(round(win*100)) + "%")
            st.header(bowling_team + "- " + str(round(loss*100)) + "%")

if selected == "Head to Head":
    st.header("Head to Head ⚔️")
    teams = ['Sunrisers Hyderabad',
            'Mumbai Indians',
            'Royal Challengers Bangalore',
            'Kolkata Knight Riders',
            'Kings XI Punjab',
            'Chennai Super Kings',
            'Rajasthan Royals',
            'Delhi Capitals']

    col6, col7 = st.columns(2)

    with col6:
        team1 = st.selectbox('Select Your team',sorted(teams))
    with col7:
        team2 = st.selectbox('Select Opponent team',sorted(teams))


    
    def visualize_head_to_head_record(team1, team2):
        # Get the number of matches won by each team
        team1_wins = df[(df['winner'] == team1) & ((df['team1'] == team2) | (df['team2'] == team2))].shape[0]
        team2_wins = df[(df['winner'] == team2) & ((df['team1'] == team1) | (df['team2'] == team1))].shape[0]
        
        # Compute the total number of matches played between the two teams
        total_matches = team1_wins + team2_wins
        
        # Compute the win percentages of the two teams
        team1_win_pct = 100 * team1_wins / total_matches if total_matches > 0 else 0
        team2_win_pct = 100 * team2_wins / total_matches if total_matches > 0 else 0
        
        # Create a donut chart to visualize the win-loss record of the two teams
        labels = [team1, team2]
        sizes = [team1_win_pct, team2_win_pct]
        colors = ['red', 'blue']
        fig, ax = plt.subplots()
        ax.axis('equal')
        plt.title(f'Head-to-Head Record: \n\n {team1} vs {team2}\n\n{team1}: {team1_wins} wins ,    {team2}: {team2_wins} wins\n\n')
        pie, _ = ax.pie(sizes, radius=1.3, colors=colors, labels=labels, startangle=90, labeldistance=1.1)
        plt.setp(pie, width=0.3, edgecolor='white')

        # Add a circle at the center to create a donut chart
        circle = plt.Circle((0,0), 0.8, color='white')
        fig = plt.gcf()
        fig.gca().add_artist(circle)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
    
    if st.button("Show Records"):
        if team1==team2:
            st.error("Bowling and batting team can't be same!")
            exit()
        visualize_head_to_head_record(team1, team2)



if selected == "Toss Factor":
    plt.figure(figsize=(5,3))
    df4=sns.countplot(x='toss_decision',data=df)
    df4.set_title('COMPARISION BATTING OR FIELDING ')
    plt.xticks(rotation=90)
    
if selected == "Win Percentage":
    teams = ['Royal Challengers Bangalore', 'Rising Pune Supergiants',
            'Kolkata Knight Riders', 'Kings XI Punjab', 'Delhi Capitals',
            'Sunrisers Hyderabad', 'Mumbai Indians', 'Gujarat Lions', 'Rajasthan Royals',
            'Chennai Super Kings', 'Pune Warriors', 'Kochi Tuskers Kerala']

    st.header("See How Your Favourite Team Has Performed in the IPL 😲")
    
    team_name = st.selectbox('Select the team',sorted(teams))
    

    def calculate_win_percentage(team_name):
        total_matches = df['team1'].value_counts() + df['team2'].value_counts()
        total_wins = df['winner'].value_counts()
        team_matches = total_matches[team_name]
        team_wins = total_wins[team_name]
        win_percentage = round((team_wins / team_matches) * 100, 2)
        return win_percentage
        
    if st.button("Calculate Win Percentage"):
        a = str(calculate_win_percentage(team_name))
        st.header(f"{a} %")


if selected == "Toss Factor":
    teams = ['Royal Challengers Bangalore', 'Rising Pune Supergiants',
            'Kolkata Knight Riders', 'Kings XI Punjab', 'Delhi Capitals',
            'Sunrisers Hyderabad', 'Mumbai Indians', 'Gujarat Lions', 'Rajasthan Royals',
            'Chennai Super Kings', 'Pune Warriors', 'Kochi Tuskers Kerala']

    st.header("Win the toss win the match?? 🤔")
    st.caption("Check how your favourite team has performed on winning the toss.")
    
    team_name = st.selectbox('Select the team',sorted(teams))
    
    def plot_win_percentage_on_toss(team_name):
        toss_wins = df['toss_winner'] == team_name
        match_wins = df['winner'] == team_name
        toss_and_match_wins = (toss_wins & match_wins).sum()
        toss_wins_only = toss_wins.sum() - toss_and_match_wins
        loss_on_toss = df.loc[(df['toss_winner'] == team_name) & (df['winner'] != team_name)].count()[0]
        win_percentage_on_toss = round((toss_and_match_wins / toss_wins_only) * 100, 2)
        loss_percentage_on_toss = round((loss_on_toss / toss_wins_only) * 100, 2)
        
        # Create a pie chart
        labels = ['Wins on Toss and Match', 'Loss on Toss']
        values = [win_percentage_on_toss, loss_percentage_on_toss]
        explode = (0.1, 0)
        fig1, ax1 = plt.subplots()
        ax1.pie(values, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title("Win Percentage on the basis of winning toss for " + team_name)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

    if st.button("Toss Factor"):
        plot_win_percentage_on_toss(team_name)

    