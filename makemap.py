import pandas as pd
import re
import json
import matplotlib.pyplot as plt
import numpy as np
import boto3

bucketname='nyg-hackathon-525684156106'

def makemap(gameid,playid):
    s3=boto3.resource('s3')
    #Get all the plays first
    itemname='movethechains/athena_runtime_queries/identified_games.csv'
    obj = s3.Object(bucketname, itemname)
    identified_plays=pd.read_csv(obj.get()['Body'])
    identified_plays.head()
    #Figure out if the posession team was the home team or the away team and who the RB was
    identified_plays=identified_plays[identified_plays.play_id==playid]
    identified_plays=identified_plays[identified_plays.game_id==gameid]
    identified_plays.reset_index(inplace=True)
    RB_gsis=identified_plays.rusher_player_id[0]
    posteam='hometeam'
    if(identified_plays.posteam[0]==identified_plays.away_team[0]):
        posteam='awayteam'
    #Now get the tracking data\n",
    itemname='movethechains/athena_runtime_queries/'+'gameid_'+str(gameid)+'_playid_'+str(playid)+'.csv'
    obj = s3.Object(bucketname, itemname)
    playdata=pd.read_csv(obj.get()['Body'])
    if(posteam=='hometeam'):
        posteamtracking=playdata.hometrackingdata[0]
        defteamtracking=playdata.awaytrackingdata[0]
    else:
        posteamtracking=playdata.awaytrackingdata[0]
        defteamtracking=playdata.hometrackingdata[0]

    #Based on the defteam positions at each timestamp, build out the map
    defteamplayertracking=defteamtracking.split('}]},')
    re_time=re.compile('time=[\\S]{23}')
    timestamps=re_time.findall(defteamplayertracking[0])
    num_timestamps=len(timestamps)
    GRIDS=[]
    RAW_GRIDS=[]

    re_x=re.compile('x=[-]*[0-9]+[.]*[0-9]*')
    re_y=re.compile('y=[-]*[0-9]+[.]*[0-9]*')
    re_dir=re.compile('dir=[-]*[0-9]+[.]*[0-9]*')
    re_onfield=re.compile('isonfield=[\\S]{5}')
    #For each player in the defensive tracking data fill out the respective grid\n",
    POS=[]
    for i in range(num_timestamps):
        POS.append([])

    r_tackle=5
    for defplayer in range(len(defteamplayertracking)):
        x_raw=re_x.findall(defteamplayertracking[defplayer])
        y_raw=re_y.findall(defteamplayertracking[defplayer])
        dir_raw=re_dir.findall(defteamplayertracking[defplayer])
        onfield=re_onfield.findall(defteamplayertracking[defplayer])
        for i in range(num_timestamps):
            x_pos=int(float(x_raw[i].split('=')[1]))
            y_pos=int(float(y_raw[i].split('=')[1]))
            if('true' in onfield[i] and x_pos<100 and y_pos<55):
                POS[i].append((x_pos,y_pos))

    for i in range(num_timestamps):
        map=np.zeros((100,55))
        fatmap=np.zeros((100,55))
        for playerpos in POS[i]:
            map[playerpos[0],playerpos[1]]=1
            seed=(playerpos[0]-r_tackle,playerpos[1]-r_tackle)
            obs_x=seed[0]
            obs_y=seed[1]
            while obs_x<seed[0]+(r_tackle):
                while obs_y<seed[1]+(r_tackle):
                    if(obs_x>0 and obs_x<100 and obs_y>0 and obs_y<55):
                        fatmap[obs_x,obs_y]=1\n",
                    #f((obs_x<0 or obs_x>99) and (obs_y>0 and obs_y<55)):\n",
                        #atmap[playerpos[0],obs_y]=1\n",
                    #f((obs_x>0 and obs_x<100) and (obs_y<0 and obs_y>55)):\n",
                        #atmap[obs_x,playerpos[1]]=1\n",
                    obs_y=obs_y+1
                obs_x=obs_x+1
            #if(playerpos[0]>1 and playerpos[0]<99):\n",
                #fatmap[playerpos[0]+r_tackle,playerpos[1]]=1\n",
                #fatmap[playerpos[0]-r_tackle,playerpos[1]]=1\n",
            #if(playerpos[1]>1 and playerpos[0]<54):\n",
                #fatmap[playerpos[0],playerpos[1]+r_tackle]=1\n",
                #fatmap[playerpos[0],playerpos[1]-r_tackle]=1\n",
        RAW_GRIDS.append(map)
        GRIDS.append(fatmap)



    SERIALIZED_GRIDS=[]
    for grid in GRIDS:
        serialized=[]
        for i in range(100):
            for j in range(55):
                serialized.append(grid[i,j])
        SERIALIZED_GRIDS.append(serialized)

    #Identify the running back and get his position
    offteamplayertracking=posteamtracking.split('}]},')
    re_gsis=re.compile('gsisid=[\\S]{10}')
    gsis_ids=re_gsis.findall(posteamtracking)
    RB_POS=[(0,0,0)]*num_timestamps

    for i in range(len(gsis_ids)):
        if(RB_gsis==gsis_ids[i].split('=')[1]):
            player_index=i
            break

    rb_x_raw=re_x.findall(offteamplayertracking[player_index])
    rb_y_raw=re_y.findall(offteamplayertracking[player_index])
    rb_dir_raw=re_dir.findall(offteamplayertracking[player_index])
    for i in range(num_timestamps):
        rbpos=[int(float(rb_x_raw[i].split('=')[1])),int(float(rb_y_raw[i].split('=')[1])),0]
        RB_POS[i]=rbpos
        if(i>0):
            try:
                angle=np.arctan((RB_POS[i][1]-RB_POS[i-1][1])/(RB_POS[i][1]-RB_POS[i-1][0]))*(180/np.pi)
            except:
                angle=90
            RB_POS[i][2]=angle

    #Figure out play direction
    approx_scrimmage_x=int(float(re_x.findall(defteamplayertracking[0])[0].split('=')[1]))
    direction='Right'
    if(RB_POS[0][0]>approx_scrimmage_x):
        direction='Left'

    #Prep data for A*
    pack={
        'GRIDS':GRIDS,
        'SERIALIZED_GRIDS':SERIALIZED_GRIDS,
        'RAW GRIDS':RAW_GRIDS,
        'RBPOS':RB_POS,
        'YARDS':identified_plays.yards_gained[0],
        'DIRECTION':direction,
        'TIMESTAMPS':timestamps,
    }
    return pack